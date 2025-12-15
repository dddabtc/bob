"""
菜单界面
"""

import pygame
from settings import *


class Button:
    """按钮类"""
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.is_hovered = False
        self.is_clicked = False

    def update(self, mouse_pos, mouse_clicked):
        """更新按钮状态"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if self.is_hovered and mouse_clicked:
            self.is_clicked = True
            return True
        self.is_clicked = False
        return False

    def draw(self, screen):
        """绘制按钮"""
        # 选择颜色
        if self.is_clicked:
            color = BUTTON_CLICK
        elif self.is_hovered:
            color = BUTTON_HOVER
        else:
            color = BUTTON_NORMAL

        # 绘制按钮背景
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, GOLD, self.rect, 2, border_radius=8)

        # 绘制文字
        text_color = MENU_HIGHLIGHT if self.is_hovered else MENU_TEXT
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class MainMenu:
    """主菜单"""
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self.buttons = []
        self.has_continue = False  # 是否有存档可继续
        self._create_buttons()

        # 装饰元素
        self.title_glow = 0
        self.glow_direction = 1

    def _create_buttons(self):
        """创建菜单按钮"""
        button_width = 280
        button_height = 60
        start_y = 320
        gap = 70
        center_x = SCREEN_WIDTH // 2 - button_width // 2

        button_data = [
            ("开始新游戏", "start"),
            ("继续游戏", "continue"),
            ("读取存档", "load"),
            ("退出游戏", "quit")
        ]

        for i, (text, action) in enumerate(button_data):
            btn = Button(
                center_x, start_y + i * gap,
                button_width, button_height,
                text, self.fonts["medium"]
            )
            btn.action = action
            self.buttons.append(btn)

    def update(self, mouse_pos, mouse_clicked):
        """更新菜单状态，返回点击的按钮动作"""
        for btn in self.buttons:
            # 继续游戏按钮需要有存档才能点击
            if btn.action == "continue" and not self.has_continue:
                btn.is_hovered = False
                continue
            if btn.update(mouse_pos, mouse_clicked):
                return btn.action
        return None

    def draw(self):
        """绘制主菜单"""
        # 背景
        self.screen.fill(MENU_BG)

        # 绘制装饰背景
        self._draw_background()

        # 标题
        self._draw_title()

        # 副标题
        subtitle = self.fonts["small"].render(
            "— 实时动作RPG —", True, GRAY
        )
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 280))
        self.screen.blit(subtitle, subtitle_rect)

        # 绘制按钮
        for btn in self.buttons:
            # 继续游戏按钮没有存档时显示禁用状态
            if btn.action == "continue" and not self.has_continue:
                self._draw_disabled_button(btn)
            else:
                btn.draw(self.screen)

        # 底部提示
        hint = self.fonts["tiny"].render(
            "选择途径，踏上非凡之路", True, DARK_GRAY
        )
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(hint, hint_rect)

    def _draw_disabled_button(self, btn):
        """绘制禁用状态的按钮"""
        # 暗色背景
        pygame.draw.rect(self.screen, (40, 40, 50), btn.rect, border_radius=8)
        pygame.draw.rect(self.screen, (80, 80, 90), btn.rect, 2, border_radius=8)
        # 灰色文字
        text_surface = btn.font.render(btn.text, True, (80, 80, 80))
        text_rect = text_surface.get_rect(center=btn.rect.center)
        self.screen.blit(text_surface, text_rect)

    def _draw_background(self):
        """绘制装饰背景"""
        # 神秘符文圆环（简化版）
        center = (SCREEN_WIDTH // 2, 180)
        for i in range(3):
            radius = 100 + i * 30
            alpha = 30 - i * 8
            color = (*DARK_PURPLE[:3], alpha) if alpha > 0 else DARK_PURPLE
            pygame.draw.circle(self.screen, DARK_PURPLE, center, radius, 1)

    def _draw_title(self):
        """绘制带发光效果的标题"""
        # 更新发光
        self.title_glow += 2 * self.glow_direction
        if self.title_glow >= 30 or self.title_glow <= 0:
            self.glow_direction *= -1

        # 标题文字
        title_text = "诡秘之主"
        glow_color = (
            min(255, GOLD[0] + self.title_glow),
            min(255, GOLD[1] + self.title_glow),
            min(255, GOLD[2])
        )

        title = self.fonts["title"].render(title_text, True, glow_color)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 180))
        self.screen.blit(title, title_rect)

        # 英文副标题
        en_title = self.fonts["medium"].render(
            "Lord of Mysteries", True, DARK_GOLD
        )
        en_rect = en_title.get_rect(center=(SCREEN_WIDTH // 2, 240))
        self.screen.blit(en_title, en_rect)


class PauseMenu:
    """暂停菜单"""
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        """创建暂停菜单按钮"""
        button_width = 200
        button_height = 50
        start_y = 260
        gap = 60
        center_x = SCREEN_WIDTH // 2 - button_width // 2

        button_data = [
            ("继续游戏", "resume"),
            ("保存游戏", "save"),
            ("读取存档", "load"),
            ("返回主菜单", "main_menu"),
            ("退出游戏", "quit")
        ]

        for i, (text, action) in enumerate(button_data):
            btn = Button(
                center_x, start_y + i * gap,
                button_width, button_height,
                text, self.fonts["small"]
            )
            btn.action = action
            self.buttons.append(btn)

    def update(self, mouse_pos, mouse_clicked):
        """更新菜单状态"""
        for btn in self.buttons:
            if btn.update(mouse_pos, mouse_clicked):
                return btn.action
        return None

    def draw(self):
        """绘制暂停菜单"""
        # 半透明遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))

        # 暂停标题
        title = self.fonts["large"].render("游戏暂停", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)

        # 绘制按钮
        for btn in self.buttons:
            btn.draw(self.screen)
