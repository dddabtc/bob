# Minecraft 2D 主游戏文件
import pygame
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE,
    BLOCK_SIZE, BlockType, COLORS
)
from systems.world import World
from systems.camera import Camera
from systems.renderer import Renderer
from systems.inventory import InventoryUI, CraftingUI
from entities.player import Player


class Game:
    """Minecraft 2D 游戏主类"""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

        # 字体
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # 显示加载画面
        self._show_loading_screen("正在生成世界...")

        # 生成世界
        self.world = World()

        # 创建玩家
        spawn_x, spawn_y = self.world.find_spawn_point()
        self.player = Player(spawn_x, spawn_y)

        # 摄像机
        self.camera = Camera()
        self.camera.follow(self.player.x, self.player.y, instant=True)

        # 渲染器
        self.renderer = Renderer()

        # UI
        self.inventory_ui = InventoryUI()
        self.crafting_ui = CraftingUI()

        # 调试模式
        self.debug_mode = False

        # 游戏时间
        self.game_time = 0

    def _show_loading_screen(self, message):
        """显示加载画面"""
        self.screen.fill((30, 30, 30))

        # 标题
        title = self.font.render("Minecraft 2D", True, COLORS['white'])
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, WINDOW_HEIGHT // 2 - 50))

        # 加载信息
        text = self.small_font.render(message, True, (200, 200, 200))
        self.screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 + 20))

        pygame.display.flip()

    def run(self):
        """主游戏循环"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # 转换为秒

            self._handle_events()

            if not self.paused and not self.inventory_ui.is_open:
                self._update(dt)

            self._render()

        pygame.quit()
        sys.exit()

    def _handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mousedown(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouseup(event)

            # 背包事件
            self.inventory_ui.handle_event(event, self.player)

    def _handle_keydown(self, event):
        """处理按键按下"""
        if event.key == pygame.K_ESCAPE:
            if self.inventory_ui.is_open:
                self.inventory_ui.toggle()
            else:
                self.paused = not self.paused

        elif event.key == pygame.K_F3:
            self.debug_mode = not self.debug_mode

        elif event.key == pygame.K_e:
            self.inventory_ui.toggle()

        elif event.key == pygame.K_c:
            self.crafting_ui.toggle()

        # 快捷栏数字键在 inventory_ui 中处理

    def _handle_mousedown(self, event):
        """处理鼠标按下"""
        if self.inventory_ui.is_open:
            return

        mouse_pos = pygame.mouse.get_pos()
        bx, by = self.camera.screen_to_block(mouse_pos[0], mouse_pos[1])

        if event.button == 1:  # 左键 - 挖掘
            self.player.start_mining(bx, by, self.world)

        elif event.button == 3:  # 右键 - 放置
            self.player.place_block(bx, by, self.world)

    def _handle_mouseup(self, event):
        """处理鼠标释放"""
        if event.button == 1:
            self.player.stop_mining()

    def _update(self, dt):
        """更新游戏状态"""
        self.game_time += dt

        # 获取按键状态
        keys = pygame.key.get_pressed()

        # 更新玩家
        self.player.update(self.world, keys)

        # 持续挖掘
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and self.player.is_mining:
            drops = self.player.update_mining(self.world, dt)
            if drops:
                for block_type, count in drops:
                    self.player.add_item(block_type, count)

        # 更新摄像机
        self.camera.follow(self.player.x + self.player.width // 2,
                          self.player.y + self.player.height // 2)

    def _render(self):
        """渲染画面"""
        # 渲染世界和玩家
        self.renderer.render(self.screen, self.world, self.camera, self.player)

        # 渲染生命值
        self.renderer.draw_health_bar(self.screen, self.player)

        # 渲染快捷栏
        self.inventory_ui.draw_hotbar(self.screen, self.player)

        # 渲染背包 (如果打开)
        self.inventory_ui.draw_inventory(self.screen, self.player)

        # 渲染合成界面 (如果打开)
        self.crafting_ui.draw(self.screen, self.player)

        # 调试信息
        if self.debug_mode:
            fps = self.clock.get_fps()
            self.renderer.draw_debug_info(self.screen, self.player, self.world, self.camera, fps)

        # 暂停画面
        if self.paused:
            self._draw_pause_screen()

        pygame.display.flip()

    def _draw_pause_screen(self):
        """绘制暂停画面"""
        # 半透明覆盖
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # 暂停文字
        text = self.font.render("游戏暂停", True, COLORS['white'])
        self.screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - 50))

        hint = self.small_font.render("按 ESC 继续", True, (200, 200, 200))
        self.screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, WINDOW_HEIGHT // 2 + 20))


def main():
    """游戏入口"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
