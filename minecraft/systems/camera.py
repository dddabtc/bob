# 摄像机系统
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE, WORLD_WIDTH, CHUNK_HEIGHT


class Camera:
    """游戏摄像机"""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0

        # 世界边界
        self.max_x = WORLD_WIDTH * BLOCK_SIZE - WINDOW_WIDTH
        self.max_y = CHUNK_HEIGHT * BLOCK_SIZE - WINDOW_HEIGHT

        # 平滑跟随参数
        self.smoothness = 0.1

    def follow(self, target_x, target_y, instant=False):
        """跟随目标"""
        # 将目标居中
        self.target_x = target_x - WINDOW_WIDTH // 2
        self.target_y = target_y - WINDOW_HEIGHT // 2

        # 限制边界
        self.target_x = max(0, min(self.target_x, self.max_x))
        self.target_y = max(0, min(self.target_y, self.max_y))

        if instant:
            self.x = self.target_x
            self.y = self.target_y
        else:
            # 平滑跟随
            self.x += (self.target_x - self.x) * self.smoothness
            self.y += (self.target_y - self.y) * self.smoothness

    def get_visible_blocks(self):
        """获取可见的方块范围"""
        start_x = max(0, int(self.x // BLOCK_SIZE) - 1)
        end_x = min(WORLD_WIDTH, int((self.x + WINDOW_WIDTH) // BLOCK_SIZE) + 2)
        start_y = max(0, int(self.y // BLOCK_SIZE) - 1)
        end_y = min(CHUNK_HEIGHT, int((self.y + WINDOW_HEIGHT) // BLOCK_SIZE) + 2)

        return start_x, end_x, start_y, end_y

    def world_to_screen(self, world_x, world_y):
        """世界坐标转屏幕坐标"""
        return (world_x - self.x, world_y - self.y)

    def screen_to_world(self, screen_x, screen_y):
        """屏幕坐标转世界坐标"""
        return (screen_x + self.x, screen_y + self.y)

    def screen_to_block(self, screen_x, screen_y):
        """屏幕坐标转方块坐标"""
        world_x, world_y = self.screen_to_world(screen_x, screen_y)
        return (int(world_x // BLOCK_SIZE), int(world_y // BLOCK_SIZE))
