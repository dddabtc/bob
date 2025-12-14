"""
途径选择界面
"""

import pygame
import sys
sys.path.append('..')
from settings import *
from systems.sprites import get_sequence_sprite, get_sequence_portrait, set_pathway


class PathwayCard:
    """途径卡片"""
    def __init__(self, x, y, width, height, pathway_id, pathway_data, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.pathway_id = pathway_id
        self.data = pathway_data
        self.font = font
        self.is_hovered = False
        self.is_selected = False

    def update(self, mouse_pos):
        """更新卡片状态"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen, small_font):
        """绘制卡片"""
        # 背景颜色
        if self.is_selected:
            bg_color = (80, 70, 100)
            border_color = GOLD
            border_width = 3
        elif self.is_hovered:
            bg_color = (60, 55, 85)
            border_color = self.data["color"]
            border_width = 2
        else:
            bg_color = (40, 35, 60)
            border_color = (80, 80, 80)
            border_width = 1

        # 绘制卡片背景
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=8)
        pygame.draw.rect(screen, border_color, self.rect, border_width, border_radius=8)

        # 途径颜色条
        color_bar = pygame.Rect(self.rect.x + 5, self.rect.y + 5, 6, self.rect.height - 10)
        pygame.draw.rect(screen, self.data["color"], color_bar, border_radius=3)

        # 途径名称
        name_color = GOLD if self.is_selected else (self.data["color"] if self.is_hovered else WHITE)
        name_text = self.font.render(self.pathway_id, True, name_color)
        screen.blit(name_text, (self.rect.x + 20, self.rect.y + 8))

        # 序列9职业
        seq9_name = self.data["sequences"][9]["name"]
        seq_text = small_font.render(f"序列9: {seq9_name}", True, GRAY)
        screen.blit(seq_text, (self.rect.x + 20, self.rect.y + 35))


class PathwaySelectUI:
    """途径选择界面"""
    def __init__(self, screen, fonts, pathways_data):
        self.screen = screen
        self.fonts = fonts
        self.pathways = pathways_data
        self.cards = []
        self.selected_pathway = None
        self.scroll_offset = 0
        self.max_scroll = 0

        # 分页
        self.current_page = 0
        self.pathways_per_page = 8  # 每页显示8个途径

        # 类型筛选
        self.type_filters = {
            "all": "全部",
            "melee": "近战物理",
            "magic": "魔法远程",
            "control": "辅助控制",
            "special": "特殊能力",
            "support": "生存支援",
            "wisdom": "智慧研究"
        }
        self.current_filter = "all"

        self._create_cards()

    def _get_filtered_pathways(self):
        """获取筛选后的途径"""
        if self.current_filter == "all":
            return list(self.pathways.items())
        return [(k, v) for k, v in self.pathways.items() if v["type"] == self.current_filter]

    def _create_cards(self):
        """创建途径卡片"""
        self.cards = []
        filtered = self._get_filtered_pathways()

        # 计算起始索引
        start_idx = self.current_page * self.pathways_per_page
        end_idx = min(start_idx + self.pathways_per_page, len(filtered))

        # 卡片布局
        card_width = 220
        card_height = 60
        start_x = 80
        start_y = 180
        gap_x = 240
        gap_y = 75

        for i, (pathway_id, data) in enumerate(filtered[start_idx:end_idx]):
            col = i % 4
            row = i // 4
            x = start_x + col * gap_x
            y = start_y + row * gap_y

            card = PathwayCard(x, y, card_width, card_height, pathway_id, data, self.fonts["small"])
            self.cards.append(card)

        # 计算最大页数
        self.max_pages = (len(filtered) + self.pathways_per_page - 1) // self.pathways_per_page

    def update(self, mouse_pos, mouse_clicked, events):
        """更新界面状态"""
        # 更新卡片悬停状态
        for card in self.cards:
            card.update(mouse_pos)
            if mouse_clicked and card.is_hovered:
                # 取消其他选择
                for c in self.cards:
                    c.is_selected = False
                card.is_selected = True
                self.selected_pathway = card.pathway_id

        # 处理键盘事件
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.current_page > 0:
                        self.current_page -= 1
                        self._create_cards()
                elif event.key == pygame.K_RIGHT:
                    if self.current_page < self.max_pages - 1:
                        self.current_page += 1
                        self._create_cards()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if self.selected_pathway:
                        return ("confirm", self.selected_pathway)
                elif event.key == pygame.K_ESCAPE:
                    return ("back", None)
                # 数字键切换筛选
                elif event.key == pygame.K_1:
                    self._set_filter("all")
                elif event.key == pygame.K_2:
                    self._set_filter("melee")
                elif event.key == pygame.K_3:
                    self._set_filter("magic")
                elif event.key == pygame.K_4:
                    self._set_filter("control")
                elif event.key == pygame.K_5:
                    self._set_filter("special")
                elif event.key == pygame.K_6:
                    self._set_filter("support")
                elif event.key == pygame.K_7:
                    self._set_filter("wisdom")

        return (None, None)

    def _set_filter(self, filter_type):
        """设置筛选类型"""
        self.current_filter = filter_type
        self.current_page = 0
        self.selected_pathway = None
        self._create_cards()

    def draw(self):
        """绘制途径选择界面"""
        self.screen.fill(MENU_BG)

        # 标题
        title = self.fonts["large"].render("选择你的途径", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        # 副标题
        subtitle = self.fonts["tiny"].render("每条途径都有独特的能力和成长路线", True, GRAY)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 90))
        self.screen.blit(subtitle, subtitle_rect)

        # 绘制筛选按钮
        self._draw_filter_buttons()

        # 绘制途径卡片
        for card in self.cards:
            card.draw(self.screen, self.fonts["tiny"])

        # 绘制选中途径的详细信息
        if self.selected_pathway:
            self._draw_pathway_detail()

        # 绘制分页信息
        self._draw_pagination()

        # 绘制操作提示
        self._draw_hints()

    def _draw_filter_buttons(self):
        """绘制筛选按钮"""
        filters = list(self.type_filters.items())
        start_x = 80
        y = 130
        btn_width = 100
        gap = 10

        for i, (filter_id, filter_name) in enumerate(filters):
            x = start_x + i * (btn_width + gap)
            rect = pygame.Rect(x, y, btn_width, 30)

            # 颜色
            if filter_id == self.current_filter:
                bg_color = GOLD
                text_color = BLACK
            else:
                bg_color = DARK_GRAY
                text_color = WHITE

            pygame.draw.rect(self.screen, bg_color, rect, border_radius=5)

            # 文字
            text = self.fonts["tiny"].render(filter_name, True, text_color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def _draw_pathway_detail(self):
        """绘制选中途径的详细信息"""
        data = self.pathways[self.selected_pathway]

        # 切换到选中的途径图片
        set_pathway(self.selected_pathway)

        # 详情面板
        panel_rect = pygame.Rect(80, 360, SCREEN_WIDTH - 160, 280)
        pygame.draw.rect(self.screen, (30, 30, 50), panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, data["color"], panel_rect, 2, border_radius=10)

        # 绘制角色图片（序列9）
        sprite = get_sequence_sprite(9, (120, 160))
        if sprite:
            # 角色图片背景框
            sprite_bg = pygame.Rect(100, 380, 130, 170)
            pygame.draw.rect(self.screen, (20, 20, 35), sprite_bg, border_radius=8)
            pygame.draw.rect(self.screen, data["color"], sprite_bg, 2, border_radius=8)
            # 绘制角色
            self.screen.blit(sprite, (105, 385))

        # 途径名称（右移以避开角色图片）
        name = self.fonts["medium"].render(f"{data['name']}", True, data["color"])
        self.screen.blit(name, (250, 375))

        # 对应神灵
        god = self.fonts["small"].render(f"对应神灵: {data['god']}", True, WHITE)
        self.screen.blit(god, (450, 380))

        # 途径描述（右侧显示）
        desc = self.fonts["small"].render(data["desc"], True, GRAY)
        self.screen.blit(desc, (250, 410))

        # 序列信息（右侧显示）
        info_x = 250
        seq_y = 445
        seq_title = self.fonts["small"].render("序列晋升路线:", True, GOLD)
        self.screen.blit(seq_title, (info_x, seq_y))

        # 显示序列9到序列0
        seq_y += 28
        sequences = data["sequences"]
        seq_text = ""
        for seq in [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]:
            if seq in sequences:
                if seq_text:
                    seq_text += " → "
                seq_text += f"{sequences[seq]['name']}({seq})"

        # 分行显示（更紧凑）
        seq_line1 = self.fonts["tiny"].render(seq_text[:55], True, WHITE)
        self.screen.blit(seq_line1, (info_x, seq_y))
        if len(seq_text) > 55:
            seq_line2 = self.fonts["tiny"].render(seq_text[55:110], True, WHITE)
            self.screen.blit(seq_line2, (info_x, seq_y + 22))
            if len(seq_text) > 110:
                seq_line3 = self.fonts["tiny"].render(seq_text[110:], True, WHITE)
                self.screen.blit(seq_line3, (info_x, seq_y + 44))

        # 初始属性
        seq9 = sequences[9]
        attr_y = seq_y + 70
        attr_title = self.fonts["small"].render("初始属性 (序列9):", True, GOLD)
        self.screen.blit(attr_title, (info_x, attr_y))

        attr_y += 25
        attrs = [
            f"HP: {seq9['hp']}",
            f"攻击: {seq9['attack']}",
            f"防御: {seq9['defense']}",
            f"速度: {seq9['speed']}"
        ]
        attr_text = self.fonts["tiny"].render("  |  ".join(attrs), True, WHITE)
        self.screen.blit(attr_text, (info_x, attr_y))

        # 初始技能
        skill_y = attr_y + 25
        skill_title = self.fonts["small"].render("初始技能:", True, GOLD)
        self.screen.blit(skill_title, (info_x, skill_y))

        skill_y += 25
        skills_text = ", ".join(seq9["skills"])
        skills = self.fonts["tiny"].render(skills_text, True, WHITE)
        self.screen.blit(skills, (info_x, skill_y))

    def _draw_pagination(self):
        """绘制分页信息"""
        filtered = self._get_filtered_pathways()
        total = len(filtered)

        page_text = self.fonts["small"].render(
            f"第 {self.current_page + 1}/{self.max_pages} 页 (共 {total} 条途径)",
            True, GRAY
        )
        page_rect = page_text.get_rect(center=(SCREEN_WIDTH // 2, 345))
        self.screen.blit(page_text, page_rect)

        # 左右箭头提示
        if self.current_page > 0:
            left_hint = self.fonts["tiny"].render("← 上一页", True, GRAY)
            self.screen.blit(left_hint, (100, 340))

        if self.current_page < self.max_pages - 1:
            right_hint = self.fonts["tiny"].render("下一页 →", True, GRAY)
            self.screen.blit(right_hint, (SCREEN_WIDTH - 180, 340))

    def _draw_hints(self):
        """绘制操作提示"""
        hints = [
            "← → 翻页  |  1-7 筛选类型  |  点击选择途径  |  ENTER/SPACE 确认  |  ESC 返回"
        ]

        y = SCREEN_HEIGHT - 40
        for hint in hints:
            text = self.fonts["tiny"].render(hint, True, DARK_GRAY)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 25


class PathwayConfirmUI:
    """途径确认界面"""
    def __init__(self, screen, fonts, pathway_id, pathway_data):
        self.screen = screen
        self.fonts = fonts
        self.pathway_id = pathway_id
        self.data = pathway_data

    def update(self, mouse_pos, mouse_clicked, events):
        """更新界面"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return ("start", self.pathway_id)
                elif event.key == pygame.K_ESCAPE:
                    return ("back", None)

        return (None, None)

    def draw(self):
        """绘制确认界面"""
        self.screen.fill(MENU_BG)

        # 切换到选中的途径图片
        set_pathway(self.pathway_id)

        # 标题
        title = self.fonts["large"].render("确认选择", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        # 绘制角色图片（大尺寸，居中偏左）
        sprite = get_sequence_sprite(9, (180, 240))
        if sprite:
            # 角色图片背景框
            sprite_x = 120
            sprite_y = 120
            sprite_bg = pygame.Rect(sprite_x - 10, sprite_y - 10, 200, 260)
            pygame.draw.rect(self.screen, (20, 20, 35), sprite_bg, border_radius=10)
            pygame.draw.rect(self.screen, self.data["color"], sprite_bg, 2, border_radius=10)
            # 添加光晕效果
            glow = pygame.Surface((220, 280), pygame.SRCALPHA)
            pygame.draw.rect(glow, (*self.data["color"], 30), (0, 0, 220, 280), border_radius=12)
            self.screen.blit(glow, (sprite_x - 20, sprite_y - 20))
            # 绘制角色
            self.screen.blit(sprite, (sprite_x, sprite_y))

        # 右侧信息区域
        info_x = 380

        # 途径名称
        name = self.fonts["title"].render(self.data["name"], True, self.data["color"])
        self.screen.blit(name, (info_x, 100))

        # 序列9职业
        seq9 = self.data["sequences"][9]
        seq_text = self.fonts["medium"].render(
            f"你将成为: {seq9['name']} (序列9)",
            True, WHITE
        )
        self.screen.blit(seq_text, (info_x, 160))

        # 途径描述
        desc = self.fonts["small"].render(self.data["desc"], True, GRAY)
        self.screen.blit(desc, (info_x, 210))

        # 初始属性
        attr_y = 270
        attrs = [
            ("生命值", seq9["hp"], HP_GREEN),
            ("攻击力", seq9["attack"], CRIMSON),
            ("防御力", seq9["defense"], (100, 150, 255)),
            ("速度", seq9["speed"], (255, 200, 100)),
        ]

        for i, (attr_name, value, color) in enumerate(attrs):
            x = info_x + i * 120
            attr_text = self.fonts["small"].render(attr_name, True, GRAY)
            self.screen.blit(attr_text, (x, attr_y))

            value_text = self.fonts["medium"].render(str(value), True, color)
            self.screen.blit(value_text, (x, attr_y + 28))

        # 初始技能
        skill_y = 360
        skill_title = self.fonts["small"].render("初始技能:", True, GOLD)
        self.screen.blit(skill_title, (info_x, skill_y))

        skills_text = self.fonts["medium"].render(
            " | ".join(seq9["skills"]),
            True, WHITE
        )
        self.screen.blit(skills_text, (info_x, skill_y + 30))

        # 绘制序列晋升预览（下方区域）
        preview_y = 450
        preview_title = self.fonts["small"].render("序列晋升预览:", True, GOLD)
        self.screen.blit(preview_title, (120, preview_y))

        # 显示所有序列的小图标
        sequences = self.data["sequences"]
        icon_size = (50, 65)
        icon_x = 120
        for seq in [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]:
            if seq in sequences:
                seq_sprite = get_sequence_sprite(seq, icon_size)
                if seq_sprite:
                    # 小图标背景
                    icon_bg = pygame.Rect(icon_x - 2, preview_y + 30, icon_size[0] + 4, icon_size[1] + 20)
                    pygame.draw.rect(self.screen, (30, 30, 45), icon_bg, border_radius=5)
                    pygame.draw.rect(self.screen, (60, 60, 80), icon_bg, 1, border_radius=5)
                    # 绘制图标
                    self.screen.blit(seq_sprite, (icon_x, preview_y + 35))
                    # 序列号
                    seq_num = self.fonts["tiny"].render(f"S{seq}", True, WHITE)
                    seq_num_rect = seq_num.get_rect(center=(icon_x + icon_size[0] // 2, preview_y + 105))
                    self.screen.blit(seq_num, seq_num_rect)
                icon_x += 90

        # 确认提示
        confirm_text = self.fonts["small"].render(
            "按 ENTER 或 SPACE 开始游戏",
            True, GOLD
        )
        confirm_rect = confirm_text.get_rect(center=(SCREEN_WIDTH // 2, 600))
        self.screen.blit(confirm_text, confirm_rect)

        back_text = self.fonts["tiny"].render(
            "按 ESC 返回重新选择",
            True, GRAY
        )
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, 640))
        self.screen.blit(back_text, back_rect)
