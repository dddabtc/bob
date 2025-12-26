# 僵尸实体
import math
import random
from settings3d import (
    ZOMBIE_SPEED, ZOMBIE_DAMAGE, ZOMBIE_HEALTH,
    ZOMBIE_ATTACK_RANGE, ZOMBIE_DETECTION_RANGE,
    ZOMBIE_SPAWN_DISTANCE_MIN, ZOMBIE_SPAWN_DISTANCE_MAX,
    ZOMBIE_MAX_COUNT, ZOMBIE_SPAWN_INTERVAL,
    CHUNK_SIZE, WORLD_HEIGHT
)


class Zombie:
    """僵尸敌人"""

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        # 属性
        self.health = ZOMBIE_HEALTH
        self.max_health = ZOMBIE_HEALTH
        self.damage = ZOMBIE_DAMAGE
        self.speed = ZOMBIE_SPEED

        # 物理
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.on_ground = False
        self.width = 0.6
        self.height = 1.9

        # AI 状态
        self.target = None  # 目标玩家
        self.state = 'idle'  # idle, chase, attack
        self.attack_cooldown = 0
        self.attack_rate = 1.0  # 每秒攻击次数

        # 动画
        self.animation_time = 0
        self.facing_angle = 0  # 朝向角度

        # 死亡
        self.is_dead = False
        self.death_timer = 0
        self.death_duration = 1.0  # 死亡动画时间

        # 受伤效果
        self.hurt_timer = 0
        self.hurt_duration = 0.2

    def update(self, world, player, dt):
        """更新僵尸状态"""
        if self.is_dead:
            self.death_timer += dt
            return self.death_timer < self.death_duration

        # 更新冷却
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        if self.hurt_timer > 0:
            self.hurt_timer -= dt

        # 动画时间
        self.animation_time += dt

        # AI 决策
        self._update_ai(player, dt)

        # 物理更新
        self._update_physics(world, dt)

        return True

    def _update_ai(self, player, dt):
        """更新AI行为"""
        # 计算与玩家的距离
        dx = player.x - self.x
        dy = player.y - self.y
        dz = player.z - self.z
        distance = math.sqrt(dx*dx + dy*dy + dz*dz)
        horizontal_dist = math.sqrt(dx*dx + dz*dz)

        # 更新朝向
        if horizontal_dist > 0.1:
            self.facing_angle = math.atan2(dx, dz)

        # 状态机
        if distance <= ZOMBIE_ATTACK_RANGE:
            # 攻击范围内
            self.state = 'attack'
            self._try_attack(player)
            self.vx = 0
            self.vz = 0
        elif distance <= ZOMBIE_DETECTION_RANGE:
            # 追击范围内
            self.state = 'chase'
            self._chase_player(player, horizontal_dist, dx, dz)
        else:
            # 空闲状态 - 随机移动
            self.state = 'idle'
            self._idle_behavior(dt)

    def _chase_player(self, player, distance, dx, dz):
        """追击玩家"""
        if distance > 0.1:
            # 归一化方向
            dir_x = dx / distance
            dir_z = dz / distance

            # 设置速度
            self.vx = dir_x * self.speed
            self.vz = dir_z * self.speed

            # 如果需要跳跃
            if self.on_ground and self._should_jump(player):
                self.vy = 8.0

    def _should_jump(self, player):
        """判断是否需要跳跃"""
        # 如果玩家在上方且距离较近，尝试跳跃
        if player.y > self.y + 0.5:
            return True
        return False

    def _idle_behavior(self, dt):
        """空闲行为"""
        # 减速停止
        self.vx *= 0.9
        self.vz *= 0.9

    def _try_attack(self, player):
        """尝试攻击玩家"""
        if self.attack_cooldown <= 0:
            # 造成伤害
            player.take_damage(self.damage)
            self.attack_cooldown = 1.0 / self.attack_rate

    def _update_physics(self, world, dt):
        """更新物理"""
        # 重力
        self.vy -= 25.0 * dt
        self.vy = max(self.vy, -50.0)

        # 移动
        new_x = self.x + self.vx * dt
        new_y = self.y + self.vy * dt
        new_z = self.z + self.vz * dt

        # 碰撞检测
        self.on_ground = False

        # X轴碰撞
        if not self._check_collision(world, new_x, self.y, self.z):
            self.x = new_x
        else:
            self.vx = 0

        # Y轴碰撞
        if not self._check_collision(world, self.x, new_y, self.z):
            self.y = new_y
        else:
            if self.vy < 0:
                self.on_ground = True
            self.vy = 0

        # Z轴碰撞
        if not self._check_collision(world, self.x, self.y, new_z):
            self.z = new_z
        else:
            self.vz = 0

    def _check_collision(self, world, x, y, z):
        """检查碰撞"""
        # 检查僵尸包围盒内的所有方块
        half_width = self.width / 2

        for check_x in [x - half_width, x + half_width]:
            for check_z in [z - half_width, z + half_width]:
                for check_y in [y, y + self.height / 2, y + self.height]:
                    if world.is_solid(check_x, check_y, check_z):
                        return True
        return False

    def take_damage(self, damage):
        """受到伤害"""
        if self.is_dead:
            return False

        self.health -= damage
        self.hurt_timer = self.hurt_duration

        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            return True  # 已死亡

        return False

    def get_render_color(self):
        """获取渲染颜色"""
        if self.hurt_timer > 0:
            # 受伤时闪红
            return (1.0, 0.3, 0.3)

        if self.is_dead:
            # 死亡时变灰
            t = self.death_timer / self.death_duration
            return (0.3 - t * 0.2, 0.5 - t * 0.3, 0.3 - t * 0.2)

        # 正常僵尸颜色 - 绿色皮肤
        return (0.3, 0.5, 0.3)

    def get_position(self):
        """获取位置"""
        return (self.x, self.y, self.z)


class ZombieManager:
    """僵尸管理器"""

    def __init__(self):
        self.zombies = []
        self.spawn_timer = 0

    def update(self, world, player, day_night, dt):
        """更新所有僵尸"""
        # 更新现有僵尸
        self.zombies = [z for z in self.zombies if z.update(world, player, dt)]

        # 夜晚生成僵尸
        if day_night.is_night():
            self.spawn_timer += dt
            if self.spawn_timer >= ZOMBIE_SPAWN_INTERVAL:
                self.spawn_timer = 0
                self._try_spawn_zombie(world, player)
        else:
            # 白天僵尸会燃烧（简化：直接移除）
            # 保留在室内的僵尸（简化：慢慢减少）
            pass

    def _try_spawn_zombie(self, world, player):
        """尝试生成僵尸"""
        if len(self.zombies) >= ZOMBIE_MAX_COUNT:
            return

        # 在玩家周围随机位置生成
        for _ in range(10):  # 最多尝试10次
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(ZOMBIE_SPAWN_DISTANCE_MIN, ZOMBIE_SPAWN_DISTANCE_MAX)

            spawn_x = player.x + math.cos(angle) * distance
            spawn_z = player.z + math.sin(angle) * distance

            # 找到地面
            spawn_y = self._find_spawn_y(world, spawn_x, spawn_z, player.y)

            if spawn_y is not None:
                zombie = Zombie(spawn_x, spawn_y, spawn_z)
                self.zombies.append(zombie)
                return

    def _find_spawn_y(self, world, x, z, player_y):
        """找到合适的生成高度"""
        # 从玩家高度向下搜索地面
        start_y = int(player_y) + 10

        for y in range(start_y, max(0, start_y - 30), -1):
            # 检查脚下是固体，头部是空气
            if world.is_solid(x, y - 1, z) and not world.is_solid(x, y, z) and not world.is_solid(x, y + 1, z):
                return y

        return None

    def get_zombies(self):
        """获取所有僵尸"""
        return self.zombies

    def clear_all(self):
        """清除所有僵尸"""
        self.zombies = []

    def damage_zombie_at(self, x, y, z, damage, radius=1.5):
        """对指定位置的僵尸造成伤害，返回命中数"""
        hits = 0
        for zombie in self.zombies:
            if zombie.is_dead:
                continue

            dx = zombie.x - x
            dz = zombie.z - z
            horizontal_dist = math.sqrt(dx*dx + dz*dz)

            # 检查Y轴是否在僵尸身体范围内（脚底到头顶）
            zombie_bottom = zombie.y
            zombie_top = zombie.y + zombie.height
            y_in_range = zombie_bottom - 0.5 <= y <= zombie_top + 0.5

            # 水平距离在范围内且Y轴在僵尸身体范围内
            if horizontal_dist <= radius and y_in_range:
                zombie.take_damage(damage)
                hits += 1

        return hits
