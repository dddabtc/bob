"""
背包和炮制界面UI
"""

import pygame
from settings import *
from data.items import QUALITY_COLORS


class InventoryUI:
    """背包界面"""

    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self.is_open = False

        # UI布局
        self.panel_rect = pygame.Rect(100, 50, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100)

        # 标签页
        self.current_tab = "materials"  # materials, consumables, craft
        self.tabs = [
            ("materials", "材料"),
            ("consumables", "消耗品"),
            ("craft", "炮制"),
        ]
        self.tab_rects = []

        # 滚动
        self.scroll_offset = 0
        self.max_scroll = 0
        self.items_per_page = 8

        # 选中项
        self.selected_index = 0

        # 炮制确认
        self.craft_confirm = False

    def toggle(self):
        """切换背包开关"""
        self.is_open = not self.is_open
        if self.is_open:
            self.scroll_offset = 0
            self.selected_index = 0
            self.craft_confirm = False

    def handle_event(self, event, inventory, player, potion_system):
        """处理输入事件"""
        if not self.is_open:
            return None

        if event.type == pygame.KEYDOWN:
            # 关闭背包
            if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                self.is_open = False
                return "close"

            # 切换标签
            if event.key == pygame.K_LEFT:
                idx = [t[0] for t in self.tabs].index(self.current_tab)
                idx = (idx - 1) % len(self.tabs)
                self.current_tab = self.tabs[idx][0]
                self.scroll_offset = 0
                self.selected_index = 0
                self.craft_confirm = False

            if event.key == pygame.K_RIGHT:
                idx = [t[0] for t in self.tabs].index(self.current_tab)
                idx = (idx + 1) % len(self.tabs)
                self.current_tab = self.tabs[idx][0]
                self.scroll_offset = 0
                self.selected_index = 0
                self.craft_confirm = False

            # 滚动/选择
            if event.key == pygame.K_UP:
                self.selected_index = max(0, self.selected_index - 1)
                self._adjust_scroll()

            if event.key == pygame.K_DOWN:
                self.selected_index += 1
                self._adjust_scroll()

            # 使用/炮制
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self._handle_action(inventory, player, potion_system)

            # 取消确认
            if event.key == pygame.K_n and self.craft_confirm:
                self.craft_confirm = False

        return None

    def _adjust_scroll(self):
        """调整滚动位置"""
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + self.items_per_page:
            self.scroll_offset = self.selected_index - self.items_per_page + 1

    def _handle_action(self, inventory, player, potion_system):
        """处理确认操作"""
        if self.current_tab == "consumables":
            # 使用消耗品
            consumables = inventory.get_all_consumables()
            if consumables and 0 <= self.selected_index < len(consumables):
                item = consumables[self.selected_index]
                success, msg = inventory.use_consumable(item["name"], player)
                return ("use", success, msg)

        elif self.current_tab == "craft":
            # 炮制魔药
            if self.craft_confirm:
                success, msg = potion_system.craft_potion(player, inventory)
                self.craft_confirm = False
                return ("craft", success, msg)
            else:
                # 检查是否可以炮制
                can_make, msg, recipe = potion_system.check_can_craft(player, inventory)
                if can_make:
                    self.craft_confirm = True
                else:
                    return ("craft", False, msg)

        return None

    def draw(self, inventory, player, potion_system):
        """绘制背包界面"""
        if not self.is_open:
            return

        # 半透明背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        # 主面板
        pygame.draw.rect(self.screen, (30, 30, 50), self.panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, GOLD, self.panel_rect, 2, border_radius=10)

        # 标题
        title = self.fonts["large"].render("背包", True, GOLD)
        self.screen.blit(title, (self.panel_rect.centerx - title.get_width() // 2, self.panel_rect.top + 15))

        # 金币显示
        gold_text = self.fonts["small"].render(f"金币: {inventory.gold}", True, GOLD)
        self.screen.blit(gold_text, (self.panel_rect.right - 150, self.panel_rect.top + 20))

        # 绘制标签页
        self._draw_tabs()

        # 绘制内容
        content_rect = pygame.Rect(
            self.panel_rect.left + 20,
            self.panel_rect.top + 80,
            self.panel_rect.width - 40,
            self.panel_rect.height - 130
        )

        if self.current_tab == "materials":
            self._draw_materials(content_rect, inventory)
        elif self.current_tab == "consumables":
            self._draw_consumables(content_rect, inventory)
        elif self.current_tab == "craft":
            self._draw_craft(content_rect, inventory, player, potion_system)

        # 绘制操作提示
        self._draw_hints()

    def _draw_tabs(self):
        """绘制标签页"""
        self.tab_rects = []
        tab_width = 120
        tab_height = 35
        start_x = self.panel_rect.left + 30
        start_y = self.panel_rect.top + 50

        for i, (tab_id, tab_name) in enumerate(self.tabs):
            rect = pygame.Rect(start_x + i * (tab_width + 10), start_y, tab_width, tab_height)
            self.tab_rects.append(rect)

            # 背景
            if tab_id == self.current_tab:
                pygame.draw.rect(self.screen, (60, 60, 100), rect, border_radius=5)
                pygame.draw.rect(self.screen, GOLD, rect, 2, border_radius=5)
            else:
                pygame.draw.rect(self.screen, (40, 40, 60), rect, border_radius=5)
                pygame.draw.rect(self.screen, GRAY, rect, 1, border_radius=5)

            # 文字
            color = WHITE if tab_id == self.current_tab else GRAY
            text = self.fonts["small"].render(tab_name, True, color)
            self.screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

    def _draw_materials(self, rect, inventory):
        """绘制材料列表"""
        materials = inventory.get_all_materials()

        if not materials:
            empty_text = self.fonts["small"].render("暂无材料", True, GRAY)
            self.screen.blit(empty_text, (rect.centerx - empty_text.get_width() // 2, rect.centery))
            return

        # 限制选中索引
        self.selected_index = min(self.selected_index, len(materials) - 1)

        # 绘制列表
        y = rect.top
        item_height = 50

        for i, item in enumerate(materials[self.scroll_offset:self.scroll_offset + self.items_per_page]):
            idx = i + self.scroll_offset
            item_rect = pygame.Rect(rect.left, y, rect.width, item_height - 5)

            # 选中高亮
            if idx == self.selected_index:
                pygame.draw.rect(self.screen, (50, 50, 80), item_rect, border_radius=5)
                pygame.draw.rect(self.screen, GOLD, item_rect, 1, border_radius=5)
            else:
                pygame.draw.rect(self.screen, (35, 35, 55), item_rect, border_radius=5)

            # 品质颜色
            quality_color = QUALITY_COLORS.get(item["quality"], WHITE)

            # 名称和数量
            name_text = self.fonts["small"].render(f"{item['name']} x{item['count']}", True, quality_color)
            self.screen.blit(name_text, (rect.left + 15, y + 5))

            # 描述
            desc_text = self.fonts["tiny"].render(item["desc"][:30], True, GRAY)
            self.screen.blit(desc_text, (rect.left + 15, y + 28))

            y += item_height

    def _draw_consumables(self, rect, inventory):
        """绘制消耗品列表"""
        consumables = inventory.get_all_consumables()

        if not consumables:
            empty_text = self.fonts["small"].render("暂无消耗品", True, GRAY)
            self.screen.blit(empty_text, (rect.centerx - empty_text.get_width() // 2, rect.centery))
            return

        # 限制选中索引
        self.selected_index = min(self.selected_index, len(consumables) - 1)

        # 绘制列表
        y = rect.top
        item_height = 50

        for i, item in enumerate(consumables[self.scroll_offset:self.scroll_offset + self.items_per_page]):
            idx = i + self.scroll_offset
            item_rect = pygame.Rect(rect.left, y, rect.width, item_height - 5)

            # 选中高亮
            if idx == self.selected_index:
                pygame.draw.rect(self.screen, (50, 50, 80), item_rect, border_radius=5)
                pygame.draw.rect(self.screen, GOLD, item_rect, 1, border_radius=5)
            else:
                pygame.draw.rect(self.screen, (35, 35, 55), item_rect, border_radius=5)

            # 品质颜色
            quality_color = QUALITY_COLORS.get(item["quality"], WHITE)

            # 名称和数量
            name_text = self.fonts["small"].render(f"{item['name']} x{item['count']}", True, quality_color)
            self.screen.blit(name_text, (rect.left + 15, y + 5))

            # 描述
            desc_text = self.fonts["tiny"].render(item["desc"], True, GRAY)
            self.screen.blit(desc_text, (rect.left + 15, y + 28))

            y += item_height

    def _draw_craft(self, rect, inventory, player, potion_system):
        """绘制炮制界面"""
        # 获取配方状态
        status = potion_system.get_recipe_status(player, inventory)

        # 当前进度
        progress = potion_system.get_pathway_progress(player)
        progress_text = self.fonts["small"].render(
            f"当前: 序列{progress['current_sequence']} {progress['current_name']}",
            True, player.color
        )
        self.screen.blit(progress_text, (rect.left, rect.top))

        if not progress["can_advance"]:
            # 已达最高可炼制序列
            info_text = self.fonts["medium"].render("已达序列7，更高序列需完成最终任务", True, GOLD)
            self.screen.blit(info_text, (rect.centerx - info_text.get_width() // 2, rect.centery - 50))
            return

        # 下一序列信息
        next_seq = progress["next_sequence"]
        next_text = self.fonts["small"].render(f"下一序列: 序列{next_seq}", True, WHITE)
        self.screen.blit(next_text, (rect.left, rect.top + 35))

        if not status["recipe"]:
            error_text = self.fonts["small"].render(status["reason"], True, CRIMSON)
            self.screen.blit(error_text, (rect.left, rect.top + 70))
            return

        # 魔药名称
        recipe = status["recipe"]
        potion_text = self.fonts["medium"].render(recipe["name"], True, GOLD)
        self.screen.blit(potion_text, (rect.left, rect.top + 70))

        # 描述
        desc_text = self.fonts["tiny"].render(recipe["desc"], True, GRAY)
        self.screen.blit(desc_text, (rect.left, rect.top + 100))

        # 材料列表
        materials_title = self.fonts["small"].render("所需材料:", True, WHITE)
        self.screen.blit(materials_title, (rect.left, rect.top + 140))

        y = rect.top + 170
        for mat in status["materials_status"]:
            color = (100, 255, 100) if mat["enough"] else CRIMSON
            mat_text = self.fonts["small"].render(
                f"  {mat['name']}: {mat['have']}/{mat['required']}",
                True, color
            )
            self.screen.blit(mat_text, (rect.left, y))
            y += 30

        # 炮制按钮/状态
        y += 20
        if status["available"]:
            if self.craft_confirm:
                # 确认提示
                confirm_text = self.fonts["medium"].render("确认炮制？ [回车]确认 [N]取消", True, GOLD)
                self.screen.blit(confirm_text, (rect.left, y))
            else:
                hint_text = self.fonts["medium"].render("按 [回车] 炮制魔药", True, (100, 255, 100))
                self.screen.blit(hint_text, (rect.left, y))
        else:
            hint_text = self.fonts["small"].render("材料不足，无法炮制", True, CRIMSON)
            self.screen.blit(hint_text, (rect.left, y))

    def _draw_hints(self):
        """绘制操作提示"""
        hints = [
            "← → 切换标签",
            "↑ ↓ 选择物品",
            "回车 使用/炮制",
            "I/ESC 关闭"
        ]

        y = self.panel_rect.bottom - 40
        x = self.panel_rect.left + 30
        for hint in hints:
            text = self.fonts["tiny"].render(hint, True, GRAY)
            self.screen.blit(text, (x, y))
            x += 180


class DropNotification:
    """掉落物通知"""

    def __init__(self):
        self.notifications = []

    def add(self, text, color=WHITE):
        """添加通知"""
        self.notifications.append({
            "text": text,
            "color": color,
            "lifetime": 2.0,
            "alpha": 255,
        })

    def update(self, dt):
        """更新通知"""
        for notif in self.notifications[:]:
            notif["lifetime"] -= dt
            if notif["lifetime"] < 0.5:
                notif["alpha"] = int(255 * (notif["lifetime"] / 0.5))
            if notif["lifetime"] <= 0:
                self.notifications.remove(notif)

    def draw(self, screen, fonts):
        """绘制通知"""
        y = 100
        for notif in self.notifications[-5:]:  # 最多显示5条
            text = fonts["small"].render(notif["text"], True, notif["color"])
            text_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
            text_surface.blit(text, (0, 0))
            text_surface.set_alpha(notif["alpha"])

            x = SCREEN_WIDTH - text.get_width() - 30
            screen.blit(text_surface, (x, y))
            y += 30


class CraftResultUI:
    """炮制结果显示"""

    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self.active = False
        self.message = ""
        self.success = False
        self.lifetime = 0

    def show(self, message, success=True, duration=3.0):
        """显示结果"""
        self.active = True
        self.message = message
        self.success = success
        self.lifetime = duration

    def update(self, dt):
        """更新"""
        if self.active:
            self.lifetime -= dt
            if self.lifetime <= 0:
                self.active = False

    def draw(self):
        """绘制"""
        if not self.active:
            return

        # 计算透明度
        alpha = int(255 * min(1, self.lifetime))

        # 背景
        panel_width = 500
        panel_height = 100
        panel_rect = pygame.Rect(
            (SCREEN_WIDTH - panel_width) // 2,
            (SCREEN_HEIGHT - panel_height) // 2,
            panel_width,
            panel_height
        )

        # 创建带透明度的surface
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        bg_color = (50, 100, 50, alpha) if self.success else (100, 50, 50, alpha)
        pygame.draw.rect(panel_surface, bg_color, (0, 0, panel_width, panel_height), border_radius=10)

        border_color = (100, 255, 100, alpha) if self.success else (255, 100, 100, alpha)
        pygame.draw.rect(panel_surface, border_color, (0, 0, panel_width, panel_height), 3, border_radius=10)

        self.screen.blit(panel_surface, panel_rect)

        # 文字
        text_color = (100, 255, 100) if self.success else (255, 100, 100)
        text = self.fonts["medium"].render(self.message, True, text_color)
        text_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
        text_surface.blit(text, (0, 0))
        text_surface.set_alpha(alpha)

        text_rect = text_surface.get_rect(center=panel_rect.center)
        self.screen.blit(text_surface, text_rect)
