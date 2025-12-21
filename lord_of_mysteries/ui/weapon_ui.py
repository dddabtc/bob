"""
武器UI系统
显示武器背包、装备界面、武器详情
"""

import pygame
from settings import *
from data.weapons import WEAPONS, get_weapon_data, WEAPON_TYPE_NAMES
from data.items import QUALITY_COLORS


class WeaponUI:
    """武器管理界面"""

    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self.visible = False

        # 界面尺寸
        self.width = 700
        self.height = 500
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2

        # 武器列表
        self.weapons = []
        self.selected_index = 0
        self.scroll_offset = 0
        self.items_per_page = 8

        # 当前装备的武器
        self.equipped_weapon = None

        # 引用
        self.inventory = None
        self.player = None

    def set_references(self, inventory, player):
        """设置引用"""
        self.inventory = inventory
        self.player = player

    def show(self):
        """显示界面"""
        self.visible = True
        self._refresh_weapons()

    def hide(self):
        """隐藏界面"""
        self.visible = False

    def toggle(self):
        """切换显示"""
        if self.visible:
            self.hide()
        else:
            self.show()

    def _refresh_weapons(self):
        """刷新武器列表"""
        if self.inventory:
            self.weapons = self.inventory.get_all_weapons()
        if self.player:
            self.equipped_weapon = self.player.get_equipped_weapon()

    def handle_event(self, event):
        """处理事件"""
        if not self.visible:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_i:
                self.hide()
                return True

            elif event.key == pygame.K_UP:
                self.selected_index = max(0, self.selected_index - 1)
                self._adjust_scroll()
                return True

            elif event.key == pygame.K_DOWN:
                self.selected_index = min(len(self.weapons) - 1, self.selected_index + 1)
                self._adjust_scroll()
                return True

            elif event.key == pygame.K_RETURN or event.key == pygame.K_e:
                self._equip_selected()
                return True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._handle_click(event.pos)
                return True
            elif event.button == 4:  # 滚轮向上
                self.scroll_offset = max(0, self.scroll_offset - 1)
                return True
            elif event.button == 5:  # 滚轮向下
                max_scroll = max(0, len(self.weapons) - self.items_per_page)
                self.scroll_offset = min(max_scroll, self.scroll_offset + 1)
                return True

        return False

    def _adjust_scroll(self):
        """调整滚动位置"""
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + self.items_per_page:
            self.scroll_offset = self.selected_index - self.items_per_page + 1

    def _handle_click(self, pos):
        """处理点击"""
        mx, my = pos

        # 检查武器列表点击
        list_x = self.x + 20
        list_y = self.y + 80
        item_height = 45

        for i in range(self.items_per_page):
            weapon_index = self.scroll_offset + i
            if weapon_index >= len(self.weapons):
                break

            item_rect = pygame.Rect(list_x, list_y + i * item_height, 300, item_height - 5)
            if item_rect.collidepoint(mx, my):
                self.selected_index = weapon_index
                return

        # 检查装备按钮点击
        equip_btn = pygame.Rect(self.x + 520, self.y + 400, 150, 40)
        if equip_btn.collidepoint(mx, my):
            self._equip_selected()

    def _equip_selected(self):
        """装备选中的武器"""
        if not self.weapons or self.selected_index >= len(self.weapons):
            return

        weapon = self.weapons[self.selected_index]
        weapon_name = weapon["name"]

        if self.player and self.player.equip_weapon(weapon_name):
            self.equipped_weapon = weapon_name
            self._refresh_weapons()

    def update(self, dt):
        """更新"""
        pass

    def draw(self):
        """绘制界面"""
        if not self.visible:
            return

        # 半透明背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # 主面板
        panel = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        panel.fill((30, 30, 40, 240))
        pygame.draw.rect(panel, GOLD, (0, 0, self.width, self.height), 2, border_radius=10)

        # 标题
        title = self.fonts["large"].render("武器背包", True, GOLD)
        title_rect = title.get_rect(center=(self.width // 2, 30))
        panel.blit(title, title_rect)

        # 分割线
        pygame.draw.line(panel, (80, 80, 100), (20, 60), (self.width - 20, 60), 2)

        # 左侧：武器列表
        self._draw_weapon_list(panel)

        # 右侧：武器详情
        self._draw_weapon_details(panel)

        # 底部提示
        hint = self.fonts["tiny"].render("↑↓选择  Enter/E装备  ESC/I关闭", True, (150, 150, 150))
        panel.blit(hint, (20, self.height - 30))

        self.screen.blit(panel, (self.x, self.y))

    def _draw_weapon_list(self, surface):
        """绘制武器列表"""
        list_x = 20
        list_y = 80
        item_height = 45
        list_width = 300

        # 列表标题
        header = self.fonts["small"].render(f"武器 ({len(self.weapons)}/{self.inventory.max_weapons if self.inventory else 20})", True, WHITE)
        surface.blit(header, (list_x, list_y - 25))

        if not self.weapons:
            empty_text = self.fonts["small"].render("暂无武器", True, (100, 100, 100))
            surface.blit(empty_text, (list_x + 50, list_y + 50))
            return

        # 绘制武器项
        for i in range(self.items_per_page):
            weapon_index = self.scroll_offset + i
            if weapon_index >= len(self.weapons):
                break

            weapon = self.weapons[weapon_index]
            item_y = list_y + i * item_height

            # 选中背景
            is_selected = weapon_index == self.selected_index
            is_equipped = weapon["name"] == self.equipped_weapon

            if is_selected:
                bg_color = (60, 60, 80)
            elif is_equipped:
                bg_color = (40, 50, 40)
            else:
                bg_color = (35, 35, 45)

            pygame.draw.rect(surface, bg_color, (list_x, item_y, list_width, item_height - 5), border_radius=5)

            # 边框
            border_color = GOLD if is_selected else (60, 60, 70)
            pygame.draw.rect(surface, border_color, (list_x, item_y, list_width, item_height - 5), 1, border_radius=5)

            # 武器名称（带品质颜色）
            quality_color = QUALITY_COLORS.get(weapon["quality"], WHITE)
            name_text = self.fonts["small"].render(weapon["name"], True, quality_color)
            surface.blit(name_text, (list_x + 10, item_y + 5))

            # 武器类型和攻击力
            type_name = WEAPON_TYPE_NAMES.get(weapon["type"], weapon["type"])
            info_text = self.fonts["tiny"].render(f"{type_name}  ATK +{weapon['attack']}", True, (150, 150, 150))
            surface.blit(info_text, (list_x + 10, item_y + 25))

            # 装备标记
            if is_equipped:
                equipped_text = self.fonts["tiny"].render("[装备中]", True, (100, 255, 100))
                surface.blit(equipped_text, (list_x + list_width - 60, item_y + 12))

        # 滚动指示
        if len(self.weapons) > self.items_per_page:
            if self.scroll_offset > 0:
                up_text = self.fonts["tiny"].render("▲", True, (150, 150, 150))
                surface.blit(up_text, (list_x + list_width // 2, list_y - 15))
            if self.scroll_offset + self.items_per_page < len(self.weapons):
                down_text = self.fonts["tiny"].render("▼", True, (150, 150, 150))
                surface.blit(down_text, (list_x + list_width // 2, list_y + self.items_per_page * item_height))

    def _draw_weapon_details(self, surface):
        """绘制武器详情"""
        detail_x = 350
        detail_y = 80
        detail_width = 330

        # 详情面板背景
        pygame.draw.rect(surface, (25, 25, 35), (detail_x, detail_y, detail_width, 300), border_radius=5)
        pygame.draw.rect(surface, (60, 60, 70), (detail_x, detail_y, detail_width, 300), 1, border_radius=5)

        if not self.weapons or self.selected_index >= len(self.weapons):
            hint = self.fonts["small"].render("选择一个武器查看详情", True, (100, 100, 100))
            surface.blit(hint, (detail_x + 50, detail_y + 130))
            return

        weapon = self.weapons[self.selected_index]
        y_offset = detail_y + 15

        # 武器名称
        quality_color = QUALITY_COLORS.get(weapon["quality"], WHITE)
        name_text = self.fonts["medium"].render(weapon["name"], True, quality_color)
        surface.blit(name_text, (detail_x + 15, y_offset))
        y_offset += 35

        # 品质和类型
        quality_names = {
            "common": "普通",
            "uncommon": "优秀",
            "rare": "稀有",
            "epic": "史诗",
            "legendary": "传说"
        }
        quality_name = quality_names.get(weapon["quality"], "未知")
        type_name = WEAPON_TYPE_NAMES.get(weapon["type"], weapon["type"])
        info_text = self.fonts["small"].render(f"{quality_name} · {type_name}", True, quality_color)
        surface.blit(info_text, (detail_x + 15, y_offset))
        y_offset += 30

        # 分割线
        pygame.draw.line(surface, (60, 60, 70), (detail_x + 15, y_offset), (detail_x + detail_width - 15, y_offset))
        y_offset += 15

        # 攻击力
        atk_text = self.fonts["small"].render(f"攻击力: +{weapon['attack']}", True, (255, 200, 100))
        surface.blit(atk_text, (detail_x + 15, y_offset))
        y_offset += 25

        # 特殊效果
        if weapon.get("special"):
            special_text = self.fonts["small"].render(f"特效: {weapon['special']}", True, (100, 200, 255))
            surface.blit(special_text, (detail_x + 15, y_offset))
            y_offset += 25

        # 分割线
        y_offset += 10
        pygame.draw.line(surface, (60, 60, 70), (detail_x + 15, y_offset), (detail_x + detail_width - 15, y_offset))
        y_offset += 15

        # 描述
        desc = weapon.get("desc", "")
        if desc:
            # 简单的文字换行
            words = desc
            line = ""
            for char in words:
                test_line = line + char
                text_width = self.fonts["tiny"].size(test_line)[0]
                if text_width > detail_width - 30:
                    desc_text = self.fonts["tiny"].render(line, True, (180, 180, 180))
                    surface.blit(desc_text, (detail_x + 15, y_offset))
                    y_offset += 20
                    line = char
                else:
                    line = test_line
            if line:
                desc_text = self.fonts["tiny"].render(line, True, (180, 180, 180))
                surface.blit(desc_text, (detail_x + 15, y_offset))

        # 装备按钮
        btn_y = detail_y + 320
        is_equipped = weapon["name"] == self.equipped_weapon

        if is_equipped:
            btn_color = (50, 80, 50)
            btn_text = "已装备"
            text_color = (150, 200, 150)
        else:
            btn_color = (60, 60, 100)
            btn_text = "装备 (E)"
            text_color = WHITE

        pygame.draw.rect(surface, btn_color, (detail_x + 90, btn_y, 150, 40), border_radius=5)
        pygame.draw.rect(surface, GOLD if not is_equipped else (100, 150, 100),
                        (detail_x + 90, btn_y, 150, 40), 2, border_radius=5)

        btn_label = self.fonts["small"].render(btn_text, True, text_color)
        btn_rect = btn_label.get_rect(center=(detail_x + 165, btn_y + 20))
        surface.blit(btn_label, btn_rect)


class WeaponHUD:
    """武器HUD - 显示当前装备的武器"""

    def __init__(self, fonts):
        self.fonts = fonts
        self.x = 10
        self.y = SCREEN_HEIGHT - 100

    def draw(self, screen, player):
        """绘制武器HUD"""
        if not player or not player.weapon_manager:
            return

        weapon_info = player.weapon_manager.get_weapon_info()
        if not weapon_info:
            return

        # 背景
        bg_width = 150
        bg_height = 60
        bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        bg_surface.fill((20, 20, 30, 200))
        pygame.draw.rect(bg_surface, (60, 60, 80), (0, 0, bg_width, bg_height), 1, border_radius=5)
        screen.blit(bg_surface, (self.x, self.y))

        # 武器名称
        quality = weapon_info.get("quality", "common")
        color = QUALITY_COLORS.get(quality, WHITE)
        name_text = self.fonts["small"].render(weapon_info["name"], True, color)
        screen.blit(name_text, (self.x + 10, self.y + 5))

        # 攻击力
        atk_text = self.fonts["tiny"].render(f"ATK +{weapon_info['attack']}", True, (200, 200, 200))
        screen.blit(atk_text, (self.x + 10, self.y + 25))

        # 左轮弹药
        if weapon_info.get("max_ammo"):
            if weapon_info.get("is_reloading"):
                ammo_text = self.fonts["tiny"].render("装填中...", True, (255, 200, 100))
                # 装填进度条
                progress = weapon_info.get("reload_progress", 0)
                pygame.draw.rect(screen, (50, 50, 50), (self.x + 10, self.y + 45, 100, 8))
                pygame.draw.rect(screen, (100, 200, 100), (self.x + 10, self.y + 45, int(100 * progress), 8))
            else:
                ammo = weapon_info["ammo"]
                max_ammo = weapon_info["max_ammo"]
                ammo_text = self.fonts["tiny"].render(f"弹药: {ammo}/{max_ammo}", True, (200, 200, 200))
            screen.blit(ammo_text, (self.x + 10, self.y + 42))
