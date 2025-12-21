"""
武器系统
管理武器的装备、攻击、特效处理
"""

import pygame
import math
import random
from data.weapons import (
    WEAPONS, WEAPON_TYPE_TRAITS, STARTER_WEAPONS,
    get_weapon_data, get_weapon_type_trait,
    WEAPON_TYPE_SWORD, WEAPON_TYPE_DAGGER, WEAPON_TYPE_STAFF,
    WEAPON_TYPE_BOW, WEAPON_TYPE_REVOLVER, WEAPON_TYPE_CANE, WEAPON_TYPE_FIST
)
from data.items import QUALITY_COLORS


class WeaponManager:
    """武器管理器 - 处理武器装备和攻击"""

    def __init__(self, player):
        self.player = player
        self.equipped_weapon = None  # 当前装备的武器
        self.weapon_data = None      # 当前武器的完整数据
        self.weapon_traits = None    # 当前武器类型特性

        # 攻击状态
        self.attack_cooldown = 0
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 0.1  # 攻击动画持续时间（更快）

        # 左轮特殊：弹药系统
        self.current_ammo = 6
        self.max_ammo = 6
        self.reload_time = 0
        self.reload_duration = 1.5
        self.is_reloading = False

        # 攻击hitbox
        self.attack_hitbox = None
        self.hitbox_active = False

        # 装备默认武器
        self._equip_starter_weapon()

    def _equip_starter_weapon(self):
        """装备初始武器"""
        starter = STARTER_WEAPONS.get("melee", "铁剑")
        self.equip_weapon(starter)

    def equip_weapon(self, weapon_name):
        """装备武器"""
        weapon_data = get_weapon_data(weapon_name)
        if not weapon_data:
            return False

        self.equipped_weapon = weapon_name
        self.weapon_data = weapon_data
        self.weapon_traits = get_weapon_type_trait(weapon_data.get("type"))

        # 如果是左轮，初始化弹药
        if weapon_data.get("type") == WEAPON_TYPE_REVOLVER:
            self.max_ammo = weapon_data.get("magazine", 6)
            self.current_ammo = self.max_ammo

        # 更新玩家属性
        self._apply_weapon_stats()

        return True

    def _apply_weapon_stats(self):
        """应用武器属性到玩家"""
        if not self.weapon_data:
            return

        # 基础攻击力加成
        weapon_attack = self.weapon_data.get("attack", 0)
        self.player.weapon_attack_bonus = weapon_attack

        # 攻击范围
        if self.weapon_traits:
            self.player.attack_range = self.weapon_traits.get("attack_range", 60)

        # 暴击率加成
        self.player.weapon_crit_rate = self.weapon_data.get("crit_rate", 0)
        self.player.weapon_crit_damage = self.weapon_data.get("crit_damage", 0)

        # 灵性加成
        spirit_bonus = self.weapon_data.get("spirit_bonus", 0)
        self.player.weapon_spirit_bonus = spirit_bonus

        # 防御加成
        defense_bonus = self.weapon_data.get("defense_bonus", 0)
        self.player.weapon_defense_bonus = defense_bonus

    def get_attack_damage(self):
        """计算武器攻击伤害（包含暴击）"""
        if not self.weapon_data:
            return self.player.attack

        base_damage = self.player.attack + self.weapon_data.get("attack", 0)

        # 暴击判定
        crit_rate = self.weapon_data.get("crit_rate", 0)
        is_crit = random.random() < crit_rate

        if is_crit:
            crit_multiplier = 1.5 + self.weapon_data.get("crit_damage", 0)
            base_damage = int(base_damage * crit_multiplier)
            return base_damage, True  # 返回伤害和是否暴击

        return base_damage, False

    def is_ranged_weapon(self):
        """当前武器是否为远程武器"""
        if self.weapon_traits:
            return self.weapon_traits.get("is_ranged", False)
        return False

    def can_attack(self):
        """是否可以攻击"""
        if self.attack_cooldown > 0:
            return False
        if self.is_reloading:
            return False

        # 左轮需要检查弹药
        if self.weapon_data and self.weapon_data.get("type") == WEAPON_TYPE_REVOLVER:
            if self.current_ammo <= 0:
                self.start_reload()
                return False

        return True

    def start_attack(self, target_pos=None):
        """开始攻击"""
        if not self.can_attack():
            return None

        self.is_attacking = True
        self.attack_timer = self.attack_duration

        # 计算攻击冷却
        attack_speed = 1.0
        if self.weapon_traits:
            attack_speed = self.weapon_traits.get("attack_speed", 1.0)
        # 匕首等武器有额外攻速加成
        attack_speed += self.weapon_data.get("attack_speed_bonus", 0)

        self.attack_cooldown = 1.0 / attack_speed

        # 远程武器创建投射物
        if self.is_ranged_weapon():
            return self._create_projectile(target_pos)
        else:
            # 近战武器创建hitbox
            return self._create_melee_hitbox()

    def _create_melee_hitbox(self):
        """创建近战攻击hitbox（360度环形攻击）"""
        if not self.weapon_traits:
            return None

        attack_range = self.weapon_traits.get("attack_range", 60)
        px, py = self.player.x, self.player.y

        # 创建以玩家为中心的环形攻击判定框
        hitbox_size = attack_range * 2
        hitbox = pygame.Rect(
            px - attack_range,
            py - attack_range,
            hitbox_size,
            hitbox_size
        )

        self.attack_hitbox = hitbox
        self.hitbox_active = True

        # 返回攻击数据
        damage, is_crit = self.get_attack_damage()
        return {
            "type": "melee",
            "hitbox": hitbox,
            "damage": damage,
            "is_crit": is_crit,
            "weapon": self.weapon_data,
            "effects": self._get_weapon_effects()
        }

    def _create_projectile(self, target_pos):
        """创建远程投射物"""
        if not self.weapon_traits or not target_pos:
            return None

        # 左轮消耗弹药
        if self.weapon_data.get("type") == WEAPON_TYPE_REVOLVER:
            self.current_ammo -= 1

        projectile_speed = self.weapon_traits.get("projectile_speed", 10)

        # 计算方向
        px, py = self.player.x, self.player.y
        dx = target_pos[0] - px
        dy = target_pos[1] - py
        dist = math.sqrt(dx * dx + dy * dy)
        if dist == 0:
            dist = 1

        # 法杖可能发射多个投射物
        multi_shot = self.weapon_data.get("multi_shot", 1)
        projectiles = []

        damage, is_crit = self.get_attack_damage()

        for i in range(multi_shot):
            # 多发时添加扩散角度
            angle_offset = 0
            if multi_shot > 1:
                spread = 30  # 度
                angle_offset = (i - (multi_shot - 1) / 2) * (spread / (multi_shot - 1)) if multi_shot > 1 else 0

            base_angle = math.atan2(dy, dx)
            angle = base_angle + math.radians(angle_offset)

            proj = {
                "type": "projectile",
                "x": px,
                "y": py,
                "vx": math.cos(angle) * projectile_speed,
                "vy": math.sin(angle) * projectile_speed,
                "damage": damage // multi_shot if multi_shot > 1 else damage,
                "is_crit": is_crit,
                "weapon": self.weapon_data,
                "homing": self.weapon_data.get("homing", False),
                "pierce": self.weapon_data.get("pierce", 0),
                "pierced_enemies": [],
                "aoe_radius": self.weapon_data.get("aoe_radius", 0),
                "effects": self._get_weapon_effects(),
                "range": self.weapon_traits.get("attack_range", 200),
                "traveled": 0,
            }
            projectiles.append(proj)

        return projectiles if len(projectiles) > 1 else projectiles[0] if projectiles else None

    def _get_weapon_effects(self):
        """获取武器特殊效果"""
        if not self.weapon_data:
            return {}

        effects = {}

        # 眩晕
        if "stun_chance" in self.weapon_data:
            effects["stun_chance"] = self.weapon_data["stun_chance"]

        # 背刺加成
        if "backstab_bonus" in self.weapon_data:
            effects["backstab_bonus"] = self.weapon_data["backstab_bonus"]

        # 持续伤害
        if "dot_damage" in self.weapon_data:
            effects["dot_damage"] = self.weapon_data["dot_damage"]
            effects["dot_duration"] = self.weapon_data.get("dot_duration", 3)

        # 击杀回血
        if "lifesteal_on_kill" in self.weapon_data:
            effects["lifesteal_on_kill"] = self.weapon_data["lifesteal_on_kill"]

        # 混乱效果
        if "confusion_chance" in self.weapon_data:
            effects["confusion_chance"] = self.weapon_data["confusion_chance"]

        # 诅咒降防
        if "curse_defense_reduce" in self.weapon_data:
            effects["curse_defense_reduce"] = self.weapon_data["curse_defense_reduce"]

        # 圣光伤害（对黑暗生物双倍）
        if self.weapon_data.get("holy_damage"):
            effects["holy_damage"] = True

        # 必中（无视闪避）
        if self.weapon_data.get("true_strike"):
            effects["true_strike"] = True

        # 对邪灵加成
        if "spirit_damage_bonus" in self.weapon_data:
            effects["spirit_damage_bonus"] = self.weapon_data["spirit_damage_bonus"]

        return effects

    def start_reload(self):
        """开始装填（左轮专用）"""
        if self.weapon_data and self.weapon_data.get("type") == WEAPON_TYPE_REVOLVER:
            if self.current_ammo < self.max_ammo and not self.is_reloading:
                self.is_reloading = True
                self.reload_time = self.reload_duration

    def update(self, dt):
        """更新武器状态"""
        # 更新攻击冷却
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        # 更新攻击动画
        if self.is_attacking:
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.is_attacking = False
                self.hitbox_active = False
                self.attack_hitbox = None

        # 更新装填
        if self.is_reloading:
            self.reload_time -= dt
            if self.reload_time <= 0:
                self.is_reloading = False
                self.current_ammo = self.max_ammo

    def get_weapon_info(self):
        """获取当前武器信息用于UI显示"""
        if not self.weapon_data:
            return None

        info = {
            "name": self.equipped_weapon,
            "type": self.weapon_data.get("type"),
            "quality": self.weapon_data.get("quality"),
            "attack": self.weapon_data.get("attack", 0),
            "special": self.weapon_data.get("special", ""),
            "desc": self.weapon_data.get("desc", ""),
            "is_ranged": self.is_ranged_weapon(),
        }

        # 左轮弹药信息
        if self.weapon_data.get("type") == WEAPON_TYPE_REVOLVER:
            info["ammo"] = self.current_ammo
            info["max_ammo"] = self.max_ammo
            info["is_reloading"] = self.is_reloading
            info["reload_progress"] = 1 - (self.reload_time / self.reload_duration) if self.is_reloading else 1

        return info

    def draw_weapon_ui(self, screen, fonts, x, y):
        """绘制武器UI（小型显示）"""
        if not self.weapon_data:
            return

        # 武器名称（带品质颜色）
        quality = self.weapon_data.get("quality", "common")
        color = QUALITY_COLORS.get(quality, (255, 255, 255))
        name_text = fonts["small"].render(self.equipped_weapon, True, color)
        screen.blit(name_text, (x, y))

        # 攻击力
        attack = self.weapon_data.get("attack", 0)
        atk_text = fonts["tiny"].render(f"ATK +{attack}", True, (200, 200, 200))
        screen.blit(atk_text, (x, y + 22))

        # 左轮弹药显示
        if self.weapon_data.get("type") == WEAPON_TYPE_REVOLVER:
            if self.is_reloading:
                ammo_text = fonts["tiny"].render("装填中...", True, (255, 200, 100))
            else:
                ammo_text = fonts["tiny"].render(f"弹药: {self.current_ammo}/{self.max_ammo}", True, (200, 200, 200))
            screen.blit(ammo_text, (x, y + 40))

        # 攻击冷却指示
        if self.attack_cooldown > 0:
            cd_width = 60
            cd_height = 4
            cd_ratio = self.attack_cooldown / (1.0 / self.weapon_traits.get("attack_speed", 1.0)) if self.weapon_traits else 0
            pygame.draw.rect(screen, (50, 50, 50), (x, y + 55, cd_width, cd_height))
            pygame.draw.rect(screen, (100, 200, 100), (x, y + 55, int(cd_width * (1 - cd_ratio)), cd_height))


class WeaponProjectile:
    """武器投射物类"""

    def __init__(self, data):
        self.x = data["x"]
        self.y = data["y"]
        self.vx = data["vx"]
        self.vy = data["vy"]
        self.damage = data["damage"]
        self.is_crit = data.get("is_crit", False)
        self.weapon = data.get("weapon", {})
        self.homing = data.get("homing", False)
        self.pierce = data.get("pierce", 0)
        self.pierced_enemies = data.get("pierced_enemies", [])
        self.aoe_radius = data.get("aoe_radius", 0)
        self.effects = data.get("effects", {})
        self.max_range = data.get("range", 200)
        self.traveled = data.get("traveled", 0)
        self.active = True
        self.size = 8

        # 根据武器类型设置颜色
        weapon_type = self.weapon.get("type", "")
        if weapon_type == WEAPON_TYPE_STAFF:
            self.color = (100, 150, 255)  # 蓝色魔法
        elif weapon_type == WEAPON_TYPE_BOW:
            self.color = (200, 150, 100)  # 棕色箭矢
        elif weapon_type == WEAPON_TYPE_REVOLVER:
            self.color = (255, 200, 100)  # 金色子弹
        else:
            self.color = (255, 255, 255)

    def update(self, dt, enemies=None):
        """更新投射物"""
        if not self.active:
            return

        # 追踪模式
        if self.homing and enemies:
            self._home_to_nearest(enemies)

        # 移动
        speed = math.sqrt(self.vx * self.vx + self.vy * self.vy)
        self.x += self.vx
        self.y += self.vy
        self.traveled += speed

        # 超出范围
        if self.traveled > self.max_range:
            self.active = False

    def _home_to_nearest(self, enemies):
        """追踪最近的敌人"""
        nearest = None
        min_dist = float('inf')

        for enemy in enemies:
            if not enemy.alive:
                continue
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < min_dist:
                min_dist = dist
                nearest = enemy

        if nearest and min_dist < 300:
            dx = nearest.x - self.x
            dy = nearest.y - self.y
            dist = max(1, min_dist)

            # 平滑转向
            target_vx = (dx / dist) * math.sqrt(self.vx * self.vx + self.vy * self.vy)
            target_vy = (dy / dist) * math.sqrt(self.vx * self.vx + self.vy * self.vy)

            self.vx = self.vx * 0.9 + target_vx * 0.1
            self.vy = self.vy * 0.9 + target_vy * 0.1

    def check_hit(self, enemy):
        """检查是否命中敌人"""
        if not self.active or not enemy.alive:
            return False

        # 已穿透的敌人不再检测
        if id(enemy) in self.pierced_enemies:
            return False

        dx = enemy.x - self.x
        dy = enemy.y - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist < enemy.size + self.size:
            self.pierced_enemies.append(id(enemy))

            # 检查穿透
            if len(self.pierced_enemies) > self.pierce:
                self.active = False

            return True

        return False

    def draw(self, screen, camera_x=0, camera_y=0):
        """绘制投射物"""
        if not self.active:
            return

        draw_x = int(self.x - camera_x)
        draw_y = int(self.y - camera_y)

        # 绘制投射物
        pygame.draw.circle(screen, self.color, (draw_x, draw_y), self.size)

        # 暴击时添加光效
        if self.is_crit:
            pygame.draw.circle(screen, (255, 255, 200), (draw_x, draw_y), self.size + 3, 2)

        # 拖尾效果
        trail_length = 3
        for i in range(trail_length):
            trail_x = draw_x - int(self.vx * (i + 1) * 0.3)
            trail_y = draw_y - int(self.vy * (i + 1) * 0.3)
            alpha = 150 - i * 40
            trail_color = tuple(max(0, c - i * 30) for c in self.color)
            pygame.draw.circle(screen, trail_color, (trail_x, trail_y), max(2, self.size - i * 2))


def apply_weapon_effects(enemy, effects, damage):
    """应用武器特殊效果到敌人"""
    result = {
        "damage": damage,
        "effects_applied": []
    }

    # 眩晕效果
    if "stun_chance" in effects:
        if random.random() < effects["stun_chance"]:
            if hasattr(enemy, 'apply_stun'):
                enemy.apply_stun(1.0)  # 眩晕1秒
                result["effects_applied"].append("眩晕")

    # 持续伤害
    if "dot_damage" in effects:
        if hasattr(enemy, 'apply_dot'):
            enemy.apply_dot(effects["dot_damage"], effects.get("dot_duration", 3))
            result["effects_applied"].append("持续伤害")

    # 降低防御
    if "curse_defense_reduce" in effects:
        if hasattr(enemy, 'apply_debuff'):
            enemy.apply_debuff("defense", -effects["curse_defense_reduce"], 5.0)
            result["effects_applied"].append("降防")

    # 混乱效果
    if "confusion_chance" in effects:
        if random.random() < effects["confusion_chance"]:
            if hasattr(enemy, 'apply_confusion'):
                enemy.apply_confusion(3.0)
                result["effects_applied"].append("混乱")

    # 圣光伤害（对暗属性敌人双倍）
    if effects.get("holy_damage"):
        enemy_type = getattr(enemy, 'enemy_type', '')
        dark_enemies = ["低级邪灵", "梦魇", "暗影猎手", "邪灵领主", "永暗巨兽"]
        if enemy_type in dark_enemies:
            result["damage"] *= 2
            result["effects_applied"].append("圣光加倍")

    # 对邪灵加成
    if "spirit_damage_bonus" in effects:
        enemy_type = getattr(enemy, 'enemy_type', '')
        spirit_enemies = ["低级邪灵", "梦魇", "邪灵领主"]
        if enemy_type in spirit_enemies:
            result["damage"] = int(result["damage"] * (1 + effects["spirit_damage_bonus"]))
            result["effects_applied"].append("对邪灵加伤")

    return result
