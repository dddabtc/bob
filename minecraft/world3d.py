# 3D 世界生成系统
import random
import math
from settings3d import (
    BlockType, BLOCK_DATA, CHUNK_SIZE, WORLD_HEIGHT,
    SEA_LEVEL, GROUND_LEVEL, RENDER_DISTANCE
)


def noise2d(x, z, seed=0, octaves=4, persistence=0.5):
    """2D Perlin噪声近似"""
    total = 0
    frequency = 1
    amplitude = 1
    max_value = 0

    for _ in range(octaves):
        # 简单的噪声函数
        nx = x * frequency * 0.01 + seed
        nz = z * frequency * 0.01 + seed * 0.7

        value = math.sin(nx * 1.5) * math.cos(nz * 1.5)
        value += math.sin(nx * 0.5 + nz * 0.3) * 0.5
        value += math.cos(nx * 2.1 - nz * 1.3) * 0.25

        total += value * amplitude
        max_value += amplitude
        amplitude *= persistence
        frequency *= 2

    return total / max_value


def noise3d(x, y, z, seed=0):
    """3D 噪声用于洞穴生成"""
    nx = x * 0.05 + seed
    ny = y * 0.05 + seed * 0.5
    nz = z * 0.05 + seed * 0.3

    value = math.sin(nx) * math.cos(ny) * math.sin(nz)
    value += math.sin(nx * 2 + 1) * math.cos(ny * 2 + 1) * math.sin(nz * 2 + 1) * 0.5
    value += math.sin(nx * 4 + 2) * math.cos(ny * 4 + 2) * math.sin(nz * 4 + 2) * 0.25

    return (value + 1) / 2  # 归一化到 0-1


class Chunk:
    """区块类 - 16x128x16 方块"""

    def __init__(self, chunk_x, chunk_z):
        self.chunk_x = chunk_x
        self.chunk_z = chunk_z

        # 方块数据: blocks[x][y][z]
        self.blocks = [[[BlockType.AIR for _ in range(CHUNK_SIZE)]
                        for _ in range(WORLD_HEIGHT)]
                       for _ in range(CHUNK_SIZE)]

        # 是否需要重新构建网格
        self.dirty = True

        # 网格数据 (由渲染器填充)
        self.mesh_vertices = None
        self.mesh_colors = None
        self.vertex_count = 0

    def get_block(self, x, y, z):
        """获取局部坐标的方块"""
        if 0 <= x < CHUNK_SIZE and 0 <= y < WORLD_HEIGHT and 0 <= z < CHUNK_SIZE:
            return self.blocks[x][y][z]
        return BlockType.AIR

    def set_block(self, x, y, z, block_type):
        """设置局部坐标的方块"""
        if 0 <= x < CHUNK_SIZE and 0 <= y < WORLD_HEIGHT and 0 <= z < CHUNK_SIZE:
            self.blocks[x][y][z] = block_type
            self.dirty = True
            return True
        return False


class World:
    """3D 游戏世界 - One Block 模式"""

    def __init__(self, seed=None, one_block_mode=True):
        self.seed = seed if seed is not None else random.randint(0, 999999)
        random.seed(self.seed)

        # 区块字典: (chunk_x, chunk_z) -> Chunk
        self.chunks = {}

        # 已生成的区块集合
        self.generated_chunks = set()

        # One Block 模式
        self.one_block_mode = one_block_mode
        self.one_block_pos = (0, 64, 0)  # 核心方块位置
        self.blocks_mined = 0  # 已挖掘次数

        # 方块生成阶段
        self.phases = [
            # 阶段1: 基础方块 (0-20)
            [BlockType.DIRT, BlockType.DIRT, BlockType.GRASS, BlockType.STONE, BlockType.COBBLESTONE],
            # 阶段2: 木材 (21-50)
            [BlockType.WOOD, BlockType.WOOD, BlockType.PLANKS, BlockType.LEAVES, BlockType.DIRT],
            # 阶段3: 矿石 (51-100)
            [BlockType.STONE, BlockType.COAL_ORE, BlockType.IRON_ORE, BlockType.COBBLESTONE, BlockType.GRAVEL],
            # 阶段4: 稀有矿石 (101-200)
            [BlockType.STONE, BlockType.IRON_ORE, BlockType.GOLD_ORE, BlockType.COAL_ORE, BlockType.DIAMOND_ORE],
            # 阶段5: 多样化 (200+)
            [BlockType.GRASS, BlockType.SAND, BlockType.SNOW, BlockType.BRICK, BlockType.GLASS,
             BlockType.DIAMOND_ORE, BlockType.GOLD_ORE, BlockType.IRON_ORE],
        ]

    def get_chunk(self, chunk_x, chunk_z):
        """获取或生成区块"""
        key = (chunk_x, chunk_z)
        if key not in self.chunks:
            self.chunks[key] = self._generate_chunk(chunk_x, chunk_z)
            self.generated_chunks.add(key)
        return self.chunks[key]

    def _generate_chunk(self, chunk_x, chunk_z):
        """生成单个区块"""
        chunk = Chunk(chunk_x, chunk_z)

        if self.one_block_mode:
            # One Block 模式 - 只生成核心方块和起始平台
            return self._generate_one_block_chunk(chunk, chunk_x, chunk_z)

        world_x_offset = chunk_x * CHUNK_SIZE
        world_z_offset = chunk_z * CHUNK_SIZE

        for local_x in range(CHUNK_SIZE):
            for local_z in range(CHUNK_SIZE):
                world_x = world_x_offset + local_x
                world_z = world_z_offset + local_z

                # 生成高度图
                height = self._get_terrain_height(world_x, world_z)

                for y in range(WORLD_HEIGHT):
                    block = self._get_block_at(world_x, y, world_z, height)
                    chunk.blocks[local_x][y][local_z] = block

        # 生成树木
        self._generate_trees(chunk, chunk_x, chunk_z)

        return chunk

    def _generate_one_block_chunk(self, chunk, chunk_x, chunk_z):
        """生成 One Block 模式的区块"""
        world_x_offset = chunk_x * CHUNK_SIZE
        world_z_offset = chunk_z * CHUNK_SIZE

        obx, oby, obz = self.one_block_pos
        platform_radius = 5000  # 10000x10000 平台 (半径5000)

        for local_x in range(CHUNK_SIZE):
            for local_z in range(CHUNK_SIZE):
                world_x = world_x_offset + local_x
                world_z = world_z_offset + local_z

                # 核心方块位置
                if world_x == obx and world_z == obz:
                    chunk.blocks[local_x][oby][local_z] = BlockType.GRASS

                # 大平台 (10000x10000)
                elif abs(world_x - obx) <= platform_radius and abs(world_z - obz) <= platform_radius:
                    chunk.blocks[local_x][oby][local_z] = BlockType.GRASS  # 改为草方块

        # 在平台上生成树木
        self._generate_one_block_trees(chunk, chunk_x, chunk_z, oby)

        return chunk

    def _generate_one_block_trees(self, chunk, chunk_x, chunk_z, ground_y):
        """在 One Block 平台上生成树木"""
        obx, oby, obz = self.one_block_pos
        platform_radius = 5000

        # 使用确定性随机数生成器
        tree_random = random.Random(self.seed + chunk_x * 10000 + chunk_z)

        # 每个区块生成 0-2 棵树
        num_trees = tree_random.randint(0, 2)

        for _ in range(num_trees):
            local_x = tree_random.randint(2, CHUNK_SIZE - 3)
            local_z = tree_random.randint(2, CHUNK_SIZE - 3)

            world_x = chunk_x * CHUNK_SIZE + local_x
            world_z = chunk_z * CHUNK_SIZE + local_z

            # 检查是否在平台范围内，且不在核心方块附近
            if abs(world_x - obx) <= platform_radius and abs(world_z - obz) <= platform_radius:
                if abs(world_x - obx) > 3 or abs(world_z - obz) > 3:  # 不在核心方块附近
                    # 检查地面是否有草方块
                    if chunk.blocks[local_x][ground_y][local_z] == BlockType.GRASS:
                        self._place_tree(chunk, local_x, ground_y + 1, local_z, tree_random)

    def get_next_one_block(self):
        """获取下一个 One Block 方块类型"""
        # 根据挖掘次数决定阶段
        if self.blocks_mined < 20:
            phase = 0
        elif self.blocks_mined < 50:
            phase = 1
        elif self.blocks_mined < 100:
            phase = 2
        elif self.blocks_mined < 200:
            phase = 3
        else:
            phase = 4

        blocks = self.phases[phase]
        return random.choice(blocks)

    def respawn_one_block(self):
        """在核心位置重新生成方块"""
        if not self.one_block_mode:
            return

        obx, oby, obz = self.one_block_pos
        new_block = self.get_next_one_block()
        self.set_block(obx, oby, obz, new_block)
        self.blocks_mined += 1
        return new_block

    def _get_terrain_height(self, x, z):
        """获取地形高度"""
        # 基础高度
        height = GROUND_LEVEL

        # 大尺度地形
        height += noise2d(x, z, self.seed) * 20

        # 山脉
        mountain = noise2d(x * 0.5, z * 0.5, self.seed + 1000)
        if mountain > 0.3:
            height += (mountain - 0.3) * 40

        # 小细节
        height += noise2d(x * 2, z * 2, self.seed + 2000) * 5

        return int(max(5, min(height, WORLD_HEIGHT - 10)))

    def _get_block_at(self, x, y, z, surface_height):
        """确定指定位置的方块类型"""
        # 基岩层
        if y == 0:
            return BlockType.BEDROCK
        if y < 5 and random.random() < 0.5:
            return BlockType.BEDROCK

        # 空气
        if y > surface_height:
            # 水面以下是水
            if y <= SEA_LEVEL:
                return BlockType.WATER
            return BlockType.AIR

        # 地表
        if y == surface_height:
            if surface_height <= SEA_LEVEL + 2:
                return BlockType.SAND
            elif surface_height > 80:
                return BlockType.SNOW
            else:
                return BlockType.GRASS

        # 地下
        depth = surface_height - y

        # 洞穴
        cave_value = noise3d(x, y, z, self.seed + 5000)
        if cave_value > 0.65 and y > 5 and y < surface_height - 3:
            return BlockType.AIR

        # 土层
        if depth <= 3:
            return BlockType.DIRT

        # 石头层和矿石
        if random.random() < 0.02 and y < 60:
            return BlockType.COAL_ORE
        if random.random() < 0.015 and y < 45:
            return BlockType.IRON_ORE
        if random.random() < 0.008 and y < 30:
            return BlockType.GOLD_ORE
        if random.random() < 0.003 and y < 16:
            return BlockType.DIAMOND_ORE

        return BlockType.STONE

    def _generate_trees(self, chunk, chunk_x, chunk_z):
        """在区块中生成树木"""
        world_x_offset = chunk_x * CHUNK_SIZE
        world_z_offset = chunk_z * CHUNK_SIZE

        # 使用确定性随机数生成器
        tree_random = random.Random(self.seed + chunk_x * 10000 + chunk_z)

        for _ in range(tree_random.randint(0, 3)):  # 每个区块0-3棵树
            local_x = tree_random.randint(3, CHUNK_SIZE - 4)
            local_z = tree_random.randint(3, CHUNK_SIZE - 4)

            # 找到地表
            surface_y = None
            for y in range(WORLD_HEIGHT - 1, 0, -1):
                if chunk.blocks[local_x][y][local_z] == BlockType.GRASS:
                    surface_y = y
                    break

            if surface_y is None or surface_y < SEA_LEVEL + 5 or surface_y > 75:
                continue

            # 放置树
            self._place_tree(chunk, local_x, surface_y + 1, local_z, tree_random)

    def _place_tree(self, chunk, x, base_y, z, rng):
        """放置一棵树"""
        trunk_height = rng.randint(4, 6)

        # 树干
        for y in range(trunk_height):
            if base_y + y < WORLD_HEIGHT:
                chunk.blocks[x][base_y + y][z] = BlockType.WOOD

        # 树叶
        leaf_y = base_y + trunk_height - 2
        for dy in range(-1, 3):
            for dx in range(-2, 3):
                for dz in range(-2, 3):
                    # 球形树冠
                    dist = abs(dx) + abs(dy) + abs(dz)
                    if dist <= 3:
                        lx, ly, lz = x + dx, leaf_y + dy, z + dz
                        if (0 <= lx < CHUNK_SIZE and 0 <= ly < WORLD_HEIGHT and 0 <= lz < CHUNK_SIZE):
                            if chunk.blocks[lx][ly][lz] == BlockType.AIR:
                                chunk.blocks[lx][ly][lz] = BlockType.LEAVES

    def get_block(self, x, y, z):
        """获取世界坐标的方块"""
        if y < 0 or y >= WORLD_HEIGHT:
            return BlockType.AIR

        # Python的整除对负数是向下取整，所以直接用 // 即可
        chunk_x = math.floor(x / CHUNK_SIZE)
        chunk_z = math.floor(z / CHUNK_SIZE)

        local_x = x - chunk_x * CHUNK_SIZE
        local_z = z - chunk_z * CHUNK_SIZE

        key = (chunk_x, chunk_z)
        if key in self.chunks:
            return self.chunks[key].get_block(local_x, y, local_z)

        return BlockType.AIR

    def set_block(self, x, y, z, block_type):
        """设置世界坐标的方块"""
        if y < 0 or y >= WORLD_HEIGHT:
            return False

        # 使用 math.floor 正确处理负坐标
        chunk_x = math.floor(x / CHUNK_SIZE)
        chunk_z = math.floor(z / CHUNK_SIZE)

        local_x = x - chunk_x * CHUNK_SIZE
        local_z = z - chunk_z * CHUNK_SIZE

        key = (chunk_x, chunk_z)
        if key in self.chunks:
            result = self.chunks[key].set_block(local_x, y, local_z, block_type)

            # 如果方块在区块边缘，也标记相邻区块为脏
            if local_x == 0:
                adj_key = (chunk_x - 1, chunk_z)
                if adj_key in self.chunks:
                    self.chunks[adj_key].dirty = True
            if local_x == CHUNK_SIZE - 1:
                adj_key = (chunk_x + 1, chunk_z)
                if adj_key in self.chunks:
                    self.chunks[adj_key].dirty = True
            if local_z == 0:
                adj_key = (chunk_x, chunk_z - 1)
                if adj_key in self.chunks:
                    self.chunks[adj_key].dirty = True
            if local_z == CHUNK_SIZE - 1:
                adj_key = (chunk_x, chunk_z + 1)
                if adj_key in self.chunks:
                    self.chunks[adj_key].dirty = True

            return result

        return False

    def is_solid(self, x, y, z):
        """检查方块是否为固体"""
        # 使用 math.floor 正确处理负坐标
        block = self.get_block(int(math.floor(x)), int(math.floor(y)), int(math.floor(z)))
        return BLOCK_DATA.get(block, {}).get('solid', False)

    def get_chunks_around(self, center_x, center_z, distance):
        """获取周围的区块"""
        chunks = []
        for dx in range(-distance, distance + 1):
            for dz in range(-distance, distance + 1):
                chunk = self.get_chunk(center_x + dx, center_z + dz)
                chunks.append(chunk)
        return chunks

    def find_spawn_point(self):
        """找到合适的出生点"""
        if self.one_block_mode:
            # One Block 模式 - 在核心方块上方出生
            obx, oby, obz = self.one_block_pos
            # 确保区块已生成
            chunk_x = math.floor(obx / CHUNK_SIZE)
            chunk_z = math.floor(obz / CHUNK_SIZE)
            for dx in range(-1, 2):
                for dz in range(-1, 2):
                    self.get_chunk(chunk_x + dx, chunk_z + dz)
            return (obx + 0.5, oby + 2, obz + 0.5)

        # 普通模式 - 从世界中心附近找
        center = CHUNK_SIZE * 2
        for x in range(center, center + 50):
            for z in range(center, center + 50):
                height = self._get_terrain_height(x, z)
                if height > SEA_LEVEL + 2:
                    chunk_x = math.floor(x / CHUNK_SIZE)
                    chunk_z = math.floor(z / CHUNK_SIZE)
                    for dx in range(-1, 2):
                        for dz in range(-1, 2):
                            self.get_chunk(chunk_x + dx, chunk_z + dz)
                    return (x + 0.5, height + 2, z + 0.5)

        return (center + 8.5, GROUND_LEVEL + 10, center + 8.5)
