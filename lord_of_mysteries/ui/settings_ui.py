"""
设置界面UI
"""

import pygame
import json
import os
from settings import *
from systems.language import t, get_lang
from systems.audio import get_audio


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

        # 系统引用
        self.lang_system = get_lang()
        self.audio_system = get_audio()

        # 配置文件路径
        self.config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "saves",
            "settings.json"
        )

        # 加载设置
        self._load_settings()

        # 设置选项
        self.options = [
            {"key": "language", "type": "language"},
            {"key": "sound", "type": "toggle"},
            {"key": "music", "type": "toggle"},
            {"key": "fullscreen", "type": "toggle"},
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

        # 全屏状态（需要Game类回调）
        self.fullscreen = False
        self.fullscreen_callback = None

    def _load_settings(self):
        """加载设置"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.fullscreen = settings.get("fullscreen", False)
        except (json.JSONDecodeError, IOError):
            self.fullscreen = False

    def _save_settings(self):
        """保存设置"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

            settings = {}
            if os.path.exists(self.config_path):
                try:
                    with open(self.config_path, 'r', encoding='utf-8') as f:
                        settings = json.load(f)
                except (json.JSONDecodeError, IOError):
                    pass

            settings["fullscreen"] = self.fullscreen

            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def set_fullscreen_callback(self, callback):
        """设置全屏切换回调函数"""
        self.fullscreen_callback = callback

    def show(self):
        """显示设置界面"""
        self.visible = True
        self.selected_index = 0
        self._load_settings()

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

        elif option["key"] == "sound":
            # 切换音效
            self.audio_system.toggle_sound()

        elif option["key"] == "music":
            # 切换音乐
            self.audio_system.toggle_music()

        elif option["key"] == "fullscreen":
            # 切换全屏
            self.fullscreen = not self.fullscreen
            self._save_settings()
            if self.fullscreen_callback:
                self.fullscreen_callback(self.fullscreen)

    def _apply_settings(self):
        """应用设置"""
        self._save_settings()

    def _get_option_value(self, key):
        """获取选项当前值"""
        if key == "language":
            return self.lang_system.get_language_name()
        elif key == "sound":
            return self.audio_system.is_sound_enabled()
        elif key == "music":
            return self.audio_system.is_music_enabled()
        elif key == "fullscreen":
            return self.fullscreen
        return False

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
            value = self._get_option_value(option["key"])

            if option["key"] == "language":
                value_text = value  # 已经是语言名称
                value_color = (100, 200, 255)
            else:
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
        hint = self.fonts["tiny"].render("↑↓: " + t("controls_move").split(":")[0] + "  ←→/Enter: " + t("settings_apply") + "  ESC: " + t("settings_back"), True, GRAY)
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
