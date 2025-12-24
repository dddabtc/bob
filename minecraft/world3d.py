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
    """3D 游戏世界"""

    def __init__(self, seed=None):
        self.seed = seed if seed is not None else random.randint(0, 999999)
        random.seed(self.seed)

        # 区块字典: (chunk_x, chunk_z) -> Chunk
        self.chunks = {}

        # 已生成的区块集合
        self.generated_chunks = set()

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

        chunk_x = x // CHUNK_SIZE if x >= 0 else (x + 1) // CHUNK_SIZE - 1
        chunk_z = z // CHUNK_SIZE if z >= 0 else (z + 1) // CHUNK_SIZE - 1

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

        chunk_x = x // CHUNK_SIZE if x >= 0 else (x + 1) // CHUNK_SIZE - 1
        chunk_z = z // CHUNK_SIZE if z >= 0 else (z + 1) // CHUNK_SIZE - 1

        local_x = x - chunk_x * CHUNK_SIZE
        local_z = z - chunk_z * CHUNK_SIZE

        key = (chunk_x, chunk_z)
        if key in self.chunks:
            return self.chunks[key].set_block(local_x, y, local_z, block_type)

        return False

    def is_solid(self, x, y, z):
        """检查方块是否为固体"""
        block = self.get_block(int(x), int(y), int(z))
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
        # 从原点附近找
        for x in range(0, 50):
            for z in range(0, 50):
                height = self._get_terrain_height(x, z)
                if height > SEA_LEVEL + 2:
                    # 确保区块已生成
                    self.get_chunk(x // CHUNK_SIZE, z // CHUNK_SIZE)
                    return (x + 0.5, height + 2, z + 0.5)

        return (8.5, GROUND_LEVEL + 10, 8.5)
