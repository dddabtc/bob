"""
对话系统UI
"""

import pygame
from settings import *


class DialogueBox:
    """对话框"""

    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts

        # 状态
        self.active = False
        self.dialogues = []
        self.current_index = 0

        # 文字动画
        self.displayed_chars = 0
        self.char_speed = 30  # 每秒显示字符数
        self.text_complete = False

        # 回调
        self.on_complete = None

        # UI布局
        self.box_height = 180
        self.box_rect = pygame.Rect(
            50, SCREEN_HEIGHT - self.box_height - 30,
            SCREEN_WIDTH - 100, self.box_height
        )

        # 说话者颜色
        self.speaker_colors = {
            "旁白": GRAY,
            "???": CRIMSON,
            "神秘商人": (200, 150, 100),
            "线人": (150, 200, 150),
            "市民": (180, 180, 180),
            "守墓人": (100, 100, 150),
            "医生": (150, 200, 255),
            "竞技场主持人": GOLD,
            "极光会主教": (200, 50, 50),
            "神秘声音": (150, 50, 200),
        }

    def start(self, dialogues, on_complete=None):
        """开始对话"""
        self.dialogues = dialogues
        self.current_index = 0
        self.displayed_chars = 0
        self.text_complete = False
        self.active = True
        self.on_complete = on_complete

    def handle_event(self, event):
        """处理输入"""
        if not self.active:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_j]:
                if not self.text_complete:
                    # 立即显示完整文字
                    current_dialogue = self.dialogues[self.current_index]
                    self.displayed_chars = len(current_dialogue.get("text", ""))
                    self.text_complete = True
                else:
                    # 下一句
                    self.current_index += 1
                    if self.current_index >= len(self.dialogues):
                        self._finish()
                    else:
                        self.displayed_chars = 0
                        self.text_complete = False
                return True

            if event.key == pygame.K_ESCAPE:
                # 跳过对话
                self._finish()
                return True

        return False

    def _finish(self):
        """结束对话"""
        self.active = False
        if self.on_complete:
            self.on_complete()

    def update(self, dt):
        """更新动画"""
        if not self.active or self.text_complete:
            return

        current_dialogue = self.dialogues[self.current_index]
        full_text = current_dialogue.get("text", "")

        self.displayed_chars += self.char_speed * dt

        if self.displayed_chars >= len(full_text):
            self.displayed_chars = len(full_text)
            self.text_complete = True

    def draw(self):
        """绘制对话框"""
        if not self.active or not self.dialogues:
            return

        current_dialogue = self.dialogues[self.current_index]
        speaker = current_dialogue.get("speaker", "")
        full_text = current_dialogue.get("text", "")

        # 显示的文字
        displayed_text = full_text[:int(self.displayed_chars)]

        # 半透明背景覆盖
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        self.screen.blit(overlay, (0, 0))

        # 对话框背景
        box_surface = pygame.Surface((self.box_rect.width, self.box_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(box_surface, (20, 20, 40, 230), (0, 0, self.box_rect.width, self.box_rect.height), border_radius=10)
        self.screen.blit(box_surface, self.box_rect)

        # 边框
        pygame.draw.rect(self.screen, GOLD, self.box_rect, 2, border_radius=10)

        # 说话者名称
        if speaker:
            speaker_color = self.speaker_colors.get(speaker, WHITE)

            # 名称背景
            name_surface = self.fonts["medium"].render(speaker, True, speaker_color)
            name_bg_rect = pygame.Rect(
                self.box_rect.left + 20,
                self.box_rect.top - 20,
                name_surface.get_width() + 30,
                40
            )
            pygame.draw.rect(self.screen, (30, 30, 50), name_bg_rect, border_radius=5)
            pygame.draw.rect(self.screen, speaker_color, name_bg_rect, 2, border_radius=5)

            self.screen.blit(name_surface, (name_bg_rect.left + 15, name_bg_rect.centery - name_surface.get_height() // 2))

        # 对话内容
        text_x = self.box_rect.left + 30
        text_y = self.box_rect.top + 40

        # 自动换行
        words = displayed_text
        line = ""
        lines = []
        max_width = self.box_rect.width - 60

        for char in words:
            test_line = line + char
            test_surface = self.fonts["medium"].render(test_line, True, WHITE)
            if test_surface.get_width() <= max_width:
                line = test_line
            else:
                if line:
                    lines.append(line)
                line = char

        if line:
            lines.append(line)

        for i, line_text in enumerate(lines[:4]):  # 最多4行
            text_surface = self.fonts["medium"].render(line_text, True, WHITE)
            self.screen.blit(text_surface, (text_x, text_y + i * 32))

        # 提示
        if self.text_complete:
            hint_text = self.fonts["tiny"].render("按 空格/回车 继续    ESC 跳过", True, GRAY)
        else:
            hint_text = self.fonts["tiny"].render("按 空格/回车 加速", True, GRAY)

        self.screen.blit(hint_text, (self.box_rect.right - hint_text.get_width() - 20, self.box_rect.bottom - 30))

        # 进度指示
        progress_text = self.fonts["tiny"].render(
            f"{self.current_index + 1}/{len(self.dialogues)}",
            True, GRAY
        )
        self.screen.blit(progress_text, (self.box_rect.left + 20, self.box_rect.bottom - 30))

    def is_active(self):
        """是否正在显示对话"""
        return self.active
