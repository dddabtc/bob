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
        self.phase_skills = enemy_data.get("phase_skills", {})
        self.skill_cooldown = 0
        self.skill_warning = None  # 技能预警 {"type": "circle", "x", "y", "radius", "timer"}
        self.skill_warning_duration = 0

        # Boss特殊属性
        self.evasion = enemy_data.get("evasion", 0)  # 闪避率
        self.can_revive = enemy_data.get("can_revive", False)  # 可复活
        self.has_revived = False
        self.dot_damage = enemy_data.get("dot_damage", 0)  # 持续伤害
        self.can_silence = enemy_data.get("can_silence", False)  # 可沉默

        # Boss战斗状态
        self.is_enraged = False  # 狂暴状态
        self.clones = []  # 分身列表
        self.ground_effects = []  # 地面效果
        self.phase_transition = False  # 阶段转换中
        self.phase_transition_timer = 0
        self.invincible = False  # 无敌状态

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

        # 更新面朝方向和保存玩家位置（用于追踪弹）
        if player:
            self.facing = 1 if player.x > self.x else -1
            self._last_player_pos = (player.x, player.y)

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

        # 阶段转换中不行动
        if self.phase_transition:
            self.phase_transition_timer -= dt
            if self.phase_transition_timer <= 0:
                self.phase_transition = False
                self.invincible = False
            return

        # 更新技能预警
        if self.skill_warning:
            self.skill_warning_duration -= dt
            if self.skill_warning_duration <= 0:
                damage_result = self._execute_warned_skill(player)
                if damage_result:
                    self._pending_skill_damage = damage_result
                self.skill_warning = None

        # 更新地面效果
        self._update_ground_effects(dt, player)

        # 更新分身
        self._update_clones(dt, player)

        dist = self._distance_to(player)

        # 更新BOSS阶段
        hp_ratio = self.hp / self.max_hp
        new_phase = self.max_phases - int(hp_ratio * self.max_phases) + 1
        new_phase = min(new_phase, self.max_phases)

        if new_phase > self.phase:
            self.phase = new_phase
            # 进入新阶段时短暂无敌
            self.phase_transition = True
            self.phase_transition_timer = 1.0
            self.invincible = True
            self.skill_cooldown = 0
            # 清除之前的地面效果
            self.ground_effects.clear()

        # BOSS技能 - 根据阶段选择可用技能
        if self.skill_cooldown <= 0 and not self.skill_warning:
            available_skills = self.phase_skills.get(self.phase, self.skills)
            if available_skills:
                self._use_boss_skill(player, available_skills)
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

    def _use_boss_skill(self, player, available_skills=None):
        """使用BOSS技能"""
        skills = available_skills or self.skills
        if not skills:
            return

        skill = random.choice(skills)

        # ===== 极光会主教技能 =====
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

        elif skill == "十字火焰":
            # 十字形地面火焰（预警后爆发）
            self.skill_warning = {
                "type": "cross",
                "x": player.x,
                "y": player.y,
                "size": 300,
                "skill": "十字火焰"
            }
            self.skill_warning_duration = 1.0

        elif skill == "神圣审判":
            # 全屏攻击（预警后爆发）
            self.skill_warning = {
                "type": "fullscreen",
                "safe_zone": {"x": self.x, "y": self.y, "radius": 80},
                "skill": "神圣审判"
            }
            self.skill_warning_duration = 1.5

        elif skill == "狂暴":
            # 提升属性
            if not self.is_enraged:
                self.is_enraged = True
                self.speed *= 1.5
                self.attack = int(self.attack * 1.3)

        # ===== 愚者之影技能 =====
        elif skill == "命运逆转":
            # 下次受到伤害时反弹50%
            self.ground_effects.append({
                "type": "reflect_shield",
                "duration": 3.0,
                "reflect_ratio": 0.5
            })

        elif skill == "欺诈迷雾":
            # 创建迷雾区域，玩家在内视野受限
            self.ground_effects.append({
                "type": "fog",
                "x": player.x,
                "y": player.y,
                "radius": 150,
                "duration": 5.0
            })

        elif skill == "纸牌风暴":
            # 螺旋弹幕
            for i in range(12):
                angle = (i / 12) * math.pi * 2
                projectile = {
                    "x": self.x,
                    "y": self.y,
                    "vx": math.cos(angle) * 4,
                    "vy": math.sin(angle) * 4,
                    "damage": self.attack * 0.7,
                    "size": 10,
                    "lifetime": 3.0,
                    "color": (200, 180, 100),
                    "spiral": True,
                    "spiral_speed": 0.1 if i % 2 == 0 else -0.1
                }
                self.projectiles.append(projectile)

        elif skill == "时间回溯":
            # 恢复部分血量
            heal = int(self.max_hp * 0.1)
            self.hp = min(self.max_hp, self.hp + heal)

        elif skill == "分身术":
            # 创建分身
            if len(self.clones) < 2:
                for _ in range(2):
                    angle = random.random() * math.pi * 2
                    dist = 100 + random.random() * 50
                    clone = {
                        "x": self.x + math.cos(angle) * dist,
                        "y": self.y + math.sin(angle) * dist,
                        "hp": 50,
                        "duration": 8.0
                    }
                    self.clones.append(clone)

        # ===== 永暗巨兽技能 =====
        elif skill == "黑暗吞噬":
            # 大范围吸引攻击
            self.skill_warning = {
                "type": "pull",
                "x": self.x,
                "y": self.y,
                "radius": 200,
                "skill": "黑暗吞噬"
            }
            self.skill_warning_duration = 0.8

        elif skill == "亡灵召唤":
            # 召唤活尸
            for _ in range(3 + self.phase):
                angle = random.random() * math.pi * 2
                dist = 100 + random.random() * 80
                self.summons_to_spawn.append({
                    "type": "活尸",
                    "x": self.x + math.cos(angle) * dist,
                    "y": self.y + math.sin(angle) * dist
                })

        elif skill == "死亡凝视":
            # 直线激光攻击（预警）
            if player:
                dx = player.x - self.x
                dy = player.y - self.y
                angle = math.atan2(dy, dx)
                self.skill_warning = {
                    "type": "laser",
                    "x": self.x,
                    "y": self.y,
                    "angle": angle,
                    "width": 40,
                    "skill": "死亡凝视"
                }
                self.skill_warning_duration = 1.0

        elif skill == "不死之躯":
            # 在该阶段不会死亡，血量锁定在1
            self.ground_effects.append({
                "type": "undying",
                "duration": 5.0
            })

        elif skill == "黑暗领域":
            # 全屏变暗，只有Boss周围可见
            self.ground_effects.append({
                "type": "darkness",
                "duration": 6.0,
                "safe_radius": 100
            })

        # ===== 原初魔女技能 =====
        elif skill == "诅咒之触":
            # 追踪弹
            if player:
                dx = player.x - self.x
                dy = player.y - self.y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist > 0:
                    projectile = {
                        "x": self.x,
                        "y": self.y,
                        "vx": (dx / dist) * 3,
                        "vy": (dy / dist) * 3,
                        "damage": self.attack,
                        "size": 15,
                        "lifetime": 5.0,
                        "color": (180, 50, 120),
                        "homing": True,
                        "homing_strength": 0.05
                    }
                    self.projectiles.append(projectile)

        elif skill == "魅惑":
            # 短暂控制玩家移动方向（通过地面效果标记）
            self.ground_effects.append({
                "type": "charm",
                "x": player.x,
                "y": player.y,
                "radius": 80,
                "duration": 2.0
            })

        elif skill == "瘟疫爆发":
            # 多个毒圈
            for _ in range(3 + self.phase):
                x = random.randint(100, SCREEN_WIDTH - 100)
                y = random.randint(100, SCREEN_HEIGHT - 100)
                self.ground_effects.append({
                    "type": "poison_zone",
                    "x": x,
                    "y": y,
                    "radius": 60,
                    "duration": 4.0,
                    "damage": self.dot_damage or 5
                })

        elif skill == "灵魂收割":
            # 扇形攻击
            if player:
                dx = player.x - self.x
                dy = player.y - self.y
                angle = math.atan2(dy, dx)
                self.skill_warning = {
                    "type": "cone",
                    "x": self.x,
                    "y": self.y,
                    "angle": angle,
                    "spread": math.pi / 3,  # 60度
                    "range": 200,
                    "skill": "灵魂收割"
                }
                self.skill_warning_duration = 0.6

        elif skill == "灾祸降临":
            # 随机落雷
            for _ in range(5):
                x = random.randint(50, SCREEN_WIDTH - 50)
                y = random.randint(50, SCREEN_HEIGHT - 50)
                self.ground_effects.append({
                    "type": "lightning_warning",
                    "x": x,
                    "y": y,
                    "radius": 50,
                    "duration": 1.0,
                    "damage": self.attack * 1.5
                })

        # ===== 知识妖鬼技能 =====
        elif skill == "疯狂低语":
            # 周围放射弹幕
            for wave in range(3):
                for angle_deg in range(0, 360, 30):
                    rad = math.radians(angle_deg + wave * 15)
                    projectile = {
                        "x": self.x,
                        "y": self.y,
                        "vx": math.cos(rad) * (3 + wave),
                        "vy": math.sin(rad) * (3 + wave),
                        "damage": self.attack * 0.5,
                        "size": 8,
                        "lifetime": 2.5,
                        "color": (200, 180, 100),
                        "delay": wave * 0.3
                    }
                    self.projectiles.append(projectile)

        elif skill == "知识压制":
            # 沉默玩家技能
            if self.can_silence:
                self.ground_effects.append({
                    "type": "silence",
                    "duration": 3.0
                })

        elif skill == "卷轴轰炸":
            # 随机位置爆炸
            for _ in range(4 + self.phase):
                x = random.randint(100, SCREEN_WIDTH - 100)
                y = random.randint(100, SCREEN_HEIGHT - 100)
                self.ground_effects.append({
                    "type": "explosion_warning",
                    "x": x,
                    "y": y,
                    "radius": 70,
                    "duration": 1.2,
                    "damage": self.attack
                })

        elif skill == "真实之眼":
            # 锁定玩家，持续造成伤害
            self.skill_warning = {
                "type": "eye_lock",
                "target": player,
                "duration": 3.0,
                "skill": "真实之眼"
            }
            self.skill_warning_duration = 0.5

        elif skill == "禁忌知识":
            # 全屏爆炸（有安全区）
            safe_x = random.randint(200, SCREEN_WIDTH - 200)
            safe_y = random.randint(200, SCREEN_HEIGHT - 200)
            self.skill_warning = {
                "type": "fullscreen",
                "safe_zone": {"x": safe_x, "y": safe_y, "radius": 100},
                "skill": "禁忌知识"
            }
            self.skill_warning_duration = 2.0

        # ===== 通用技能 =====
        elif skill == "冲锋":
            if player:
                dx = player.x - self.x
                dy = player.y - self.y
                dist = math.sqrt(dx * dx + dy * dy)
                if dist > 0:
                    self.x += (dx / dist) * 100
                    self.y += (dy / dist) * 100

        elif skill == "重击":
            self.is_attacking = True
            self.attack_duration = 0.5

    def _execute_warned_skill(self, player):
        """执行预警后的技能"""
        if not self.skill_warning:
            return None

        warning = self.skill_warning
        skill_name = warning.get("skill", "")
        damage_result = None

        if warning["type"] == "cross":
            # 十字火焰：检查玩家是否在十字范围内
            if player:
                in_horizontal = abs(player.y - warning["y"]) < 30
                in_vertical = abs(player.x - warning["x"]) < 30
                if in_horizontal or in_vertical:
                    damage_result = ("skill_hit", self.attack * 1.2, skill_name)

        elif warning["type"] == "fullscreen":
            # 全屏攻击：检查玩家是否在安全区
            if player and "safe_zone" in warning:
                safe = warning["safe_zone"]
                dx = player.x - safe["x"]
                dy = player.y - safe["y"]
                dist = math.sqrt(dx*dx + dy*dy)
                if dist > safe["radius"]:
                    damage_result = ("skill_hit", self.attack * 2, skill_name)

        elif warning["type"] == "pull":
            # 黑暗吞噬：拉扯玩家并造成伤害
            if player:
                dx = player.x - warning["x"]
                dy = player.y - warning["y"]
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < warning["radius"]:
                    # 拉向Boss
                    if dist > 0:
                        pull_strength = 50
                        player.x -= (dx / dist) * pull_strength
                        player.y -= (dy / dist) * pull_strength
                    damage_result = ("skill_hit", self.attack, skill_name)

        elif warning["type"] == "laser":
            # 死亡凝视：直线激光
            if player:
                # 检查玩家是否在激光路径上
                angle = warning["angle"]
                laser_dx = math.cos(angle)
                laser_dy = math.sin(angle)
                # 计算玩家到激光线的距离
                px = player.x - warning["x"]
                py = player.y - warning["y"]
                # 投影长度
                proj_len = px * laser_dx + py * laser_dy
                if proj_len > 0:  # 在激光前方
                    # 到激光线的垂直距离
                    perp_dist = abs(px * laser_dy - py * laser_dx)
                    if perp_dist < warning["width"] / 2:
                        damage_result = ("skill_hit", self.attack * 1.5, skill_name)

        elif warning["type"] == "cone":
            # 灵魂收割：扇形攻击
            if player:
                dx = player.x - warning["x"]
                dy = player.y - warning["y"]
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < warning["range"]:
                    player_angle = math.atan2(dy, dx)
                    angle_diff = abs(player_angle - warning["angle"])
                    if angle_diff > math.pi:
                        angle_diff = 2 * math.pi - angle_diff
                    if angle_diff < warning["spread"] / 2:
                        damage_result = ("skill_hit", self.attack * 1.3, skill_name)

        elif warning["type"] == "eye_lock":
            # 真实之眼：持续伤害
            damage_result = ("skill_hit", self.attack * 0.5, skill_name)

        return damage_result

    def _update_ground_effects(self, dt, player):
        """更新地面效果"""
        effects_to_remove = []

        for effect in self.ground_effects:
            effect["duration"] -= dt

            if effect["duration"] <= 0:
                # 效果结束时的爆发伤害
                if effect["type"] in ["lightning_warning", "explosion_warning"]:
                    if player:
                        dx = player.x - effect["x"]
                        dy = player.y - effect["y"]
                        dist = math.sqrt(dx*dx + dy*dy)
                        if dist < effect["radius"]:
                            # 标记需要对玩家造成伤害
                            effect["triggered"] = True
                            effect["final_damage"] = effect.get("damage", self.attack)
                effects_to_remove.append(effect)
                continue

            # 持续效果
            if effect["type"] == "poison_zone" and player:
                dx = player.x - effect["x"]
                dy = player.y - effect["y"]
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < effect["radius"]:
                    # 每秒造成伤害（通过标记）
                    if not effect.get("last_tick"):
                        effect["last_tick"] = 0
                    effect["last_tick"] += dt
                    if effect["last_tick"] >= 1.0:
                        effect["last_tick"] = 0
                        effect["tick_damage"] = effect.get("damage", 5)

        for effect in effects_to_remove:
            self.ground_effects.remove(effect)

    def _update_clones(self, dt, player):
        """更新分身"""
        clones_to_remove = []

        for clone in self.clones:
            clone["duration"] -= dt
            if clone["duration"] <= 0 or clone["hp"] <= 0:
                clones_to_remove.append(clone)
                continue

            # 分身向玩家移动
            if player:
                dx = player.x - clone["x"]
                dy = player.y - clone["y"]
                dist = math.sqrt(dx*dx + dy*dy)
                if dist > 0:
                    clone["x"] += (dx / dist) * 2
                    clone["y"] += (dy / dist) * 2

        for clone in clones_to_remove:
            self.clones.remove(clone)

    def _update_projectiles(self, dt):
        """更新投射物"""
        for proj in self.projectiles[:]:
            # 处理延迟发射
            if proj.get("delay", 0) > 0:
                proj["delay"] -= dt
                continue

            proj["x"] += proj["vx"]
            proj["y"] += proj["vy"]
            proj["lifetime"] -= dt

            # 螺旋弹幕
            if proj.get("spiral"):
                angle = math.atan2(proj["vy"], proj["vx"])
                angle += proj["spiral_speed"]
                speed = math.sqrt(proj["vx"]**2 + proj["vy"]**2)
                proj["vx"] = math.cos(angle) * speed
                proj["vy"] = math.sin(angle) * speed

            # 追踪弹
            if proj.get("homing") and hasattr(self, '_last_player_pos'):
                target_x, target_y = self._last_player_pos
                dx = target_x - proj["x"]
                dy = target_y - proj["y"]
                dist = math.sqrt(dx*dx + dy*dy)
                if dist > 0:
                    strength = proj.get("homing_strength", 0.05)
                    proj["vx"] += (dx / dist) * strength
                    proj["vy"] += (dy / dist) * strength

            if proj["lifetime"] <= 0:
                self.projectiles.remove(proj)
            elif proj["x"] < 0 or proj["x"] > SCREEN_WIDTH:
                self.projectiles.remove(proj)
            elif proj["y"] < 0 or proj["y"] > SCREEN_HEIGHT:
                self.projectiles.remove(proj)

    def take_damage(self, damage, source="player"):
        """受到伤害"""
        # 无敌状态不受伤害
        if self.invincible:
            return 0

        # 闪避检测
        if self.evasion > 0 and random.random() < self.evasion:
            return "evaded"

        # 检查反弹护盾
        reflect_damage = 0
        for effect in self.ground_effects:
            if effect["type"] == "reflect_shield":
                reflect_damage = int(damage * effect["reflect_ratio"])
                self.ground_effects.remove(effect)
                break

        actual_damage = max(1, damage - self.defense // 2)

        # 检查不死效果
        for effect in self.ground_effects:
            if effect["type"] == "undying":
                if self.hp - actual_damage < 1:
                    actual_damage = self.hp - 1
                break

        self.hp -= actual_damage

        # 复活检测
        if self.hp <= 0 and self.can_revive and not self.has_revived:
            self.has_revived = True
            self.hp = int(self.max_hp * 0.3)
            self.phase_transition = True
            self.phase_transition_timer = 1.5
            self.invincible = True

        self.is_hit = True
        self.hit_timer = 0.1

        if reflect_damage > 0:
            return ("damage_reflect", actual_damage, reflect_damage)
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

        # 绘制Boss地面效果（在投射物之前）
        if self.enemy_type == "boss":
            self._draw_ground_effects(screen)
            self._draw_skill_warning(screen)
            self._draw_clones(screen)

        # 绘制投射物
        for proj in self.projectiles:
            # 延迟发射的投射物不绘制
            if proj.get("delay", 0) > 0:
                continue
            pygame.draw.circle(
                screen,
                proj["color"],
                (int(proj["x"]), int(proj["y"])),
                proj["size"]
            )
            # 追踪弹添加尾迹效果
            if proj.get("homing"):
                pygame.draw.circle(
                    screen,
                    (*proj["color"][:3], 100) if len(proj["color"]) == 3 else proj["color"],
                    (int(proj["x"] - proj["vx"]), int(proj["y"] - proj["vy"])),
                    proj["size"] - 2
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

                # 阶段转换提示
                if self.phase_transition:
                    trans_text = fonts["small"].render("阶段转换中...", True, (255, 200, 100))
                    trans_rect = trans_text.get_rect(center=(self.x, self.y - self.size - 55))
                    screen.blit(trans_text, trans_rect)

                # 狂暴状态指示
                if self.is_enraged:
                    rage_text = fonts["tiny"].render("狂暴!", True, (255, 50, 50))
                    rage_rect = rage_text.get_rect(center=(self.x, self.y + self.size + 15))
                    screen.blit(rage_text, rage_rect)

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

    def _draw_ground_effects(self, screen):
        """绘制地面效果"""
        for effect in self.ground_effects:
            if effect["type"] == "poison_zone":
                # 毒圈
                surface = pygame.Surface((effect["radius"] * 2, effect["radius"] * 2), pygame.SRCALPHA)
                pygame.draw.circle(surface, (100, 200, 100, 80), (effect["radius"], effect["radius"]), effect["radius"])
                pygame.draw.circle(surface, (50, 150, 50, 150), (effect["radius"], effect["radius"]), effect["radius"], 2)
                screen.blit(surface, (effect["x"] - effect["radius"], effect["y"] - effect["radius"]))

            elif effect["type"] in ["lightning_warning", "explosion_warning"]:
                # 预警圈（闪烁）
                alpha = int(100 + 55 * math.sin(time.time() * 10))
                surface = pygame.Surface((effect["radius"] * 2, effect["radius"] * 2), pygame.SRCALPHA)
                color = (255, 100, 100, alpha) if effect["type"] == "explosion_warning" else (255, 255, 100, alpha)
                pygame.draw.circle(surface, color, (effect["radius"], effect["radius"]), effect["radius"])
                pygame.draw.circle(surface, (255, 255, 255, 200), (effect["radius"], effect["radius"]), effect["radius"], 3)
                screen.blit(surface, (effect["x"] - effect["radius"], effect["y"] - effect["radius"]))

            elif effect["type"] == "fog":
                # 迷雾
                surface = pygame.Surface((effect["radius"] * 2, effect["radius"] * 2), pygame.SRCALPHA)
                pygame.draw.circle(surface, (100, 100, 150, 100), (effect["radius"], effect["radius"]), effect["radius"])
                screen.blit(surface, (effect["x"] - effect["radius"], effect["y"] - effect["radius"]))

            elif effect["type"] == "charm":
                # 魅惑区域
                surface = pygame.Surface((effect["radius"] * 2, effect["radius"] * 2), pygame.SRCALPHA)
                pygame.draw.circle(surface, (255, 100, 200, 80), (effect["radius"], effect["radius"]), effect["radius"])
                screen.blit(surface, (effect["x"] - effect["radius"], effect["y"] - effect["radius"]))

            elif effect["type"] == "reflect_shield":
                # 反弹护盾（围绕Boss）
                surface = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
                center = self.size * 1.5
                pygame.draw.circle(surface, (100, 200, 255, 100), (int(center), int(center)), int(self.size * 0.8))
                pygame.draw.circle(surface, (150, 220, 255, 200), (int(center), int(center)), int(self.size * 0.8), 3)
                screen.blit(surface, (self.x - center, self.y - center))

            elif effect["type"] == "darkness":
                # 黑暗领域 - 全屏变暗效果（只绘制遮罩）
                darkness_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                darkness_surface.fill((0, 0, 0, 180))
                # 在Boss周围挖一个可见的圆
                safe_radius = effect.get("safe_radius", 100)
                pygame.draw.circle(darkness_surface, (0, 0, 0, 0), (int(self.x), int(self.y)), safe_radius)
                screen.blit(darkness_surface, (0, 0))

    def _draw_skill_warning(self, screen):
        """绘制技能预警"""
        if not self.skill_warning:
            return

        warning = self.skill_warning
        alpha = int(100 + 55 * math.sin(time.time() * 8))

        if warning["type"] == "cross":
            # 十字火焰预警
            surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            # 水平线
            pygame.draw.rect(surface, (255, 100, 50, alpha), (0, warning["y"] - 30, SCREEN_WIDTH, 60))
            # 垂直线
            pygame.draw.rect(surface, (255, 100, 50, alpha), (warning["x"] - 30, 0, 60, SCREEN_HEIGHT))
            screen.blit(surface, (0, 0))

        elif warning["type"] == "fullscreen":
            # 全屏攻击预警
            surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            surface.fill((255, 50, 50, alpha // 2))
            # 绘制安全区
            if "safe_zone" in warning:
                safe = warning["safe_zone"]
                pygame.draw.circle(surface, (50, 255, 50, 150), (int(safe["x"]), int(safe["y"])), safe["radius"])
                pygame.draw.circle(surface, (100, 255, 100, 255), (int(safe["x"]), int(safe["y"])), safe["radius"], 3)
            screen.blit(surface, (0, 0))

        elif warning["type"] == "pull":
            # 吸引攻击预警
            surface = pygame.Surface((warning["radius"] * 2, warning["radius"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (50, 50, 100, alpha), (warning["radius"], warning["radius"]), warning["radius"])
            # 绘制向心箭头效果
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                outer_x = warning["radius"] + math.cos(rad) * warning["radius"] * 0.9
                outer_y = warning["radius"] + math.sin(rad) * warning["radius"] * 0.9
                inner_x = warning["radius"] + math.cos(rad) * warning["radius"] * 0.5
                inner_y = warning["radius"] + math.sin(rad) * warning["radius"] * 0.5
                pygame.draw.line(surface, (100, 100, 200, 200), (outer_x, outer_y), (inner_x, inner_y), 3)
            screen.blit(surface, (warning["x"] - warning["radius"], warning["y"] - warning["radius"]))

        elif warning["type"] == "laser":
            # 激光预警
            angle = warning["angle"]
            length = 1000
            end_x = warning["x"] + math.cos(angle) * length
            end_y = warning["y"] + math.sin(angle) * length
            # 绘制预警线
            surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(surface, (255, 50, 50, alpha), (warning["x"], warning["y"]), (end_x, end_y), warning["width"])
            screen.blit(surface, (0, 0))

        elif warning["type"] == "cone":
            # 扇形攻击预警
            surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            points = [(warning["x"], warning["y"])]
            num_points = 10
            for i in range(num_points + 1):
                a = warning["angle"] - warning["spread"] / 2 + (warning["spread"] * i / num_points)
                px = warning["x"] + math.cos(a) * warning["range"]
                py = warning["y"] + math.sin(a) * warning["range"]
                points.append((px, py))
            pygame.draw.polygon(surface, (200, 50, 150, alpha), points)
            screen.blit(surface, (0, 0))

        elif warning["type"] == "eye_lock":
            # 锁定预警（在玩家头上画眼睛图标）
            if warning.get("target"):
                target = warning["target"]
                pygame.draw.circle(screen, (255, 200, 50, 200), (int(target.x), int(target.y - 50)), 20, 3)
                pygame.draw.circle(screen, (255, 50, 50), (int(target.x), int(target.y - 50)), 8)

    def _draw_clones(self, screen):
        """绘制分身"""
        for clone in self.clones:
            # 分身比本体小且半透明
            clone_surface = pygame.Surface((self.size * 1.5, self.size * 1.5), pygame.SRCALPHA)
            center = (int(self.size * 0.75), int(self.size * 0.75))
            # 六边形
            points = []
            for i in range(6):
                angle = math.pi / 3 * i - math.pi / 2
                px = center[0] + math.cos(angle) * self.size // 3
                py = center[1] + math.sin(angle) * self.size // 3
                points.append((px, py))
            pygame.draw.polygon(clone_surface, (*self.color, 150), points)
            pygame.draw.polygon(clone_surface, (255, 255, 255, 100), points, 2)
            screen.blit(clone_surface, (clone["x"] - self.size * 0.75, clone["y"] - self.size * 0.75))

    def get_boss_effects_damage(self, player):
        """获取Boss效果对玩家造成的伤害（供game.py调用）"""
        damages = []

        # 检查地面效果的伤害
        for effect in self.ground_effects[:]:
            if effect.get("triggered"):
                damages.append(("ground_effect", effect.get("final_damage", self.attack), effect["type"]))
                effect["triggered"] = False

            if effect.get("tick_damage"):
                damages.append(("dot", effect["tick_damage"], effect["type"]))
                effect["tick_damage"] = 0

        # 检查分身碰撞
        for clone in self.clones:
            dx = player.x - clone["x"]
            dy = player.y - clone["y"]
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < player.size + self.size // 3:
                damages.append(("clone", self.attack // 2, "分身"))

        return damages
