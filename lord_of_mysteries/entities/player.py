"""
玩家类
"""

import pygame
import math
import time
from settings import *


class Player:
    """玩家角色"""

    def __init__(self, x, y, pathway_id, pathway_data, sequence=9):
        self.x = x
        self.y = y
        self.pathway_id = pathway_id
        self.pathway_name = pathway_id  # 途径名称，用于魔药配方查询
        self.pathway_data = pathway_data
        self.sequence = sequence

        # 获取序列数据
        self.seq_data = pathway_data["sequences"][sequence]

        # 基础属性
        self.max_hp = self.seq_data["hp"]
        self.hp = self.max_hp
        self.attack = self.seq_data["attack"]
        self.defense = self.seq_data["defense"]
        self.base_speed = self.seq_data["speed"]
        self.speed = self.base_speed

        # 外观
        self.color = pathway_data["color"]
        self.size = PLAYER_SIZE
        self.name = self.seq_data["name"]

        # 精灵图
        self.sprite = None
        self.sprite_size = (60, 80)  # 游戏中显示的大小
        self._load_sprite()

        # 方向 (四方向: "right", "left", "up", "down")
        self.facing = "right"
        self.facing_x = 1  # 水平方向 (1=右, -1=左, 0=无)
        self.facing_y = 0  # 垂直方向 (1=下, -1=上, 0=无)

        # 状态
        self.is_attacking = False
        self.is_dodging = False
        self.is_invincible = False
        self.invincible_timer = 0

        # 攻击相关
        self.attack_cooldown = 0
        self.attack_duration = 0
        self.attack_range = 60
        self.attack_hitbox = None

        # 闪避相关
        self.dodge_cooldown = 0
        self.dodge_duration = 0
        self.dodge_speed = 15
        self.dodge_direction = (0, 0)

        # 技能系统
        self.skills = {}
        self._init_skills()

        # 增益/减益效果
        self.buffs = []

        # 动画相关
        self.animation_frame = 0
        self.animation_timer = 0

        # 生命恢复系统
        self.hp_regen_rate = 2  # 每秒恢复2点生命
        self.hp_regen_timer = 0
        self.hp_regen_interval = 1.0  # 每1秒恢复一次

        # 魔药消化系统
        self.is_digesting = False  # 是否正在消化魔药
        self.digest_timer = 0  # 消化计时器
        self.digest_duration = 30.0  # 消化时间（30秒）
        self.digest_progress = 0  # 消化进度 0-100%

        # 投射物列表
        self.projectiles = []

        # 武器系统
        self.weapon_manager = None
        self.weapon_attack_bonus = 0
        self.weapon_crit_rate = 0
        self.weapon_crit_damage = 0
        self.weapon_spirit_bonus = 0
        self.weapon_defense_bonus = 0
        self.weapon_projectiles = []  # 武器投射物单独管理
        self._init_weapon_system()

    def _init_weapon_system(self):
        """初始化武器系统"""
        try:
            from systems.weapon import WeaponManager
            self.weapon_manager = WeaponManager(self)
        except Exception as e:
            print(f"初始化武器系统失败: {e}")
            self.weapon_manager = None

    def _init_skills(self):
        """初始化技能"""
        from data.pathways import SKILLS

        for skill_name in self.seq_data["skills"]:
            if skill_name in SKILLS:
                skill_data = SKILLS[skill_name].copy()
                skill_data["current_cooldown"] = 0
                skill_data["name"] = skill_name
                self.skills[skill_name] = skill_data

    def _load_sprite(self):
        """加载角色精灵图"""
        try:
            from systems.sprites import get_sequence_sprite
            self.sprite = get_sequence_sprite(self.sequence, self.sprite_size)
        except Exception as e:
            print(f"加载精灵图失败: {e}")
            self.sprite = None

    def get_skill_list(self):
        """获取技能列表（前4个）"""
        return list(self.skills.keys())[:4]

    def update(self, dt, keys, events):
        """更新玩家状态"""
        # 更新计时器
        self._update_timers(dt)

        # 更新增益效果
        self._update_buffs(dt)

        # 处理输入
        if not self.is_attacking and not self.is_dodging:
            self._handle_movement(keys)

        # 处理闪避移动
        if self.is_dodging:
            self._update_dodge(dt)

        # 处理攻击
        if self.is_attacking:
            self._update_attack(dt)

        # 处理事件输入
        self._handle_events(events)

        # 更新投射物
        self._update_projectiles(dt)

        # 更新武器系统
        if self.weapon_manager:
            self.weapon_manager.update(dt)

        # 更新武器投射物
        self._update_weapon_projectiles(dt)

        # 更新动画
        self._update_animation(dt)

        # 限制在屏幕内
        self.x = max(self.size, min(SCREEN_WIDTH - self.size, self.x))
        self.y = max(self.size, min(SCREEN_HEIGHT - self.size, self.y))

    def _update_timers(self, dt):
        """更新各种计时器"""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        if self.dodge_cooldown > 0:
            self.dodge_cooldown -= dt
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.is_invincible = False

        # 更新技能冷却
        for skill in self.skills.values():
            if skill["current_cooldown"] > 0:
                skill["current_cooldown"] -= dt

        # 生命恢复
        self._update_hp_regen(dt)

    def _update_hp_regen(self, dt):
        """更新生命值恢复"""
        if self.hp < self.max_hp:
            self.hp_regen_timer += dt
            if self.hp_regen_timer >= self.hp_regen_interval:
                self.hp_regen_timer = 0
                self.hp = min(self.max_hp, self.hp + self.hp_regen_rate)

        # 更新魔药消化
        self._update_digest(dt)

    def _update_digest(self, dt):
        """更新魔药消化进度"""
        if self.is_digesting:
            self.digest_timer += dt
            self.digest_progress = min(100, (self.digest_timer / self.digest_duration) * 100)
            if self.digest_timer >= self.digest_duration:
                self.is_digesting = False
                self.digest_timer = 0
                self.digest_progress = 100

    def start_digest(self):
        """开始消化魔药"""
        self.is_digesting = True
        self.digest_timer = 0
        self.digest_progress = 0

    def can_advance(self):
        """是否可以继续晋升（需要消化完成）"""
        return not self.is_digesting or self.digest_progress >= 100

    def _update_buffs(self, dt):
        """更新增益效果"""
        # 移除过期的buff
        self.buffs = [b for b in self.buffs if b["duration"] > 0]

        for buff in self.buffs:
            buff["duration"] -= dt

        # 重新计算属性
        self._recalculate_stats()

    def _recalculate_stats(self):
        """重新计算属性（基于buff）"""
        self.speed = self.base_speed

        for buff in self.buffs:
            if buff["type"] == "speed":
                self.speed += buff["value"]
            # 可以添加更多buff类型

    def _handle_movement(self, keys):
        """处理移动输入"""
        dx, dy = 0, 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1

        # 更新朝向（四方向）
        if dx != 0 or dy != 0:
            # 优先使用最后按下的方向
            if abs(dx) >= abs(dy):
                # 水平方向优先
                self.facing_x = dx
                self.facing_y = 0
                self.facing = "right" if dx > 0 else "left"
            else:
                # 垂直方向优先
                self.facing_x = 0
                self.facing_y = dy
                self.facing = "down" if dy > 0 else "up"

        # 归一化对角线移动
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707

        self.x += dx * self.speed
        self.y += dy * self.speed

    def _handle_events(self, events):
        """处理事件输入"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                # 普通攻击 - J键或鼠标左键
                if event.key == pygame.K_j:
                    self.start_attack()

                # 闪避 - K键
                elif event.key == pygame.K_k:
                    self.start_dodge()

                # 技能 - 1-4数字键
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    skill_index = event.key - pygame.K_1
                    self.use_skill(skill_index)

                # R键装填（左轮专用）
                elif event.key == pygame.K_r:
                    if self.weapon_manager:
                        self.weapon_manager.start_reload()

            # 鼠标攻击（用于远程武器瞄准）
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键
                    self.start_attack(pygame.mouse.get_pos())

    def start_attack(self, target_pos=None):
        """开始攻击"""
        if self.is_attacking or self.is_dodging:
            return

        # 使用武器系统攻击
        if self.weapon_manager:
            if not self.weapon_manager.can_attack():
                return

            result = self.weapon_manager.start_attack(target_pos)
            if result:
                self.is_attacking = True
                self.attack_duration = 0.3

                # 处理攻击结果
                if isinstance(result, dict):
                    if result["type"] == "melee":
                        self.attack_hitbox = result["hitbox"]
                        self._current_attack_data = result
                    elif result["type"] == "projectile":
                        self._create_weapon_projectile(result)
                elif isinstance(result, list):
                    # 多个投射物
                    for proj_data in result:
                        self._create_weapon_projectile(proj_data)
                return

        # 备用：无武器时的基础攻击
        if self.attack_cooldown > 0:
            return

        self.is_attacking = True
        self.attack_duration = 0.15  # 攻击持续时间（缩短）
        self.attack_cooldown = 0.2   # 攻击冷却（大幅缩短）

        # 创建360度攻击判定框
        self.attack_hitbox = self._create_directional_hitbox()

    def _create_weapon_projectile(self, proj_data):
        """创建武器投射物"""
        from systems.weapon import WeaponProjectile
        projectile = WeaponProjectile(proj_data)
        self.weapon_projectiles.append(projectile)

    def _create_directional_hitbox(self):
        """创建360度环形攻击判定框（以玩家为中心）"""
        # 攻击范围半径
        attack_radius = 60
        # 创建以玩家为中心的正方形判定框
        hitbox_size = attack_radius * 2
        return pygame.Rect(
            self.x - attack_radius,
            self.y - attack_radius,
            hitbox_size,
            hitbox_size
        )

    def _update_attack(self, dt):
        """更新攻击状态"""
        self.attack_duration -= dt
        if self.attack_duration <= 0:
            self.is_attacking = False
            self.attack_hitbox = None

    def start_dodge(self):
        """开始闪避"""
        if self.dodge_cooldown > 0 or self.is_dodging or self.is_attacking:
            return

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1

        # 如果没有方向输入，向面朝方向闪避
        if dx == 0 and dy == 0:
            dx = self.facing_x
            dy = self.facing_y
            # 如果朝向也是0，默认向右
            if dx == 0 and dy == 0:
                dx = 1

        # 归一化
        length = math.sqrt(dx * dx + dy * dy)
        if length > 0:
            dx /= length
            dy /= length

        self.is_dodging = True
        self.is_invincible = True
        self.dodge_duration = 0.2
        self.dodge_cooldown = 0.8
        self.dodge_direction = (dx, dy)

    def _update_dodge(self, dt):
        """更新闪避状态"""
        self.x += self.dodge_direction[0] * self.dodge_speed
        self.y += self.dodge_direction[1] * self.dodge_speed

        self.dodge_duration -= dt
        if self.dodge_duration <= 0:
            self.is_dodging = False
            self.invincible_timer = 0.1  # 闪避后短暂无敌

    def use_skill(self, skill_index):
        """使用技能"""
        skill_names = self.get_skill_list()
        if skill_index >= len(skill_names):
            return False

        skill_name = skill_names[skill_index]
        skill = self.skills.get(skill_name)
        if not skill:
            return False

        if skill["current_cooldown"] > 0:
            return False

        # 设置冷却
        skill["current_cooldown"] = skill["cooldown"]

        # 根据技能类型执行效果
        skill_type = skill.get("type", "")

        if skill_type == "projectile":
            self._cast_projectile(skill)
        elif skill_type == "buff":
            self._cast_buff(skill)
        elif skill_type == "heal":
            self._cast_heal(skill)
        elif skill_type == "dash":
            self._cast_dash(skill)
        elif skill_type == "aoe":
            self._cast_aoe(skill)
        elif skill_type == "melee":
            self._cast_melee(skill)

        return True

    def _cast_projectile(self, skill):
        """释放投射物技能（支持四方向）"""
        # 根据朝向计算投射物方向
        offset_x = self.facing_x * 30
        offset_y = self.facing_y * 30
        vel_x = self.facing_x * 12
        vel_y = self.facing_y * 12

        projectile = {
            "x": self.x + offset_x,
            "y": self.y + offset_y,
            "vx": vel_x,
            "vy": vel_y,
            "damage": skill.get("damage", 20),
            "size": 10,
            "lifetime": 2.0,
            "color": self.color
        }
        self.projectiles.append(projectile)

    def _cast_buff(self, skill):
        """释放增益技能"""
        duration = skill.get("duration", 5)
        buff = {
            "name": skill["name"],
            "type": "buff",
            "duration": duration,
            "effect": skill.get("desc", "")
        }

        # 特殊buff效果
        if "无敌" in skill.get("desc", "") or "闪避" in skill.get("desc", ""):
            self.is_invincible = True
            self.invincible_timer = duration

        self.buffs.append(buff)

    def _cast_heal(self, skill):
        """释放治疗技能"""
        heal_amount = skill.get("heal", 30)
        self.hp = min(self.max_hp, self.hp + heal_amount)

    def _cast_dash(self, skill):
        """释放冲刺技能（支持四方向）"""
        # 快速位移
        dash_distance = 100
        self.x += self.facing_x * dash_distance
        self.y += self.facing_y * dash_distance

        # 如果技能有伤害，创建伤害区域
        if "damage" in skill:
            # 创建一个大的投射物作为伤害判定
            projectile = {
                "x": self.x,
                "y": self.y,
                "vx": 0,
                "vy": 0,
                "damage": skill["damage"],
                "size": 40,
                "lifetime": 0.1,
                "color": self.color
            }
            self.projectiles.append(projectile)

    def _cast_aoe(self, skill):
        """释放范围技能（支持四方向）"""
        # 根据朝向计算AOE位置
        offset_x = self.facing_x * 80
        offset_y = self.facing_y * 80

        # 创建一个大范围的投射物
        projectile = {
            "x": self.x + offset_x,
            "y": self.y + offset_y,
            "vx": 0,
            "vy": 0,
            "damage": skill.get("damage", 40),
            "size": 60,
            "lifetime": 0.5,
            "color": self.color,
            "is_aoe": True
        }
        self.projectiles.append(projectile)

    def _cast_melee(self, skill):
        """释放近战技能（360度环形攻击）"""
        # 强化版普通攻击
        self.is_attacking = True
        self.attack_duration = 0.4
        self.attack_cooldown = 0.3

        # 创建以玩家为中心的环形攻击判定框
        attack_radius = 80  # 技能攻击范围更大
        self.attack_hitbox = pygame.Rect(
            self.x - attack_radius,
            self.y - attack_radius,
            attack_radius * 2,
            attack_radius * 2
        )

        # 标记为技能攻击，伤害更高
        self.skill_attack_damage = skill.get("damage", self.attack * 2)

    def _update_projectiles(self, dt):
        """更新投射物"""
        for proj in self.projectiles[:]:
            proj["x"] += proj["vx"]
            proj["y"] += proj["vy"]
            proj["lifetime"] -= dt

            # 移除过期或出界的投射物
            if proj["lifetime"] <= 0:
                self.projectiles.remove(proj)
            elif proj["x"] < 0 or proj["x"] > SCREEN_WIDTH:
                self.projectiles.remove(proj)
            elif proj["y"] < 0 or proj["y"] > SCREEN_HEIGHT:
                self.projectiles.remove(proj)

    def _update_weapon_projectiles(self, dt, enemies=None):
        """更新武器投射物"""
        for proj in self.weapon_projectiles[:]:
            proj.update(dt, enemies)
            if not proj.active:
                self.weapon_projectiles.remove(proj)

    def _update_animation(self, dt):
        """更新动画"""
        self.animation_timer += dt
        if self.animation_timer >= 0.1:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4

    def take_damage(self, damage):
        """受到伤害"""
        if self.is_invincible:
            return 0

        # 计算实际伤害
        actual_damage = max(1, damage - self.defense // 2)
        self.hp -= actual_damage

        # 受伤后短暂无敌
        self.is_invincible = True
        self.invincible_timer = 0.5

        return actual_damage

    def is_alive(self):
        """是否存活"""
        return self.hp > 0

    def get_rect(self):
        """获取碰撞矩形"""
        return pygame.Rect(
            self.x - self.size // 2,
            self.y - self.size // 2,
            self.size,
            self.size
        )

    def get_attack_damage(self):
        """获取当前攻击伤害"""
        if hasattr(self, 'skill_attack_damage') and self.skill_attack_damage:
            damage = self.skill_attack_damage
            self.skill_attack_damage = None
            return damage

        # 使用武器系统的伤害
        if self.weapon_manager and hasattr(self, '_current_attack_data') and self._current_attack_data is not None:
            attack_data = self._current_attack_data
            self._current_attack_data = None
            return attack_data.get("damage", self.attack), attack_data.get("is_crit", False), attack_data.get("effects", {})

        return self.attack + self.weapon_attack_bonus

    def get_total_attack(self):
        """获取总攻击力（包含武器加成）"""
        return self.attack + self.weapon_attack_bonus

    def get_total_defense(self):
        """获取总防御力（包含武器加成）"""
        return self.defense + self.weapon_defense_bonus

    def equip_weapon(self, weapon_name):
        """装备武器"""
        if self.weapon_manager:
            return self.weapon_manager.equip_weapon(weapon_name)
        return False

    def get_equipped_weapon(self):
        """获取当前装备的武器名"""
        if self.weapon_manager:
            return self.weapon_manager.equipped_weapon
        return None

    def draw(self, screen, fonts):
        """绘制玩家"""
        # 闪避时半透明
        alpha = 128 if self.is_dodging else 255

        # 无敌时闪烁
        if self.is_invincible and not self.is_dodging:
            if int(time.time() * 10) % 2 == 0:
                alpha = 128

        # 优先使用精灵图
        if self.sprite:
            # 创建临时surface用于应用透明度和翻转
            sprite_to_draw = self.sprite.copy()

            # 根据面朝方向翻转（左右方向）
            if self.facing == "left":
                sprite_to_draw = pygame.transform.flip(sprite_to_draw, True, False)

            # 应用透明度
            if alpha < 255:
                sprite_to_draw.set_alpha(alpha)

            # 攻击时添加发光效果
            if self.is_attacking:
                glow = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
                glow.fill((*self.color, 50))
                sprite_to_draw.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

            # 绘制精灵图（居中于玩家位置）
            sprite_x = self.x - self.sprite_size[0] // 2
            sprite_y = self.y - self.sprite_size[1] // 2
            screen.blit(sprite_to_draw, (sprite_x, sprite_y))
        else:
            # 备用：绘制简单圆形
            player_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

            if self.is_attacking:
                color = tuple(min(255, c + 50) for c in self.color)
            elif self.is_dodging:
                color = tuple(c // 2 for c in self.color)
            else:
                color = self.color

            pygame.draw.circle(
                player_surface,
                (*color, alpha),
                (self.size // 2, self.size // 2),
                self.size // 2
            )
            pygame.draw.circle(
                player_surface,
                (255, 255, 255, alpha),
                (self.size // 2, self.size // 2),
                self.size // 2,
                2
            )

            # 方向指示器（支持四方向）
            center = self.size // 2
            if self.facing == "right":
                indicator_x = center + 10
                indicator_y = center
            elif self.facing == "left":
                indicator_x = center - 10
                indicator_y = center
            elif self.facing == "up":
                indicator_x = center
                indicator_y = center - 10
            else:  # down
                indicator_x = center
                indicator_y = center + 10

            pygame.draw.circle(
                player_surface,
                (255, 255, 255, alpha),
                (indicator_x, indicator_y),
                5
            )

            screen.blit(player_surface, (self.x - self.size // 2, self.y - self.size // 2))

        # 绘制攻击效果
        if self.is_attacking and self.attack_hitbox:
            attack_surface = pygame.Surface(
                (self.attack_hitbox.width, self.attack_hitbox.height),
                pygame.SRCALPHA
            )
            pygame.draw.ellipse(
                attack_surface,
                (*self.color, 100),
                (0, 0, self.attack_hitbox.width, self.attack_hitbox.height)
            )
            screen.blit(attack_surface, self.attack_hitbox.topleft)

        # 绘制投射物
        for proj in self.projectiles:
            if proj.get("is_aoe"):
                # AOE效果
                aoe_surface = pygame.Surface((proj["size"] * 2, proj["size"] * 2), pygame.SRCALPHA)
                pygame.draw.circle(
                    aoe_surface,
                    (*proj["color"], 80),
                    (proj["size"], proj["size"]),
                    proj["size"]
                )
                screen.blit(aoe_surface, (proj["x"] - proj["size"], proj["y"] - proj["size"]))
            else:
                # 普通投射物
                pygame.draw.circle(screen, proj["color"], (int(proj["x"]), int(proj["y"])), proj["size"])
                pygame.draw.circle(screen, WHITE, (int(proj["x"]), int(proj["y"])), proj["size"], 2)

        # 绘制武器投射物
        for proj in self.weapon_projectiles:
            proj.draw(screen)

        # 绘制名称
        name_text = fonts["tiny"].render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(self.x, self.y - self.size - 5))
        screen.blit(name_text, name_rect)

        # 绘制buff图标
        self._draw_buffs(screen, fonts)

    def _draw_buffs(self, screen, fonts):
        """绘制buff图标"""
        buff_x = self.x - 40
        buff_y = self.y - self.size - 25

        for i, buff in enumerate(self.buffs[:3]):  # 最多显示3个
            # buff背景
            buff_rect = pygame.Rect(buff_x + i * 25, buff_y, 20, 20)
            pygame.draw.rect(screen, (50, 50, 80), buff_rect, border_radius=3)
            pygame.draw.rect(screen, GOLD, buff_rect, 1, border_radius=3)

            # buff首字母
            initial = buff["name"][0] if buff["name"] else "?"
            text = fonts["tiny"].render(initial, True, WHITE)
            text_rect = text.get_rect(center=buff_rect.center)
            screen.blit(text, text_rect)
