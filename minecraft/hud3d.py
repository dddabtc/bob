# 3D 游戏 HUD 系统
import pygame
from settings3d import (
    WINDOW_WIDTH, WINDOW_HEIGHT, HOTBAR_SLOTS,
    INVENTORY_ROWS, INVENTORY_COLS,
    BlockType, BLOCK_DATA, BLOCK_COLORS
)


class HUD:
    """游戏界面HUD"""

    SLOT_SIZE = 50
    SLOT_PADDING = 4

    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 20)
        self.large_font = pygame.font.Font(None, 48)

    def render(self, screen, player, fps=0, debug=False, world=None):
        """渲染HUD"""
        self._render_hotbar(screen, player)
        self._render_crosshair(screen)
        self._render_health(screen, player)

        # One Block 模式显示挖掘次数
        if world and world.one_block_mode:
            self._render_one_block_info(screen, world)

        if debug:
            self._render_debug(screen, player, fps)

    def _render_crosshair(self, screen):
        """渲染准星"""
        cx = WINDOW_WIDTH // 2
        cy = WINDOW_HEIGHT // 2
        size = 12
        thickness = 2
        gap = 4

        color = (255, 255, 255)
        shadow = (50, 50, 50)

        # 阴影
        pygame.draw.line(screen, shadow, (cx - size + 1, cy + 1), (cx - gap + 1, cy + 1), thickness)
        pygame.draw.line(screen, shadow, (cx + gap + 1, cy + 1), (cx + size + 1, cy + 1), thickness)
        pygame.draw.line(screen, shadow, (cx + 1, cy - size + 1), (cx + 1, cy - gap + 1), thickness)
        pygame.draw.line(screen, shadow, (cx + 1, cy + gap + 1), (cx + 1, cy + size + 1), thickness)

        # 准星
        pygame.draw.line(screen, color, (cx - size, cy), (cx - gap, cy), thickness)
        pygame.draw.line(screen, color, (cx + gap, cy), (cx + size, cy), thickness)
        pygame.draw.line(screen, color, (cx, cy - size), (cx, cy - gap), thickness)
        pygame.draw.line(screen, color, (cx, cy + gap), (cx, cy + size), thickness)

    def _render_hotbar(self, screen, player):
        """渲染快捷栏"""
        hotbar_width = HOTBAR_SLOTS * (self.SLOT_SIZE + self.SLOT_PADDING) + self.SLOT_PADDING
        start_x = (WINDOW_WIDTH - hotbar_width) // 2
        y = WINDOW_HEIGHT - self.SLOT_SIZE - 20

        # 背景
        bg_rect = (start_x - 5, y - 5, hotbar_width + 10, self.SLOT_SIZE + 10)
        s = pygame.Surface((bg_rect[2], bg_rect[3]), pygame.SRCALPHA)
        s.fill((30, 30, 30, 180))
        screen.blit(s, (bg_rect[0], bg_rect[1]))
        pygame.draw.rect(screen, (60, 60, 60), bg_rect, 2)

        for i in range(HOTBAR_SLOTS):
            slot_x = start_x + self.SLOT_PADDING + i * (self.SLOT_SIZE + self.SLOT_PADDING)

            # 槽位背景
            if i == player.selected_slot:
                pygame.draw.rect(screen, (100, 100, 100), (slot_x, y, self.SLOT_SIZE, self.SLOT_SIZE))
                pygame.draw.rect(screen, (255, 255, 255), (slot_x, y, self.SLOT_SIZE, self.SLOT_SIZE), 3)
            else:
                pygame.draw.rect(screen, (50, 50, 50), (slot_x, y, self.SLOT_SIZE, self.SLOT_SIZE))
                pygame.draw.rect(screen, (80, 80, 80), (slot_x, y, self.SLOT_SIZE, self.SLOT_SIZE), 1)

            # 物品
            item = player.inventory[i]
            if item is not None:
                self._render_item(screen, slot_x, y, item)

            # 快捷键数字
            num = self.small_font.render(str(i + 1), True, (180, 180, 180))
            screen.blit(num, (slot_x + 3, y + 3))

    def _render_item(self, screen, x, y, item):
        """渲染背包物品"""
        block_type, count = item

        # 获取方块颜色
        block_colors = BLOCK_COLORS.get(block_type, {'all': (0.5, 0.5, 0.5)})
        if 'all' in block_colors:
            color = block_colors['all']
        else:
            color = block_colors.get('top', (0.5, 0.5, 0.5))

        # 转换为0-255
        r = int(color[0] * 255)
        g = int(color[1] * 255)
        b = int(color[2] * 255)

        # 绘制3D方块效果
        margin = 8
        size = self.SLOT_SIZE - margin * 2

        # 顶面 (亮)
        top_color = (min(r + 40, 255), min(g + 40, 255), min(b + 40, 255))
        points = [
            (x + margin + size // 4, y + margin),
            (x + margin + size, y + margin + size // 4),
            (x + margin + size * 3 // 4, y + margin + size // 2),
            (x + margin, y + margin + size // 4)
        ]
        pygame.draw.polygon(screen, top_color, points)

        # 右面
        right_color = (max(r - 20, 0), max(g - 20, 0), max(b - 20, 0))
        points = [
            (x + margin + size, y + margin + size // 4),
            (x + margin + size, y + margin + size),
            (x + margin + size * 3 // 4, y + margin + size + size // 4),
            (x + margin + size * 3 // 4, y + margin + size // 2)
        ]
        pygame.draw.polygon(screen, right_color, points)

        # 前面
        front_color = (r, g, b)
        points = [
            (x + margin, y + margin + size // 4),
            (x + margin + size * 3 // 4, y + margin + size // 2),
            (x + margin + size * 3 // 4, y + margin + size + size // 4),
            (x + margin, y + margin + size)
        ]
        pygame.draw.polygon(screen, front_color, points)

        # 数量
        if count > 1:
            count_text = self.small_font.render(str(count), True, (255, 255, 255))
            # 阴影
            shadow = self.small_font.render(str(count), True, (30, 30, 30))
            screen.blit(shadow, (x + self.SLOT_SIZE - 14, y + self.SLOT_SIZE - 16))
            screen.blit(count_text, (x + self.SLOT_SIZE - 15, y + self.SLOT_SIZE - 17))

    def _render_health(self, screen, player):
        """渲染生命值"""
        x = 20
        y = WINDOW_HEIGHT - 90
        heart_size = 18
        spacing = 20

        for i in range(10):
            hx = x + i * spacing
            # 空心
            pygame.draw.polygon(screen, (80, 20, 20), self._heart_points(hx, y, heart_size))

            # 填充
            if player.health > i * 2:
                fill = min(1.0, (player.health - i * 2) / 2)
                if fill >= 1:
                    pygame.draw.polygon(screen, (220, 50, 50), self._heart_points(hx, y, heart_size))
                elif fill > 0:
                    pygame.draw.polygon(screen, (180, 40, 40), self._heart_points(hx, y, heart_size * 0.7))

    def _heart_points(self, x, y, size):
        """心形顶点"""
        return [
            (x, y + size * 0.3),
            (x + size * 0.25, y),
            (x + size * 0.5, y + size * 0.2),
            (x + size * 0.75, y),
            (x + size, y + size * 0.3),
            (x + size * 0.5, y + size),
        ]

    def _render_one_block_info(self, screen, world):
        """渲染 One Block 模式信息"""
        # 阶段名称
        if world.blocks_mined < 20:
            phase_name = "Phase 1: Basic"
        elif world.blocks_mined < 50:
            phase_name = "Phase 2: Wood"
        elif world.blocks_mined < 100:
            phase_name = "Phase 3: Ores"
        elif world.blocks_mined < 200:
            phase_name = "Phase 4: Rare"
        else:
            phase_name = "Phase 5: Ultimate"

        # 显示在右上角
        text = self.font.render(f"ONE BLOCK", True, (255, 220, 100))
        screen.blit(text, (WINDOW_WIDTH - text.get_width() - 15, 10))

        text2 = self.small_font.render(f"Blocks: {world.blocks_mined}", True, (255, 255, 255))
        screen.blit(text2, (WINDOW_WIDTH - text2.get_width() - 15, 38))

        text3 = self.small_font.render(phase_name, True, (200, 200, 200))
        screen.blit(text3, (WINDOW_WIDTH - text3.get_width() - 15, 56))

    def _render_debug(self, screen, player, fps):
        """渲染调试信息"""
        lines = [
            f"FPS: {fps:.0f}",
            f"XYZ: {player.x:.1f} / {player.y:.1f} / {player.z:.1f}",
            f"Yaw: {player.yaw:.2f}  Pitch: {player.pitch:.2f}",
            f"Velocity: {player.vx:.1f} / {player.vy:.1f} / {player.vz:.1f}",
            f"On Ground: {player.on_ground}",
            f"In Water: {player.in_water}",
        ]

        y = 10
        for line in lines:
            # 阴影
            shadow = self.font.render(line, True, (30, 30, 30))
            screen.blit(shadow, (12, y + 2))
            # 文字
            text = self.font.render(line, True, (255, 255, 255))
            screen.blit(text, (10, y))
            y += 28

    def render_mining_progress(self, screen, progress):
        """渲染挖掘进度"""
        if progress <= 0:
            return

        cx = WINDOW_WIDTH // 2
        cy = WINDOW_HEIGHT // 2 + 50

        bar_width = 100
        bar_height = 8

        # 背景
        pygame.draw.rect(screen, (50, 50, 50),
                        (cx - bar_width // 2, cy, bar_width, bar_height))
        # 进度
        pygame.draw.rect(screen, (100, 200, 100),
                        (cx - bar_width // 2, cy, int(bar_width * progress), bar_height))
        # 边框
        pygame.draw.rect(screen, (100, 100, 100),
                        (cx - bar_width // 2, cy, bar_width, bar_height), 1)


class InventoryScreen:
    """背包界面"""

    SLOT_SIZE = 50
    SLOT_PADDING = 4

    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 40)

        # 拖拽状态
        self.dragging = None  # (slot_index, item)
        self.drag_pos = (0, 0)

    def render(self, screen, player):
        """渲染背包界面"""
        # 半透明背景
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # 背包窗口
        inv_width = INVENTORY_COLS * (self.SLOT_SIZE + self.SLOT_PADDING) + self.SLOT_PADDING + 20
        inv_height = (INVENTORY_ROWS + 2) * (self.SLOT_SIZE + self.SLOT_PADDING) + 80
        inv_x = (WINDOW_WIDTH - inv_width) // 2
        inv_y = (WINDOW_HEIGHT - inv_height) // 2

        # 背景面板
        pygame.draw.rect(screen, (60, 60, 60), (inv_x, inv_y, inv_width, inv_height))
        pygame.draw.rect(screen, (100, 100, 100), (inv_x, inv_y, inv_width, inv_height), 3)

        # 标题
        title = self.title_font.render("Inventory", True, (255, 255, 255))
        screen.blit(title, (inv_x + (inv_width - title.get_width()) // 2, inv_y + 10))

        # 主背包格子 (3行9列)
        start_y = inv_y + 50
        for row in range(INVENTORY_ROWS):
            for col in range(INVENTORY_COLS):
                slot_idx = HOTBAR_SLOTS + row * INVENTORY_COLS + col
                slot_x = inv_x + 10 + col * (self.SLOT_SIZE + self.SLOT_PADDING)
                slot_y = start_y + row * (self.SLOT_SIZE + self.SLOT_PADDING)
                self._render_slot(screen, slot_x, slot_y, player.inventory[slot_idx], slot_idx == player.selected_slot)

        # 分隔线
        sep_y = start_y + INVENTORY_ROWS * (self.SLOT_SIZE + self.SLOT_PADDING) + 10
        pygame.draw.line(screen, (100, 100, 100), (inv_x + 10, sep_y), (inv_x + inv_width - 10, sep_y), 2)

        # 快捷栏标签
        hotbar_label = self.small_font.render("Hotbar", True, (180, 180, 180))
        screen.blit(hotbar_label, (inv_x + 10, sep_y + 5))

        # 快捷栏格子
        hotbar_y = sep_y + 25
        for i in range(HOTBAR_SLOTS):
            slot_x = inv_x + 10 + i * (self.SLOT_SIZE + self.SLOT_PADDING)
            self._render_slot(screen, slot_x, hotbar_y, player.inventory[i], i == player.selected_slot)

        # 拖拽物品
        if self.dragging:
            mx, my = pygame.mouse.get_pos()
            self._render_item_at(screen, mx - self.SLOT_SIZE // 2, my - self.SLOT_SIZE // 2, self.dragging[1])

        # 提示
        hint = self.small_font.render("E / ESC to close  |  Click to move items", True, (150, 150, 150))
        screen.blit(hint, (inv_x + (inv_width - hint.get_width()) // 2, inv_y + inv_height - 25))

    def _render_slot(self, screen, x, y, item, selected=False):
        """渲染单个槽位"""
        # 背景
        if selected:
            pygame.draw.rect(screen, (100, 100, 100), (x, y, self.SLOT_SIZE, self.SLOT_SIZE))
            pygame.draw.rect(screen, (255, 255, 255), (x, y, self.SLOT_SIZE, self.SLOT_SIZE), 2)
        else:
            pygame.draw.rect(screen, (40, 40, 40), (x, y, self.SLOT_SIZE, self.SLOT_SIZE))
            pygame.draw.rect(screen, (80, 80, 80), (x, y, self.SLOT_SIZE, self.SLOT_SIZE), 1)

        # 物品
        if item:
            self._render_item_at(screen, x, y, item)

    def _render_item_at(self, screen, x, y, item):
        """在指定位置渲染物品"""
        block_type, count = item

        # 获取方块颜色
        block_colors = BLOCK_COLORS.get(block_type, {'all': (0.5, 0.5, 0.5)})
        if 'all' in block_colors:
            color = block_colors['all']
        else:
            color = block_colors.get('top', (0.5, 0.5, 0.5))

        r = int(color[0] * 255)
        g = int(color[1] * 255)
        b = int(color[2] * 255)

        # 3D方块效果
        margin = 8
        size = self.SLOT_SIZE - margin * 2

        # 顶面
        top_color = (min(r + 40, 255), min(g + 40, 255), min(b + 40, 255))
        points = [
            (x + margin + size // 4, y + margin),
            (x + margin + size, y + margin + size // 4),
            (x + margin + size * 3 // 4, y + margin + size // 2),
            (x + margin, y + margin + size // 4)
        ]
        pygame.draw.polygon(screen, top_color, points)

        # 右面
        right_color = (max(r - 20, 0), max(g - 20, 0), max(b - 20, 0))
        points = [
            (x + margin + size, y + margin + size // 4),
            (x + margin + size, y + margin + size),
            (x + margin + size * 3 // 4, y + margin + size + size // 4),
            (x + margin + size * 3 // 4, y + margin + size // 2)
        ]
        pygame.draw.polygon(screen, right_color, points)

        # 前面
        front_color = (r, g, b)
        points = [
            (x + margin, y + margin + size // 4),
            (x + margin + size * 3 // 4, y + margin + size // 2),
            (x + margin + size * 3 // 4, y + margin + size + size // 4),
            (x + margin, y + margin + size)
        ]
        pygame.draw.polygon(screen, front_color, points)

        # 数量
        if count > 1:
            count_text = self.small_font.render(str(count), True, (255, 255, 255))
            shadow = self.small_font.render(str(count), True, (30, 30, 30))
            screen.blit(shadow, (x + self.SLOT_SIZE - 14, y + self.SLOT_SIZE - 16))
            screen.blit(count_text, (x + self.SLOT_SIZE - 15, y + self.SLOT_SIZE - 17))

    def get_slot_at(self, mx, my):
        """获取鼠标位置的槽位索引"""
        inv_width = INVENTORY_COLS * (self.SLOT_SIZE + self.SLOT_PADDING) + self.SLOT_PADDING + 20
        inv_height = (INVENTORY_ROWS + 2) * (self.SLOT_SIZE + self.SLOT_PADDING) + 80
        inv_x = (WINDOW_WIDTH - inv_width) // 2
        inv_y = (WINDOW_HEIGHT - inv_height) // 2

        # 主背包
        start_y = inv_y + 50
        for row in range(INVENTORY_ROWS):
            for col in range(INVENTORY_COLS):
                slot_idx = HOTBAR_SLOTS + row * INVENTORY_COLS + col
                slot_x = inv_x + 10 + col * (self.SLOT_SIZE + self.SLOT_PADDING)
                slot_y = start_y + row * (self.SLOT_SIZE + self.SLOT_PADDING)
                if slot_x <= mx < slot_x + self.SLOT_SIZE and slot_y <= my < slot_y + self.SLOT_SIZE:
                    return slot_idx

        # 快捷栏
        sep_y = start_y + INVENTORY_ROWS * (self.SLOT_SIZE + self.SLOT_PADDING) + 10
        hotbar_y = sep_y + 25
        for i in range(HOTBAR_SLOTS):
            slot_x = inv_x + 10 + i * (self.SLOT_SIZE + self.SLOT_PADDING)
            if slot_x <= mx < slot_x + self.SLOT_SIZE and hotbar_y <= my < hotbar_y + self.SLOT_SIZE:
                return i

        return None

    def handle_click(self, mx, my, player):
        """处理点击"""
        slot = self.get_slot_at(mx, my)
        if slot is None:
            # 点击空白处，取消拖拽
            if self.dragging:
                # 把物品放回原位
                orig_slot, item = self.dragging
                if player.inventory[orig_slot] is None:
                    player.inventory[orig_slot] = item
                else:
                    # 尝试合并或找空位
                    player.add_item(item[0], item[1])
                self.dragging = None
            return

        if self.dragging:
            # 放下物品
            orig_slot, drag_item = self.dragging
            target_item = player.inventory[slot]

            if target_item is None:
                # 空槽，直接放下
                player.inventory[slot] = drag_item
                self.dragging = None
            elif target_item[0] == drag_item[0]:
                # 同类物品，尝试合并
                total = target_item[1] + drag_item[1]
                if total <= 64:
                    player.inventory[slot] = (target_item[0], total)
                    self.dragging = None
                else:
                    player.inventory[slot] = (target_item[0], 64)
                    self.dragging = (orig_slot, (drag_item[0], total - 64))
            else:
                # 交换
                player.inventory[slot] = drag_item
                self.dragging = (slot, target_item)
        else:
            # 拾起物品
            if player.inventory[slot] is not None:
                self.dragging = (slot, player.inventory[slot])
                player.inventory[slot] = None


class PauseMenu:
    """暂停菜单"""

    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)

    def render(self, screen):
        """渲染暂停菜单"""
        # 半透明覆盖
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # 标题
        title = self.font.render("PAUSED", True, (255, 255, 255))
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, WINDOW_HEIGHT // 2 - 60))

        # 提示
        hint = self.small_font.render("Press ESC to continue", True, (200, 200, 200))
        screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, WINDOW_HEIGHT // 2 + 20))

        hint2 = self.small_font.render("Press Q to quit", True, (200, 200, 200))
        screen.blit(hint2, (WINDOW_WIDTH // 2 - hint2.get_width() // 2, WINDOW_HEIGHT // 2 + 60))
