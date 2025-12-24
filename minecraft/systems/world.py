# 世界生成系统
import random
import math
from settings import (
    BlockType, BLOCK_DATA, CHUNK_WIDTH, CHUNK_HEIGHT,
    WORLD_WIDTH, SEA_LEVEL, GROUND_LEVEL, CAVE_THRESHOLD
)


class World:
    """游戏世界管理"""

    def __init__(self, seed=None):
        self.seed = seed if seed is not None else random.randint(0, 999999)
        random.seed(self.seed)

        # 世界数据: blocks[x][y]
        self.blocks = [[BlockType.AIR for _ in range(CHUNK_HEIGHT)] for _ in range(WORLD_WIDTH)]

        # 光照数据
        self.light_map = [[0 for _ in range(CHUNK_HEIGHT)] for _ in range(WORLD_WIDTH)]

        # 生成世界
        self.generate()

    def generate(self):
        """生成完整世界"""
        # 1. 生成地形高度
        heights = self._generate_terrain_heights()

        # 2. 填充基本方块
        self._fill_terrain(heights)

        # 3. 生成洞穴
        self._generate_caves()

        # 4. 生成矿石
        self._generate_ores()

        # 5. 生成树木
        self._generate_trees(heights)

        # 6. 填充水
        self._fill_water()

        # 7. 添加基岩层
        self._add_bedrock()

    def _generate_terrain_heights(self):
        """使用噪声生成地形高度"""
        heights = []

        for x in range(WORLD_WIDTH):
            # 多层噪声叠加
            height = GROUND_LEVEL

            # 大尺度地形
            height += int(self._noise(x * 0.01) * 15)

            # 中等起伏
            height += int(self._noise(x * 0.05 + 100) * 8)

            # 小细节
            height += int(self._noise(x * 0.1 + 200) * 3)

            heights.append(max(20, min(height, CHUNK_HEIGHT - 20)))

        return heights

    def _noise(self, x):
        """简单的Perlin噪声近似"""
        # 使用种子
        x = x + self.seed * 0.01
        return math.sin(x) * 0.5 + math.sin(x * 2.1 + 1) * 0.25 + math.sin(x * 4.3 + 2) * 0.125

    def _fill_terrain(self, heights):
        """填充基本地形"""
        for x in range(WORLD_WIDTH):
            surface_height = heights[x]

            for y in range(CHUNK_HEIGHT):
                if y > surface_height:
                    # 地下
                    depth = y - surface_height
                    if depth <= 3:
                        self.blocks[x][y] = BlockType.DIRT
                    else:
                        self.blocks[x][y] = BlockType.STONE
                elif y == surface_height:
                    # 地表
                    if surface_height < SEA_LEVEL + 2:
                        self.blocks[x][y] = BlockType.SAND
                    else:
                        self.blocks[x][y] = BlockType.GRASS
                # y < surface_height 保持为空气

    def _generate_caves(self):
        """生成洞穴"""
        for x in range(WORLD_WIDTH):
            for y in range(CHUNK_HEIGHT):
                if self.blocks[x][y] == BlockType.STONE:
                    # 洞穴噪声
                    cave_noise = self._cave_noise(x, y)
                    if cave_noise > CAVE_THRESHOLD:
                        self.blocks[x][y] = BlockType.AIR

    def _cave_noise(self, x, y):
        """洞穴噪声"""
        nx = x * 0.05 + self.seed
        ny = y * 0.05

        value = math.sin(nx) * math.cos(ny) * 0.5
        value += math.sin(nx * 2 + 1) * math.cos(ny * 2 + 1) * 0.3
        value += math.sin(nx * 4 + 2) * math.cos(ny * 4 + 2) * 0.2

        return (value + 1) / 2  # 归一化到 0-1

    def _generate_ores(self):
        """生成矿石"""
        ore_configs = [
            (BlockType.COAL_ORE, 0.02, 10, 80),      # 煤矿: 2%几率, 10-80深度
            (BlockType.IRON_ORE, 0.015, 20, 60),    # 铁矿
            (BlockType.GOLD_ORE, 0.008, 30, 50),    # 金矿
            (BlockType.DIAMOND_ORE, 0.003, 40, 55), # 钻石
        ]

        for x in range(WORLD_WIDTH):
            for y in range(CHUNK_HEIGHT):
                if self.blocks[x][y] == BlockType.STONE:
                    for ore_type, chance, min_depth, max_depth in ore_configs:
                        # 计算深度 (从底部算)
                        depth = CHUNK_HEIGHT - y
                        if min_depth <= depth <= max_depth:
                            if random.random() < chance:
                                self.blocks[x][y] = ore_type
                                break

    def _generate_trees(self, heights):
        """生成树木"""
        last_tree_x = -10

        for x in range(5, WORLD_WIDTH - 5):
            surface_y = heights[x]

            # 只在草方块上生成树
            if self.blocks[x][surface_y] != BlockType.GRASS:
                continue

            # 保持树间距
            if x - last_tree_x < 5:
                continue

            # 随机生成
            if random.random() < 0.08:
                self._place_tree(x, surface_y - 1)
                last_tree_x = x

    def _place_tree(self, x, base_y):
        """放置一棵树"""
        trunk_height = random.randint(4, 6)

        # 树干
        for i in range(trunk_height):
            if 0 <= base_y - i < CHUNK_HEIGHT:
                self.blocks[x][base_y - i] = BlockType.WOOD

        # 树叶
        leaf_start = base_y - trunk_height + 1
        leaf_size = 2

        for dy in range(-2, 2):
            for dx in range(-leaf_size, leaf_size + 1):
                if abs(dx) + abs(dy) <= leaf_size + 1:
                    lx, ly = x + dx, leaf_start + dy
                    if 0 <= lx < WORLD_WIDTH and 0 <= ly < CHUNK_HEIGHT:
                        if self.blocks[lx][ly] == BlockType.AIR:
                            self.blocks[lx][ly] = BlockType.LEAVES

    def _fill_water(self):
        """填充水"""
        for x in range(WORLD_WIDTH):
            for y in range(CHUNK_HEIGHT):
                if y < SEA_LEVEL and self.blocks[x][y] == BlockType.AIR:
                    self.blocks[x][y] = BlockType.WATER

    def _add_bedrock(self):
        """添加基岩层"""
        for x in range(WORLD_WIDTH):
            # 底部5层基岩
            for y in range(CHUNK_HEIGHT - 5, CHUNK_HEIGHT):
                if random.random() < 0.7 or y == CHUNK_HEIGHT - 1:
                    self.blocks[x][y] = BlockType.BEDROCK

    def get_block(self, x, y):
        """获取方块类型"""
        if 0 <= x < WORLD_WIDTH and 0 <= y < CHUNK_HEIGHT:
            return self.blocks[x][y]
        return BlockType.AIR

    def set_block(self, x, y, block_type):
        """设置方块"""
        if 0 <= x < WORLD_WIDTH and 0 <= y < CHUNK_HEIGHT:
            self.blocks[x][y] = block_type
            return True
        return False

    def is_solid(self, x, y):
        """检查方块是否为固体"""
        block = self.get_block(x, y)
        return BLOCK_DATA.get(block, {}).get('solid', False)

    def find_spawn_point(self):
        """找到合适的出生点"""
        # 从世界中央开始找
        start_x = WORLD_WIDTH // 2

        for offset in range(50):
            for x in [start_x + offset, start_x - offset]:
                if 0 <= x < WORLD_WIDTH:
                    # 从上往下找第一个固体方块
                    for y in range(CHUNK_HEIGHT):
                        if self.is_solid(x, y):
                            # 确保上方有空间
                            if (not self.is_solid(x, y-1) and
                                not self.is_solid(x, y-2)):
                                return (x, y - 2)

        return (WORLD_WIDTH // 2, GROUND_LEVEL - 2)

    def get_surface_height(self, x):
        """获取地表高度"""
        for y in range(CHUNK_HEIGHT):
            if self.is_solid(x, y):
                return y
        return CHUNK_HEIGHT - 1
