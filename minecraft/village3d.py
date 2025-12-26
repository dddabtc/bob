# 村庄生成系统
import random
import math
from settings3d import BlockType, CHUNK_SIZE, WORLD_HEIGHT


class VillageGenerator:
    """村庄生成器 - 生成类似截图中的Minecraft村庄场景"""

    # 建筑类型权重
    STRUCTURE_WEIGHTS = {
        'house': 30,
        'watchtower': 15,
        'farm': 20,
        'well': 10,
        'market_stall': 15,
        'windmill': 5,
        'bridge': 5,
    }

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
        """在区块中生成村庄 - 增强版本，类似截图中的场景"""
        world_x_offset = chunk_x * CHUNK_SIZE
        world_z_offset = chunk_z * CHUNK_SIZE

        # 使用确定性随机数生成器
        village_rng = random.Random(self.seed + chunk_x * 10007 + chunk_z * 7919)

        # 检查是否应该在这个区块生成村庄
        # 强制生成或约10%几率
        if not force and village_rng.random() > 0.10:
            return False

        # 村庄中心位置 - 确保在区块中央
        center_local_x = CHUNK_SIZE // 2
        center_local_z = CHUNK_SIZE // 2
        center_x = world_x_offset + center_local_x
        center_z = world_z_offset + center_local_z

        # 生成村庄结构
        structures_placed = 0
        structure_positions = []  # 记录建筑位置用于生成道路

        # 1. 生成中央结构 - 水井或池塘
        if village_rng.random() < 0.6:
            # 水井
            self._generate_well(chunk, center_x - 1, ground_y, center_z - 1,
                               world_x_offset, world_z_offset, village_rng)
        else:
            # 池塘
            self._generate_pond(chunk, center_x, ground_y, center_z,
                               world_x_offset, world_z_offset, village_rng)
        structure_positions.append((center_x, center_z))
        structures_placed += 1

        # 2. 生成小屋 - 固定在区块的四个角落方向
        house_local_positions = [
            (2, 2),   # 左上
            (10, 2),  # 右上
            (2, 10),  # 左下
            (10, 10), # 右下
        ]

        num_houses = village_rng.randint(1, 3)
        village_rng.shuffle(house_local_positions)

        for i in range(num_houses):
            local_x, local_z = house_local_positions[i]
            hx = world_x_offset + local_x
            hz = world_z_offset + local_z
            self._generate_house(chunk, hx, ground_y, hz,
                                world_x_offset, world_z_offset, village_rng)
            structure_positions.append((hx + 2, hz + 2))  # 记录房屋中心
            structures_placed += 1

        # 3. 生成瞭望塔 - 选择一个角落
        tower_local_positions = [(1, 12), (12, 1), (1, 1), (12, 12)]
        village_rng.shuffle(tower_local_positions)
        tx_local, tz_local = tower_local_positions[0]
        tx = world_x_offset + tx_local
        tz = world_z_offset + tz_local
        self._generate_watchtower(chunk, tx, ground_y, tz,
                                  world_x_offset, world_z_offset, village_rng)
        structure_positions.append((tx + 1, tz + 1))
        structures_placed += 1

        # 4. 生成农田
        farm_local_positions = [(2, 7), (9, 7), (7, 2), (7, 9)]
        village_rng.shuffle(farm_local_positions)
        fx_local, fz_local = farm_local_positions[0]
        fx = world_x_offset + fx_local
        fz = world_z_offset + fz_local
        self._generate_farm(chunk, fx, ground_y, fz,
                           world_x_offset, world_z_offset, village_rng)
        structure_positions.append((fx + 2, fz + 2))
        structures_placed += 1

        # 5. 新增：生成市场摊位（30%几率）
        if village_rng.random() < 0.3:
            stall_positions = [(5, 5), (9, 5), (5, 9), (9, 9)]
            village_rng.shuffle(stall_positions)
            sx_local, sz_local = stall_positions[0]
            sx = world_x_offset + sx_local
            sz = world_z_offset + sz_local
            self._generate_market_stall(chunk, sx, ground_y, sz,
                                        world_x_offset, world_z_offset, village_rng)
            structure_positions.append((sx + 1, sz + 1))
            structures_placed += 1

        # 6. 新增：生成风车（15%几率，作为地标）
        if village_rng.random() < 0.15:
            windmill_positions = [(0, 6), (13, 6), (6, 0), (6, 13)]
            village_rng.shuffle(windmill_positions)
            wx_local, wz_local = windmill_positions[0]
            wx = world_x_offset + wx_local
            wz = world_z_offset + wz_local
            self._generate_windmill(chunk, wx, ground_y, wz,
                                    world_x_offset, world_z_offset, village_rng)
            structures_placed += 1

        # 7. 生成道路连接建筑物
        if len(structure_positions) >= 2:
            # 从中心向各建筑生成道路
            center_pos = structure_positions[0]
            for pos in structure_positions[1:]:
                self._generate_path(chunk, center_pos[0], center_pos[1],
                                   pos[0], pos[1], ground_y,
                                   world_x_offset, world_z_offset)

        # 8. 生成路灯（沿着道路）
        num_lamps = village_rng.randint(2, 4)
        for _ in range(num_lamps):
            lamp_x = world_x_offset + village_rng.randint(3, 12)
            lamp_z = world_z_offset + village_rng.randint(3, 12)
            self._generate_lamp_post(chunk, lamp_x, ground_y, lamp_z,
                                    world_x_offset, world_z_offset)

        # 9. 生成栅栏围墙
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

    def _generate_well(self, chunk, x, y, z, wx_off, wz_off, rng):
        """生成水井 - 村庄中心常见结构"""
        # 3x3 水井
        for dx in range(3):
            for dz in range(3):
                px, pz = x + dx, z + dz
                if self._is_in_chunk(px, pz, wx_off, wz_off):
                    # 边缘是圆石
                    if dx == 0 or dx == 2 or dz == 0 or dz == 2:
                        self.set_block_safe(chunk, px, y, pz, BlockType.COBBLESTONE, wx_off, wz_off)
                        self.set_block_safe(chunk, px, y + 1, pz, BlockType.COBBLESTONE, wx_off, wz_off)
                    else:
                        # 中心是水
                        self.set_block_safe(chunk, px, y - 1, pz, BlockType.WATER, wx_off, wz_off)
                        self.set_block_safe(chunk, px, y, pz, BlockType.WATER, wx_off, wz_off)

        # 井盖支架
        cx, cz = x + 1, z + 1
        if self._is_in_chunk(cx, cz, wx_off, wz_off):
            # 四角支柱
            for dx, dz in [(0, 0), (2, 0), (0, 2), (2, 2)]:
                px, pz = x + dx, z + dz
                if self._is_in_chunk(px, pz, wx_off, wz_off):
                    self.set_block_safe(chunk, px, y + 2, pz, BlockType.FENCE, wx_off, wz_off)
            # 屋顶
            for dx in range(3):
                for dz in range(3):
                    px, pz = x + dx, z + dz
                    if self._is_in_chunk(px, pz, wx_off, wz_off):
                        self.set_block_safe(chunk, px, y + 3, pz, BlockType.STAIRS, wx_off, wz_off)

    def _generate_market_stall(self, chunk, x, y, z, wx_off, wz_off, rng):
        """生成市场摊位 - 小型开放式结构"""
        # 3x3 摊位
        # 地板
        for dx in range(3):
            for dz in range(3):
                px, pz = x + dx, z + dz
                if self._is_in_chunk(px, pz, wx_off, wz_off):
                    self.set_block_safe(chunk, px, y, pz, BlockType.PLANKS, wx_off, wz_off)

        # 四角柱子
        for dx, dz in [(0, 0), (2, 0), (0, 2), (2, 2)]:
            px, pz = x + dx, z + dz
            if self._is_in_chunk(px, pz, wx_off, wz_off):
                self.set_block_safe(chunk, px, y + 1, pz, BlockType.FENCE, wx_off, wz_off)
                self.set_block_safe(chunk, px, y + 2, pz, BlockType.FENCE, wx_off, wz_off)

        # 顶棚（羊毛或楼梯）
        roof_type = rng.choice([BlockType.WOOL, BlockType.STAIRS])
        for dx in range(3):
            for dz in range(3):
                px, pz = x + dx, z + dz
                if self._is_in_chunk(px, pz, wx_off, wz_off):
                    self.set_block_safe(chunk, px, y + 3, pz, roof_type, wx_off, wz_off)

        # 摊位物品（木桶、南瓜等）
        items = [BlockType.BARREL, BlockType.PUMPKIN, BlockType.HAY]
        px, pz = x + 1, z + 1
        if self._is_in_chunk(px, pz, wx_off, wz_off):
            self.set_block_safe(chunk, px, y + 1, pz, rng.choice(items), wx_off, wz_off)

    def _generate_windmill(self, chunk, x, y, z, wx_off, wz_off, rng):
        """生成风车 - 高耸的地标建筑"""
        # 底座 3x3
        for dx in range(3):
            for dz in range(3):
                px, pz = x + dx, z + dz
                if self._is_in_chunk(px, pz, wx_off, wz_off):
                    self.set_block_safe(chunk, px, y, pz, BlockType.COBBLESTONE, wx_off, wz_off)

        # 塔身
        tower_height = 8
        for dy in range(1, tower_height):
            for dx in range(3):
                for dz in range(3):
                    # 只建外墙
                    if dx == 0 or dx == 2 or dz == 0 or dz == 2:
                        px, pz = x + dx, z + dz
                        if self._is_in_chunk(px, pz, wx_off, wz_off):
                            # 交替使用木板和圆石
                            block = BlockType.PLANKS if dy % 2 == 0 else BlockType.COBBLESTONE
                            self.set_block_safe(chunk, px, y + dy, pz, block, wx_off, wz_off)

        # 风车叶片（简化版 - 用栅栏表示）
        blade_y = y + tower_height - 2
        center_x, center_z = x + 1, z + 1

        # 四个方向的叶片
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for i in range(1, 4):
                bx = center_x + direction[0] * i
                bz = center_z + direction[1] * i
                if self._is_in_chunk(bx, bz, wx_off, wz_off):
                    self.set_block_safe(chunk, bx, blade_y, bz, BlockType.FENCE, wx_off, wz_off)

        # 屋顶
        for dx in range(3):
            for dz in range(3):
                px, pz = x + dx, z + dz
                if self._is_in_chunk(px, pz, wx_off, wz_off):
                    self.set_block_safe(chunk, px, y + tower_height, pz, BlockType.STAIRS, wx_off, wz_off)

    def _generate_path(self, chunk, start_x, start_z, end_x, end_z, y, wx_off, wz_off):
        """生成道路连接建筑"""
        # 简单的L形路径
        current_x, current_z = start_x, start_z

        # 先走X方向
        step_x = 1 if end_x > start_x else -1
        while current_x != end_x:
            if self._is_in_chunk(current_x, current_z, wx_off, wz_off):
                self.set_block_safe(chunk, current_x, y, current_z,
                                   BlockType.GRAVEL, wx_off, wz_off)
            current_x += step_x

        # 再走Z方向
        step_z = 1 if end_z > start_z else -1
        while current_z != end_z:
            if self._is_in_chunk(current_x, current_z, wx_off, wz_off):
                self.set_block_safe(chunk, current_x, y, current_z,
                                   BlockType.GRAVEL, wx_off, wz_off)
            current_z += step_z

    def _generate_lamp_post(self, chunk, x, y, z, wx_off, wz_off):
        """生成路灯"""
        if not self._is_in_chunk(x, z, wx_off, wz_off):
            return

        # 灯柱
        for dy in range(1, 4):
            self.set_block_safe(chunk, x, y + dy, z, BlockType.FENCE, wx_off, wz_off)

        # 灯笼（用火把方块表示）
        self.set_block_safe(chunk, x, y + 4, z, BlockType.LANTERN, wx_off, wz_off)


def generate_terrain_with_hills(chunk, chunk_x, chunk_z, seed, ground_y):
    """生成带起伏的地形（类似截图中的草地）"""
    world_x_offset = chunk_x * CHUNK_SIZE
    world_z_offset = chunk_z * CHUNK_SIZE

    terrain_rng = random.Random(seed + chunk_x * 1000 + chunk_z)

    # 记录地面高度用于后续装饰
    ground_heights = [[0 for _ in range(CHUNK_SIZE)] for _ in range(CHUNK_SIZE)]

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
            ground_heights[local_x][local_z] = local_ground

            # 填充地面
            for y in range(local_ground + 1):
                if y == local_ground:
                    chunk.blocks[local_x][y][local_z] = BlockType.GRASS
                elif y >= local_ground - 3:
                    chunk.blocks[local_x][y][local_z] = BlockType.DIRT
                else:
                    chunk.blocks[local_x][y][local_z] = BlockType.STONE

    # 生成自然装饰（高草和花朵）
    _generate_terrain_decorations(chunk, ground_heights, terrain_rng)

    return chunk


def _generate_terrain_decorations(chunk, ground_heights, rng):
    """在地形上生成高草和花朵装饰"""
    # 高草的生成概率较高（约15%的草方块上）
    # 花朵较稀少（约3%）

    for local_x in range(CHUNK_SIZE):
        for local_z in range(CHUNK_SIZE):
            ground_y = ground_heights[local_x][local_z]

            # 只在草方块上生成装饰
            if chunk.blocks[local_x][ground_y][local_z] != BlockType.GRASS:
                continue

            # 确保上方是空气
            if ground_y + 1 >= WORLD_HEIGHT:
                continue
            if chunk.blocks[local_x][ground_y + 1][local_z] != BlockType.AIR:
                continue

            roll = rng.random()

            if roll < 0.12:
                # 高草 (12%)
                chunk.blocks[local_x][ground_y + 1][local_z] = BlockType.TALL_GRASS
            elif roll < 0.14:
                # 红花 (2%)
                chunk.blocks[local_x][ground_y + 1][local_z] = BlockType.FLOWER_RED
            elif roll < 0.155:
                # 黄花 (1.5%)
                chunk.blocks[local_x][ground_y + 1][local_z] = BlockType.FLOWER_YELLOW
            elif roll < 0.165:
                # 蓝花 (1%)
                chunk.blocks[local_x][ground_y + 1][local_z] = BlockType.FLOWER_BLUE


def generate_fortress(world, center_x, center_y, center_z):
    """在指定位置生成玩家出生堡垒"""
    # 堡垒尺寸
    fortress_size = 11  # 11x11 基础
    wall_height = 6
    tower_height = 10

    half = fortress_size // 2

    # 获取需要修改的区块
    chunks_to_modify = set()
    for dx in range(-half - 2, half + 3):
        for dz in range(-half - 2, half + 3):
            wx = center_x + dx
            wz = center_z + dz
            chunk_x = math.floor(wx / CHUNK_SIZE)
            chunk_z = math.floor(wz / CHUNK_SIZE)
            chunks_to_modify.add((chunk_x, chunk_z))

    # 确保所有相关区块已生成
    for chunk_key in chunks_to_modify:
        world.get_chunk(chunk_key[0], chunk_key[1])

    def set_block(x, y, z, block_type):
        """设置世界方块"""
        world.set_block(x, y, z, block_type)

    # 1. 清理堡垒区域（清除地形）
    for dx in range(-half - 1, half + 2):
        for dz in range(-half - 1, half + 2):
            wx = center_x + dx
            wz = center_z + dz
            # 清除上方障碍物
            for y in range(center_y, center_y + tower_height + 5):
                set_block(wx, y, wz, BlockType.AIR)

    # 2. 地基 - 石砖地板
    for dx in range(-half, half + 1):
        for dz in range(-half, half + 1):
            wx = center_x + dx
            wz = center_z + dz
            set_block(wx, center_y - 1, wz, BlockType.COBBLESTONE)
            set_block(wx, center_y, wz, BlockType.STONE)

    # 3. 城墙
    for dx in range(-half, half + 1):
        for dz in range(-half, half + 1):
            wx = center_x + dx
            wz = center_z + dz

            # 只在边缘建墙
            is_edge = (dx == -half or dx == half or dz == -half or dz == half)
            is_corner = (abs(dx) == half and abs(dz) == half)

            if is_corner:
                # 角落建高塔
                for y in range(center_y + 1, center_y + tower_height + 1):
                    set_block(wx, y, wz, BlockType.COBBLESTONE)
                # 塔顶火把
                set_block(wx, center_y + tower_height + 1, wz, BlockType.LANTERN)
            elif is_edge:
                # 普通城墙
                for y in range(center_y + 1, center_y + wall_height + 1):
                    # 交替使用石头和圆石
                    if y % 2 == 0:
                        set_block(wx, y, wz, BlockType.COBBLESTONE)
                    else:
                        set_block(wx, y, wz, BlockType.STONE)

                # 城墙垛口
                if (dx + dz) % 2 == 0:
                    set_block(wx, center_y + wall_height + 1, wz, BlockType.COBBLESTONE)

    # 4. 入口（南面开门）
    entrance_z = center_z + half
    for dx in range(-1, 2):
        wx = center_x + dx
        for dy in range(1, 4):
            set_block(wx, center_y + dy, entrance_z, BlockType.AIR)

    # 门框装饰
    set_block(center_x - 2, center_y + 1, entrance_z, BlockType.COBBLESTONE)
    set_block(center_x - 2, center_y + 2, entrance_z, BlockType.COBBLESTONE)
    set_block(center_x - 2, center_y + 3, entrance_z, BlockType.COBBLESTONE)
    set_block(center_x + 2, center_y + 1, entrance_z, BlockType.COBBLESTONE)
    set_block(center_x + 2, center_y + 2, entrance_z, BlockType.COBBLESTONE)
    set_block(center_x + 2, center_y + 3, entrance_z, BlockType.COBBLESTONE)
    # 门楣
    for dx in range(-2, 3):
        set_block(center_x + dx, center_y + 4, entrance_z, BlockType.STONE)

    # 5. 内部地板（木板）
    for dx in range(-half + 1, half):
        for dz in range(-half + 1, half):
            wx = center_x + dx
            wz = center_z + dz
            set_block(wx, center_y, wz, BlockType.PLANKS)

    # 6. 中央武器架/工作台
    set_block(center_x, center_y + 1, center_z, BlockType.CRAFTING_TABLE)
    set_block(center_x + 1, center_y + 1, center_z, BlockType.FURNACE)
    set_block(center_x - 1, center_y + 1, center_z, BlockType.BARREL)

    # 7. 内部火把/灯笼
    torch_positions = [
        (center_x - 3, center_y + 3, center_z - 3),
        (center_x + 3, center_y + 3, center_z - 3),
        (center_x - 3, center_y + 3, center_z + 3),
        (center_x + 3, center_y + 3, center_z + 3),
    ]
    for tx, ty, tz in torch_positions:
        set_block(tx, ty, tz, BlockType.LANTERN)

    # 8. 旗帜柱（中央后方）
    flag_x, flag_z = center_x, center_z - half + 2
    for dy in range(1, 6):
        set_block(flag_x, center_y + dy, flag_z, BlockType.FENCE)
    # 旗帜（用羊毛表示）
    set_block(flag_x + 1, center_y + 5, flag_z, BlockType.WOOL)
    set_block(flag_x + 1, center_y + 4, flag_z, BlockType.WOOL)

    # 9. 瞭望台（西北角内部）
    lookout_x = center_x - half + 2
    lookout_z = center_z - half + 2
    # 楼梯
    for i in range(4):
        set_block(lookout_x + i, center_y + 1 + i, lookout_z, BlockType.STAIRS)
    # 平台
    for dx in range(3):
        for dz in range(3):
            set_block(lookout_x + dx, center_y + 5, lookout_z + dz, BlockType.PLANKS)

    # 标记区块为脏，需要重新渲染
    for chunk_key in chunks_to_modify:
        if chunk_key in world.chunks:
            world.chunks[chunk_key].dirty = True

    return True
