# 背包和合成系统
import pygame
from settings import (
    BlockType, BLOCK_DATA, RECIPES,
    HOTBAR_SLOTS, INVENTORY_ROWS, INVENTORY_COLS,
    COLORS, WINDOW_WIDTH, WINDOW_HEIGHT
)


class InventoryUI:
    """背包界面"""

    SLOT_SIZE = 50
    SLOT_PADDING = 4
    HOTBAR_Y = 10

    def __init__(self):
        self.is_open = False
        self.dragging_item = None
        self.dragging_from = None
        self.hovered_slot = None

        # 界面位置
        inv_width = INVENTORY_COLS * (self.SLOT_SIZE + self.SLOT_PADDING) + self.SLOT_PADDING
        inv_height = (INVENTORY_ROWS + 1) * (self.SLOT_SIZE + self.SLOT_PADDING) + self.SLOT_PADDING + 60
        self.inv_x = (WINDOW_WIDTH - inv_width) // 2
        self.inv_y = (WINDOW_HEIGHT - inv_height) // 2

        # 字体
        self.font = None
        self.small_font = None

    def init_fonts(self):
        """初始化字体"""
        if self.font is None:
            self.font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 18)

    def toggle(self):
        """切换背包开关"""
        self.is_open = not self.is_open
        if not self.is_open:
            self.dragging_item = None
            self.dragging_from = None

    def handle_event(self, event, player):
        """处理背包事件"""
        if event.type == pygame.KEYDOWN:
            # 数字键选择快捷栏
            if pygame.K_1 <= event.key <= pygame.K_9:
                player.select_slot(event.key - pygame.K_1)

            # E键切换背包
            if event.key == pygame.K_e:
                self.toggle()

        if event.type == pygame.MOUSEBUTTONDOWN and self.is_open:
            mouse_pos = pygame.mouse.get_pos()
            slot = self._get_slot_at(mouse_pos)

            if slot is not None and event.button == 1:  # 左键
                if self.dragging_item is None:
                    # 拾起物品
                    if player.inventory[slot] is not None:
                        self.dragging_item = player.inventory[slot]
                        self.dragging_from = slot
                        player.inventory[slot] = None
                else:
                    # 放下物品
                    if player.inventory[slot] is None:
                        player.inventory[slot] = self.dragging_item
                    else:
                        # 交换或堆叠
                        existing = player.inventory[slot]
                        if existing[0] == self.dragging_item[0]:
                            # 堆叠
                            total = existing[1] + self.dragging_item[1]
                            if total <= 64:
                                player.inventory[slot] = (existing[0], total)
                                self.dragging_item = None
                            else:
                                player.inventory[slot] = (existing[0], 64)
                                self.dragging_item = (existing[0], total - 64)
                        else:
                            # 交换
                            player.inventory[slot] = self.dragging_item
                            self.dragging_item = existing

                    if self.dragging_item is None or (slot == self.dragging_from):
                        self.dragging_item = None
                        self.dragging_from = None

            elif event.button == 3 and slot is not None:  # 右键
                # 分一半
                if self.dragging_item is None and player.inventory[slot] is not None:
                    item = player.inventory[slot]
                    if item[1] > 1:
                        half = item[1] // 2
                        player.inventory[slot] = (item[0], item[1] - half)
                        self.dragging_item = (item[0], half)
                        self.dragging_from = slot
                elif self.dragging_item is not None:
                    # 放一个
                    if player.inventory[slot] is None:
                        player.inventory[slot] = (self.dragging_item[0], 1)
                        if self.dragging_item[1] <= 1:
                            self.dragging_item = None
                            self.dragging_from = None
                        else:
                            self.dragging_item = (self.dragging_item[0], self.dragging_item[1] - 1)
                    elif player.inventory[slot][0] == self.dragging_item[0]:
                        if player.inventory[slot][1] < 64:
                            player.inventory[slot] = (player.inventory[slot][0], player.inventory[slot][1] + 1)
                            if self.dragging_item[1] <= 1:
                                self.dragging_item = None
                                self.dragging_from = None
                            else:
                                self.dragging_item = (self.dragging_item[0], self.dragging_item[1] - 1)

    def _get_slot_at(self, pos):
        """获取鼠标位置的槽位索引"""
        mx, my = pos

        # 检查快捷栏
        hotbar_start_x = (WINDOW_WIDTH - HOTBAR_SLOTS * (self.SLOT_SIZE + self.SLOT_PADDING)) // 2

        if not self.is_open:
            # 只检查底部快捷栏
            hotbar_y = WINDOW_HEIGHT - self.SLOT_SIZE - 10
            for i in range(HOTBAR_SLOTS):
                slot_x = hotbar_start_x + i * (self.SLOT_SIZE + self.SLOT_PADDING)
                if slot_x <= mx <= slot_x + self.SLOT_SIZE and hotbar_y <= my <= hotbar_y + self.SLOT_SIZE:
                    return i
            return None

        # 背包打开时检查所有槽位
        # 主背包
        for row in range(INVENTORY_ROWS):
            for col in range(INVENTORY_COLS):
                slot_x = self.inv_x + self.SLOT_PADDING + col * (self.SLOT_SIZE + self.SLOT_PADDING)
                slot_y = self.inv_y + 40 + row * (self.SLOT_SIZE + self.SLOT_PADDING)

                if slot_x <= mx <= slot_x + self.SLOT_SIZE and slot_y <= my <= slot_y + self.SLOT_SIZE:
                    return HOTBAR_SLOTS + row * INVENTORY_COLS + col

        # 快捷栏 (在背包底部)
        hotbar_y = self.inv_y + 40 + INVENTORY_ROWS * (self.SLOT_SIZE + self.SLOT_PADDING) + 20
        for i in range(HOTBAR_SLOTS):
            slot_x = self.inv_x + self.SLOT_PADDING + i * (self.SLOT_SIZE + self.SLOT_PADDING)
            if slot_x <= mx <= slot_x + self.SLOT_SIZE and hotbar_y <= my <= hotbar_y + self.SLOT_SIZE:
                return i

        return None

    def draw_hotbar(self, screen, player):
        """绘制快捷栏"""
        self.init_fonts()

        hotbar_start_x = (WINDOW_WIDTH - HOTBAR_SLOTS * (self.SLOT_SIZE + self.SLOT_PADDING)) // 2
        hotbar_y = WINDOW_HEIGHT - self.SLOT_SIZE - 10

        for i in range(HOTBAR_SLOTS):
            slot_x = hotbar_start_x + i * (self.SLOT_SIZE + self.SLOT_PADDING)

            # 槽位背景
            bg_color = (60, 60, 60) if i != player.selected_slot else (100, 100, 100)
            pygame.draw.rect(screen, bg_color, (slot_x, hotbar_y, self.SLOT_SIZE, self.SLOT_SIZE))

            # 选中边框
            border_color = (255, 255, 255) if i == player.selected_slot else (80, 80, 80)
            pygame.draw.rect(screen, border_color, (slot_x, hotbar_y, self.SLOT_SIZE, self.SLOT_SIZE), 2)

            # 物品
            item = player.inventory[i]
            if item is not None:
                self._draw_item(screen, slot_x, hotbar_y, item)

            # 槽位编号
            num_text = self.small_font.render(str(i + 1), True, (200, 200, 200))
            screen.blit(num_text, (slot_x + 3, hotbar_y + 3))

    def draw_inventory(self, screen, player):
        """绘制完整背包界面"""
        if not self.is_open:
            return

        self.init_fonts()

        # 半透明背景
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # 背包窗口
        inv_width = INVENTORY_COLS * (self.SLOT_SIZE + self.SLOT_PADDING) + self.SLOT_PADDING
        inv_height = (INVENTORY_ROWS + 1) * (self.SLOT_SIZE + self.SLOT_PADDING) + self.SLOT_PADDING + 80

        pygame.draw.rect(screen, (50, 50, 50), (self.inv_x, self.inv_y, inv_width, inv_height))
        pygame.draw.rect(screen, (100, 100, 100), (self.inv_x, self.inv_y, inv_width, inv_height), 3)

        # 标题
        title = self.font.render("背包", True, COLORS['white'])
        screen.blit(title, (self.inv_x + 10, self.inv_y + 10))

        # 主背包槽位
        for row in range(INVENTORY_ROWS):
            for col in range(INVENTORY_COLS):
                slot_idx = HOTBAR_SLOTS + row * INVENTORY_COLS + col
                slot_x = self.inv_x + self.SLOT_PADDING + col * (self.SLOT_SIZE + self.SLOT_PADDING)
                slot_y = self.inv_y + 40 + row * (self.SLOT_SIZE + self.SLOT_PADDING)

                self._draw_slot(screen, slot_x, slot_y, player.inventory[slot_idx])

        # 快捷栏
        hotbar_y = self.inv_y + 40 + INVENTORY_ROWS * (self.SLOT_SIZE + self.SLOT_PADDING) + 20
        for i in range(HOTBAR_SLOTS):
            slot_x = self.inv_x + self.SLOT_PADDING + i * (self.SLOT_SIZE + self.SLOT_PADDING)

            bg_color = (70, 70, 70) if i != player.selected_slot else (100, 100, 100)
            pygame.draw.rect(screen, bg_color, (slot_x, hotbar_y, self.SLOT_SIZE, self.SLOT_SIZE))

            border_color = (255, 255, 0) if i == player.selected_slot else (80, 80, 80)
            pygame.draw.rect(screen, border_color, (slot_x, hotbar_y, self.SLOT_SIZE, self.SLOT_SIZE), 2)

            if player.inventory[i] is not None:
                self._draw_item(screen, slot_x, hotbar_y, player.inventory[i])

        # 拖拽物品
        if self.dragging_item is not None:
            mx, my = pygame.mouse.get_pos()
            self._draw_item(screen, mx - self.SLOT_SIZE // 2, my - self.SLOT_SIZE // 2, self.dragging_item)

        # 悬停信息
        mouse_pos = pygame.mouse.get_pos()
        slot = self._get_slot_at(mouse_pos)
        if slot is not None and player.inventory[slot] is not None:
            self._draw_tooltip(screen, mouse_pos, player.inventory[slot])

    def _draw_slot(self, screen, x, y, item):
        """绘制单个槽位"""
        pygame.draw.rect(screen, (60, 60, 60), (x, y, self.SLOT_SIZE, self.SLOT_SIZE))
        pygame.draw.rect(screen, (80, 80, 80), (x, y, self.SLOT_SIZE, self.SLOT_SIZE), 1)

        if item is not None:
            self._draw_item(screen, x, y, item)

    def _draw_item(self, screen, x, y, item):
        """绘制物品"""
        block_type, count = item
        block_data = BLOCK_DATA.get(block_type, {})
        color = block_data.get('color', (128, 128, 128))

        if len(color) == 4:  # RGBA
            color = color[:3]

        # 物品图标
        icon_margin = 8
        pygame.draw.rect(screen, color,
                        (x + icon_margin, y + icon_margin,
                         self.SLOT_SIZE - icon_margin * 2, self.SLOT_SIZE - icon_margin * 2))

        # 数量
        if count > 1:
            count_text = self.small_font.render(str(count), True, COLORS['white'])
            screen.blit(count_text, (x + self.SLOT_SIZE - 15, y + self.SLOT_SIZE - 15))

    def _draw_tooltip(self, screen, pos, item):
        """绘制物品提示"""
        block_type, count = item
        block_data = BLOCK_DATA.get(block_type, {})
        name = block_data.get('name', '未知')

        text = self.font.render(name, True, COLORS['white'])
        text_rect = text.get_rect()

        tooltip_x = pos[0] + 15
        tooltip_y = pos[1] + 15

        # 确保不超出屏幕
        if tooltip_x + text_rect.width + 10 > WINDOW_WIDTH:
            tooltip_x = WINDOW_WIDTH - text_rect.width - 15

        bg_rect = (tooltip_x - 5, tooltip_y - 5, text_rect.width + 10, text_rect.height + 10)
        pygame.draw.rect(screen, (30, 30, 30), bg_rect)
        pygame.draw.rect(screen, (100, 100, 100), bg_rect, 1)
        screen.blit(text, (tooltip_x, tooltip_y))


class CraftingUI:
    """合成界面"""

    def __init__(self):
        self.is_open = False
        self.selected_recipe = None

    def toggle(self):
        self.is_open = not self.is_open

    def can_craft(self, recipe_name, player):
        """检查是否可以合成"""
        if recipe_name not in RECIPES:
            return False

        recipe = RECIPES[recipe_name]
        ingredients = recipe['ingredients']

        for block_type, needed in ingredients.items():
            has = 0
            for slot in player.inventory:
                if slot is not None and slot[0] == block_type:
                    has += slot[1]
            if has < needed:
                return False
        return True

    def craft(self, recipe_name, player):
        """执行合成"""
        if not self.can_craft(recipe_name, player):
            return False

        recipe = RECIPES[recipe_name]
        ingredients = recipe['ingredients']
        result = recipe['result']

        # 消耗材料
        for block_type, needed in ingredients.items():
            remaining = needed
            for i, slot in enumerate(player.inventory):
                if slot is not None and slot[0] == block_type:
                    if slot[1] <= remaining:
                        remaining -= slot[1]
                        player.inventory[i] = None
                    else:
                        player.inventory[i] = (block_type, slot[1] - remaining)
                        remaining = 0
                if remaining <= 0:
                    break

        # 添加产物
        player.add_item(result[0], result[1])
        return True

    def draw(self, screen, player):
        """绘制合成界面"""
        if not self.is_open:
            return

        # TODO: 实现合成界面UI
        pass
