# 玩家实体
import pygame
from settings import (
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, JUMP_FORCE,
    GRAVITY, MAX_FALL_SPEED, BLOCK_SIZE, MINING_RANGE, PLACE_RANGE,
    BlockType, BLOCK_DATA, BLOCK_DROPS, HOTBAR_SLOTS, INVENTORY_ROWS, INVENTORY_COLS,
    CHUNK_HEIGHT, WORLD_WIDTH
)


class Player:
    """玩家类"""

    def __init__(self, x, y):
        # 位置 (像素坐标)
        self.x = x * BLOCK_SIZE
        self.y = y * BLOCK_SIZE
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        # 速度
        self.vx = 0
        self.vy = 0

        # 状态
        self.on_ground = False
        self.facing_right = True
        self.is_mining = False
        self.mining_progress = 0
        self.mining_target = None

        # 生命值
        self.max_health = 20
        self.health = self.max_health
        self.max_hunger = 20
        self.hunger = self.max_hunger

        # 背包: list of (block_type, count) or None
        total_slots = HOTBAR_SLOTS + INVENTORY_ROWS * INVENTORY_COLS
        self.inventory = [None] * total_slots
        self.selected_slot = 0

        # 初始物品
        self._give_starter_items()

    def _give_starter_items(self):
        """给予初始物品"""
        self.inventory[0] = (BlockType.WOOD, 10)
        self.inventory[1] = (BlockType.PLANKS, 20)
        self.inventory[2] = (BlockType.COBBLESTONE, 30)
        self.inventory[3] = (BlockType.TORCH, 10)

    def update(self, world, keys):
        """更新玩家状态"""
        # 水平移动
        self.vx = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = PLAYER_SPEED
            self.facing_right = True

        # 跳跃
        if (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vy = -JUMP_FORCE
            self.on_ground = False

        # 重力
        self.vy += GRAVITY
        if self.vy > MAX_FALL_SPEED:
            self.vy = MAX_FALL_SPEED

        # 水中减速
        block_at_player = world.get_block(
            int(self.x // BLOCK_SIZE),
            int((self.y + self.height // 2) // BLOCK_SIZE)
        )
        if block_at_player == BlockType.WATER:
            self.vx *= 0.6
            self.vy *= 0.6
            # 水中可以游泳
            if keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                self.vy = -3

        # 应用移动并处理碰撞
        self._move_with_collision(world)

    def _move_with_collision(self, world):
        """带碰撞检测的移动"""
        # 水平移动
        self.x += self.vx
        self._handle_horizontal_collision(world)

        # 垂直移动
        self.y += self.vy
        self._handle_vertical_collision(world)

    def _handle_horizontal_collision(self, world):
        """处理水平碰撞"""
        # 检查玩家占据的方块
        left = int(self.x // BLOCK_SIZE)
        right = int((self.x + self.width - 1) // BLOCK_SIZE)
        top = int(self.y // BLOCK_SIZE)
        bottom = int((self.y + self.height - 1) // BLOCK_SIZE)

        for bx in range(left, right + 1):
            for by in range(top, bottom + 1):
                if world.is_solid(bx, by):
                    if self.vx > 0:
                        self.x = bx * BLOCK_SIZE - self.width
                    elif self.vx < 0:
                        self.x = (bx + 1) * BLOCK_SIZE
                    self.vx = 0
                    return

    def _handle_vertical_collision(self, world):
        """处理垂直碰撞"""
        left = int(self.x // BLOCK_SIZE)
        right = int((self.x + self.width - 1) // BLOCK_SIZE)
        top = int(self.y // BLOCK_SIZE)
        bottom = int((self.y + self.height - 1) // BLOCK_SIZE)

        self.on_ground = False

        for bx in range(left, right + 1):
            for by in range(top, bottom + 1):
                if world.is_solid(bx, by):
                    if self.vy > 0:
                        self.y = by * BLOCK_SIZE - self.height
                        self.on_ground = True
                    elif self.vy < 0:
                        self.y = (by + 1) * BLOCK_SIZE
                    self.vy = 0
                    return

    def get_center(self):
        """获取玩家中心位置"""
        return (self.x + self.width // 2, self.y + self.height // 2)

    def get_block_pos(self):
        """获取玩家所在方块坐标"""
        return (int(self.x // BLOCK_SIZE), int(self.y // BLOCK_SIZE))

    def can_reach_block(self, bx, by, max_range):
        """检查是否能够够到方块"""
        cx, cy = self.get_center()
        player_bx = cx / BLOCK_SIZE
        player_by = cy / BLOCK_SIZE

        distance = ((bx - player_bx) ** 2 + (by - player_by) ** 2) ** 0.5
        return distance <= max_range

    def start_mining(self, bx, by, world):
        """开始挖掘方块"""
        if not self.can_reach_block(bx, by, MINING_RANGE):
            return False

        block_type = world.get_block(bx, by)
        if block_type == BlockType.AIR:
            return False

        hardness = BLOCK_DATA.get(block_type, {}).get('hardness', 1)
        if hardness < 0:  # 基岩等不可破坏
            return False

        self.is_mining = True
        self.mining_target = (bx, by)
        self.mining_progress = 0
        return True

    def update_mining(self, world, dt):
        """更新挖掘进度"""
        if not self.is_mining or not self.mining_target:
            return None

        bx, by = self.mining_target
        block_type = world.get_block(bx, by)

        if block_type == BlockType.AIR:
            self.stop_mining()
            return None

        hardness = BLOCK_DATA.get(block_type, {}).get('hardness', 1)
        if hardness <= 0:
            hardness = 0.1

        # 挖掘速度
        mining_speed = 1.0 / hardness
        self.mining_progress += mining_speed * dt

        if self.mining_progress >= 1.0:
            # 挖掘完成
            self.stop_mining()

            # 获取掉落物
            drops = BLOCK_DROPS.get(block_type, [(block_type, 1)])

            # 移除方块
            world.set_block(bx, by, BlockType.AIR)

            # 返回掉落物
            return drops

        return None

    def stop_mining(self):
        """停止挖掘"""
        self.is_mining = False
        self.mining_target = None
        self.mining_progress = 0

    def place_block(self, bx, by, world):
        """放置方块"""
        if not self.can_reach_block(bx, by, PLACE_RANGE):
            return False

        # 检查目标位置是否为空
        if world.get_block(bx, by) != BlockType.AIR:
            return False

        # 检查是否有物品
        item = self.inventory[self.selected_slot]
        if item is None:
            return False

        block_type, count = item

        # 检查是否是可放置的方块
        if block_type not in BLOCK_DATA:
            return False

        # 检查是否会和玩家重叠
        player_left = int(self.x // BLOCK_SIZE)
        player_right = int((self.x + self.width - 1) // BLOCK_SIZE)
        player_top = int(self.y // BLOCK_SIZE)
        player_bottom = int((self.y + self.height - 1) // BLOCK_SIZE)

        if player_left <= bx <= player_right and player_top <= by <= player_bottom:
            return False

        # 放置方块
        world.set_block(bx, by, block_type)

        # 减少物品
        if count <= 1:
            self.inventory[self.selected_slot] = None
        else:
            self.inventory[self.selected_slot] = (block_type, count - 1)

        return True

    def add_item(self, block_type, count=1):
        """添加物品到背包"""
        # 先尝试堆叠
        for i, slot in enumerate(self.inventory):
            if slot is not None and slot[0] == block_type:
                new_count = slot[1] + count
                if new_count <= 64:
                    self.inventory[i] = (block_type, new_count)
                    return True
                else:
                    self.inventory[i] = (block_type, 64)
                    count = new_count - 64

        # 找空槽位
        for i, slot in enumerate(self.inventory):
            if slot is None:
                self.inventory[i] = (block_type, min(count, 64))
                return True

        return False  # 背包满了

    def select_slot(self, slot):
        """选择快捷栏槽位"""
        if 0 <= slot < HOTBAR_SLOTS:
            self.selected_slot = slot

    def get_selected_item(self):
        """获取当前选中的物品"""
        return self.inventory[self.selected_slot]

    def take_damage(self, amount):
        """受到伤害"""
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            return True  # 死亡
        return False

    def heal(self, amount):
        """治疗"""
        self.health = min(self.health + amount, self.max_health)

    def draw(self, screen, camera):
        """绘制玩家"""
        # 转换为屏幕坐标
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y

        # 绘制身体
        body_color = (64, 64, 200)
        pygame.draw.rect(screen, body_color,
                        (screen_x + 4, screen_y + 12, self.width - 8, self.height - 12))

        # 绘制头
        head_color = (255, 200, 150)
        pygame.draw.rect(screen, head_color,
                        (screen_x + 2, screen_y, self.width - 4, 14))

        # 绘制眼睛
        eye_color = (0, 0, 0)
        if self.facing_right:
            pygame.draw.rect(screen, eye_color, (screen_x + 14, screen_y + 4, 3, 3))
        else:
            pygame.draw.rect(screen, eye_color, (screen_x + 7, screen_y + 4, 3, 3))

        # 挖掘进度条
        if self.is_mining and self.mining_target:
            bx, by = self.mining_target
            bar_x = bx * BLOCK_SIZE - camera.x
            bar_y = by * BLOCK_SIZE - camera.y - 8
            bar_width = int(BLOCK_SIZE * self.mining_progress)

            pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, BLOCK_SIZE, 5))
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width, 5))
