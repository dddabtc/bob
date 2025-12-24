"""
Black Ops - 武器系统
"""

import pygame
import math
import random
from settings import *

# 导入武器数据
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.weapons import WEAPONS, AMMO_TYPES


class Weapon:
    """武器类"""

    def __init__(self, weapon_id):
        if weapon_id not in WEAPONS:
            raise ValueError(f"Unknown weapon: {weapon_id}")

        data = WEAPONS[weapon_id]

        self.id = weapon_id
        self.name = data["name"]
        self.type = data["type"]
        self.damage = data["damage"]
        self.fire_rate = data["fire_rate"]
        self.magazine = data["magazine"]
        self.max_ammo = data["max_ammo"]
        self.reload_time = data["reload_time"]
        self.accuracy = data["accuracy"]
        self.recoil = data["recoil"]
        self.range = data["range"]
        self.is_auto = data["is_auto"]
        self.has_scope = data["has_scope"]
        self.description = data["description"]

        # 可选属性
        self.scope_zoom = data.get("scope_zoom", 1.0)
        self.pellets = data.get("pellets", 1)
        self.spread = data.get("spread", 0)
        self.single_reload = data.get("single_reload", False)

        # 当前状态
        self.current_ammo = self.magazine
        self.reserve_ammo = self.max_ammo

        # 动画状态
        self.recoil_offset = 0
        self.muzzle_flash = 0

    def can_shoot(self):
        """检查是否可以射击"""
        return self.current_ammo > 0

    def shoot(self):
        """射击 - 返回射击数据"""
        if not self.can_shoot():
            return None

        self.current_ammo -= 1
        self.recoil_offset = self.recoil * 20
        self.muzzle_flash = 0.1

        return {
            'damage': self.damage,
            'pellets': self.pellets,
            'spread': self.spread,
            'range': self.range,
        }

    def update(self, dt):
        """更新武器状态"""
        # 后坐力恢复
        if self.recoil_offset > 0:
            self.recoil_offset -= 100 * dt
            if self.recoil_offset < 0:
                self.recoil_offset = 0

        # 枪口火焰
        if self.muzzle_flash > 0:
            self.muzzle_flash -= dt

    def get_ammo_display(self):
        """获取弹药显示"""
        return f"{self.current_ammo}/{self.reserve_ammo}"


class WeaponManager:
    """武器管理器"""

    def __init__(self):
        self.unlocked_weapons = set(['m1911', 'knife'])  # 初始解锁

    def unlock_weapon(self, weapon_id):
        """解锁武器"""
        if weapon_id in WEAPONS:
            self.unlocked_weapons.add(weapon_id)

    def is_unlocked(self, weapon_id):
        """检查武器是否解锁"""
        return weapon_id in self.unlocked_weapons

    def create_weapon(self, weapon_id):
        """创建武器实例"""
        return Weapon(weapon_id)

    def get_weapon_info(self, weapon_id):
        """获取武器信息"""
        return WEAPONS.get(weapon_id)

    def get_all_weapons(self):
        """获取所有武器"""
        return WEAPONS

    def get_unlocked_weapons(self):
        """获取已解锁的武器"""
        return {wid: WEAPONS[wid] for wid in self.unlocked_weapons if wid in WEAPONS}


class WeaponRenderer:
    """高画质武器渲染器"""

    def __init__(self, screen):
        self.screen = screen
        self.weapon_sprites = {}
        self._generate_hd_weapon_sprites()
        self.sway_timer = 0
        self.bob_timer = 0

    def _generate_hd_weapon_sprites(self):
        """生成高清武器图像"""

        # M1911 手枪 (高清版)
        pistol = pygame.Surface((160, 120), pygame.SRCALPHA)
        # 套筒
        pygame.draw.rect(pistol, (45, 45, 50), (40, 45, 90, 35))
        pygame.draw.rect(pistol, (55, 55, 60), (40, 45, 90, 8))  # 高光
        pygame.draw.rect(pistol, (35, 35, 40), (40, 72, 90, 8))  # 阴影
        # 枪管
        pygame.draw.rect(pistol, (50, 50, 55), (120, 52, 35, 22))
        pygame.draw.rect(pistol, (60, 60, 65), (120, 52, 35, 5))  # 高光
        # 握把
        pygame.draw.polygon(pistol, (70, 50, 35), [(40, 75), (55, 75), (60, 115), (35, 115)])
        # 握把纹理
        for i in range(8):
            y = 80 + i * 4
            pygame.draw.line(pistol, (55, 38, 25), (42, y), (55, y), 1)
        # 扳机护圈
        pygame.draw.arc(pistol, (40, 40, 45), (55, 78, 25, 20), 3.14, 6.28, 3)
        # 扳机
        pygame.draw.rect(pistol, (35, 35, 40), (65, 82, 4, 12))
        # 准星
        pygame.draw.rect(pistol, (60, 60, 65), (148, 45, 6, 10))
        # 击锤
        pygame.draw.rect(pistol, (40, 40, 45), (42, 38, 15, 10))
        self.weapon_sprites['m1911'] = pistol
        self.weapon_sprites['python'] = pistol

        # M16 突击步枪 (高清版)
        rifle = pygame.Surface((350, 140), pygame.SRCALPHA)
        # 枪托
        pygame.draw.polygon(rifle, (65, 45, 30), [(15, 70), (80, 60), (85, 90), (15, 95)])
        pygame.draw.polygon(rifle, (75, 55, 38), [(15, 70), (80, 60), (80, 75), (15, 82)])  # 高光
        # 托底
        pygame.draw.rect(rifle, (50, 35, 22), (5, 75, 15, 18))
        # 机匣
        pygame.draw.rect(rifle, (42, 42, 48), (75, 52, 130, 42))
        pygame.draw.rect(rifle, (52, 52, 58), (75, 52, 130, 10))  # 高光
        pygame.draw.rect(rifle, (32, 32, 38), (75, 84, 130, 10))  # 阴影
        # 提把/瞄准镜座
        pygame.draw.rect(rifle, (45, 45, 50), (120, 35, 50, 20))
        pygame.draw.rect(rifle, (55, 55, 60), (122, 37, 46, 5))  # 高光
        # 弹匣
        pygame.draw.rect(rifle, (38, 38, 42), (115, 90, 25, 45))
        pygame.draw.rect(rifle, (48, 48, 52), (115, 90, 25, 8))  # 高光
        # 弹匣底部
        pygame.draw.rect(rifle, (30, 30, 35), (113, 130, 29, 8))
        # 护木
        pygame.draw.rect(rifle, (35, 35, 40), (200, 55, 70, 35))
        pygame.draw.rect(rifle, (45, 45, 50), (200, 55, 70, 8))  # 高光
        # 枪管
        pygame.draw.rect(rifle, (50, 50, 55), (265, 62, 80, 18))
        pygame.draw.rect(rifle, (60, 60, 65), (265, 62, 80, 4))  # 高光
        # 消焰器
        pygame.draw.rect(rifle, (40, 40, 45), (340, 58, 8, 26))
        # 准星
        pygame.draw.rect(rifle, (50, 50, 55), (335, 50, 8, 15))
        self.weapon_sprites['m16'] = rifle
        self.weapon_sprites['commando'] = rifle

        # AK47 (略有不同的外观)
        ak = pygame.Surface((350, 140), pygame.SRCALPHA)
        # 枪托 (木质)
        pygame.draw.polygon(ak, (100, 65, 35), [(10, 72), (85, 60), (90, 92), (10, 98)])
        pygame.draw.polygon(ak, (115, 78, 45), [(10, 72), (85, 60), (85, 75), (10, 82)])
        # 机匣
        pygame.draw.rect(ak, (45, 45, 48), (80, 50, 125, 45))
        pygame.draw.rect(ak, (55, 55, 58), (80, 50, 125, 10))
        # 弹匣 (弧形)
        pygame.draw.polygon(ak, (40, 40, 42), [(120, 92), (145, 92), (155, 140), (110, 140)])
        # 护木 (木质)
        pygame.draw.rect(ak, (95, 60, 32), (200, 55, 65, 38))
        pygame.draw.rect(ak, (110, 75, 42), (200, 55, 65, 8))
        # 导气管
        pygame.draw.rect(ak, (50, 50, 52), (200, 48, 120, 10))
        # 枪管
        pygame.draw.rect(ak, (48, 48, 52), (260, 62, 85, 16))
        # 准星
        pygame.draw.polygon(ak, (45, 45, 48), [(338, 45), (345, 65), (352, 45)])
        self.weapon_sprites['ak47'] = ak

        # MP5 冲锋枪 (高清版)
        smg = pygame.Surface((280, 130), pygame.SRCALPHA)
        # 枪托 (伸缩)
        pygame.draw.rect(smg, (40, 40, 45), (15, 62, 45, 12))
        pygame.draw.rect(smg, (50, 50, 55), (15, 62, 45, 3))
        # 机匣
        pygame.draw.rect(smg, (42, 42, 48), (55, 48, 100, 40))
        pygame.draw.rect(smg, (52, 52, 58), (55, 48, 100, 10))
        # 握把
        pygame.draw.polygon(smg, (45, 45, 50), [(70, 85), (90, 85), (95, 125), (65, 125)])
        # 扳机护圈
        pygame.draw.arc(smg, (40, 40, 45), (88, 88, 22, 18), 3.14, 6.28, 2)
        # 弹匣
        pygame.draw.rect(smg, (38, 38, 42), (100, 85, 20, 40))
        # 护木
        pygame.draw.rect(smg, (48, 48, 52), (150, 52, 55, 32))
        # 枪管 (带消音器效果)
        pygame.draw.rect(smg, (45, 45, 50), (200, 58, 75, 22))
        pygame.draw.rect(smg, (55, 55, 60), (200, 58, 75, 5))
        # 准星
        pygame.draw.rect(smg, (50, 50, 55), (268, 50, 6, 12))
        self.weapon_sprites['mp5'] = smg
        self.weapon_sprites['mac11'] = smg

        # L96 狙击枪 (高清版)
        sniper = pygame.Surface((400, 150), pygame.SRCALPHA)
        # 枪托 (战术型)
        pygame.draw.polygon(sniper, (55, 55, 60), [(8, 80), (100, 62), (105, 100), (8, 110)])
        pygame.draw.polygon(sniper, (65, 65, 70), [(8, 80), (100, 62), (100, 78), (8, 92)])
        # 托腮板
        pygame.draw.rect(sniper, (50, 50, 55), (30, 55, 40, 15))
        # 机匣
        pygame.draw.rect(sniper, (45, 45, 50), (95, 55, 150, 48))
        pygame.draw.rect(sniper, (55, 55, 60), (95, 55, 150, 12))
        # 瞄准镜
        pygame.draw.rect(sniper, (35, 35, 40), (115, 25, 100, 35))
        pygame.draw.ellipse(sniper, (25, 25, 30), (108, 30, 25, 25))  # 物镜
        pygame.draw.ellipse(sniper, (40, 60, 80), (112, 34, 17, 17))  # 镜片反光
        pygame.draw.ellipse(sniper, (25, 25, 30), (198, 32, 22, 22))  # 目镜
        # 镜座
        pygame.draw.rect(sniper, (40, 40, 45), (120, 52, 30, 8))
        pygame.draw.rect(sniper, (40, 40, 45), (180, 52, 30, 8))
        # 弹匣
        pygame.draw.rect(sniper, (40, 40, 45), (160, 100, 30, 35))
        # 拉机柄
        pygame.draw.rect(sniper, (50, 50, 55), (200, 58, 35, 12))
        pygame.draw.ellipse(sniper, (45, 45, 50), (228, 55, 15, 18))
        # 枪管 (加长)
        pygame.draw.rect(sniper, (48, 48, 52), (240, 68, 155, 20))
        pygame.draw.rect(sniper, (58, 58, 62), (240, 68, 155, 5))
        # 消焰器
        pygame.draw.rect(sniper, (42, 42, 46), (388, 62, 10, 32))
        self.weapon_sprites['l96'] = sniper
        self.weapon_sprites['dragunov'] = sniper

        # SPAS-12 霰弹枪 (高清版)
        shotgun = pygame.Surface((330, 140), pygame.SRCALPHA)
        # 枪托 (折叠)
        pygame.draw.polygon(shotgun, (60, 45, 30), [(8, 72), (75, 58), (80, 95), (8, 102)])
        pygame.draw.polygon(shotgun, (72, 55, 38), [(8, 72), (75, 58), (75, 72), (8, 82)])
        # 机匣
        pygame.draw.rect(shotgun, (42, 42, 48), (70, 48, 120, 50))
        pygame.draw.rect(shotgun, (52, 52, 58), (70, 48, 120, 12))
        # 握把
        pygame.draw.polygon(shotgun, (48, 48, 52), [(85, 95), (108, 95), (115, 138), (78, 138)])
        # 泵动护木
        pygame.draw.rect(shotgun, (40, 40, 45), (185, 75, 65, 25))
        pygame.draw.rect(shotgun, (50, 50, 55), (185, 75, 65, 6))
        # 弹仓管
        pygame.draw.rect(shotgun, (46, 46, 50), (185, 52, 130, 20))
        pygame.draw.rect(shotgun, (56, 56, 60), (185, 52, 130, 5))
        # 枪管
        pygame.draw.rect(shotgun, (48, 48, 52), (185, 72, 140, 18))
        pygame.draw.rect(shotgun, (58, 58, 62), (185, 72, 140, 4))
        # 准星
        pygame.draw.rect(shotgun, (50, 50, 55), (318, 62, 8, 15))
        self.weapon_sprites['spas12'] = shotgun
        self.weapon_sprites['stakeout'] = shotgun

        # 战术刀 (高清版)
        knife = pygame.Surface((200, 80), pygame.SRCALPHA)
        # 刀刃
        pygame.draw.polygon(knife, (180, 185, 195), [(60, 35), (190, 25), (190, 50), (60, 48)])
        # 刀刃高光
        pygame.draw.polygon(knife, (210, 215, 225), [(65, 36), (185, 27), (185, 35), (65, 42)])
        # 刀背 (锯齿)
        for i in range(12):
            x = 70 + i * 10
            pygame.draw.polygon(knife, (150, 155, 165), [(x, 25), (x + 5, 20), (x + 10, 25)])
        # 血槽
        pygame.draw.line(knife, (140, 145, 155), (80, 40), (175, 32), 2)
        # 护手
        pygame.draw.rect(knife, (55, 55, 60), (50, 28, 15, 28))
        pygame.draw.rect(knife, (65, 65, 70), (50, 28, 15, 6))
        # 握把
        pygame.draw.rect(knife, (60, 42, 28), (8, 32, 48, 22))
        # 握把纹理
        for i in range(6):
            x = 12 + i * 7
            pygame.draw.line(knife, (48, 32, 20), (x, 34), (x, 52), 2)
        # 尾锥
        pygame.draw.polygon(knife, (50, 50, 55), [(5, 38), (12, 32), (12, 54), (5, 48)])
        self.weapon_sprites['knife'] = knife

    def draw_weapon(self, weapon, is_aiming=False, recoil_offset=0):
        """绘制武器 (带摇摆动画)"""
        if weapon.id not in self.weapon_sprites:
            return

        sprite = self.weapon_sprites[weapon.id]

        # 计算基础位置
        if is_aiming and weapon.has_scope:
            x = SCREEN_WIDTH // 2 - sprite.get_width() // 2
            y = SCREEN_HEIGHT - sprite.get_height() - 80
        else:
            x = SCREEN_WIDTH - sprite.get_width() - 30
            y = SCREEN_HEIGHT - sprite.get_height() - 20

        # 应用后坐力
        y += int(recoil_offset)

        # 绘制枪口火焰 (高质量)
        if weapon.muzzle_flash > 0:
            flash_ratio = weapon.muzzle_flash / 0.1
            flash_x = x + sprite.get_width() - 5
            flash_y = y + sprite.get_height() // 3

            # 多层火焰效果
            for i in range(4):
                size = int((45 - i * 10) * flash_ratio)
                if size > 0:
                    colors = [(255, 255, 220), (255, 220, 100), (255, 180, 50), (255, 100, 20)]
                    pygame.draw.circle(self.screen, colors[i], (flash_x, flash_y), size)

            # 火花
            import random
            random.seed(int(flash_ratio * 100))
            for _ in range(5):
                spark_x = flash_x + random.randint(-20, 40)
                spark_y = flash_y + random.randint(-15, 15)
                pygame.draw.circle(self.screen, (255, 255, 200), (spark_x, spark_y), 2)

        # 绘制武器阴影
        shadow = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
        shadow.blit(sprite, (0, 0))
        shadow.fill((0, 0, 0, 60), special_flags=pygame.BLEND_RGBA_MULT)
        self.screen.blit(shadow, (x + 4, y + 4))

        # 绘制武器
        self.screen.blit(sprite, (x, y))

    def draw_scope(self):
        """绘制高清狙击镜"""
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        radius = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 3

        # 黑色遮罩
        mask = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 245))
        pygame.draw.circle(mask, (0, 0, 0, 0), (cx, cy), radius)
        self.screen.blit(mask, (0, 0))

        # 镜框 (多层)
        pygame.draw.circle(self.screen, (15, 15, 18), (cx, cy), radius + 5, 8)
        pygame.draw.circle(self.screen, (25, 25, 28), (cx, cy), radius, 4)
        pygame.draw.circle(self.screen, (40, 40, 45), (cx, cy), radius - 3, 2)

        # 内部轻微暗角
        vignette = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        for r in range(radius, radius - 30, -1):
            alpha = int((radius - r) * 3)
            pygame.draw.circle(vignette, (0, 0, 0, alpha), (radius, radius), r, 1)
        self.screen.blit(vignette, (cx - radius, cy - radius))

        # 十字线 (Mil-Dot风格)
        line_color = (0, 0, 0)
        thick_line = (20, 20, 25)

        # 主十字线 (粗)
        pygame.draw.line(self.screen, thick_line, (cx - radius + 20, cy), (cx - 25, cy), 3)
        pygame.draw.line(self.screen, thick_line, (cx + 25, cy), (cx + radius - 20, cy), 3)
        pygame.draw.line(self.screen, thick_line, (cx, cy - radius + 20), (cx, cy - 25), 3)
        pygame.draw.line(self.screen, thick_line, (cx, cy + 25), (cx, cy + radius - 20), 3)

        # 细十字线
        pygame.draw.line(self.screen, line_color, (cx - 20, cy), (cx - 5, cy), 1)
        pygame.draw.line(self.screen, line_color, (cx + 5, cy), (cx + 20, cy), 1)
        pygame.draw.line(self.screen, line_color, (cx, cy - 20), (cx, cy - 5), 1)
        pygame.draw.line(self.screen, line_color, (cx, cy + 5), (cx, cy + 20), 1)

        # Mil-Dot 测距点
        for i in range(1, 8):
            dist = i * 28
            # 水平
            if cx - dist > cx - radius + 30:
                pygame.draw.circle(self.screen, line_color, (cx - dist, cy), 3)
            if cx + dist < cx + radius - 30:
                pygame.draw.circle(self.screen, line_color, (cx + dist, cy), 3)
            # 垂直
            if cy + dist < cy + radius - 30:
                pygame.draw.circle(self.screen, line_color, (cx, cy + dist), 3)
            if cy - dist > cy - radius + 30:
                pygame.draw.circle(self.screen, line_color, (cx, cy - dist), 3)

        # 测距刻度线
        for i in range(1, 6):
            y = cy + i * 35
            if y < cy + radius - 30:
                w = 12 - i * 2
                pygame.draw.line(self.screen, line_color, (cx - w, y), (cx + w, y), 1)

        # 中心红点
        pygame.draw.circle(self.screen, (180, 30, 30), (cx, cy), 3)
        pygame.draw.circle(self.screen, (255, 50, 50), (cx, cy), 2)
