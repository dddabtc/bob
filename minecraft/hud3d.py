# 3D 游戏 HUD 系统
import pygame
from settings3d import (
    WINDOW_WIDTH, WINDOW_HEIGHT, HOTBAR_SLOTS,
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

    def render(self, screen, player, fps=0, debug=False):
        """渲染HUD"""
        self._render_hotbar(screen, player)
        self._render_crosshair(screen)
        self._render_health(screen, player)

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
        title = self.font.render("游戏暂停", True, (255, 255, 255))
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, WINDOW_HEIGHT // 2 - 60))

        # 提示
        hint = self.small_font.render("按 ESC 继续游戏", True, (200, 200, 200))
        screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, WINDOW_HEIGHT // 2 + 20))

        hint2 = self.small_font.render("按 Q 退出游戏", True, (200, 200, 200))
        screen.blit(hint2, (WINDOW_WIDTH // 2 - hint2.get_width() // 2, WINDOW_HEIGHT // 2 + 60))
