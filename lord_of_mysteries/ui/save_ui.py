"""
存档界面UI
存档/读档/继续游戏界面
"""

import pygame
from settings import *


class SaveLoadUI:
    """存档/读档界面"""

    def __init__(self, screen, fonts, save_system):
        self.screen = screen
        self.fonts = fonts
        self.save_system = save_system
        self.visible = False
        self.mode = "save"  # "save" 或 "load"

        # 界面尺寸
        self.width = 600
        self.height = 500
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2

        # 存档槽位
        self.saves = []
        self.selected_index = 0
        self.scroll_offset = 0
        self.items_per_page = 6

        # 确认对话框
        self.confirm_dialog = False
        self.confirm_action = None
        self.confirm_slot = None

        # 回调
        self.on_load_callback = None
        self.on_save_callback = None

    def show(self, mode="save"):
        """显示界面"""
        self.visible = True
        self.mode = mode
        self.selected_index = 0
        self.scroll_offset = 0
        self.confirm_dialog = False
        self._refresh_saves()

    def hide(self):
        """隐藏界面"""
        self.visible = False
        self.confirm_dialog = False

    def _refresh_saves(self):
        """刷新存档列表"""
        self.saves = self.save_system.get_all_saves()

    def handle_event(self, event):
        """处理事件"""
        if not self.visible:
            return None

        if event.type == pygame.KEYDOWN:
            if self.confirm_dialog:
                return self._handle_confirm_event(event)

            if event.key == pygame.K_ESCAPE:
                self.hide()
                return "close"

            elif event.key == pygame.K_UP:
                self.selected_index = max(0, self.selected_index - 1)
                self._adjust_scroll()

            elif event.key == pygame.K_DOWN:
                self.selected_index = min(len(self.saves) - 1, self.selected_index + 1)
                self._adjust_scroll()

            elif event.key == pygame.K_RETURN:
                return self._handle_select()

            elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                return self._handle_delete()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.confirm_dialog:
                return self._handle_confirm_click(event.pos)
            else:
                return self._handle_click(event.pos)

        return None

    def _adjust_scroll(self):
        """调整滚动"""
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + self.items_per_page:
            self.scroll_offset = self.selected_index - self.items_per_page + 1

    def _handle_select(self):
        """处理选择"""
        if not self.saves or self.selected_index >= len(self.saves):
            return None

        save = self.saves[self.selected_index]
        slot = save.get("slot")

        if self.mode == "save":
            if not save.get("empty"):
                # 覆盖确认
                self.confirm_dialog = True
                self.confirm_action = "overwrite"
                self.confirm_slot = slot
            else:
                # 直接保存
                return ("save", slot)

        else:  # load
            if not save.get("empty"):
                return ("load", slot)

        return None

    def _handle_delete(self):
        """处理删除"""
        if not self.saves or self.selected_index >= len(self.saves):
            return None

        save = self.saves[self.selected_index]
        if not save.get("empty"):
            self.confirm_dialog = True
            self.confirm_action = "delete"
            self.confirm_slot = save.get("slot")

        return None

    def _handle_confirm_event(self, event):
        """处理确认对话框事件"""
        if event.key == pygame.K_RETURN or event.key == pygame.K_y:
            return self._confirm_action()
        elif event.key == pygame.K_ESCAPE or event.key == pygame.K_n:
            self.confirm_dialog = False
            return None
        return None

    def _handle_confirm_click(self, pos):
        """处理确认对话框点击"""
        mx, my = pos
        dialog_x = self.x + (self.width - 300) // 2
        dialog_y = self.y + (self.height - 150) // 2

        # 是按钮
        yes_rect = pygame.Rect(dialog_x + 40, dialog_y + 90, 80, 35)
        no_rect = pygame.Rect(dialog_x + 180, dialog_y + 90, 80, 35)

        if yes_rect.collidepoint(mx, my):
            return self._confirm_action()
        elif no_rect.collidepoint(mx, my):
            self.confirm_dialog = False

        return None

    def _confirm_action(self):
        """执行确认操作"""
        action = self.confirm_action
        slot = self.confirm_slot
        self.confirm_dialog = False

        if action == "overwrite":
            return ("save", slot)
        elif action == "delete":
            self.save_system.delete_save(slot)
            self._refresh_saves()
            return ("deleted", slot)

        return None

    def _handle_click(self, pos):
        """处理点击"""
        mx, my = pos

        # 检查存档项点击
        list_y = self.y + 80
        item_height = 65

        for i in range(self.items_per_page):
            save_index = self.scroll_offset + i
            if save_index >= len(self.saves):
                break

            item_rect = pygame.Rect(self.x + 20, list_y + i * item_height, self.width - 40, item_height - 5)
            if item_rect.collidepoint(mx, my):
                self.selected_index = save_index
                return self._handle_select()

        return None

    def draw(self):
        """绘制界面"""
        if not self.visible:
            return

        # 半透明背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        # 主面板
        panel = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        panel.fill((30, 30, 40, 240))
        pygame.draw.rect(panel, GOLD, (0, 0, self.width, self.height), 2, border_radius=10)

        # 标题
        title_text = "保存游戏" if self.mode == "save" else "读取存档"
        title = self.fonts["large"].render(title_text, True, GOLD)
        title_rect = title.get_rect(center=(self.width // 2, 35))
        panel.blit(title, title_rect)

        # 分割线
        pygame.draw.line(panel, (80, 80, 100), (20, 65), (self.width - 20, 65), 2)

        # 存档列表
        self._draw_save_list(panel)

        # 底部提示
        hints = "↑↓选择  Enter确认  Delete删除  ESC返回"
        hint = self.fonts["tiny"].render(hints, True, (150, 150, 150))
        panel.blit(hint, (20, self.height - 30))

        self.screen.blit(panel, (self.x, self.y))

        # 确认对话框
        if self.confirm_dialog:
            self._draw_confirm_dialog()

    def _draw_save_list(self, surface):
        """绘制存档列表"""
        list_y = 80
        item_height = 65

        if not self.saves:
            empty_text = self.fonts["small"].render("没有存档", True, (100, 100, 100))
            surface.blit(empty_text, (self.width // 2 - 40, 200))
            return

        for i in range(self.items_per_page):
            save_index = self.scroll_offset + i
            if save_index >= len(self.saves):
                break

            save = self.saves[save_index]
            item_y = list_y + i * item_height
            is_selected = save_index == self.selected_index

            # 背景
            if is_selected:
                bg_color = (60, 60, 80)
            else:
                bg_color = (35, 35, 45)

            pygame.draw.rect(surface, bg_color, (20, item_y, self.width - 40, item_height - 5), border_radius=5)

            # 边框
            border_color = GOLD if is_selected else (60, 60, 70)
            pygame.draw.rect(surface, border_color, (20, item_y, self.width - 40, item_height - 5), 1, border_radius=5)

            # 槽位标识
            slot = save.get("slot")
            if save.get("is_auto"):
                slot_text = "[自动]"
                slot_color = (100, 200, 255)
            else:
                slot_text = f"[槽位 {slot}]"
                slot_color = (200, 200, 200)

            slot_label = self.fonts["small"].render(slot_text, True, slot_color)
            surface.blit(slot_label, (30, item_y + 8))

            if save.get("empty"):
                # 空槽位
                empty_text = self.fonts["small"].render("- 空 -", True, (100, 100, 100))
                surface.blit(empty_text, (120, item_y + 20))
            else:
                # 存档信息
                # 途径和序列
                pathway = save.get("pathway", "未知")
                sequence = save.get("sequence", 9)
                info_text = f"{pathway} 序列{sequence}"
                info = self.fonts["small"].render(info_text, True, WHITE)
                surface.blit(info, (120, item_y + 5))

                # 波次和时间
                wave = save.get("wave", 1)
                playtime_sec = int(save.get("playtime", 0))
                playtime_min = playtime_sec // 60
                playtime_str = f"波次 {wave} | 游玩 {playtime_min}分钟"
                detail = self.fonts["tiny"].render(playtime_str, True, (150, 150, 150))
                surface.blit(detail, (120, item_y + 28))

                # 存档日期
                datetime_str = save.get("datetime", "未知")
                date = self.fonts["tiny"].render(datetime_str, True, (120, 120, 120))
                surface.blit(date, (self.width - 180, item_y + 20))

        # 滚动指示
        if len(self.saves) > self.items_per_page:
            if self.scroll_offset > 0:
                up_text = self.fonts["small"].render("▲", True, (150, 150, 150))
                surface.blit(up_text, (self.width // 2, list_y - 15))
            if self.scroll_offset + self.items_per_page < len(self.saves):
                down_y = list_y + self.items_per_page * item_height
                down_text = self.fonts["small"].render("▼", True, (150, 150, 150))
                surface.blit(down_text, (self.width // 2, down_y))

    def _draw_confirm_dialog(self):
        """绘制确认对话框"""
        dialog_width = 300
        dialog_height = 150
        dialog_x = self.x + (self.width - dialog_width) // 2
        dialog_y = self.y + (self.height - dialog_height) // 2

        # 背景
        dialog_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
        dialog_surface.fill((40, 40, 50, 250))
        pygame.draw.rect(dialog_surface, (255, 200, 100), (0, 0, dialog_width, dialog_height), 2, border_radius=8)

        # 文字
        if self.confirm_action == "overwrite":
            text = "确认覆盖此存档？"
        elif self.confirm_action == "delete":
            text = "确认删除此存档？"
        else:
            text = "确认？"

        confirm_text = self.fonts["medium"].render(text, True, WHITE)
        text_rect = confirm_text.get_rect(center=(dialog_width // 2, 40))
        dialog_surface.blit(confirm_text, text_rect)

        # 按钮
        # 是
        yes_rect = pygame.Rect(40, 90, 80, 35)
        pygame.draw.rect(dialog_surface, (60, 100, 60), yes_rect, border_radius=5)
        pygame.draw.rect(dialog_surface, (100, 200, 100), yes_rect, 2, border_radius=5)
        yes_text = self.fonts["small"].render("是 (Y)", True, WHITE)
        yes_text_rect = yes_text.get_rect(center=yes_rect.center)
        dialog_surface.blit(yes_text, yes_text_rect)

        # 否
        no_rect = pygame.Rect(180, 90, 80, 35)
        pygame.draw.rect(dialog_surface, (100, 60, 60), no_rect, border_radius=5)
        pygame.draw.rect(dialog_surface, (200, 100, 100), no_rect, 2, border_radius=5)
        no_text = self.fonts["small"].render("否 (N)", True, WHITE)
        no_text_rect = no_text.get_rect(center=no_rect.center)
        dialog_surface.blit(no_text, no_text_rect)

        self.screen.blit(dialog_surface, (dialog_x, dialog_y))


class ContinueButton:
    """继续游戏按钮（用于主菜单）"""

    def __init__(self, save_system):
        self.save_system = save_system

    def is_available(self):
        """检查是否有可继续的存档"""
        return self.save_system.has_any_save()

    def get_latest_save_info(self):
        """获取最新存档信息"""
        return self.save_system.get_latest_save()

    def get_continue_slot(self):
        """获取继续游戏的存档槽位"""
        latest = self.save_system.get_latest_save()
        if latest:
            return latest.get("slot")
        return None
