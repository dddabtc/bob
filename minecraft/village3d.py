# 村庄生成系统
import random
import math
from settings3d import BlockType, CHUNK_SIZE, WORLD_HEIGHT


class VillageGenerator:
    """村庄生成器 - 生成类似截图中的Minecraft村庄场景"""

    def __init__(self, seed=0):
        self.seed = seed
        self.rng = random.Random(seed)

    def set_block_safe(self, chunk, x, y, z, block_type, world_x_offset=0, world_z_offset=0):
        """安全设置方块，处理跨区块情况"""
        # 转换为区块内坐标
        local_x = x - world_x_offset
        local_z = z - world_z_offset

        if 0 <= local_x < CHUNK_SIZE and 0 <= y < WORLD_HEIGHT and 0 <= local_z < CHUNK_SIZE:
            chunk.blocks[local_x][y][local_z] = block_type
            return True
        return False

    def generate_village(self, chunk, chunk_x, chunk_z, ground_y, force=False):
        """在区块中生成村庄"""
        world_x_offset = chunk_x * CHUNK_SIZE
        world_z_offset = chunk_z * CHUNK_SIZE

        # 使用确定性随机数生成器
        village_rng = random.Random(self.seed + chunk_x * 10007 + chunk_z * 7919)

        # 检查是否应该在这个区块生成村庄
        # 强制生成或约8%几率
        if not force and village_rng.random() > 0.08:
            return False

        # 村庄中心位置 - 确保在区块中央
        center_local_x = CHUNK_SIZE // 2
        center_local_z = CHUNK_SIZE // 2
        center_x = world_x_offset + center_local_x
        center_z = world_z_offset + center_local_z

        # 生成村庄结构
        structures_placed = 0

        # 1. 生成中央水池/池塘（小一点）
        self._generate_pond(chunk, center_x, ground_y, center_z,
                           world_x_offset, world_z_offset, village_rng)
        structures_placed += 1

        # 2. 生成小屋 - 固定在区块的四个角落方向
        house_local_positions = [
            (2, 2),   # 左上
            (10, 2),  # 右上
            (2, 10),  # 左下
            (10, 10), # 右下
        ]

        num_houses = village_rng.randint(1, 2)
        village_rng.shuffle(house_local_positions)

        for i in range(num_houses):
            local_x, local_z = house_local_positions[i]
            hx = world_x_offset + local_x
            hz = world_z_offset + local_z
            self._generate_house(chunk, hx, ground_y, hz,
                                world_x_offset, world_z_offset, village_rng)
            structures_placed += 1

        # 3. 生成瞭望塔 - 选择一个角落
        tower_local_positions = [(1, 12), (12, 1), (1, 1), (12, 12)]
        village_rng.shuffle(tower_local_positions)
        tx_local, tz_local = tower_local_positions[0]
        tx = world_x_offset + tx_local
        tz = world_z_offset + tz_local
        self._generate_watchtower(chunk, tx, ground_y, tz,
                                  world_x_offset, world_z_offset, village_rng)
        structures_placed += 1

        # 4. 生成农田 - 选择一个位置
        farm_local_positions = [(2, 7), (9, 7), (7, 2), (7, 9)]
        village_rng.shuffle(farm_local_positions)
        fx_local, fz_local = farm_local_positions[0]
        fx = world_x_offset + fx_local
        fz = world_z_offset + fz_local
        self._generate_farm(chunk, fx, ground_y, fz,
                           world_x_offset, world_z_offset, village_rng)
        structures_placed += 1

        # 5. 生成栅栏围墙
        self._generate_fences(chunk, center_x, ground_y, center_z,
                             world_x_offset, world_z_offset, village_rng)

        return structures_placed > 0

    def _is_in_chunk(self, x, z, world_x_offset, world_z_offset):
        """检查坐标是否在区块内"""
        local_x = x - world_x_offset
        local_z = z - world_z_offset
        return 0 <= local_x < CHUNK_SIZE and 0 <= local_z < CHUNK_SIZE

    def _is_area_in_chunk(self, x, z, width, length, world_x_offset, world_z_offset):
        """检查一个区域是否完全在区块内"""
        local_x = x - world_x_offset
        local_z = z - world_z_offset
        return (0 <= local_x and local_x + width < CHUNK_SIZE and
                0 <= local_z and local_z + length < CHUNK_SIZE)

    def _generate_pond(self, chunk, x, y, z, wx_off, wz_off, rng):
        """生成水池/池塘"""
        radius = rng.randint(2, 4)
        depth = rng.randint(1, 2)

        for dx in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                dist = math.sqrt(dx*dx + dz*dz)
                if dist <= radius:
                    px, pz = x + dx, z + dz
                    if self._is_in_chunk(px, pz, wx_off, wz_off):
                        # 挖掘池塘
                        for dy in range(depth):
                            if dist <= radius - 0.5:
                                self.set_block_safe(chunk, px, y - dy, pz,
                                                   BlockType.WATER, wx_off, wz_off)
                            else:
                                self.set_block_safe(chunk, px, y - dy, pz,
                                                   BlockType.SAND, wx_off, wz_off)

    def _generate_house(self, chunk, x, y, z, wx_off, wz_off, rng):
        """生成村庄小屋 - 紧凑版本"""
        # 小屋尺寸 - 缩小为4x4
        width = 4
        length = 4
        height = 3

        # 选择建筑材料
        wall_type = rng.choice([BlockType.PLANKS, BlockType.COBBLESTONE, BlockType.WOOD])
        floor_type = BlockType.PLANKS

        # 地基和地板
        for dx in range(width):
            for dz in range(length):
                px, pz = x + dx, z + dz
                if self._is_in_chunk(px, pz, wx_off, wz_off):
                    self.set_block_safe(chunk, px, y, pz, BlockType.COBBLESTONE, wx_off, wz_off)
                    self.set_block_safe(chunk, px, y + 1, pz, floor_type, wx_off, wz_off)

        # 墙壁
        for dy in range(2, height + 1):
            for dx in range(width):
                for dz in range(length):
                    # 只在边缘放墙
                    if dx == 0 or dx == width - 1 or dz == 0 or dz == length - 1:
                        px, pz = x + dx, z + dz
                        if self._is_in_chunk(px, pz, wx_off, wz_off):
                            # 窗户位置 - 每面墙中间
                            is_window = (dy == 3 and
                                        ((dx in [1, 2] and (dz == 0 or dz == length - 1)) or
                                         (dz in [1, 2] and (dx == 0 or dx == width - 1))))
                            if is_window:
                                self.set_block_safe(chunk, px, y + dy, pz,
                                                   BlockType.GLASS, wx_off, wz_off)
                            else:
                                self.set_block_safe(chunk, px, y + dy, pz,
                                                   wall_type, wx_off, wz_off)

        # 门
        door_x, door_z = x + 1, z
        if self._is_in_chunk(door_x, door_z, wx_off, wz_off):
            self.set_block_safe(chunk, door_x, y + 2, door_z, BlockType.AIR, wx_off, wz_off)
            self.set_block_safe(chunk, door_x, y + 3, door_z, BlockType.AIR, wx_off, wz_off)

        # 屋顶（平屋顶 + 边缘楼梯）
        roof_y = y + height + 1
        for dx in range(width):
            for dz in range(length):
                px, pz = x + dx, z + dz
                if self._is_in_chunk(px, pz, wx_off, wz_off):
                    self.set_block_safe(chunk, px, roof_y, pz,
                                       BlockType.STAIRS, wx_off, wz_off)

        # 内部家具
        # 工作台
        fx, fz = x + 1, z + 2
        if self._is_in_chunk(fx, fz, wx_off, wz_off):
            self.set_block_safe(chunk, fx, y + 2, fz,
                               BlockType.CRAFTING_TABLE, wx_off, wz_off)
        # 熔炉
        fx, fz = x + 2, z + 2
        if self._is_in_chunk(fx, fz, wx_off, wz_off):
            self.set_block_safe(chunk, fx, y + 2, fz,
                               BlockType.FURNACE, wx_off, wz_off)

    def _generate_watchtower(self, chunk, x, y, z, wx_off, wz_off, rng):
        """生成瞭望塔（类似截图中的高架木塔）- 紧凑版本"""
        tower_height = rng.randint(6, 8)
        platform_size = 2  # 缩小平台

        # 四根支柱
        pillars = [
            (0, 0), (platform_size, 0),
            (0, platform_size), (platform_size, platform_size)
        ]

        for dx, dz in pillars:
            px, pz = x + dx, z + dz
            if self._is_in_chunk(px, pz, wx_off, wz_off):
                for dy in range(tower_height):
                    self.set_block_safe(chunk, px, y + 1 + dy, pz,
                                       BlockType.LOG, wx_off, wz_off)

        # 平台
        platform_y = y + tower_height
        for dx in range(platform_size + 1):
            for dz in range(platform_size + 1):
                px, pz = x + dx, z + dz
                if self._is_in_chunk(px, pz, wx_off, wz_off):
                    self.set_block_safe(chunk, px, platform_y, pz,
                                       BlockType.PLANKS, wx_off, wz_off)

        # 栏杆
        for dx in range(platform_size + 1):
            for dz in range(platform_size + 1):
                # 只在边缘放栏杆
                if dx == 0 or dx == platform_size or dz == 0 or dz == platform_size:
                    px, pz = x + dx, z + dz
                    if self._is_in_chunk(px, pz, wx_off, wz_off):
                        self.set_block_safe(chunk, px, platform_y + 1, pz,
                                           BlockType.FENCE, wx_off, wz_off)

        # 顶棚
        roof_y = platform_y + 2
        for dx in range(platform_size + 1):
            for dz in range(platform_size + 1):
                px, pz = x + dx, z + dz
                if self._is_in_chunk(px, pz, wx_off, wz_off):
                    self.set_block_safe(chunk, px, roof_y, pz,
                                       BlockType.STAIRS, wx_off, wz_off)

        # 顶棚支柱
        for dx, dz in pillars:
            px, pz = x + dx, z + dz
            if self._is_in_chunk(px, pz, wx_off, wz_off):
                self.set_block_safe(chunk, px, platform_y + 1, pz,
                                   BlockType.FENCE, wx_off, wz_off)

    def _generate_farm(self, chunk, x, y, z, wx_off, wz_off, rng):
        """生成农田 - 紧凑版本"""
        farm_width = 4
        farm_length = 4

        for dx in range(farm_width):
            for dz in range(farm_length):
                px, pz = x + dx, z + dz
                if self._is_in_chunk(px, pz, wx_off, wz_off):
                    # 水渠在中间
                    if dx == farm_width // 2:
                        self.set_block_safe(chunk, px, y, pz, BlockType.WATER, wx_off, wz_off)
                    else:
                        # 农田（用泥土表示耕地）
                        self.set_block_safe(chunk, px, y, pz, BlockType.DIRT, wx_off, wz_off)
                        # 作物（用干草块和南瓜表示）
                        if rng.random() < 0.3:
                            crop = rng.choice([BlockType.HAY, BlockType.PUMPKIN])
                            self.set_block_safe(chunk, px, y + 1, pz, crop, wx_off, wz_off)

    def _generate_fences(self, chunk, center_x, y, center_z, wx_off, wz_off, rng):
        """生成栅栏 - 紧凑版本"""
        # 在村庄周围放置一些短栅栏
        num_fence_sections = rng.randint(2, 4)

        for _ in range(num_fence_sections):
            # 栅栏段的起点 - 限制在区块内
            local_start_x = rng.randint(1, CHUNK_SIZE - 5)
            local_start_z = rng.randint(1, CHUNK_SIZE - 5)
            start_x = wx_off + local_start_x
            start_z = wz_off + local_start_z
            length = rng.randint(2, 4)

            # 方向（水平或垂直）
            horizontal = rng.random() < 0.5

            for i in range(length):
                if horizontal:
                    fx, fz = start_x + i, start_z
                else:
                    fx, fz = start_x, start_z + i

                if self._is_in_chunk(fx, fz, wx_off, wz_off):
                    self.set_block_safe(chunk, fx, y + 1, fz, BlockType.FENCE, wx_off, wz_off)


def generate_terrain_with_hills(chunk, chunk_x, chunk_z, seed, ground_y):
    """生成带起伏的地形（类似截图中的草地）"""
    world_x_offset = chunk_x * CHUNK_SIZE
    world_z_offset = chunk_z * CHUNK_SIZE

    terrain_rng = random.Random(seed + chunk_x * 1000 + chunk_z)

    for local_x in range(CHUNK_SIZE):
        for local_z in range(CHUNK_SIZE):
            world_x = world_x_offset + local_x
            world_z = world_z_offset + local_z

            # 使用正弦波组合创建起伏地形
            height_offset = 0
            height_offset += math.sin(world_x * 0.05 + seed) * 2
            height_offset += math.sin(world_z * 0.07 + seed * 0.5) * 1.5
            height_offset += math.sin((world_x + world_z) * 0.03 + seed * 0.3) * 3
            height_offset += math.sin(world_x * 0.15) * math.cos(world_z * 0.15) * 1

            local_ground = ground_y + int(height_offset)

            # 确保地面不会太低
            local_ground = max(ground_y - 3, min(ground_y + 5, local_ground))

            # 填充地面
            for y in range(local_ground + 1):
                if y == local_ground:
                    chunk.blocks[local_x][y][local_z] = BlockType.GRASS
                elif y >= local_ground - 3:
                    chunk.blocks[local_x][y][local_z] = BlockType.DIRT
                else:
                    chunk.blocks[local_x][y][local_z] = BlockType.STONE

    return chunk
