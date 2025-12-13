"""
敌人类
"""

import pygame
import math
import random
import time
from settings import *


class Enemy:
    """敌人基类"""

    def __init__(self, x, y, enemy_data):
        self.x = x
        self.y = y
        self.data = enemy_data

        # 基础属性
        self.name = enemy_data["name"]
        self.max_hp = enemy_data["hp"]
        self.hp = self.max_hp
        self.attack = enemy_data["attack"]
        self.defense = enemy_data["defense"]
        self.speed = enemy_data["speed"]
        self.size = enemy_data["size"]
        self.color = enemy_data["color"]
        self.exp = enemy_data["exp"]
        self.enemy_type = enemy_data.get("type", "normal")

        # 行为
        self.behavior = enemy_data.get("behavior", "chase")
        self.attack_range = enemy_data.get("attack_range", 40)
        self.attack_cooldown_max = enemy_data.get("attack_cooldown", 1.5)
        self.attack_cooldown = 0

        # 状态
        self.is_attacking = False
        self.attack_duration = 0
        self.is_hit = False
        self.hit_timer = 0
        self.facing = 1

        # 投射物（远程敌人）
        self.projectiles = []
        self.projectile_speed = enemy_data.get("projectile_speed", 5)

        # 召唤（召唤型敌人）
        self.summon_cooldown = 0
        self.summon_cooldown_max = enemy_data.get("summon_cooldown", 10)
        self.summon_type = enemy_data.get("summon_type", None)
        self.summons_to_spawn = []

        # 隐身（刺客型敌人）
        self.can_stealth = enemy_data.get("can_stealth", False)
        self.is_stealthed = False
        self.stealth_cooldown = 0

        # BOSS相关
        self.phase = 1
        self.max_phases = enemy_data.get("phases", 1)
        self.skills = enemy_data.get("skills", [])
        self.skill_cooldown = 0

        # 掉落物
        self.drops = enemy_data.get("drops", [])

        # 动画
        self.animation_offset = random.random() * math.pi * 2

    def update(self, dt, player):
        """更新敌人状态"""
        # 更新计时器
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        if self.hit_timer > 0:
            self.hit_timer -= dt
            if self.hit_timer <= 0:
                self.is_hit = False
        if self.skill_cooldown > 0:
            self.skill_cooldown -= dt
        if self.summon_cooldown > 0:
            self.summon_cooldown -= dt
        if self.stealth_cooldown > 0:
            self.stealth_cooldown -= dt

        # 更新攻击状态
        if self.is_attacking:
            self.attack_duration -= dt
            if self.attack_duration <= 0:
                self.is_attacking = False

        # 根据行为模式行动
        if self.behavior == "chase":
            self._behavior_chase(dt, player)
        elif self.behavior == "ranged":
            self._behavior_ranged(dt, player)
        elif self.behavior == "smart":
            self._behavior_smart(dt, player)
        elif self.behavior == "assassin":
            self._behavior_assassin(dt, player)
        elif self.behavior == "summoner":
            self._behavior_summoner(dt, player)
        elif self.behavior == "boss":
            self._behavior_boss(dt, player)

        # 更新投射物
        self._update_projectiles(dt)

        # 更新面朝方向
        if player:
            self.facing = 1 if player.x > self.x else -1

        # 限制在屏幕内
        self.x = max(self.size, min(SCREEN_WIDTH - self.size, self.x))
        self.y = max(self.size, min(SCREEN_HEIGHT - self.size, self.y))

    def _behavior_chase(self, dt, player):
        """追逐行为"""
        if not player:
            return

        dist = self._distance_to(player)

        if dist <= self.attack_range:
            # 在攻击范围内，尝试攻击
            self._try_attack(player)
        else:
            # 追逐玩家
            self._move_towards(player.x, player.y, dt)

    def _behavior_ranged(self, dt, player):
        """远程攻击行为"""
        if not player:
            return

        dist = self._distance_to(player)
        preferred_dist = self.attack_range * 0.7

        if dist < preferred_dist * 0.5:
            # 太近了，后退
            self._move_away(player.x, player.y, dt)
        elif dist > self.attack_range:
            # 太远了，靠近
            self._move_towards(player.x, player.y, dt)
        else:
            # 合适距离，攻击
            self._try_ranged_attack(player)

    def _behavior_smart(self, dt, player):
        """智能行为（精英怪）"""
        if not player:
            return

        dist = self._distance_to(player)

        # 低血量时更加谨慎
        hp_ratio = self.hp / self.max_hp

        if hp_ratio < 0.3:
            # 低血量，保持距离
            if dist < 100:
                self._move_away(player.x, player.y, dt)
            elif self.attack_cooldown <= 0:
                self._try_attack(player)
        else:
            # 正常战斗
            if dist <= self.attack_range:
                self._try_attack(player)
            else:
                self._move_towards(player.x, player.y, dt)

    def _behavior_assassin(self, dt, player):
        """刺客行为"""
        if not player:
            return

        dist = self._distance_to(player)

        # 隐身逻辑
        if self.can_stealth and not self.is_stealthed and self.stealth_cooldown <= 0:
            if dist > 150:
                self.is_stealthed = True

        if self.is_stealthed:
            # 隐身时快速接近
            self._move_towards(player.x, player.y, dt, speed_mult=1.5)
            if dist <= self.attack_range:
                # 解除隐身并攻击（暴击）
                self.is_stealthed = False
                self.stealth_cooldown = 5.0
                self._try_attack(player, crit=True)
        else:
            # 正常战斗
            if dist <= self.attack_range:
                self._try_attack(player)
            else:
                self._move_towards(player.x, player.y, dt)

    def _behavior_summoner(self, dt, player):
        """召唤行为"""
        if not player:
            return

        dist = self._distance_to(player)

        # 保持距离
        if dist < 100:
            self._move_away(player.x, player.y, dt)
        elif dist > self.attack_range:
            self._move_towards(player.x, player.y, dt)
        else:
            # 尝试召唤或攻击
            if self.summon_cooldown <= 0 and self.summon_type:
                self._summon_minion()
            else:
                self._try_ranged_attack(player)

    def _behavior_boss(self, dt, player):
        """BOSS行为"""
        if not player:
            return

        dist = self._distance_to(player)

        # 更新BOSS阶段
        hp_ratio = self.hp / self.max_hp
        new_phase = self.max_phases - int(hp_ratio * self.max_phases) + 1
        new_phase = min(new_phase, self.max_phases)

        if new_phase > self.phase:
            self.phase = new_phase
            # 进入新阶段时短暂无敌或释放技能
            self.skill_cooldown = 0

        # BOSS技能
        if self.skill_cooldown <= 0 and self.skills:
            self._use_boss_skill(player)
            self.skill_cooldown = 3.0 / self.phase  # 阶段越高，技能越频繁

        # 基础行为
        if dist <= self.attack_range:
            self._try_attack(player)
        else:
            self._move_towards(player.x, player.y, dt, speed_mult=1 + 0.2 * (self.phase - 1))

    def _move_towards(self, target_x, target_y, dt, speed_mult=1.0):
        """向目标移动"""
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > 0:
            dx /= dist
            dy /= dist
            self.x += dx * self.speed * speed_mult
            self.y += dy * self.speed * speed_mult

    def _move_away(self, target_x, target_y, dt):
        """远离目标"""
        dx = self.x - target_x
        dy = self.y - target_y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > 0:
            dx /= dist
            dy /= dist
            self.x += dx * self.speed
            self.y += dy * self.speed

    def _distance_to(self, player):
        """计算到玩家的距离"""
        dx = player.x - self.x
        dy = player.y - self.y
        return math.sqrt(dx * dx + dy * dy)

    def _try_attack(self, player, crit=False):
        """尝试攻击"""
        if self.attack_cooldown > 0 or self.is_attacking:
            return False

        self.is_attacking = True
        self.attack_duration = 0.3
        self.attack_cooldown = self.attack_cooldown_max

        # 计算伤害
        damage = self.attack
        if crit:
            damage *= 2

        # 检查是否命中
        dist = self._distance_to(player)
        if dist <= self.attack_range + player.size // 2:
            return ("hit", damage)

        return False

    def _try_ranged_attack(self, player):
        """尝试远程攻击"""
        if self.attack_cooldown > 0:
            return

        self.attack_cooldown = self.attack_cooldown_max

        # 创建投射物
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > 0:
            dx /= dist
            dy /= dist

            projectile = {
                "x": self.x,
                "y": self.y,
                "vx": dx * self.projectile_speed,
                "vy": dy * self.projectile_speed,
                "damage": self.attack,
                "size": 8,
                "lifetime": 3.0,
                "color": self.color
            }
            self.projectiles.append(projectile)

    def _summon_minion(self):
        """召唤小怪"""
        self.summon_cooldown = self.summon_cooldown_max

        # 在周围生成召唤位置
        angle = random.random() * math.pi * 2
        dist = 60 + random.random() * 40
        spawn_x = self.x + math.cos(angle) * dist
        spawn_y = self.y + math.sin(angle) * dist

        self.summons_to_spawn.append({
            "type": self.summon_type,
            "x": spawn_x,
            "y": spawn_y
        })

    def _use_boss_skill(self, player):
        """使用BOSS技能"""
        if not self.skills:
            return

        skill = random.choice(self.skills)

        if skill == "火焰风暴":
            # 多方向投射物
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                projectile = {
                    "x": self.x,
                    "y": self.y,
                    "vx": math.cos(rad) * 5,
                    "vy": math.sin(rad) * 5,
                    "damage": self.attack,
                    "size": 12,
                    "lifetime": 2.0,
                    "color": (255, 100, 50)
                }
                self.projectiles.append(projectile)

        elif skill == "召唤信徒":
            # 召唤多个小怪
            for _ in range(2 + self.phase):
                angle = random.random() * math.pi * 2
                dist = 80 + random.random() * 60
                self.summons_to_spawn.append({
                    "type": "疯狂信徒",
                    "x": self.x + math.cos(angle) * dist,
                    "y": self.y + math.sin(angle) * dist
                })

        elif skill == "冲锋":
            # 快速冲向玩家
            if player:
                dx = player.x - self.x
                dy = player.y - self.y
                dist = math.sqrt(dx * dx + dy * dy)
                if dist > 0:
                    self.x += (dx / dist) * 100
                    self.y += (dy / dist) * 100

        elif skill == "重击":
            # 范围攻击
            self.is_attacking = True
            self.attack_duration = 0.5

        elif skill == "狂暴":
            # 临时提升属性
            self.speed *= 1.5
            self.attack *= 1.3

    def _update_projectiles(self, dt):
        """更新投射物"""
        for proj in self.projectiles[:]:
            proj["x"] += proj["vx"]
            proj["y"] += proj["vy"]
            proj["lifetime"] -= dt

            if proj["lifetime"] <= 0:
                self.projectiles.remove(proj)
            elif proj["x"] < 0 or proj["x"] > SCREEN_WIDTH:
                self.projectiles.remove(proj)
            elif proj["y"] < 0 or proj["y"] > SCREEN_HEIGHT:
                self.projectiles.remove(proj)

    def take_damage(self, damage, source="player"):
        """受到伤害"""
        actual_damage = max(1, damage - self.defense // 2)
        self.hp -= actual_damage

        self.is_hit = True
        self.hit_timer = 0.1

        return actual_damage

    def is_alive(self):
        """是否存活"""
        return self.hp > 0

    def get_rect(self):
        """获取碰撞矩形"""
        return pygame.Rect(
            self.x - self.size // 2,
            self.y - self.size // 2,
            self.size,
            self.size
        )

    def get_attack_rect(self):
        """获取攻击判定矩形"""
        if not self.is_attacking:
            return None

        attack_x = self.x + self.facing * (self.size // 2 + 10)
        return pygame.Rect(
            attack_x - 20, self.y - 25,
            40, 50
        )

    def get_drops(self):
        """获取掉落物"""
        result = []
        for drop in self.drops:
            if random.random() < drop["chance"]:
                count = random.randint(drop["count"][0], drop["count"][1])
                result.append({
                    "item": drop["item"],
                    "count": count
                })
        return result

    def draw(self, screen, fonts):
        """绘制敌人"""
        # 隐身时半透明
        if self.is_stealthed:
            alpha = 50
        elif self.is_hit:
            alpha = 180
        else:
            alpha = 255

        # 创建敌人surface
        enemy_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)

        # 绘制身体（根据类型不同形状）
        center = (self.size, self.size)

        if self.enemy_type == "boss":
            # BOSS用六边形
            points = []
            for i in range(6):
                angle = math.pi / 3 * i - math.pi / 2
                px = center[0] + math.cos(angle) * self.size // 2
                py = center[1] + math.sin(angle) * self.size // 2
                points.append((px, py))
            pygame.draw.polygon(enemy_surface, (*self.color, alpha), points)
            pygame.draw.polygon(enemy_surface, (255, 255, 255, alpha), points, 3)
        elif self.enemy_type == "elite":
            # 精英用菱形
            points = [
                (center[0], center[1] - self.size // 2),
                (center[0] + self.size // 2, center[1]),
                (center[0], center[1] + self.size // 2),
                (center[0] - self.size // 2, center[1]),
            ]
            pygame.draw.polygon(enemy_surface, (*self.color, alpha), points)
            pygame.draw.polygon(enemy_surface, (255, 255, 255, alpha), points, 2)
        else:
            # 普通怪用圆形
            pygame.draw.circle(
                enemy_surface,
                (*self.color, alpha),
                center,
                self.size // 2
            )
            pygame.draw.circle(
                enemy_surface,
                (255, 255, 255, alpha),
                center,
                self.size // 2,
                2
            )

        # 受伤闪烁
        if self.is_hit:
            pygame.draw.circle(
                enemy_surface,
                (255, 255, 255, 100),
                center,
                self.size // 2 - 2
            )

        screen.blit(enemy_surface, (self.x - self.size, self.y - self.size))

        # 绘制攻击效果
        if self.is_attacking:
            attack_rect = self.get_attack_rect()
            if attack_rect:
                attack_surface = pygame.Surface(
                    (attack_rect.width, attack_rect.height),
                    pygame.SRCALPHA
                )
                pygame.draw.ellipse(
                    attack_surface,
                    (*self.color, 100),
                    (0, 0, attack_rect.width, attack_rect.height)
                )
                screen.blit(attack_surface, attack_rect.topleft)

        # 绘制投射物
        for proj in self.projectiles:
            pygame.draw.circle(
                screen,
                proj["color"],
                (int(proj["x"]), int(proj["y"])),
                proj["size"]
            )

        # 绘制血条
        self._draw_hp_bar(screen)

        # 绘制名称（精英和BOSS）
        if self.enemy_type in ["elite", "boss"]:
            name_text = fonts["tiny"].render(self.name, True, WHITE)
            name_rect = name_text.get_rect(center=(self.x, self.y - self.size - 20))
            screen.blit(name_text, name_rect)

            # BOSS显示阶段
            if self.enemy_type == "boss":
                phase_text = fonts["tiny"].render(f"阶段 {self.phase}/{self.max_phases}", True, CRIMSON)
                phase_rect = phase_text.get_rect(center=(self.x, self.y - self.size - 35))
                screen.blit(phase_text, phase_rect)

    def _draw_hp_bar(self, screen):
        """绘制血条"""
        bar_width = self.size + 20
        bar_height = 6

        # 背景
        bg_rect = pygame.Rect(
            self.x - bar_width // 2,
            self.y - self.size // 2 - 15,
            bar_width,
            bar_height
        )
        pygame.draw.rect(screen, (40, 40, 40), bg_rect)

        # 血量
        hp_ratio = self.hp / self.max_hp
        hp_width = int(bar_width * hp_ratio)
        if hp_width > 0:
            hp_rect = pygame.Rect(
                self.x - bar_width // 2,
                self.y - self.size // 2 - 15,
                hp_width,
                bar_height
            )
            hp_color = (50, 200, 50) if hp_ratio > 0.3 else (200, 50, 50)
            pygame.draw.rect(screen, hp_color, hp_rect)

        # 边框
        pygame.draw.rect(screen, (100, 100, 100), bg_rect, 1)
