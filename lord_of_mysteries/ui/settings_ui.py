"""
设置界面UI
"""

import pygame
from settings import *
from systems.language import t, get_lang


class SettingsUI:
    """设置界面"""

    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self.visible = False

        # 界面尺寸
        self.width = 500
        self.height = 400
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2

        # 设置选项
        self.options = [
            {"key": "language", "type": "toggle"},
            {"key": "sound", "type": "toggle", "value": True},
            {"key": "music", "type": "toggle", "value": True},
            {"key": "fullscreen", "type": "toggle", "value": False},
        ]

        self.selected_index = 0
        self.hover_index = -1

        # 按钮
        self.back_button = pygame.Rect(
            self.x + 50, self.y + self.height - 60,
            180, 45
        )
        self.apply_button = pygame.Rect(
            self.x + self.width - 230, self.y + self.height - 60,
            180, 45
        )

        self.hover_back = False
        self.hover_apply = False

        # 语言系统
        self.lang_system = get_lang()

    def show(self):
        """显示设置界面"""
        self.visible = True
        self.selected_index = 0

    def hide(self):
        """隐藏设置界面"""
        self.visible = False

    def toggle(self):
        """切换显示/隐藏"""
        if self.visible:
            self.hide()
        else:
            self.show()

    def handle_event(self, event):
        """处理事件"""
        if not self.visible:
            return None

        mouse_pos = pygame.mouse.get_pos()

        # 更新悬停状态
        self._update_hover(mouse_pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.hide()
                return "close"
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_LEFT, pygame.K_RIGHT):
                self._toggle_option(self.selected_index)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # 检查选项点击
                if self.hover_index >= 0:
                    self._toggle_option(self.hover_index)

                # 检查按钮点击
                if self.back_button.collidepoint(mouse_pos):
                    self.hide()
                    return "close"
                elif self.apply_button.collidepoint(mouse_pos):
                    self._apply_settings()
                    return "apply"

        return None

    def _update_hover(self, mouse_pos):
        """更新悬停状态"""
        self.hover_index = -1
        option_y = self.y + 80

        for i, option in enumerate(self.options):
            option_rect = pygame.Rect(self.x + 40, option_y + i * 60, self.width - 80, 50)
            if option_rect.collidepoint(mouse_pos):
                self.hover_index = i
                break

        self.hover_back = self.back_button.collidepoint(mouse_pos)
        self.hover_apply = self.apply_button.collidepoint(mouse_pos)

    def _toggle_option(self, index):
        """切换选项值"""
        if index < 0 or index >= len(self.options):
            return

        option = self.options[index]

        if option["key"] == "language":
            # 切换语言
            self.lang_system.next_language()
        elif option["type"] == "toggle":
            option["value"] = not option.get("value", False)

    def _apply_settings(self):
        """应用设置"""
        # 这里可以添加应用其他设置的逻辑
        # 语言设置已经在切换时自动保存
        pass

    def draw(self):
        """绘制设置界面"""
        if not self.visible:
            return

        # 半透明背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # 主面板
        panel = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        panel.fill((30, 30, 45, 240))
        pygame.draw.rect(panel, GOLD, (0, 0, self.width, self.height), 3, border_radius=15)
        self.screen.blit(panel, (self.x, self.y))

        # 标题
        title = self.fonts["large"].render(t("settings_title"), True, GOLD)
        title_rect = title.get_rect(centerx=self.x + self.width // 2, top=self.y + 20)
        self.screen.blit(title, title_rect)

        # 绘制选项
        option_y = self.y + 80

        for i, option in enumerate(self.options):
            is_selected = i == self.selected_index
            is_hover = i == self.hover_index

            # 选项背景
            option_rect = pygame.Rect(self.x + 40, option_y + i * 60, self.width - 80, 50)

            if is_selected or is_hover:
                bg_color = (60, 60, 80, 200)
            else:
                bg_color = (40, 40, 55, 150)

            option_surface = pygame.Surface((option_rect.width, option_rect.height), pygame.SRCALPHA)
            option_surface.fill(bg_color)
            pygame.draw.rect(option_surface, GOLD if is_selected else (100, 100, 120),
                           (0, 0, option_rect.width, option_rect.height), 2, border_radius=8)
            self.screen.blit(option_surface, option_rect.topleft)

            # 选项名称
            label_key = f"settings_{option['key']}"
            label = self.fonts["medium"].render(t(label_key), True, WHITE)
            self.screen.blit(label, (option_rect.x + 20, option_rect.y + 12))

            # 选项值
            if option["key"] == "language":
                value_text = self.lang_system.get_language_name()
                value_color = (100, 200, 255)
            else:
                value = option.get("value", False)
                value_text = t("settings_on") if value else t("settings_off")
                value_color = (100, 255, 100) if value else (255, 100, 100)

            value_surface = self.fonts["medium"].render(value_text, True, value_color)
            value_rect = value_surface.get_rect(right=option_rect.right - 20, centery=option_rect.centery)
            self.screen.blit(value_surface, value_rect)

            # 左右箭头提示
            arrow_color = GOLD if (is_selected or is_hover) else GRAY
            left_arrow = self.fonts["medium"].render("<", True, arrow_color)
            right_arrow = self.fonts["medium"].render(">", True, arrow_color)
            self.screen.blit(left_arrow, (value_rect.left - 25, option_rect.y + 10))
            self.screen.blit(right_arrow, (value_rect.right + 5, option_rect.y + 10))

        # 绘制按钮
        self._draw_button(self.back_button, t("settings_back"), self.hover_back)
        self._draw_button(self.apply_button, t("settings_apply"), self.hover_apply)

        # 操作提示
        hint = self.fonts["tiny"].render("↑↓: 选择  ←→/Enter: 切换  ESC: 返回", True, GRAY)
        hint_rect = hint.get_rect(centerx=self.x + self.width // 2, bottom=self.y + self.height - 10)
        self.screen.blit(hint, hint_rect)

    def _draw_button(self, rect, text, is_hover):
        """绘制按钮"""
        if is_hover:
            color = BUTTON_HOVER
            border_color = GOLD
        else:
            color = BUTTON_NORMAL
            border_color = (100, 100, 120)

        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=8)

        text_surface = self.fonts["small"].render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
