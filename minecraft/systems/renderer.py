# 渲染系统
import pygame
from settings import (
    BLOCK_SIZE, BlockType, BLOCK_DATA, COLORS,
    WINDOW_WIDTH, WINDOW_HEIGHT, CHUNK_HEIGHT
)


class Renderer:
    """游戏渲染器"""

    def __init__(self):
        self.block_surfaces = {}
        self._create_block_surfaces()

        # 天空渐变缓存
        self.sky_surface = None
        self._create_sky()

    def _create_block_surfaces(self):
        """预创建方块表面"""
        for block_type, data in BLOCK_DATA.items():
            if data['color'] is None:
                continue

            surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
            color = data['color']

            # 基础颜色
            if len(color) == 4:  # RGBA
                surface.fill(color)
            else:
                surface.fill(color)

            # 添加边框效果
            if block_type not in [BlockType.WATER, BlockType.AIR]:
                # 高光
                lighter = tuple(min(c + 30, 255) for c in color[:3])
                pygame.draw.line(surface, lighter, (0, 0), (BLOCK_SIZE - 1, 0), 1)
                pygame.draw.line(surface, lighter, (0, 0), (0, BLOCK_SIZE - 1), 1)

                # 阴影
                darker = tuple(max(c - 40, 0) for c in color[:3])
                pygame.draw.line(surface, darker, (0, BLOCK_SIZE - 1), (BLOCK_SIZE - 1, BLOCK_SIZE - 1), 1)
                pygame.draw.line(surface, darker, (BLOCK_SIZE - 1, 0), (BLOCK_SIZE - 1, BLOCK_SIZE - 1), 1)

            # 特殊方块处理
            if block_type == BlockType.GRASS:
                top_color = data.get('top_color', color)
                pygame.draw.rect(surface, top_color, (1, 0, BLOCK_SIZE - 2, 4))

            elif block_type == BlockType.WOOD:
                # 木纹
                bark_color = tuple(max(c - 20, 0) for c in color[:3])
                for i in range(0, BLOCK_SIZE, 8):
                    pygame.draw.line(surface, bark_color, (0, i), (BLOCK_SIZE, i), 1)

            elif block_type in [BlockType.COAL_ORE, BlockType.IRON_ORE, BlockType.GOLD_ORE, BlockType.DIAMOND_ORE]:
                # 矿石斑点
                ore_colors = {
                    BlockType.COAL_ORE: (30, 30, 30),
                    BlockType.IRON_ORE: (200, 180, 160),
                    BlockType.GOLD_ORE: (255, 215, 0),
                    BlockType.DIAMOND_ORE: (100, 255, 255),
                }
                ore_color = ore_colors.get(block_type, (255, 255, 255))
                spots = [(6, 6), (20, 8), (10, 20), (24, 22), (16, 14)]
                for sx, sy in spots:
                    pygame.draw.rect(surface, ore_color, (sx, sy, 4, 4))

            elif block_type == BlockType.LEAVES:
                # 树叶纹理
                surface.set_alpha(220)

            elif block_type == BlockType.WATER:
                surface.set_alpha(180)

            elif block_type == BlockType.TORCH:
                # 火把
                surface.fill((0, 0, 0, 0))
                pygame.draw.rect(surface, (139, 90, 43), (12, 16, 8, 16))  # 木柄
                pygame.draw.circle(surface, (255, 200, 50), (16, 12), 6)  # 火焰
                pygame.draw.circle(surface, (255, 255, 200), (16, 10), 3)  # 亮心

            elif block_type == BlockType.TNT:
                # TNT
                pygame.draw.rect(surface, (200, 50, 50), (0, 0, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(surface, (255, 255, 255), (4, 10, BLOCK_SIZE - 8, 12))
                # 简单的 TNT 字样
                pygame.draw.rect(surface, (0, 0, 0), (8, 12, 4, 8))
                pygame.draw.rect(surface, (0, 0, 0), (14, 12, 4, 8))
                pygame.draw.rect(surface, (0, 0, 0), (20, 12, 4, 8))

            elif block_type == BlockType.CRAFTING_TABLE:
                # 工作台顶部
                pygame.draw.rect(surface, (100, 60, 30), (0, 0, BLOCK_SIZE, 6))
                pygame.draw.line(surface, (80, 50, 25), (BLOCK_SIZE // 2, 0), (BLOCK_SIZE // 2, 6), 2)
                pygame.draw.line(surface, (80, 50, 25), (0, 3), (BLOCK_SIZE, 3), 1)

            elif block_type == BlockType.FURNACE:
                # 熔炉前面
                pygame.draw.rect(surface, (60, 60, 60), (8, 12, 16, 16))  # 炉口
                pygame.draw.rect(surface, (40, 40, 40), (10, 14, 12, 12))  # 内部

            self.block_surfaces[block_type] = surface

    def _create_sky(self):
        """创建天空渐变"""
        self.sky_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        # 渐变天空
        for y in range(WINDOW_HEIGHT):
            ratio = y / WINDOW_HEIGHT
            r = int(135 * (1 - ratio * 0.3))
            g = int(206 * (1 - ratio * 0.2))
            b = int(235 * (1 - ratio * 0.1))
            pygame.draw.line(self.sky_surface, (r, g, b), (0, y), (WINDOW_WIDTH, y))

    def render(self, screen, world, camera, player):
        """渲染一帧"""
        # 天空背景
        screen.blit(self.sky_surface, (0, 0))

        # 获取可见区域
        start_x, end_x, start_y, end_y = camera.get_visible_blocks()

        # 渲染方块 (分层渲染: 先不透明, 后透明)
        transparent_blocks = []

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                block_type = world.get_block(x, y)
                if block_type == BlockType.AIR:
                    continue

                data = BLOCK_DATA.get(block_type, {})
                screen_x = x * BLOCK_SIZE - camera.x
                screen_y = y * BLOCK_SIZE - camera.y

                if data.get('transparent', False):
                    transparent_blocks.append((block_type, screen_x, screen_y))
                else:
                    self._draw_block(screen, block_type, screen_x, screen_y)

        # 渲染透明方块
        for block_type, screen_x, screen_y in transparent_blocks:
            self._draw_block(screen, block_type, screen_x, screen_y)

        # 渲染玩家
        player.draw(screen, camera)

        # 渲染方块选择框
        self._draw_block_selection(screen, camera, player)

    def _draw_block(self, screen, block_type, x, y):
        """绘制单个方块"""
        if block_type in self.block_surfaces:
            screen.blit(self.block_surfaces[block_type], (x, y))

    def _draw_block_selection(self, screen, camera, player):
        """绘制方块选择框"""
        mouse_pos = pygame.mouse.get_pos()
        bx, by = camera.screen_to_block(mouse_pos[0], mouse_pos[1])

        # 检查是否在范围内
        from settings import MINING_RANGE
        if player.can_reach_block(bx, by, MINING_RANGE):
            screen_x = bx * BLOCK_SIZE - camera.x
            screen_y = by * BLOCK_SIZE - camera.y

            # 绘制选择框
            pygame.draw.rect(screen, (255, 255, 255),
                           (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 2)

    def draw_debug_info(self, screen, player, world, camera, fps):
        """绘制调试信息"""
        font = pygame.font.Font(None, 24)

        info_lines = [
            f"FPS: {fps:.0f}",
            f"Pos: ({player.x / BLOCK_SIZE:.1f}, {player.y / BLOCK_SIZE:.1f})",
            f"Block: {player.get_block_pos()}",
            f"Velocity: ({player.vx:.1f}, {player.vy:.1f})",
            f"On Ground: {player.on_ground}",
            f"Seed: {world.seed}",
        ]

        y = 10
        for line in info_lines:
            text = font.render(line, True, COLORS['white'])
            # 阴影
            shadow = font.render(line, True, COLORS['black'])
            screen.blit(shadow, (12, y + 2))
            screen.blit(text, (10, y))
            y += 22

    def draw_health_bar(self, screen, player):
        """绘制生命值条"""
        bar_width = 200
        bar_height = 20
        x = 10
        y = WINDOW_HEIGHT - 80

        # 背景
        pygame.draw.rect(screen, (40, 40, 40), (x, y, bar_width, bar_height))

        # 生命值
        health_width = int(bar_width * player.health / player.max_health)
        pygame.draw.rect(screen, (200, 50, 50), (x, y, health_width, bar_height))

        # 边框
        pygame.draw.rect(screen, (100, 100, 100), (x, y, bar_width, bar_height), 2)

        # 文字
        font = pygame.font.Font(None, 20)
        text = font.render(f"{player.health}/{player.max_health}", True, COLORS['white'])
        screen.blit(text, (x + bar_width // 2 - text.get_width() // 2, y + 3))
