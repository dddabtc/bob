# 枪械系统 - 无限子弹
import math
import random


# 枪的设置
GUN_DAMAGE = 15          # 枪伤害
GUN_RANGE = 50.0         # 射程
GUN_FIRE_RATE = 0.15     # 射击间隔（秒）
BULLET_SPEED = 100.0     # 子弹速度
BULLET_LIFETIME = 1.0    # 子弹存活时间


class Bullet:
    """子弹类"""

    def __init__(self, x, y, z, dir_x, dir_y, dir_z):
        self.x = x
        self.y = y
        self.z = z
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.dir_z = dir_z
        self.speed = BULLET_SPEED
        self.lifetime = BULLET_LIFETIME
        self.active = True

        # 子弹轨迹
        self.trail = []
        self.max_trail = 5

    def update(self, world, zombie_manager, dt):
        """更新子弹状态"""
        if not self.active:
            return False

        # 减少存活时间
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.active = False
            return False

        # 保存上一个位置用于轨迹
        if len(self.trail) >= self.max_trail:
            self.trail.pop(0)
        self.trail.append((self.x, self.y, self.z))

        # 移动子弹
        move_dist = self.speed * dt
        steps = max(1, int(move_dist / 0.5))  # 每0.5单位检测一次碰撞

        for _ in range(steps):
            step_dist = move_dist / steps
            new_x = self.x + self.dir_x * step_dist
            new_y = self.y + self.dir_y * step_dist
            new_z = self.z + self.dir_z * step_dist

            # 检测与方块的碰撞
            block_x = int(math.floor(new_x))
            block_y = int(math.floor(new_y))
            block_z = int(math.floor(new_z))

            if world.is_solid(block_x, block_y, block_z):
                self.active = False
                return False

            # 检测与僵尸的碰撞 - 使用较大半径确保命中
            killed = zombie_manager.damage_zombie_at(new_x, new_y, new_z, GUN_DAMAGE, radius=1.0)
            if killed > 0:
                self.active = False
                return False

            self.x = new_x
            self.y = new_y
            self.z = new_z

        return True

    def get_position(self):
        """获取位置"""
        return (self.x, self.y, self.z)

    def get_trail(self):
        """获取轨迹点"""
        return self.trail


class Gun:
    """枪械类 - 无限子弹"""

    def __init__(self):
        self.name = "手枪"
        self.damage = GUN_DAMAGE
        self.range = GUN_RANGE
        self.fire_rate = GUN_FIRE_RATE

        # 射击冷却
        self.cooldown = 0

        # 子弹列表
        self.bullets = []

        # 枪口闪光效果
        self.muzzle_flash = 0
        self.muzzle_flash_duration = 0.05

        # 后座力效果
        self.recoil = 0
        self.recoil_recovery = 10.0

        # 射击统计
        self.shots_fired = 0
        self.zombies_killed = 0

    def can_shoot(self):
        """是否可以射击"""
        return self.cooldown <= 0

    def shoot(self, player):
        """射击 - 返回新子弹"""
        if not self.can_shoot():
            return None

        # 获取射击起点和方向
        cam_x, cam_y, cam_z = player.get_camera_position()
        dir_x, dir_y, dir_z = player.get_look_direction()

        # 子弹从玩家前方一点开始
        start_offset = 0.5
        start_x = cam_x + dir_x * start_offset
        start_y = cam_y + dir_y * start_offset
        start_z = cam_z + dir_z * start_offset

        # 创建子弹
        bullet = Bullet(start_x, start_y, start_z, dir_x, dir_y, dir_z)
        self.bullets.append(bullet)

        # 设置冷却
        self.cooldown = self.fire_rate

        # 枪口闪光
        self.muzzle_flash = self.muzzle_flash_duration

        # 后座力
        self.recoil = 0.03

        # 统计
        self.shots_fired += 1

        return bullet

    def update(self, world, zombie_manager, dt):
        """更新枪状态和所有子弹"""
        # 更新冷却
        if self.cooldown > 0:
            self.cooldown -= dt

        # 更新枪口闪光
        if self.muzzle_flash > 0:
            self.muzzle_flash -= dt

        # 更新后座力
        if self.recoil > 0:
            self.recoil -= self.recoil_recovery * dt
            if self.recoil < 0:
                self.recoil = 0

        # 更新所有子弹
        active_bullets = []
        for bullet in self.bullets:
            if bullet.update(world, zombie_manager, dt):
                active_bullets.append(bullet)
        self.bullets = active_bullets

    def get_bullets(self):
        """获取所有活跃子弹"""
        return self.bullets

    def has_muzzle_flash(self):
        """是否显示枪口闪光"""
        return self.muzzle_flash > 0

    def get_recoil(self):
        """获取后座力值"""
        return self.recoil
