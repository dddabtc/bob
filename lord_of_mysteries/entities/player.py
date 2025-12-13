"""
玩家类
"""

import pygame
import math
import time
from settings import *


class Player:
    """玩家角色"""

    def __init__(self, x, y, pathway_id, pathway_data, sequence=9):
        self.x = x
        self.y = y
        self.pathway_id = pathway_id
        self.pathway_data = pathway_data
        self.sequence = sequence

        # 获取序列数据
        self.seq_data = pathway_data["sequences"][sequence]

        # 基础属性
        self.max_hp = self.seq_data["hp"]
        self.hp = self.max_hp
        self.attack = self.seq_data["attack"]
        self.defense = self.seq_data["defense"]
        self.base_speed = self.seq_data["speed"]
        self.speed = self.base_speed

        # 外观
        self.color = pathway_data["color"]
        self.size = PLAYER_SIZE
        self.name = self.seq_data["name"]

        # 方向 (1=右, -1=左)
        self.facing = 1

        # 状态
        self.is_attacking = False
        self.is_dodging = False
        self.is_invincible = False
        self.invincible_timer = 0

        # 攻击相关
        self.attack_cooldown = 0
        self.attack_duration = 0
        self.attack_range = 60
        self.attack_hitbox = None

        # 闪避相关
        self.dodge_cooldown = 0
        self.dodge_duration = 0
        self.dodge_speed = 15
        self.dodge_direction = (0, 0)

        # 技能系统
        self.skills = {}
        self._init_skills()

        # 增益/减益效果
        self.buffs = []

        # 动画相关
        self.animation_frame = 0
        self.animation_timer = 0

        # 投射物列表
        self.projectiles = []

    def _init_skills(self):
        """初始化技能"""
        from data.pathways import SKILLS

        for skill_name in self.seq_data["skills"]:
            if skill_name in SKILLS:
                skill_data = SKILLS[skill_name].copy()
                skill_data["current_cooldown"] = 0
                skill_data["name"] = skill_name
                self.skills[skill_name] = skill_data

    def get_skill_list(self):
        """获取技能列表（前4个）"""
        return list(self.skills.keys())[:4]

    def update(self, dt, keys, events):
        """更新玩家状态"""
        # 更新计时器
        self._update_timers(dt)

        # 更新增益效果
        self._update_buffs(dt)

        # 处理输入
        if not self.is_attacking and not self.is_dodging:
            self._handle_movement(keys)

        # 处理闪避移动
        if self.is_dodging:
            self._update_dodge(dt)

        # 处理攻击
        if self.is_attacking:
            self._update_attack(dt)

        # 处理事件输入
        self._handle_events(events)

        # 更新投射物
        self._update_projectiles(dt)

        # 更新动画
        self._update_animation(dt)

        # 限制在屏幕内
        self.x = max(self.size, min(SCREEN_WIDTH - self.size, self.x))
        self.y = max(self.size, min(SCREEN_HEIGHT - self.size, self.y))

    def _update_timers(self, dt):
        """更新各种计时器"""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        if self.dodge_cooldown > 0:
            self.dodge_cooldown -= dt
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.is_invincible = False

        # 更新技能冷却
        for skill in self.skills.values():
            if skill["current_cooldown"] > 0:
                skill["current_cooldown"] -= dt

    def _update_buffs(self, dt):
        """更新增益效果"""
        # 移除过期的buff
        self.buffs = [b for b in self.buffs if b["duration"] > 0]

        for buff in self.buffs:
            buff["duration"] -= dt

        # 重新计算属性
        self._recalculate_stats()

    def _recalculate_stats(self):
        """重新计算属性（基于buff）"""
        self.speed = self.base_speed

        for buff in self.buffs:
            if buff["type"] == "speed":
                self.speed += buff["value"]
            # 可以添加更多buff类型

    def _handle_movement(self, keys):
        """处理移动输入"""
        dx, dy = 0, 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
            self.facing = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1
            self.facing = 1

        # 归一化对角线移动
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707

        self.x += dx * self.speed
        self.y += dy * self.speed

    def _handle_events(self, events):
        """处理事件输入"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                # 普通攻击 - J键
                if event.key == pygame.K_j:
                    self.start_attack()

                # 闪避 - K键
                elif event.key == pygame.K_k:
                    self.start_dodge()

                # 技能 - 1-4数字键
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    skill_index = event.key - pygame.K_1
                    self.use_skill(skill_index)

    def start_attack(self):
        """开始攻击"""
        if self.attack_cooldown > 0 or self.is_attacking or self.is_dodging:
            return

        self.is_attacking = True
        self.attack_duration = 0.3  # 攻击持续时间
        self.attack_cooldown = 0.5  # 攻击冷却

        # 创建攻击判定框
        attack_x = self.x + self.facing * (self.size // 2 + 20)
        attack_y = self.y
        self.attack_hitbox = pygame.Rect(
            attack_x - 25, attack_y - 30,
            50, 60
        )

    def _update_attack(self, dt):
        """更新攻击状态"""
        self.attack_duration -= dt
        if self.attack_duration <= 0:
            self.is_attacking = False
            self.attack_hitbox = None

    def start_dodge(self):
        """开始闪避"""
        if self.dodge_cooldown > 0 or self.is_dodging or self.is_attacking:
            return

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1

        # 如果没有方向输入，向面朝方向闪避
        if dx == 0 and dy == 0:
            dx = self.facing

        # 归一化
        length = math.sqrt(dx * dx + dy * dy)
        if length > 0:
            dx /= length
            dy /= length

        self.is_dodging = True
        self.is_invincible = True
        self.dodge_duration = 0.2
        self.dodge_cooldown = 0.8
        self.dodge_direction = (dx, dy)

    def _update_dodge(self, dt):
        """更新闪避状态"""
        self.x += self.dodge_direction[0] * self.dodge_speed
        self.y += self.dodge_direction[1] * self.dodge_speed

        self.dodge_duration -= dt
        if self.dodge_duration <= 0:
            self.is_dodging = False
            self.invincible_timer = 0.1  # 闪避后短暂无敌

    def use_skill(self, skill_index):
        """使用技能"""
        skill_names = self.get_skill_list()
        if skill_index >= len(skill_names):
            return False

        skill_name = skill_names[skill_index]
        skill = self.skills.get(skill_name)
        if not skill:
            return False

        if skill["current_cooldown"] > 0:
            return False

        # 设置冷却
        skill["current_cooldown"] = skill["cooldown"]

        # 根据技能类型执行效果
        skill_type = skill.get("type", "")

        if skill_type == "projectile":
            self._cast_projectile(skill)
        elif skill_type == "buff":
            self._cast_buff(skill)
        elif skill_type == "heal":
            self._cast_heal(skill)
        elif skill_type == "dash":
            self._cast_dash(skill)
        elif skill_type == "aoe":
            self._cast_aoe(skill)
        elif skill_type == "melee":
            self._cast_melee(skill)

        return True

    def _cast_projectile(self, skill):
        """释放投射物技能"""
        projectile = {
            "x": self.x + self.facing * 30,
            "y": self.y,
            "vx": self.facing * 12,
            "vy": 0,
            "damage": skill.get("damage", 20),
            "size": 10,
            "lifetime": 2.0,
            "color": self.color
        }
        self.projectiles.append(projectile)

    def _cast_buff(self, skill):
        """释放增益技能"""
        duration = skill.get("duration", 5)
        buff = {
            "name": skill["name"],
            "type": "buff",
            "duration": duration,
            "effect": skill.get("desc", "")
        }

        # 特殊buff效果
        if "无敌" in skill.get("desc", "") or "闪避" in skill.get("desc", ""):
            self.is_invincible = True
            self.invincible_timer = duration

        self.buffs.append(buff)

    def _cast_heal(self, skill):
        """释放治疗技能"""
        heal_amount = skill.get("heal", 30)
        self.hp = min(self.max_hp, self.hp + heal_amount)

    def _cast_dash(self, skill):
        """释放冲刺技能"""
        # 快速位移
        dash_distance = 100
        self.x += self.facing * dash_distance

        # 如果技能有伤害，创建伤害区域
        if "damage" in skill:
            # 创建一个大的投射物作为伤害判定
            projectile = {
                "x": self.x,
                "y": self.y,
                "vx": 0,
                "vy": 0,
                "damage": skill["damage"],
                "size": 40,
                "lifetime": 0.1,
                "color": self.color
            }
            self.projectiles.append(projectile)

    def _cast_aoe(self, skill):
        """释放范围技能"""
        # 创建一个大范围的投射物
        projectile = {
            "x": self.x + self.facing * 80,
            "y": self.y,
            "vx": 0,
            "vy": 0,
            "damage": skill.get("damage", 40),
            "size": 60,
            "lifetime": 0.5,
            "color": self.color,
            "is_aoe": True
        }
        self.projectiles.append(projectile)

    def _cast_melee(self, skill):
        """释放近战技能"""
        # 强化版普通攻击
        self.is_attacking = True
        self.attack_duration = 0.4
        self.attack_cooldown = 0.3

        # 创建更大的攻击判定框
        attack_x = self.x + self.facing * (self.size // 2 + 30)
        attack_y = self.y
        self.attack_hitbox = pygame.Rect(
            attack_x - 35, attack_y - 40,
            70, 80
        )
        # 标记为技能攻击，伤害更高
        self.skill_attack_damage = skill.get("damage", self.attack * 2)

    def _update_projectiles(self, dt):
        """更新投射物"""
        for proj in self.projectiles[:]:
            proj["x"] += proj["vx"]
            proj["y"] += proj["vy"]
            proj["lifetime"] -= dt

            # 移除过期或出界的投射物
            if proj["lifetime"] <= 0:
                self.projectiles.remove(proj)
            elif proj["x"] < 0 or proj["x"] > SCREEN_WIDTH:
                self.projectiles.remove(proj)
            elif proj["y"] < 0 or proj["y"] > SCREEN_HEIGHT:
                self.projectiles.remove(proj)

    def _update_animation(self, dt):
        """更新动画"""
        self.animation_timer += dt
        if self.animation_timer >= 0.1:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4

    def take_damage(self, damage):
        """受到伤害"""
        if self.is_invincible:
            return 0

        # 计算实际伤害
        actual_damage = max(1, damage - self.defense // 2)
        self.hp -= actual_damage

        # 受伤后短暂无敌
        self.is_invincible = True
        self.invincible_timer = 0.5

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

    def get_attack_damage(self):
        """获取当前攻击伤害"""
        if hasattr(self, 'skill_attack_damage') and self.skill_attack_damage:
            damage = self.skill_attack_damage
            self.skill_attack_damage = None
            return damage
        return self.attack

    def draw(self, screen, fonts):
        """绘制玩家"""
        # 闪避时半透明
        alpha = 128 if self.is_dodging else 255

        # 无敌时闪烁
        if self.is_invincible and not self.is_dodging:
            if int(time.time() * 10) % 2 == 0:
                alpha = 128

        # 玩家身体
        player_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

        # 根据状态绘制不同效果
        if self.is_attacking:
            # 攻击时颜色变亮
            color = tuple(min(255, c + 50) for c in self.color)
        elif self.is_dodging:
            # 闪避时颜色变淡
            color = tuple(c // 2 for c in self.color)
        else:
            color = self.color

        # 绘制圆形身体
        pygame.draw.circle(
            player_surface,
            (*color, alpha),
            (self.size // 2, self.size // 2),
            self.size // 2
        )

        # 边框
        pygame.draw.circle(
            player_surface,
            (255, 255, 255, alpha),
            (self.size // 2, self.size // 2),
            self.size // 2,
            2
        )

        # 面朝方向指示器
        indicator_x = self.size // 2 + self.facing * 10
        indicator_y = self.size // 2
        pygame.draw.circle(
            player_surface,
            (255, 255, 255, alpha),
            (indicator_x, indicator_y),
            5
        )

        screen.blit(player_surface, (self.x - self.size // 2, self.y - self.size // 2))

        # 绘制攻击效果
        if self.is_attacking and self.attack_hitbox:
            attack_surface = pygame.Surface(
                (self.attack_hitbox.width, self.attack_hitbox.height),
                pygame.SRCALPHA
            )
            pygame.draw.ellipse(
                attack_surface,
                (*self.color, 100),
                (0, 0, self.attack_hitbox.width, self.attack_hitbox.height)
            )
            screen.blit(attack_surface, self.attack_hitbox.topleft)

        # 绘制投射物
        for proj in self.projectiles:
            if proj.get("is_aoe"):
                # AOE效果
                aoe_surface = pygame.Surface((proj["size"] * 2, proj["size"] * 2), pygame.SRCALPHA)
                pygame.draw.circle(
                    aoe_surface,
                    (*proj["color"], 80),
                    (proj["size"], proj["size"]),
                    proj["size"]
                )
                screen.blit(aoe_surface, (proj["x"] - proj["size"], proj["y"] - proj["size"]))
            else:
                # 普通投射物
                pygame.draw.circle(screen, proj["color"], (int(proj["x"]), int(proj["y"])), proj["size"])
                pygame.draw.circle(screen, WHITE, (int(proj["x"]), int(proj["y"])), proj["size"], 2)

        # 绘制名称
        name_text = fonts["tiny"].render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(self.x, self.y - self.size - 5))
        screen.blit(name_text, name_rect)

        # 绘制buff图标
        self._draw_buffs(screen, fonts)

    def _draw_buffs(self, screen, fonts):
        """绘制buff图标"""
        buff_x = self.x - 40
        buff_y = self.y - self.size - 25

        for i, buff in enumerate(self.buffs[:3]):  # 最多显示3个
            # buff背景
            buff_rect = pygame.Rect(buff_x + i * 25, buff_y, 20, 20)
            pygame.draw.rect(screen, (50, 50, 80), buff_rect, border_radius=3)
            pygame.draw.rect(screen, GOLD, buff_rect, 1, border_radius=3)

            # buff首字母
            initial = buff["name"][0] if buff["name"] else "?"
            text = fonts["tiny"].render(initial, True, WHITE)
            text_rect = text.get_rect(center=buff_rect.center)
            screen.blit(text, text_rect)
