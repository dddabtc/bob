"""
Boss战斗UI系统
显示Boss血条、阶段、技能预警等
"""

import pygame
import math
import time
from settings import *


class BossUI:
    """Boss战斗UI管理器"""

    def __init__(self, fonts):
        self.fonts = fonts
        self.current_boss = None
        self.show_intro = False
        self.intro_timer = 0
        self.show_victory = False
        self.victory_timer = 0

        # 血条动画
        self.displayed_hp_ratio = 1.0
        self.hp_animation_speed = 2.0

        # UI尺寸
        self.bar_width = 600
        self.bar_height = 25
        self.bar_x = (SCREEN_WIDTH - self.bar_width) // 2
        self.bar_y = 30

    def set_boss(self, boss):
        """设置当前Boss"""
        self.current_boss = boss
        self.displayed_hp_ratio = 1.0
        self.show_intro = True
        self.intro_timer = 2.5

    def clear_boss(self):
        """清除当前Boss"""
        if self.current_boss:
            self.show_victory = True
            self.victory_timer = 3.0
        self.current_boss = None

    def update(self, dt):
        """更新UI状态"""
        # 更新介绍动画
        if self.show_intro:
            self.intro_timer -= dt
            if self.intro_timer <= 0:
                self.show_intro = False

        # 更新胜利动画
        if self.show_victory:
            self.victory_timer -= dt
            if self.victory_timer <= 0:
                self.show_victory = False

        # 更新血条动画
        if self.current_boss:
            target_ratio = self.current_boss.hp / self.current_boss.max_hp
            if self.displayed_hp_ratio > target_ratio:
                self.displayed_hp_ratio -= self.hp_animation_speed * dt
                self.displayed_hp_ratio = max(target_ratio, self.displayed_hp_ratio)

    def draw(self, screen):
        """绘制Boss UI"""
        # 绘制Boss入场动画
        if self.show_intro and self.current_boss:
            self._draw_intro(screen)
            return  # 入场动画期间不绘制其他UI

        # 绘制胜利画面
        if self.show_victory:
            self._draw_victory(screen)

        # 绘制Boss血条和信息
        if self.current_boss:
            self._draw_boss_bar(screen)
            self._draw_phase_indicator(screen)

    def _draw_intro(self, screen):
        """绘制Boss入场动画"""
        # 半透明背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        alpha = int(min(150, (2.5 - self.intro_timer) * 200))
        overlay.fill((0, 0, 0, alpha))
        screen.blit(overlay, (0, 0))

        # Boss名称（渐入效果）
        name_alpha = int(min(255, (2.5 - self.intro_timer) * 300))
        name_surface = pygame.Surface((SCREEN_WIDTH, 100), pygame.SRCALPHA)

        boss_name = self.current_boss.name
        name_text = self.fonts["large"].render(boss_name, True, (255, 200, 100))
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, 50))

        # 添加阴影效果
        shadow_text = self.fonts["large"].render(boss_name, True, (50, 30, 0))
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 3, 53))
        name_surface.blit(shadow_text, shadow_rect)
        name_surface.blit(name_text, name_rect)
        name_surface.set_alpha(name_alpha)

        screen.blit(name_surface, (0, SCREEN_HEIGHT // 2 - 80))

        # 副标题
        if self.intro_timer < 2.0:
            subtitle = "BOSS战开始!"
            sub_text = self.fonts["medium"].render(subtitle, True, (200, 50, 50))
            sub_rect = sub_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(sub_text, sub_rect)

        # 血量信息
        if self.intro_timer < 1.5:
            hp_info = f"HP: {self.current_boss.hp} / 阶段: {self.current_boss.max_phases}"
            hp_text = self.fonts["small"].render(hp_info, True, (180, 180, 180))
            hp_rect = hp_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(hp_text, hp_rect)

    def _draw_victory(self, screen):
        """绘制胜利画面"""
        # 半透明背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        alpha = int(max(0, min(100, self.victory_timer * 50)))
        overlay.fill((0, 0, 0, alpha))
        screen.blit(overlay, (0, 0))

        # 胜利文字
        victory_text = self.fonts["large"].render("BOSS 已击败!", True, GOLD)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # 添加闪光效果
        glow_alpha = int(100 + 50 * math.sin(time.time() * 5))
        glow_surf = pygame.Surface((victory_rect.width + 20, victory_rect.height + 10), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (255, 215, 0, glow_alpha), glow_surf.get_rect(), border_radius=5)
        screen.blit(glow_surf, (victory_rect.x - 10, victory_rect.y - 5))
        screen.blit(victory_text, victory_rect)

    def _draw_boss_bar(self, screen):
        """绘制Boss血条"""
        boss = self.current_boss

        # 血条背景
        bg_rect = pygame.Rect(self.bar_x - 5, self.bar_y - 5, self.bar_width + 10, self.bar_height + 10)
        pygame.draw.rect(screen, (20, 20, 30), bg_rect, border_radius=5)
        pygame.draw.rect(screen, (80, 60, 40), bg_rect, 2, border_radius=5)

        # 当前血量背景（用于动画效果）
        hp_ratio = boss.hp / boss.max_hp
        if self.displayed_hp_ratio > hp_ratio:
            delayed_width = int(self.bar_width * self.displayed_hp_ratio)
            delayed_rect = pygame.Rect(self.bar_x, self.bar_y, delayed_width, self.bar_height)
            pygame.draw.rect(screen, (150, 50, 50), delayed_rect, border_radius=3)

        # 当前血量
        hp_width = int(self.bar_width * hp_ratio)
        if hp_width > 0:
            hp_rect = pygame.Rect(self.bar_x, self.bar_y, hp_width, self.bar_height)
            # 根据血量比例改变颜色
            if hp_ratio > 0.5:
                hp_color = (200, 50, 50)
            elif hp_ratio > 0.25:
                hp_color = (200, 150, 50)
            else:
                hp_color = (200, 50, 50)
            pygame.draw.rect(screen, hp_color, hp_rect, border_radius=3)

            # 血条高光
            highlight_rect = pygame.Rect(self.bar_x, self.bar_y, hp_width, self.bar_height // 3)
            highlight_color = tuple(min(255, c + 50) for c in hp_color)
            pygame.draw.rect(screen, highlight_color, highlight_rect, border_radius=3)

        # 阶段分隔线
        phases = boss.max_phases
        if phases > 1:
            for i in range(1, phases):
                phase_x = self.bar_x + int(self.bar_width * (1 - i / phases))
                pygame.draw.line(screen, (255, 255, 255), (phase_x, self.bar_y), (phase_x, self.bar_y + self.bar_height), 2)

        # Boss名称（血条上方）
        name_text = self.fonts["medium"].render(boss.name, True, (255, 200, 100))
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, self.bar_y - 20))
        # 阴影
        shadow_text = self.fonts["medium"].render(boss.name, True, (30, 20, 0))
        screen.blit(shadow_text, (name_rect.x + 2, name_rect.y + 2))
        screen.blit(name_text, name_rect)

        # HP数值
        hp_text = self.fonts["tiny"].render(f"{boss.hp} / {boss.max_hp}", True, WHITE)
        hp_text_rect = hp_text.get_rect(center=(SCREEN_WIDTH // 2, self.bar_y + self.bar_height // 2))
        screen.blit(hp_text, hp_text_rect)

        # 无敌/阶段转换提示
        if boss.invincible:
            inv_text = self.fonts["tiny"].render("无敌", True, (100, 200, 255))
            inv_rect = inv_text.get_rect(midleft=(self.bar_x + self.bar_width + 15, self.bar_y + self.bar_height // 2))
            screen.blit(inv_text, inv_rect)

        # 狂暴提示
        if boss.is_enraged:
            rage_text = self.fonts["tiny"].render("狂暴!", True, (255, 100, 100))
            rage_rect = rage_text.get_rect(midright=(self.bar_x - 15, self.bar_y + self.bar_height // 2))
            # 闪烁效果
            if int(time.time() * 4) % 2 == 0:
                screen.blit(rage_text, rage_rect)

    def _draw_phase_indicator(self, screen):
        """绘制阶段指示器"""
        boss = self.current_boss
        phases = boss.max_phases
        current_phase = boss.phase

        # 在血条下方绘制阶段点
        indicator_y = self.bar_y + self.bar_height + 10
        indicator_spacing = 20
        total_width = (phases - 1) * indicator_spacing
        start_x = SCREEN_WIDTH // 2 - total_width // 2

        for i in range(1, phases + 1):
            x = start_x + (i - 1) * indicator_spacing

            if i <= current_phase:
                # 已经过的阶段
                color = (200, 50, 50)
                pygame.draw.circle(screen, color, (x, indicator_y), 6)
                pygame.draw.circle(screen, (255, 255, 255), (x, indicator_y), 6, 1)
            else:
                # 未到达的阶段
                color = (60, 60, 60)
                pygame.draw.circle(screen, color, (x, indicator_y), 5)
                pygame.draw.circle(screen, (100, 100, 100), (x, indicator_y), 5, 1)

        # 当前阶段文字
        phase_text = self.fonts["tiny"].render(f"阶段 {current_phase}/{phases}", True, (180, 180, 180))
        phase_rect = phase_text.get_rect(center=(SCREEN_WIDTH // 2, indicator_y + 20))
        screen.blit(phase_text, phase_rect)


class BossIntroAnimation:
    """Boss入场动画（可选的独立动画类）"""

    def __init__(self, boss_name, fonts):
        self.boss_name = boss_name
        self.fonts = fonts
        self.duration = 3.0
        self.timer = 0
        self.is_complete = False

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.duration:
            self.is_complete = True

    def draw(self, screen):
        if self.is_complete:
            return

        progress = self.timer / self.duration

        # 背景变暗
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        alpha = int(150 * (1 - abs(progress - 0.5) * 2))
        overlay.fill((0, 0, 0, alpha))
        screen.blit(overlay, (0, 0))

        # Boss名称从下方滑入
        if progress < 0.3:
            y_offset = int(100 * (1 - progress / 0.3))
        elif progress > 0.7:
            y_offset = int(-100 * (progress - 0.7) / 0.3)
        else:
            y_offset = 0

        name_text = self.fonts["title"].render(self.boss_name, True, (255, 200, 100))
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
        screen.blit(name_text, name_rect)

        # "警告"文字
        if 0.2 < progress < 0.8:
            warning_alpha = int(255 * math.sin((progress - 0.2) / 0.6 * math.pi))
            warning_surf = pygame.Surface((200, 50), pygame.SRCALPHA)
            warning_text = self.fonts["small"].render("! WARNING !", True, (255, 50, 50))
            warning_rect = warning_text.get_rect(center=(100, 25))
            warning_surf.blit(warning_text, warning_rect)
            warning_surf.set_alpha(warning_alpha)
            screen.blit(warning_surf, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 80))
