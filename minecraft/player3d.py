# 3D 玩家控制器
import math
import pygame
from settings3d import (
    PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_SPEED, SPRINT_SPEED,
    JUMP_FORCE, GRAVITY, MAX_FALL_SPEED, MOUSE_SENSITIVITY,
    MINING_RANGE, PLACE_RANGE, BlockType, BLOCK_DATA, BLOCK_DROPS,
    HOTBAR_SLOTS, INVENTORY_ROWS, INVENTORY_COLS
)


class Player:
    """第一人称玩家控制器"""

    def __init__(self, x, y, z):
        # 位置
        self.x = x
        self.y = y
        self.z = z

        # 速度
        self.vx = 0
        self.vy = 0
        self.vz = 0

        # 视角 (弧度)
        self.yaw = 0      # 水平旋转
        self.pitch = 0    # 垂直旋转

        # 尺寸
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        # 状态
        self.on_ground = False
        self.is_sprinting = False
        self.is_sneaking = False
        self.in_water = False

        # 挖掘
        self.is_mining = False
        self.mining_progress = 0
        self.mining_target = None  # (x, y, z)

        # 放置冷却
        self.place_cooldown = 0

        # 生命值
        self.max_health = 20
        self.health = self.max_health

        # 背包
        total_slots = HOTBAR_SLOTS + INVENTORY_ROWS * INVENTORY_COLS
        self.inventory = [None] * total_slots
        self.selected_slot = 0

        # 初始物品
        self._give_starter_items()

    def _give_starter_items(self):
        """给予初始物品"""
        self.inventory[0] = (BlockType.GRASS, 64)
        self.inventory[1] = (BlockType.DIRT, 64)
        self.inventory[2] = (BlockType.STONE, 64)
        self.inventory[3] = (BlockType.WOOD, 64)
        self.inventory[4] = (BlockType.PLANKS, 64)
        self.inventory[5] = (BlockType.GLASS, 64)
        self.inventory[6] = (BlockType.BRICK, 64)
        self.inventory[7] = (BlockType.COBBLESTONE, 64)
        self.inventory[8] = (BlockType.SAND, 64)

    def get_camera_position(self):
        """获取摄像机位置 (眼睛位置)"""
        return (self.x, self.y + self.height - 0.2, self.z)

    def get_look_direction(self):
        """获取视线方向向量"""
        # 从 yaw 和 pitch 计算方向
        cos_pitch = math.cos(self.pitch)
        return (
            math.sin(self.yaw) * cos_pitch,
            -math.sin(self.pitch),
            -math.cos(self.yaw) * cos_pitch
        )

    def get_forward_direction(self):
        """获取前进方向 (忽略垂直分量)"""
        return (math.sin(self.yaw), 0, -math.cos(self.yaw))

    def get_right_direction(self):
        """获取右侧方向"""
        return (math.cos(self.yaw), 0, math.sin(self.yaw))

    def handle_mouse_motion(self, dx, dy):
        """处理鼠标移动"""
        self.yaw += dx * MOUSE_SENSITIVITY
        self.pitch += dy * MOUSE_SENSITIVITY

        # 限制俯仰角
        max_pitch = math.pi / 2 - 0.01
        self.pitch = max(-max_pitch, min(max_pitch, self.pitch))

        # 保持 yaw 在 0-2pi
        self.yaw = self.yaw % (2 * math.pi)

    def update(self, world, keys, dt):
        """更新玩家状态"""
        # 获取移动输入
        forward = 0
        strafe = 0

        if keys[pygame.K_w]:
            forward += 1
        if keys[pygame.K_s]:
            forward -= 1
        if keys[pygame.K_a]:
            strafe -= 1
        if keys[pygame.K_d]:
            strafe += 1

        # 冲刺
        self.is_sprinting = keys[pygame.K_LSHIFT] and forward > 0
        speed = SPRINT_SPEED if self.is_sprinting else PLAYER_SPEED

        # 潜行
        self.is_sneaking = keys[pygame.K_LCTRL]
        if self.is_sneaking:
            speed *= 0.3

        # 计算移动方向
        fx, _, fz = self.get_forward_direction()
        rx, _, rz = self.get_right_direction()

        # 归一化对角移动
        if forward != 0 and strafe != 0:
            norm = 1.0 / math.sqrt(2)
            forward *= norm
            strafe *= norm

        # 目标水平速度
        target_vx = (fx * forward + rx * strafe) * speed
        target_vz = (fz * forward + rz * strafe) * speed

        # 平滑加速
        accel = 20 if self.on_ground else 5
        self.vx += (target_vx - self.vx) * accel * dt
        self.vz += (target_vz - self.vz) * accel * dt

        # 检查是否在水中
        cam_pos = self.get_camera_position()
        self.in_water = world.get_block(int(cam_pos[0]), int(cam_pos[1]), int(cam_pos[2])) == BlockType.WATER

        # 重力和跳跃
        if self.in_water:
            # 水中物理
            self.vy *= 0.9
            if keys[pygame.K_SPACE]:
                self.vy = min(self.vy + 15 * dt, 3)
            else:
                self.vy -= GRAVITY * 0.3 * dt
            self.vx *= 0.9
            self.vz *= 0.9
        else:
            # 正常物理
            if keys[pygame.K_SPACE] and self.on_ground:
                self.vy = JUMP_FORCE
                self.on_ground = False
            else:
                self.vy -= GRAVITY * dt

            if self.vy < -MAX_FALL_SPEED:
                self.vy = -MAX_FALL_SPEED

        # 应用移动
        self._move_with_collision(world, dt)

        # 更新冷却
        if self.place_cooldown > 0:
            self.place_cooldown -= dt

    def _move_with_collision(self, world, dt):
        """带碰撞检测的移动"""
        # 分轴移动
        # X轴
        self.x += self.vx * dt
        if self._check_collision(world):
            self.x -= self.vx * dt
            self.vx = 0

        # Y轴
        old_y = self.y
        self.y += self.vy * dt
        if self._check_collision(world):
            self.y = old_y
            if self.vy < 0:
                self.on_ground = True
            self.vy = 0
        else:
            self.on_ground = False

        # Z轴
        self.z += self.vz * dt
        if self._check_collision(world):
            self.z -= self.vz * dt
            self.vz = 0

    def _check_collision(self, world):
        """检查玩家是否与固体方块碰撞"""
        # 玩家边界
        half_width = self.width / 2
        min_x = self.x - half_width
        max_x = self.x + half_width
        min_y = self.y
        max_y = self.y + self.height
        min_z = self.z - half_width
        max_z = self.z + half_width

        # 检查所有可能碰撞的方块
        for bx in range(int(min_x), int(max_x) + 1):
            for by in range(int(min_y), int(max_y) + 1):
                for bz in range(int(min_z), int(max_z) + 1):
                    if world.is_solid(bx, by, bz):
                        # AABB碰撞检测
                        if (min_x < bx + 1 and max_x > bx and
                            min_y < by + 1 and max_y > by and
                            min_z < bz + 1 and max_z > bz):
                            return True
        return False

    def raycast(self, world, max_distance=MINING_RANGE):
        """射线检测，返回目标方块和放置位置"""
        cam_x, cam_y, cam_z = self.get_camera_position()
        dir_x, dir_y, dir_z = self.get_look_direction()

        # 射线步进
        step = 0.05
        for i in range(int(max_distance / step)):
            t = i * step
            x = cam_x + dir_x * t
            y = cam_y + dir_y * t
            z = cam_z + dir_z * t

            bx, by, bz = int(x), int(y), int(z)
            block = world.get_block(bx, by, bz)

            if block != BlockType.AIR and block != BlockType.WATER:
                # 找到方块，计算放置位置
                # 回退一步找到空位
                prev_t = (i - 1) * step
                px = int(cam_x + dir_x * prev_t)
                py = int(cam_y + dir_y * prev_t)
                pz = int(cam_z + dir_z * prev_t)

                return (bx, by, bz), (px, py, pz)

        return None, None

    def start_mining(self, target, world):
        """开始挖掘"""
        if target is None:
            return False

        bx, by, bz = target
        block = world.get_block(bx, by, bz)

        if block == BlockType.AIR or block == BlockType.WATER:
            return False

        hardness = BLOCK_DATA.get(block, {}).get('hardness', 1)
        if hardness < 0:  # 不可破坏
            return False

        self.is_mining = True
        self.mining_target = target
        self.mining_progress = 0
        return True

    def update_mining(self, world, dt):
        """更新挖掘进度"""
        if not self.is_mining or not self.mining_target:
            return None

        bx, by, bz = self.mining_target
        block = world.get_block(bx, by, bz)

        if block == BlockType.AIR:
            self.stop_mining()
            return None

        hardness = BLOCK_DATA.get(block, {}).get('hardness', 1)
        if hardness <= 0:
            hardness = 0.1

        # 挖掘速度
        mining_speed = 1.0 / hardness
        self.mining_progress += mining_speed * dt

        if self.mining_progress >= 1.0:
            # 挖掘完成
            drop = BLOCK_DROPS.get(block, block)
            world.set_block(bx, by, bz, BlockType.AIR)
            self.stop_mining()
            return drop

        return None

    def stop_mining(self):
        """停止挖掘"""
        self.is_mining = False
        self.mining_target = None
        self.mining_progress = 0

    def place_block(self, place_pos, world):
        """放置方块"""
        if place_pos is None or self.place_cooldown > 0:
            return False

        px, py, pz = place_pos

        # 检查是否为空
        if world.get_block(px, py, pz) != BlockType.AIR:
            return False

        # 检查是否与玩家重叠
        half_width = self.width / 2
        if (px < self.x + half_width and px + 1 > self.x - half_width and
            py < self.y + self.height and py + 1 > self.y and
            pz < self.z + half_width and pz + 1 > self.z - half_width):
            return False

        # 获取当前物品
        item = self.inventory[self.selected_slot]
        if item is None:
            return False

        block_type, count = item

        # 放置
        world.set_block(px, py, pz, block_type)

        # 减少物品
        if count <= 1:
            self.inventory[self.selected_slot] = None
        else:
            self.inventory[self.selected_slot] = (block_type, count - 1)

        self.place_cooldown = 0.2
        return True

    def add_item(self, block_type, count=1):
        """添加物品到背包"""
        if block_type == BlockType.AIR:
            return True

        # 先尝试堆叠
        for i, slot in enumerate(self.inventory):
            if slot is not None and slot[0] == block_type and slot[1] < 64:
                add = min(count, 64 - slot[1])
                self.inventory[i] = (block_type, slot[1] + add)
                count -= add
                if count <= 0:
                    return True

        # 找空槽位
        while count > 0:
            for i, slot in enumerate(self.inventory):
                if slot is None:
                    add = min(count, 64)
                    self.inventory[i] = (block_type, add)
                    count -= add
                    break
            else:
                return False  # 背包满了

        return True

    def select_slot(self, slot):
        """选择快捷栏槽位"""
        if 0 <= slot < HOTBAR_SLOTS:
            self.selected_slot = slot

    def scroll_slot(self, direction):
        """滚轮切换槽位"""
        self.selected_slot = (self.selected_slot - direction) % HOTBAR_SLOTS
