"""
Black Ops - 游戏HUD界面
"""

import pygame
import math
from settings import *


class GameHUD:
    """游戏内HUD界面"""

    def __init__(self, screen):
        self.screen = screen

        # 加载字体
        pygame.font.init()
        self.font_small = pygame.font.Font(None, FONT_SIZES['small'])
        self.font_medium = pygame.font.Font(None, FONT_SIZES['medium'])
        self.font_large = pygame.font.Font(None, FONT_SIZES['large'])

        # HUD元素
        self.damage_indicators = []  # 伤害方向指示器
        self.hit_marker_timer = 0
        self.kill_feed = []  # 击杀信息

    def update(self, dt):
        """更新HUD状态"""
        # 更新命中标记
        if self.hit_marker_timer > 0:
            self.hit_marker_timer -= dt

        # 更新伤害指示器
        self.damage_indicators = [
            (angle, timer - dt)
            for angle, timer in self.damage_indicators
            if timer - dt > 0
        ]

        # 更新击杀信息
        self.kill_feed = [
            (text, timer - dt)
            for text, timer in self.kill_feed
            if timer - dt > 0
        ]

    def show_hit_marker(self):
        """显示命中标记"""
        self.hit_marker_timer = 0.2

    def show_damage_indicator(self, angle):
        """显示伤害方向指示"""
        self.damage_indicators.append((angle, 1.0))

    def add_kill_feed(self, text):
        """添加击杀信息"""
        self.kill_feed.append((text, 5.0))
        if len(self.kill_feed) > 5:
            self.kill_feed.pop(0)

    def draw(self, player, weapon, mission_system=None):
        """绘制HUD"""
        # 准心
        self._draw_crosshair(player.is_aiming)

        # 命中标记
        if self.hit_marker_timer > 0:
            self._draw_hit_marker()

        # 伤害指示器
        self._draw_damage_indicators(player.angle)

        # 生命值和护甲
        self._draw_health_armor(player)

        # 弹药信息
        if weapon:
            self._draw_ammo(weapon, player.is_reloading)

        # 武器信息
        if weapon:
            self._draw_weapon_info(weapon, player)

        # 任务目标
        if mission_system:
            self._draw_objectives(mission_system)

        # 击杀信息
        self._draw_kill_feed()

        # 小地图
        # self._draw_minimap(player)

    def _draw_crosshair(self, is_aiming):
        """绘制准心"""
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        if is_aiming:
            # 瞄准时更精确的准心
            size = 8
            gap = 3
            color = (0, 255, 0)
            thickness = 1
        else:
            # 普通准心
            size = 15
            gap = 5
            color = (255, 255, 255)
            thickness = 2

        # 四条线
        pygame.draw.line(self.screen, color, (cx - size, cy), (cx - gap, cy), thickness)
        pygame.draw.line(self.screen, color, (cx + gap, cy), (cx + size, cy), thickness)
        pygame.draw.line(self.screen, color, (cx, cy - size), (cx, cy - gap), thickness)
        pygame.draw.line(self.screen, color, (cx, cy + gap), (cx, cy + size), thickness)

        # 中心点
        if not is_aiming:
            pygame.draw.circle(self.screen, color, (cx, cy), 2)

    def _draw_hit_marker(self):
        """绘制命中标记 (X形)"""
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        size = 12
        color = (255, 255, 255)

        alpha = int(255 * (self.hit_marker_timer / 0.2))
        surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)

        pygame.draw.line(surface, (*color, alpha), (0, 0), (size - 4, size - 4), 3)
        pygame.draw.line(surface, (*color, alpha), (size * 2, 0), (size + 4, size - 4), 3)
        pygame.draw.line(surface, (*color, alpha), (0, size * 2), (size - 4, size + 4), 3)
        pygame.draw.line(surface, (*color, alpha), (size * 2, size * 2), (size + 4, size + 4), 3)

        self.screen.blit(surface, (cx - size, cy - size))

    def _draw_damage_indicators(self, player_angle):
        """绘制伤害方向指示器"""
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        radius = 100

        for damage_angle, timer in self.damage_indicators:
            # 计算相对角度
            rel_angle = damage_angle - player_angle + math.pi

            # 计算指示器位置
            x = cx + math.cos(rel_angle) * radius
            y = cy + math.sin(rel_angle) * radius

            # 绘制红色弧形
            alpha = int(200 * (timer / 1.0))
            size = 30

            # 绘制三角形指向伤害来源
            angle1 = rel_angle - 0.3
            angle2 = rel_angle + 0.3
            points = [
                (x, y),
                (x + math.cos(angle1) * size, y + math.sin(angle1) * size),
                (x + math.cos(angle2) * size, y + math.sin(angle2) * size),
            ]

            surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.polygon(surface, (255, 0, 0, alpha), points)
            self.screen.blit(surface, (0, 0))

    def _draw_health_armor(self, player):
        """绘制生命值和护甲条"""
        # 背景
        bar_width = 200
        bar_height = 20
        x = 30
        y = SCREEN_HEIGHT - 80

        # 生命值背景
        pygame.draw.rect(self.screen, (40, 40, 40), (x, y, bar_width, bar_height))
        # 生命值
        hp_width = int(bar_width * (player.hp / player.max_hp))
        hp_color = HUD_HEALTH if player.hp > 30 else (255, 100, 100)
        pygame.draw.rect(self.screen, hp_color, (x, y, hp_width, bar_height))
        # 边框
        pygame.draw.rect(self.screen, WHITE, (x, y, bar_width, bar_height), 2)
        # 文字
        hp_text = self.font_medium.render(f"{int(player.hp)}", True, WHITE)
        self.screen.blit(hp_text, (x + bar_width + 10, y))

        # 护甲
        if player.armor > 0 or True:  # 始终显示护甲条
            y -= 25
            pygame.draw.rect(self.screen, (40, 40, 40), (x, y, bar_width, bar_height - 5))
            armor_width = int(bar_width * (player.armor / player.max_armor))
            pygame.draw.rect(self.screen, HUD_ARMOR, (x, y, armor_width, bar_height - 5))
            pygame.draw.rect(self.screen, WHITE, (x, y, bar_width, bar_height - 5), 1)
            armor_text = self.font_small.render(f"{int(player.armor)}", True, WHITE)
            self.screen.blit(armor_text, (x + bar_width + 10, y))

    def _draw_ammo(self, weapon, is_reloading):
        """绘制弹药信息"""
        x = SCREEN_WIDTH - 200
        y = SCREEN_HEIGHT - 80

        # 当前弹匣 / 备弹
        ammo_color = HUD_AMMO if weapon.current_ammo > 0 else RED
        ammo_text = self.font_large.render(f"{weapon.current_ammo}", True, ammo_color)
        self.screen.blit(ammo_text, (x, y))

        slash_text = self.font_medium.render(f"/ {weapon.reserve_ammo}", True, LIGHT_GRAY)
        self.screen.blit(slash_text, (x + 50, y + 10))

        # 换弹提示
        if is_reloading:
            reload_text = self.font_medium.render("RELOADING...", True, YELLOW)
            text_rect = reload_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(reload_text, text_rect)

    def _draw_weapon_info(self, weapon, player):
        """绘制武器信息"""
        x = SCREEN_WIDTH - 200
        y = SCREEN_HEIGHT - 45

        # 武器名称
        name_text = self.font_small.render(weapon.name, True, WHITE)
        self.screen.blit(name_text, (x, y))

        # 手雷数量
        if player.grenades > 0:
            grenade_text = self.font_small.render(f"G: {player.grenades}", True, ORANGE)
            self.screen.blit(grenade_text, (x + 120, y))

    def _draw_objectives(self, mission_system):
        """绘制任务目标"""
        x = 30
        y = 30

        # 任务名称
        if mission_system.current_mission:
            mission_name = mission_system.current_mission.get('name', '')
            name_text = self.font_medium.render(mission_name, True, YELLOW)
            self.screen.blit(name_text, (x, y))
            y += 30

        # 当前目标
        current_obj = mission_system.get_current_objective()
        if current_obj:
            obj_text = self.font_small.render(f"> {current_obj.description}", True, WHITE)
            self.screen.blit(obj_text, (x, y))

    def _draw_kill_feed(self):
        """绘制击杀信息"""
        x = SCREEN_WIDTH - 250
        y = 30

        for text, timer in self.kill_feed:
            alpha = min(255, int(255 * (timer / 5.0) * 2))
            surface = self.font_small.render(text, True, WHITE)
            surface.set_alpha(alpha)
            self.screen.blit(surface, (x, y))
            y += 25


class DialogueBox:
    """对话框"""

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, FONT_SIZES['medium'])
        self.current_text = ""
        self.display_text = ""
        self.char_index = 0
        self.char_timer = 0
        self.is_active = False
        self.auto_close_timer = 0

    def show(self, text, auto_close=3.0):
        """显示对话"""
        self.current_text = text
        self.display_text = ""
        self.char_index = 0
        self.char_timer = 0
        self.is_active = True
        self.auto_close_timer = auto_close

    def update(self, dt):
        """更新对话框"""
        if not self.is_active:
            return

        # 逐字显示
        if self.char_index < len(self.current_text):
            self.char_timer += dt
            if self.char_timer > 0.03:
                self.char_timer = 0
                self.char_index += 1
                self.display_text = self.current_text[:self.char_index]
        else:
            # 自动关闭
            self.auto_close_timer -= dt
            if self.auto_close_timer <= 0:
                self.is_active = False

    def skip(self):
        """跳过当前对话"""
        if self.char_index < len(self.current_text):
            self.char_index = len(self.current_text)
            self.display_text = self.current_text
        else:
            self.is_active = False

    def draw(self):
        """绘制对话框"""
        if not self.is_active:
            return

        # 背景
        box_height = 80
        box_y = SCREEN_HEIGHT - box_height - 20
        pygame.draw.rect(
            self.screen,
            (0, 0, 0, 200),
            (20, box_y, SCREEN_WIDTH - 40, box_height)
        )
        pygame.draw.rect(
            self.screen,
            WHITE,
            (20, box_y, SCREEN_WIDTH - 40, box_height),
            2
        )

        # 文字
        text_surface = self.font.render(self.display_text, True, WHITE)
        self.screen.blit(text_surface, (40, box_y + 25))

        # 按键提示
        if self.char_index >= len(self.current_text):
            hint = self.font.render("[SPACE]", True, GRAY)
            self.screen.blit(hint, (SCREEN_WIDTH - 120, box_y + box_height - 30))


class MissionBriefing:
    """任务简报界面"""

    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, FONT_SIZES['title'])
        self.font_subtitle = pygame.font.Font(None, FONT_SIZES['large'])
        self.font_text = pygame.font.Font(None, FONT_SIZES['medium'])

    def draw(self, mission_data):
        """绘制任务简报"""
        # 半透明背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        y = 100

        # 任务名称
        title = self.font_title.render(mission_data['name'], True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.screen.blit(title, title_rect)
        y += 50

        # 副标题
        if 'subtitle' in mission_data:
            subtitle = self.font_subtitle.render(mission_data['subtitle'], True, LIGHT_GRAY)
            subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(subtitle, subtitle_rect)
        y += 80

        # 任务简报
        if 'briefing' in mission_data:
            for line in mission_data['briefing']:
                text = self.font_text.render(line, True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
                self.screen.blit(text, text_rect)
                y += 35

        y += 40

        # 目标列表
        objectives_title = self.font_subtitle.render("OBJECTIVES", True, ORANGE)
        self.screen.blit(objectives_title, (SCREEN_WIDTH // 2 - 100, y))
        y += 40

        for obj in mission_data['objectives']:
            marker = "[!]" if obj.get('required', True) else "[ ]"
            obj_text = self.font_text.render(f"{marker} {obj['description']}", True, WHITE)
            self.screen.blit(obj_text, (SCREEN_WIDTH // 2 - 150, y))
            y += 30

        # 开始提示
        y = SCREEN_HEIGHT - 80
        hint = self.font_text.render("Press SPACE to start mission", True, GREEN)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.screen.blit(hint, hint_rect)
