"""
Black Ops - 敌人AI系统
"""

import pygame
import math
import random
from settings import *

# 导入敌人数据
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.enemies import ENEMY_TYPES, ENEMY_BEHAVIOR


class Enemy:
    """敌人类"""

    def __init__(self, x, y, enemy_type, patrol_points=None):
        if enemy_type not in ENEMY_TYPES:
            enemy_type = "soldier"

        data = ENEMY_TYPES[enemy_type]

        self.x = x
        self.y = y
        self.type = enemy_type
        self.angle = random.uniform(0, 2 * math.pi)

        # 属性
        self.hp = data["hp"]
        self.max_hp = data["hp"]
        self.damage = data["damage"]
        self.fire_rate = data["fire_rate"]
        self.accuracy = data["accuracy"]
        self.speed = data["speed"]
        self.view_distance = data["view_distance"]
        self.view_angle = data["view_angle"]
        self.attack_range = data["attack_range"]
        self.color = data["color"]
        self.points = data["points"]
        self.is_boss = data.get("is_boss", False)
        self.drops = data.get("drops", [])

        # AI状态
        self.state = EnemyState.PATROL if patrol_points else EnemyState.IDLE
        self.patrol_points = patrol_points or []
        self.patrol_index = 0
        self.wait_timer = 0
        self.alert_timer = 0
        self.last_known_player_pos = None

        # 战斗状态
        self.shoot_cooldown = 0
        self.is_alive = True
        self.death_timer = 0

        # 动画
        self.animation_frame = 0
        self.animation_timer = 0
        self.hit_flash = 0
        self.sprite_surface = None

        # 生成精灵
        self._generate_sprite()

    def _generate_sprite(self):
        """生成敌人精灵 (像素风格)"""
        size = 64
        self.sprite_base = pygame.Surface((size, size), pygame.SRCALPHA)

        # 身体颜色
        body_color = self.color
        darker = tuple(max(0, c - 30) for c in body_color)
        skin_color = (220, 180, 150)

        # 头部
        head_y = 8
        head_size = 16
        pygame.draw.rect(self.sprite_base, skin_color, (24, head_y, head_size, head_size))
        # 头盔
        if self.type in ['soldier', 'elite', 'heavy']:
            helmet_color = (60, 80, 60) if self.type != 'elite' else (40, 40, 60)
            pygame.draw.rect(self.sprite_base, helmet_color, (22, head_y - 2, 20, 10))

        # 身体
        body_y = head_y + head_size
        body_height = 24
        pygame.draw.rect(self.sprite_base, body_color, (20, body_y, 24, body_height))

        # 武器 (根据类型)
        weapon_color = (50, 50, 55)
        if self.type == 'sniper':
            # 长枪
            pygame.draw.rect(self.sprite_base, weapon_color, (42, body_y + 5, 20, 6))
        elif self.type == 'shotgunner':
            # 霰弹枪
            pygame.draw.rect(self.sprite_base, weapon_color, (40, body_y + 8, 18, 8))
        elif self.type in ['commander', 'general']:
            # 手枪
            pygame.draw.rect(self.sprite_base, weapon_color, (42, body_y + 10, 12, 5))
        else:
            # 步枪
            pygame.draw.rect(self.sprite_base, weapon_color, (40, body_y + 6, 16, 6))

        # 腿
        leg_y = body_y + body_height
        leg_color = (60, 60, 50)
        pygame.draw.rect(self.sprite_base, leg_color, (22, leg_y, 8, 16))
        pygame.draw.rect(self.sprite_base, leg_color, (34, leg_y, 8, 16))

        # Boss 特效
        if self.is_boss:
            # 金色边框
            pygame.draw.rect(self.sprite_base, (200, 180, 50), (18, head_y - 4, 28, 48), 2)

    def update(self, dt, player, game_map, enemies):
        """更新敌人状态"""
        if not self.is_alive:
            self.death_timer += dt
            return

        # 更新计时器
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
        if self.hit_flash > 0:
            self.hit_flash -= dt

        # 动画更新
        self.animation_timer += dt
        if self.animation_timer > 0.2:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4

        # AI状态机
        can_see = self._check_line_of_sight(player, game_map)

        if can_see:
            self.state = EnemyState.COMBAT
            self.last_known_player_pos = (player.x, player.y)
            self._combat_behavior(dt, player, game_map)
        elif self.state == EnemyState.COMBAT:
            self.state = EnemyState.ALERT
            self.alert_timer = ENEMY_BEHAVIOR['alert_duration']
        elif self.state == EnemyState.ALERT:
            self._alert_behavior(dt, player, game_map)
        elif self.state == EnemyState.PATROL:
            self._patrol_behavior(dt, game_map)
        else:
            self._idle_behavior(dt)

    def _check_line_of_sight(self, player, game_map):
        """检查是否能看到玩家"""
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        # 距离检查
        if distance > self.view_distance:
            return False

        # 角度检查
        angle_to_player = math.atan2(dy, dx)
        angle_diff = abs(self._normalize_angle(angle_to_player - self.angle))
        if angle_diff > math.radians(self.view_angle / 2):
            return False

        # 射线检测 (墙壁遮挡)
        return self._raycast_to_point(player.x, player.y, game_map)

    def _raycast_to_point(self, target_x, target_y, game_map):
        """射线检测到目标点"""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < 0.1:
            return True

        steps = int(distance * 4)
        step_x = dx / steps
        step_y = dy / steps

        x, y = self.x, self.y
        for _ in range(steps):
            x += step_x
            y += step_y
            if game_map.is_wall(x, y):
                return False

        return True

    def _normalize_angle(self, angle):
        """归一化角度到 [-pi, pi]"""
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

    def _combat_behavior(self, dt, player, game_map):
        """战斗行为"""
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        # 面向玩家
        target_angle = math.atan2(dy, dx)
        self._rotate_towards(target_angle, dt)

        # 根据距离决定行为
        if distance < self.attack_range * 0.5:
            # 太近了，后退
            self._move_away_from(player.x, player.y, dt, game_map)
        elif distance > self.attack_range:
            # 靠近玩家
            self._move_towards(player.x, player.y, dt, game_map)

        # 攻击
        if distance <= self.attack_range and self.shoot_cooldown <= 0:
            return self._attack(player)

        return None

    def _alert_behavior(self, dt, player, game_map):
        """警戒行为"""
        self.alert_timer -= dt

        if self.last_known_player_pos:
            # 向最后看到玩家的位置移动
            self._move_towards(
                self.last_known_player_pos[0],
                self.last_known_player_pos[1],
                dt, game_map
            )

            # 检查是否到达
            dx = self.last_known_player_pos[0] - self.x
            dy = self.last_known_player_pos[1] - self.y
            if dx * dx + dy * dy < 1:
                self.last_known_player_pos = None

        if self.alert_timer <= 0:
            self.state = EnemyState.PATROL if self.patrol_points else EnemyState.IDLE

    def _patrol_behavior(self, dt, game_map):
        """巡逻行为"""
        if not self.patrol_points:
            self.state = EnemyState.IDLE
            return

        target = self.patrol_points[self.patrol_index]
        dx = target[0] - self.x
        dy = target[1] - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < 0.5:
            # 到达巡逻点
            self.wait_timer += dt
            if self.wait_timer > ENEMY_BEHAVIOR['patrol_wait_time']:
                self.wait_timer = 0
                self.patrol_index = (self.patrol_index + 1) % len(self.patrol_points)
        else:
            # 移动到巡逻点
            self._move_towards(target[0], target[1], dt, game_map)

    def _idle_behavior(self, dt):
        """空闲行为"""
        # 随机转向
        if random.random() < 0.01:
            self.angle += random.uniform(-0.5, 0.5)

    def _move_towards(self, target_x, target_y, dt, game_map):
        """向目标移动"""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < 0.1:
            return

        # 归一化方向
        dx /= distance
        dy /= distance

        # 面向移动方向
        target_angle = math.atan2(dy, dx)
        self._rotate_towards(target_angle, dt)

        # 移动
        new_x = self.x + dx * self.speed * dt
        new_y = self.y + dy * self.speed * dt

        if game_map.is_walkable(new_x, self.y, 0.3):
            self.x = new_x
        if game_map.is_walkable(self.x, new_y, 0.3):
            self.y = new_y

    def _move_away_from(self, target_x, target_y, dt, game_map):
        """远离目标"""
        dx = self.x - target_x
        dy = self.y - target_y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < 0.1:
            return

        dx /= distance
        dy /= distance

        new_x = self.x + dx * self.speed * dt * 0.7
        new_y = self.y + dy * self.speed * dt * 0.7

        if game_map.is_walkable(new_x, self.y, 0.3):
            self.x = new_x
        if game_map.is_walkable(self.x, new_y, 0.3):
            self.y = new_y

    def _rotate_towards(self, target_angle, dt):
        """转向目标角度"""
        diff = self._normalize_angle(target_angle - self.angle)
        rotation_speed = 3.0 * dt

        if abs(diff) < rotation_speed:
            self.angle = target_angle
        elif diff > 0:
            self.angle += rotation_speed
        else:
            self.angle -= rotation_speed

    def _attack(self, player):
        """攻击玩家"""
        self.shoot_cooldown = 1.0 / self.fire_rate

        # 计算精度
        accuracy = self.accuracy
        if self.state == EnemyState.ALERT:
            accuracy *= 0.7

        # 随机散布
        spread = (1 - accuracy) * 0.5
        angle_offset = random.uniform(-spread, spread)

        return {
            'type': 'enemy_attack',
            'x': self.x,
            'y': self.y,
            'angle': self.angle + angle_offset,
            'damage': self.damage,
            'enemy': self,
        }

    def take_damage(self, damage):
        """受到伤害"""
        self.hp -= damage
        self.hit_flash = 0.2
        self.state = EnemyState.ALERT  # 被攻击时进入警戒

        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            return self._get_drops()

        return None

    def _get_drops(self):
        """获取掉落物"""
        drops = []
        for drop in self.drops:
            if random.random() < drop['chance']:
                drops.append(drop)
        return drops

    def get_sprite_surface(self, width, height):
        """获取缩放后的精灵"""
        # 复制基础精灵
        sprite = self.sprite_base.copy()

        # 受伤闪烁
        if self.hit_flash > 0:
            flash = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
            flash.fill((255, 100, 100, 100))
            sprite.blit(flash, (0, 0))

        # 死亡效果
        if not self.is_alive:
            # 淡出
            alpha = max(0, 255 - int(self.death_timer * 200))
            sprite.set_alpha(alpha)

        # 缩放
        return pygame.transform.scale(sprite, (width, height))


class EnemyManager:
    """敌人管理器"""

    def __init__(self):
        self.enemies = []

    def spawn_enemy(self, x, y, enemy_type, patrol_points=None):
        """生成敌人"""
        enemy = Enemy(x, y, enemy_type, patrol_points)
        self.enemies.append(enemy)
        return enemy

    def spawn_from_mission(self, mission_data):
        """从关卡数据生成敌人"""
        self.enemies.clear()
        for enemy_data in mission_data.get('enemies', []):
            patrol = enemy_data.get('patrol')
            enemy = self.spawn_enemy(
                enemy_data['x'],
                enemy_data['y'],
                enemy_data['type'],
                patrol
            )
            if enemy_data.get('is_target'):
                enemy.is_target = True

    def update(self, dt, player, game_map):
        """更新所有敌人"""
        attacks = []
        for enemy in self.enemies:
            result = enemy.update(dt, player, game_map, self.enemies)
            if result:
                attacks.append(result)
        return attacks

    def get_alive_enemies(self):
        """获取存活的敌人"""
        return [e for e in self.enemies if e.is_alive]

    def get_dead_enemies(self):
        """获取死亡的敌人 (用于渲染尸体)"""
        return [e for e in self.enemies if not e.is_alive and e.death_timer < 5]

    def remove_dead(self):
        """移除死亡时间过长的敌人"""
        self.enemies = [e for e in self.enemies if e.is_alive or e.death_timer < 5]

    def count_alive(self):
        """计算存活敌人数量"""
        return sum(1 for e in self.enemies if e.is_alive)

    def check_target_killed(self, target_type):
        """检查目标是否被击杀"""
        for enemy in self.enemies:
            if enemy.type == target_type and not enemy.is_alive:
                return True
        return False
