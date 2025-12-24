"""
Black Ops - 玩家类
"""

import pygame
import math
from settings import *


class Player:
    """玩家角色"""

    def __init__(self, x=2, y=2, angle=0):
        # 位置与方向
        self.x = x
        self.y = y
        self.angle = angle  # 弧度

        # 生命与护甲
        self.hp = 100
        self.max_hp = 100
        self.armor = 0
        self.max_armor = 100
        self.is_alive = True

        # 移动
        self.move_speed = PLAYER_SPEED
        self.sprint_speed = PLAYER_SPRINT_SPEED
        self.rot_speed = PLAYER_ROT_SPEED
        self.is_sprinting = False
        self.is_crouching = False
        self.stamina = 100
        self.max_stamina = 100

        # 武器系统
        self.weapons = []  # 武器列表
        self.current_weapon_index = 0
        self.is_reloading = False
        self.reload_timer = 0
        self.is_aiming = False
        self.shoot_cooldown = 0

        # 手雷
        self.grenades = 2
        self.max_grenades = 4

        # 击杀统计
        self.kills = 0
        self.score = 0

        # 受伤效果
        self.damage_flash = 0
        self.last_damage_dir = 0  # 最后受伤方向

        # 脚步声计时
        self.footstep_timer = 0

    def update(self, dt, keys, mouse_rel, game_map):
        """更新玩家状态"""
        if not self.is_alive:
            return

        # 更新计时器
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
        if self.damage_flash > 0:
            self.damage_flash -= dt

        # 更新换弹
        if self.is_reloading:
            self.reload_timer -= dt
            if self.reload_timer <= 0:
                self._finish_reload()

        # 更新耐力
        self._update_stamina(dt, keys)

        # 处理移动
        self._handle_movement(dt, keys, game_map)

        # 处理视角
        self._handle_rotation(dt, keys, mouse_rel)

    def _update_stamina(self, dt, keys):
        """更新耐力"""
        if self.is_sprinting and (keys[pygame.K_w] or keys[pygame.K_UP]):
            self.stamina -= 30 * dt
            if self.stamina <= 0:
                self.stamina = 0
                self.is_sprinting = False
        else:
            self.stamina = min(self.max_stamina, self.stamina + 20 * dt)

    def _handle_movement(self, dt, keys, game_map):
        """处理移动输入"""
        # 计算移动速度
        speed = self.sprint_speed if self.is_sprinting else self.move_speed
        if self.is_crouching:
            speed *= 0.5
        if self.is_aiming:
            speed *= 0.6

        # 前后移动
        forward = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            forward = 1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            forward = -1

        # 左右平移
        strafe = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            strafe = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            strafe = 1

        # 计算移动向量
        if forward != 0 or strafe != 0:
            # 归一化对角线移动
            if forward != 0 and strafe != 0:
                forward *= 0.707
                strafe *= 0.707

            dx = (math.cos(self.angle) * forward - math.sin(self.angle) * strafe) * speed * dt
            dy = (math.sin(self.angle) * forward + math.cos(self.angle) * strafe) * speed * dt

            # 碰撞检测 (分别检测x和y)
            new_x = self.x + dx
            new_y = self.y + dy

            if game_map.is_walkable(new_x, self.y, PLAYER_SIZE):
                self.x = new_x
            if game_map.is_walkable(self.x, new_y, PLAYER_SIZE):
                self.y = new_y

            # 脚步声
            self.footstep_timer += dt
            if self.footstep_timer > (0.3 if self.is_sprinting else 0.5):
                self.footstep_timer = 0
                # TODO: 播放脚步声

    def _handle_rotation(self, dt, keys, mouse_rel):
        """处理视角旋转"""
        # 鼠标控制
        if mouse_rel[0] != 0:
            rotation = mouse_rel[0] * MOUSE_SENSITIVITY
            rotation = max(-0.1, min(0.1, rotation))  # 限制单帧旋转量
            self.angle += rotation

        # 键盘控制 (Q/E)
        if keys[pygame.K_q]:
            self.angle -= self.rot_speed * dt
        if keys[pygame.K_e]:
            self.angle += self.rot_speed * dt

        # 归一化角度
        while self.angle < 0:
            self.angle += 2 * math.pi
        while self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi

    def handle_event(self, event):
        """处理事件"""
        if not self.is_alive:
            return None

        if event.type == pygame.KEYDOWN:
            # 冲刺
            if event.key == pygame.K_LSHIFT:
                if self.stamina > 20:
                    self.is_sprinting = True
            # 蹲下
            elif event.key == pygame.K_LCTRL:
                self.is_crouching = not self.is_crouching
            # 换弹
            elif event.key == pygame.K_r:
                self.reload()
            # 切换武器
            elif event.key == pygame.K_1:
                self.switch_weapon(0)
            elif event.key == pygame.K_2:
                self.switch_weapon(1)
            elif event.key == pygame.K_TAB:
                self.switch_weapon((self.current_weapon_index + 1) % len(self.weapons))
            # 投掷手雷
            elif event.key == pygame.K_g:
                return self.throw_grenade()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                self.is_sprinting = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 左键射击
            if event.button == 1:
                return self.shoot()
            # 右键瞄准
            elif event.button == 3:
                self.is_aiming = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                self.is_aiming = False

        return None

    def shoot(self):
        """射击"""
        if not self.weapons or self.is_reloading:
            return None

        weapon = self.weapons[self.current_weapon_index]

        if self.shoot_cooldown > 0:
            return None

        if weapon.current_ammo <= 0:
            # 自动换弹
            self.reload()
            return None

        # 射击
        weapon.current_ammo -= 1
        self.shoot_cooldown = 1.0 / weapon.fire_rate

        # 计算射击精度
        accuracy = weapon.accuracy
        if self.is_aiming and weapon.has_scope:
            accuracy = min(1.0, accuracy + 0.1)
        if self.is_sprinting:
            accuracy *= 0.5
        elif not self.is_aiming:
            accuracy *= 0.85

        # 计算散布
        import random
        spread = (1 - accuracy) * 0.3
        angle_offset = random.uniform(-spread, spread)

        return {
            'type': 'shoot',
            'x': self.x,
            'y': self.y,
            'angle': self.angle + angle_offset,
            'damage': weapon.damage,
            'range': weapon.range,
            'weapon_type': weapon.type,
            'pellets': getattr(weapon, 'pellets', 1),
            'spread': getattr(weapon, 'spread', 0),
        }

    def reload(self):
        """换弹"""
        if not self.weapons or self.is_reloading:
            return

        weapon = self.weapons[self.current_weapon_index]

        if weapon.current_ammo >= weapon.magazine:
            return  # 弹匣已满

        if weapon.reserve_ammo <= 0:
            return  # 没有备弹

        self.is_reloading = True
        self.reload_timer = weapon.reload_time

    def _finish_reload(self):
        """完成换弹"""
        self.is_reloading = False

        weapon = self.weapons[self.current_weapon_index]
        ammo_needed = weapon.magazine - weapon.current_ammo

        if weapon.single_reload:
            # 单发装填 (霰弹枪)
            ammo_to_load = min(1, weapon.reserve_ammo)
            weapon.current_ammo += ammo_to_load
            weapon.reserve_ammo -= ammo_to_load

            # 继续装填
            if weapon.current_ammo < weapon.magazine and weapon.reserve_ammo > 0:
                self.is_reloading = True
                self.reload_timer = weapon.reload_time
        else:
            # 整匣换弹
            ammo_to_load = min(ammo_needed, weapon.reserve_ammo)
            weapon.current_ammo += ammo_to_load
            weapon.reserve_ammo -= ammo_to_load

    def switch_weapon(self, index):
        """切换武器"""
        if 0 <= index < len(self.weapons):
            if index != self.current_weapon_index:
                self.current_weapon_index = index
                self.is_reloading = False
                self.shoot_cooldown = 0.3  # 切枪延迟

    def throw_grenade(self):
        """投掷手雷"""
        if self.grenades <= 0:
            return None

        self.grenades -= 1
        return {
            'type': 'grenade',
            'x': self.x,
            'y': self.y,
            'angle': self.angle,
        }

    def take_damage(self, damage, from_angle=None):
        """受到伤害"""
        if not self.is_alive:
            return

        # 护甲吸收部分伤害
        if self.armor > 0:
            armor_absorb = min(self.armor, damage * 0.5)
            self.armor -= armor_absorb
            damage -= armor_absorb

        self.hp -= damage
        self.damage_flash = 0.5

        if from_angle is not None:
            self.last_damage_dir = from_angle

        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False

    def heal(self, amount):
        """治疗"""
        self.hp = min(self.max_hp, self.hp + amount)

    def add_armor(self, amount):
        """添加护甲"""
        self.armor = min(self.max_armor, self.armor + amount)

    def add_ammo(self, ammo_type, amount):
        """添加弹药"""
        for weapon in self.weapons:
            if weapon.type == ammo_type:
                weapon.reserve_ammo = min(
                    weapon.max_ammo,
                    weapon.reserve_ammo + amount
                )

    def get_current_weapon(self):
        """获取当前武器"""
        if self.weapons:
            return self.weapons[self.current_weapon_index]
        return None

    def add_weapon(self, weapon):
        """添加武器"""
        # 检查是否已有同类武器
        for i, w in enumerate(self.weapons):
            if w.id == weapon.id:
                # 补充弹药
                w.reserve_ammo = min(w.max_ammo, w.reserve_ammo + weapon.magazine)
                return

        # 最多携带2把武器
        if len(self.weapons) >= 2:
            # 替换当前武器
            self.weapons[self.current_weapon_index] = weapon
        else:
            self.weapons.append(weapon)

    def set_position(self, x, y, angle=None):
        """设置位置"""
        self.x = x
        self.y = y
        if angle is not None:
            self.angle = angle
