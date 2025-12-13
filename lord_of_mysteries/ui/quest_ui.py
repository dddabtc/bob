"""
任务界面UI
"""

import pygame
from settings import *
from data.quests import (
    get_quest_data, QUEST_TYPE_MAIN, QUEST_TYPE_SIDE, QUEST_TYPE_DAILY,
    QUEST_STATUS_AVAILABLE, QUEST_STATUS_ACTIVE, QUEST_STATUS_COMPLETE, QUEST_STATUS_FINISHED
)


class QuestUI:
    """任务界面"""

    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self.is_open = False

        # UI布局
        self.panel_rect = pygame.Rect(100, 50, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100)

        # 标签页
        self.current_tab = "active"  # active, available, completed
        self.tabs = [
            ("active", "进行中"),
            ("available", "可接取"),
            ("completed", "已完成"),
        ]

        # 选中项
        self.selected_index = 0
        self.scroll_offset = 0
        self.items_per_page = 6

        # 详情面板
        self.show_detail = False
        self.detail_quest_id = None

    def toggle(self):
        """切换开关"""
        self.is_open = not self.is_open
        if self.is_open:
            self.scroll_offset = 0
            self.selected_index = 0
            self.show_detail = False

    def handle_event(self, event, quest_system, inventory, player):
        """处理输入事件"""
        if not self.is_open:
            return None

        if event.type == pygame.KEYDOWN:
            # 关闭
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                if self.show_detail:
                    self.show_detail = False
                else:
                    self.is_open = False
                return "close"

            # 切换标签
            if event.key == pygame.K_LEFT and not self.show_detail:
                idx = [t[0] for t in self.tabs].index(self.current_tab)
                idx = (idx - 1) % len(self.tabs)
                self.current_tab = self.tabs[idx][0]
                self.scroll_offset = 0
                self.selected_index = 0

            if event.key == pygame.K_RIGHT and not self.show_detail:
                idx = [t[0] for t in self.tabs].index(self.current_tab)
                idx = (idx + 1) % len(self.tabs)
                self.current_tab = self.tabs[idx][0]
                self.scroll_offset = 0
                self.selected_index = 0

            # 选择
            if event.key == pygame.K_UP:
                self.selected_index = max(0, self.selected_index - 1)
                self._adjust_scroll()

            if event.key == pygame.K_DOWN:
                self.selected_index += 1
                self._adjust_scroll()

            # 确认/查看详情
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self._handle_action(quest_system, inventory, player)

        return None

    def _adjust_scroll(self):
        """调整滚动"""
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + self.items_per_page:
            self.scroll_offset = self.selected_index - self.items_per_page + 1

    def _handle_action(self, quest_system, inventory, player):
        """处理确认操作"""
        quests = self._get_current_quests(quest_system, player)
        if not quests or self.selected_index >= len(quests):
            return None

        quest_id = quests[self.selected_index]
        quest = get_quest_data(quest_id)
        status = quest_system.get_quest_status(quest_id)

        if self.show_detail:
            # 在详情页面
            if status == QUEST_STATUS_AVAILABLE:
                # 接受任务
                success, msg = quest_system.accept_quest(quest_id)
                if success:
                    self.show_detail = False
                    self.current_tab = "active"
                    return ("accept", quest_id, msg)
            elif status == QUEST_STATUS_COMPLETE:
                # 完成任务
                success, msg, rewards = quest_system.complete_quest(quest_id, inventory)
                if success:
                    self.show_detail = False
                    return ("complete", quest_id, msg, rewards)
        else:
            # 显示详情
            self.show_detail = True
            self.detail_quest_id = quest_id

        return None

    def _get_current_quests(self, quest_system, player):
        """获取当前标签页的任务列表"""
        if self.current_tab == "active":
            return quest_system.get_active_quests()
        elif self.current_tab == "available":
            return quest_system.get_available_quests(player.sequence)
        elif self.current_tab == "completed":
            return list(quest_system.completed_quests)
        return []

    def draw(self, quest_system, player):
        """绘制任务界面"""
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
        title = self.fonts["large"].render("任务", True, GOLD)
        self.screen.blit(title, (self.panel_rect.centerx - title.get_width() // 2, self.panel_rect.top + 15))

        # 主线进度
        progress = quest_system.get_main_quest_progress()
        progress_text = self.fonts["tiny"].render(
            f"主线进度: {progress['completed']}/{progress['total']} ({progress['progress_percent']:.0f}%)",
            True, GRAY
        )
        self.screen.blit(progress_text, (self.panel_rect.right - 200, self.panel_rect.top + 25))

        if self.show_detail:
            self._draw_detail(quest_system)
        else:
            # 绘制标签页
            self._draw_tabs()
            # 绘制任务列表
            self._draw_quest_list(quest_system, player)

        # 绘制操作提示
        self._draw_hints()

    def _draw_tabs(self):
        """绘制标签页"""
        tab_width = 100
        tab_height = 30
        start_x = self.panel_rect.left + 30
        start_y = self.panel_rect.top + 55

        for i, (tab_id, tab_name) in enumerate(self.tabs):
            rect = pygame.Rect(start_x + i * (tab_width + 10), start_y, tab_width, tab_height)

            if tab_id == self.current_tab:
                pygame.draw.rect(self.screen, (60, 60, 100), rect, border_radius=5)
                pygame.draw.rect(self.screen, GOLD, rect, 2, border_radius=5)
            else:
                pygame.draw.rect(self.screen, (40, 40, 60), rect, border_radius=5)
                pygame.draw.rect(self.screen, GRAY, rect, 1, border_radius=5)

            color = WHITE if tab_id == self.current_tab else GRAY
            text = self.fonts["small"].render(tab_name, True, color)
            self.screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

    def _draw_quest_list(self, quest_system, player):
        """绘制任务列表"""
        quests = self._get_current_quests(quest_system, player)

        content_rect = pygame.Rect(
            self.panel_rect.left + 20,
            self.panel_rect.top + 100,
            self.panel_rect.width - 40,
            self.panel_rect.height - 150
        )

        if not quests:
            empty_text = self.fonts["small"].render("暂无任务", True, GRAY)
            self.screen.blit(empty_text, (content_rect.centerx - empty_text.get_width() // 2, content_rect.centery))
            return

        # 限制选中索引
        self.selected_index = min(self.selected_index, len(quests) - 1)

        y = content_rect.top
        item_height = 80

        for i, quest_id in enumerate(quests[self.scroll_offset:self.scroll_offset + self.items_per_page]):
            idx = i + self.scroll_offset
            quest = get_quest_data(quest_id)
            if not quest:
                continue

            item_rect = pygame.Rect(content_rect.left, y, content_rect.width, item_height - 5)

            # 选中高亮
            if idx == self.selected_index:
                pygame.draw.rect(self.screen, (50, 50, 80), item_rect, border_radius=5)
                pygame.draw.rect(self.screen, GOLD, item_rect, 1, border_radius=5)
            else:
                pygame.draw.rect(self.screen, (35, 35, 55), item_rect, border_radius=5)

            # 任务类型图标/颜色
            type_color = {
                QUEST_TYPE_MAIN: GOLD,
                QUEST_TYPE_SIDE: (100, 200, 255),
                QUEST_TYPE_DAILY: (100, 255, 100),
            }.get(quest.get("type"), WHITE)

            type_text = {
                QUEST_TYPE_MAIN: "[主线]",
                QUEST_TYPE_SIDE: "[支线]",
                QUEST_TYPE_DAILY: "[日常]",
            }.get(quest.get("type"), "")

            # 类型标签
            type_label = self.fonts["tiny"].render(type_text, True, type_color)
            self.screen.blit(type_label, (content_rect.left + 10, y + 8))

            # 任务名称
            name_text = self.fonts["small"].render(quest["name"], True, WHITE)
            self.screen.blit(name_text, (content_rect.left + 70, y + 5))

            # 任务描述（截断）
            desc = quest.get("desc", "")[:40] + "..." if len(quest.get("desc", "")) > 40 else quest.get("desc", "")
            desc_text = self.fonts["tiny"].render(desc, True, GRAY)
            self.screen.blit(desc_text, (content_rect.left + 70, y + 30))

            # 状态/进度
            status = quest_system.get_quest_status(quest_id)
            if status == QUEST_STATUS_ACTIVE:
                progress = quest_system.get_quest_progress(quest_id)
                if progress:
                    completed = sum(1 for p in progress if p["complete"])
                    total = len(progress)
                    progress_str = f"进度: {completed}/{total}"
                    progress_color = (100, 255, 100) if completed == total else WHITE
                    prog_text = self.fonts["tiny"].render(progress_str, True, progress_color)
                    self.screen.blit(prog_text, (content_rect.right - 100, y + 30))
            elif status == QUEST_STATUS_COMPLETE:
                complete_text = self.fonts["tiny"].render("可提交", True, GOLD)
                self.screen.blit(complete_text, (content_rect.right - 80, y + 30))

            y += item_height

    def _draw_detail(self, quest_system):
        """绘制任务详情"""
        quest = get_quest_data(self.detail_quest_id)
        if not quest:
            return

        content_rect = pygame.Rect(
            self.panel_rect.left + 30,
            self.panel_rect.top + 60,
            self.panel_rect.width - 60,
            self.panel_rect.height - 100
        )

        # 任务类型
        type_color = {
            QUEST_TYPE_MAIN: GOLD,
            QUEST_TYPE_SIDE: (100, 200, 255),
            QUEST_TYPE_DAILY: (100, 255, 100),
        }.get(quest.get("type"), WHITE)

        type_text = {
            QUEST_TYPE_MAIN: "[主线任务]",
            QUEST_TYPE_SIDE: "[支线任务]",
            QUEST_TYPE_DAILY: "[日常任务]",
        }.get(quest.get("type"), "")

        type_label = self.fonts["small"].render(type_text, True, type_color)
        self.screen.blit(type_label, (content_rect.left, content_rect.top))

        # 章节（主线）
        if quest.get("chapter"):
            chapter_text = self.fonts["tiny"].render(f"第{quest['chapter']}章", True, GRAY)
            self.screen.blit(chapter_text, (content_rect.left + 100, content_rect.top + 5))

        # 任务名称
        name_text = self.fonts["medium"].render(quest["name"], True, WHITE)
        self.screen.blit(name_text, (content_rect.left, content_rect.top + 35))

        # 分隔线
        pygame.draw.line(
            self.screen, GRAY,
            (content_rect.left, content_rect.top + 70),
            (content_rect.right, content_rect.top + 70)
        )

        # 任务描述
        y = content_rect.top + 85
        desc_text = self.fonts["small"].render(quest.get("desc", ""), True, GRAY)
        self.screen.blit(desc_text, (content_rect.left, y))

        # 目标
        y += 50
        obj_title = self.fonts["small"].render("任务目标:", True, WHITE)
        self.screen.blit(obj_title, (content_rect.left, y))
        y += 30

        status = quest_system.get_quest_status(self.detail_quest_id)
        progress = quest_system.get_quest_progress(self.detail_quest_id) if status == QUEST_STATUS_ACTIVE else None

        for i, obj in enumerate(quest.get("objectives", [])):
            # 进度
            if progress and i < len(progress):
                p = progress[i]
                obj_str = f"  • {obj['desc']}: {p['current']}/{p['required']}"
                color = (100, 255, 100) if p["complete"] else WHITE
            else:
                obj_str = f"  • {obj['desc']}: 0/{obj.get('count', 1)}"
                color = WHITE

            obj_text = self.fonts["small"].render(obj_str, True, color)
            self.screen.blit(obj_text, (content_rect.left, y))
            y += 28

        # 奖励
        y += 20
        reward_title = self.fonts["small"].render("任务奖励:", True, WHITE)
        self.screen.blit(reward_title, (content_rect.left, y))
        y += 30

        rewards = quest.get("rewards", {})
        if rewards.get("exp"):
            exp_text = self.fonts["small"].render(f"  • 经验: {rewards['exp']}", True, (200, 200, 100))
            self.screen.blit(exp_text, (content_rect.left, y))
            y += 25

        for mat_name, mat_count in rewards.get("materials", {}).items():
            mat_text = self.fonts["small"].render(f"  • {mat_name} x{mat_count}", True, (100, 200, 100))
            self.screen.blit(mat_text, (content_rect.left, y))
            y += 25

        # 操作按钮
        y = content_rect.bottom - 50
        if status == QUEST_STATUS_AVAILABLE:
            btn_text = self.fonts["medium"].render("[ 按回车接受任务 ]", True, GOLD)
            self.screen.blit(btn_text, (content_rect.centerx - btn_text.get_width() // 2, y))
        elif status == QUEST_STATUS_COMPLETE:
            btn_text = self.fonts["medium"].render("[ 按回车完成任务 ]", True, (100, 255, 100))
            self.screen.blit(btn_text, (content_rect.centerx - btn_text.get_width() // 2, y))
        elif status == QUEST_STATUS_ACTIVE:
            btn_text = self.fonts["small"].render("任务进行中...", True, GRAY)
            self.screen.blit(btn_text, (content_rect.centerx - btn_text.get_width() // 2, y))

    def _draw_hints(self):
        """绘制操作提示"""
        if self.show_detail:
            hints = ["ESC 返回", "回车 确认"]
        else:
            hints = ["← → 切换标签", "↑ ↓ 选择", "回车 查看详情", "Q/ESC 关闭"]

        y = self.panel_rect.bottom - 35
        x = self.panel_rect.left + 30
        for hint in hints:
            text = self.fonts["tiny"].render(hint, True, GRAY)
            self.screen.blit(text, (x, y))
            x += 150


class QuestTracker:
    """任务追踪器（显示在游戏界面右侧）"""

    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self.visible = True

    def toggle(self):
        """切换显示"""
        self.visible = not self.visible

    def draw(self, quest_system):
        """绘制任务追踪"""
        if not self.visible:
            return

        active_quests = quest_system.get_active_quests()
        if not active_quests:
            return

        # 只显示第一个活动任务
        quest_id = active_quests[0]
        quest = get_quest_data(quest_id)
        if not quest:
            return

        # 背景面板
        panel_width = 220
        panel_height = 150
        panel_x = SCREEN_WIDTH - panel_width - 20
        panel_y = 120

        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

        # 半透明背景
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((0, 0, 0, 150))
        self.screen.blit(panel_surface, panel_rect)

        pygame.draw.rect(self.screen, GOLD, panel_rect, 1, border_radius=5)

        # 任务名称
        name_text = self.fonts["small"].render(quest["name"], True, GOLD)
        self.screen.blit(name_text, (panel_x + 10, panel_y + 10))

        # 目标进度
        progress = quest_system.get_quest_progress(quest_id)
        y = panel_y + 40

        if progress:
            for p in progress[:3]:  # 最多显示3个目标
                if p["complete"]:
                    status_text = "✓"
                    color = (100, 255, 100)
                else:
                    status_text = f"{p['current']}/{p['required']}"
                    color = WHITE

                obj_text = self.fonts["tiny"].render(
                    f"{p['desc'][:15]}... {status_text}" if len(p['desc']) > 15 else f"{p['desc']} {status_text}",
                    True, color
                )
                self.screen.blit(obj_text, (panel_x + 10, y))
                y += 22

        # 任务状态
        status = quest_system.get_quest_status(quest_id)
        if status == QUEST_STATUS_COMPLETE:
            complete_text = self.fonts["small"].render("任务完成！按Q打开任务面板", True, GOLD)
            self.screen.blit(complete_text, (panel_x + 10, panel_y + panel_height - 30))


class QuestNotification:
    """任务通知"""

    def __init__(self):
        self.notifications = []

    def add(self, text, color=GOLD, duration=3.0):
        """添加通知"""
        self.notifications.append({
            "text": text,
            "color": color,
            "lifetime": duration,
            "alpha": 255,
        })

    def update(self, dt):
        """更新通知"""
        for notif in self.notifications[:]:
            notif["lifetime"] -= dt
            if notif["lifetime"] < 1.0:
                notif["alpha"] = int(255 * notif["lifetime"])
            if notif["lifetime"] <= 0:
                self.notifications.remove(notif)

    def draw(self, screen, fonts):
        """绘制通知"""
        y = SCREEN_HEIGHT // 2 - 100
        for notif in self.notifications[-3:]:
            text = fonts["medium"].render(notif["text"], True, notif["color"])
            text_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
            text_surface.blit(text, (0, 0))
            text_surface.set_alpha(notif["alpha"])

            x = SCREEN_WIDTH // 2 - text.get_width() // 2
            screen.blit(text_surface, (x, y))
            y += 40
