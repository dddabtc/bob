"""
Black Ops - 游戏主循环
类似使命召唤的第一人称射击游戏
"""

import pygame
import math
import random
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))

from settings import *
from raycaster import Raycaster, GameMap
from entities.player import Player
from entities.enemy import Enemy, EnemyManager
from systems.weapon import Weapon, WeaponManager, WeaponRenderer
from systems.mission import MissionSystem, ItemManager
from ui.menu import MainMenu, MissionSelectMenu, PauseMenu, GameOverScreen
from ui.hud import GameHUD, DialogueBox, MissionBriefing
from data.weapons import WEAPONS, DEFAULT_LOADOUT


class Game:
    """游戏主类"""

    def __init__(self):
        # macOS 需要特殊处理才能正确显示窗口
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

        pygame.init()
        pygame.mixer.init()

        # 创建窗口 - 使用 SHOWN 标志确保窗口可见
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.SHOWN
        )

        pygame.display.set_caption(TITLE)
        pygame.display.flip()
        self.clock = pygame.time.Clock()
        print(f"窗口已创建: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

        # 游戏状态
        self.state = GameState.MENU

        # 菜单状态下显示鼠标
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        self.running = True

        # 初始化系统
        self._init_systems()

        # 统计数据
        self.stats = {
            'kills': 0,
            'shots_fired': 0,
            'shots_hit': 0,
            'time_played': 0,
        }

    def _init_systems(self):
        """初始化游戏系统"""
        # 地图
        self.game_map = GameMap()

        # 渲染器
        self.raycaster = Raycaster(self.screen, self.game_map)
        self.weapon_renderer = WeaponRenderer(self.screen)

        # 玩家
        self.player = Player()

        # 武器管理器
        self.weapon_manager = WeaponManager()

        # 敌人管理器
        self.enemy_manager = EnemyManager()

        # 任务系统
        self.mission_system = MissionSystem()

        # 物品管理器
        self.item_manager = ItemManager()

        # UI
        self.main_menu = MainMenu(self.screen)
        self.mission_select = None
        self.pause_menu = PauseMenu(self.screen)
        self.game_over_screen = GameOverScreen(self.screen)
        self.hud = GameHUD(self.screen)
        self.dialogue_box = DialogueBox(self.screen)
        self.mission_briefing = MissionBriefing(self.screen)

        # 特效
        self.muzzle_flash_timer = 0
        self.screen_shake = 0

    def run(self):
        """游戏主循环"""
        print("=" * 50)
        print("   BLACK OPS - 黑色行动")
        print("=" * 50)
        print("\n控制说明:")
        print("  WASD - 移动")
        print("  鼠标 - 瞄准")
        print("  左键/J - 射击")
        print("  右键 - 瞄准镜")
        print("  R - 换弹")
        print("  G - 投掷手雷")
        print("  TAB - 切换武器")
        print("  ESC - 暂停")
        print("=" * 50)

        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            # 处理事件
            self._handle_events()

            # 更新
            self._update(dt)

            # 渲染
            self._draw()

            pygame.display.flip()

        pygame.quit()

    def _handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            # 根据状态分发事件
            if self.state == GameState.MENU:
                self._handle_menu_event(event)
            elif self.state == GameState.MISSION_BRIEFING:
                self._handle_briefing_event(event)
            elif self.state == GameState.PLAYING:
                self._handle_playing_event(event)
            elif self.state == GameState.PAUSED:
                self._handle_pause_event(event)
            elif self.state == GameState.GAME_OVER:
                self._handle_game_over_event(event)
            elif self.state == GameState.MISSION_COMPLETE:
                self._handle_mission_complete_event(event)
            elif self.state == GameState.WEAPON_SELECT:
                self._handle_mission_select_event(event)

    def _handle_menu_event(self, event):
        """处理主菜单事件"""
        action = self.main_menu.handle_event(event)
        if action == 'new_game':
            self._start_mission('mission1')
        elif action == 'select_mission':
            self.mission_select = MissionSelectMenu(self.screen, self.mission_system)
            self.state = GameState.WEAPON_SELECT
        elif action == 'settings':
            pass  # TODO: 设置界面
        elif action == 'quit':
            self.running = False

    def _handle_mission_select_event(self, event):
        """处理关卡选择事件"""
        result = self.mission_select.handle_event(event)
        if result:
            action, data = result
            if action == 'start_mission':
                self._start_mission(data)
            elif action == 'back':
                self.state = GameState.MENU

    def _handle_briefing_event(self, event):
        """处理任务简报事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.state = GameState.PLAYING
                pygame.mouse.set_visible(False)
                pygame.event.set_grab(True)
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU

    def _handle_playing_event(self, event):
        """处理游戏中事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = GameState.PAUSED
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
            elif event.key == pygame.K_SPACE:
                # 跳过对话
                if self.dialogue_box.is_active:
                    self.dialogue_box.skip()
            elif event.key == pygame.K_j:
                # J键射击
                result = self.player.shoot()
                if result:
                    self._process_shot(result)

        # 玩家事件处理
        result = self.player.handle_event(event)
        if result:
            if result['type'] == 'shoot':
                self._process_shot(result)
            elif result['type'] == 'grenade':
                self._throw_grenade(result)

    def _handle_pause_event(self, event):
        """处理暂停菜单事件"""
        action = self.pause_menu.handle_event(event)
        if action == 'resume':
            self.state = GameState.PLAYING
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)
        elif action == 'restart':
            self._start_mission(self.mission_system.current_mission_id)
        elif action == 'quit_menu':
            self.state = GameState.MENU
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)

    def _handle_game_over_event(self, event):
        """处理游戏结束事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self._start_mission(self.mission_system.current_mission_id)
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)

    def _handle_mission_complete_event(self, event):
        """处理任务完成事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                next_mission = self.mission_system.get_next_mission()
                if next_mission:
                    self._start_mission(next_mission)
                else:
                    self.state = GameState.MENU
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)

    def _start_mission(self, mission_id):
        """开始关卡"""
        # 加载关卡数据
        mission_data = self.mission_system.load_mission(mission_id)
        if not mission_data:
            print(f"Failed to load mission: {mission_id}")
            return

        # 加载地图
        map_path = os.path.join(os.path.dirname(__file__), 'maps', mission_data['map'])
        self.game_map.load_from_file(map_path)

        # 设置玩家
        start_pos = self.mission_system.get_player_start()
        start_angle = self.mission_system.get_player_angle()
        self.player = Player(start_pos[0], start_pos[1], start_angle)

        # 设置武器
        loadout = self.mission_system.get_loadout()
        primary = loadout.get('primary', DEFAULT_LOADOUT['primary'])
        secondary = loadout.get('secondary', DEFAULT_LOADOUT['secondary'])

        self.player.add_weapon(Weapon(primary))
        self.player.add_weapon(Weapon(secondary))
        self.player.grenades = loadout.get('grenades', 2)

        # 生成敌人
        self.enemy_manager.spawn_from_mission(mission_data)

        # 生成物品
        self.item_manager.spawn_from_mission(mission_data)

        # 重置统计
        self.stats = {
            'kills': 0,
            'shots_fired': 0,
            'shots_hit': 0,
            'time_played': 0,
        }

        # 显示任务简报
        self.state = GameState.MISSION_BRIEFING
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)

    def _update(self, dt):
        """更新游戏状态"""
        if self.state == GameState.MENU:
            self.main_menu.update(dt)

        elif self.state == GameState.PLAYING:
            self._update_playing(dt)

        elif self.state == GameState.PAUSED:
            pass  # 暂停时不更新

    def _update_playing(self, dt):
        """更新游戏进行中的状态"""
        self.stats['time_played'] += dt

        # 获取输入
        keys = pygame.key.get_pressed()
        mouse_rel = pygame.mouse.get_rel()

        # 限制鼠标移动
        mouse_rel = (
            max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, mouse_rel[0])),
            max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, mouse_rel[1]))
        )

        # 更新玩家
        self.player.update(dt, keys, mouse_rel, self.game_map)

        # 更新武器
        weapon = self.player.get_current_weapon()
        if weapon:
            weapon.update(dt)

        # 持续射击 (自动武器)
        if weapon and weapon.is_auto:
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0] and not self.player.is_reloading:
                result = self.player.shoot()
                if result:
                    self._process_shot(result)

        # 更新敌人
        attacks = self.enemy_manager.update(dt, self.player, self.game_map)

        # 处理敌人攻击
        for attack in attacks:
            self._process_enemy_attack(attack)

        # 更新物品
        pickups = self.item_manager.update(dt, self.player.x, self.player.y)
        for item in pickups:
            self._process_pickup(item)

        # 检查任务目标
        self._check_objectives()

        # 更新对话
        if self.mission_system.has_next_dialogue() and not self.dialogue_box.is_active:
            dialogue = self.mission_system.get_next_dialogue()
            self.dialogue_box.show(dialogue)

        self.dialogue_box.update(dt)

        # 更新HUD
        self.hud.update(dt)

        # 更新特效
        if self.muzzle_flash_timer > 0:
            self.muzzle_flash_timer -= dt
        if self.screen_shake > 0:
            self.screen_shake -= dt * 5

        # 检查玩家死亡
        if not self.player.is_alive:
            self.state = GameState.GAME_OVER

        # 清理死亡敌人
        self.enemy_manager.remove_dead()

    def _process_shot(self, shot_data):
        """处理射击"""
        self.stats['shots_fired'] += 1
        self.muzzle_flash_timer = 0.05
        self.screen_shake = 0.1

        # 射线检测
        hit_enemies = self._raycast_shot(
            self.player.x, self.player.y,
            shot_data['angle'], shot_data['range'],
            shot_data['damage'], shot_data.get('pellets', 1),
            shot_data.get('spread', 0)
        )

        for enemy, damage in hit_enemies:
            self.stats['shots_hit'] += 1
            self.hud.show_hit_marker()

            drops = enemy.take_damage(damage)
            if drops:
                # 敌人死亡
                self.stats['kills'] += 1
                self.hud.add_kill_feed(f"Killed {enemy.type}")

                # 生成掉落物
                for drop in drops:
                    self.item_manager.spawn_drop(enemy.x, enemy.y, drop)

                # 检查击杀目标
                self.mission_system.check_objectives(enemy_type=enemy.type)

    def _raycast_shot(self, start_x, start_y, angle, max_range, damage, pellets=1, spread=0):
        """射线检测射击命中"""
        hit_enemies = []

        for _ in range(pellets):
            # 计算散布
            shot_angle = angle + random.uniform(-spread, spread)
            dx = math.cos(shot_angle)
            dy = math.sin(shot_angle)

            # 逐步检测
            for dist in range(1, int(max_range * 4)):
                check_x = start_x + dx * (dist / 4)
                check_y = start_y + dy * (dist / 4)

                # 检查墙壁
                if self.game_map.is_wall(check_x, check_y):
                    break

                # 检查敌人
                for enemy in self.enemy_manager.get_alive_enemies():
                    ex, ey = enemy.x, enemy.y
                    dist_to_enemy = math.sqrt((check_x - ex) ** 2 + (check_y - ey) ** 2)
                    if dist_to_enemy < 0.5:
                        # 命中
                        hit_enemies.append((enemy, damage))
                        break
                else:
                    continue
                break

        return hit_enemies

    def _process_enemy_attack(self, attack):
        """处理敌人攻击"""
        # 简化的命中检测
        dx = self.player.x - attack['x']
        dy = self.player.y - attack['y']
        dist = math.sqrt(dx * dx + dy * dy)

        if dist < 15:  # 在攻击范围内
            # 根据距离和精度计算命中概率
            hit_chance = attack['enemy'].accuracy * (1 - dist / 20)
            if random.random() < hit_chance:
                # 命中玩家
                damage_angle = math.atan2(dy, dx)
                self.player.take_damage(attack['damage'], damage_angle)
                self.hud.show_damage_indicator(damage_angle)
                self.screen_shake = 0.2

    def _throw_grenade(self, grenade_data):
        """投掷手雷"""
        # TODO: 实现手雷系统
        pass

    def _process_pickup(self, item):
        """处理物品拾取"""
        if item.type == 'health':
            self.player.heal(item.amount)
        elif item.type == 'armor':
            self.player.add_armor(item.amount)
        elif item.type == 'ammo':
            self.player.add_ammo(item.ammo_type, 30)
        elif item.type == 'weapon':
            new_weapon = Weapon(item.weapon_id)
            self.player.add_weapon(new_weapon)
        elif item.type == 'intel':
            self.mission_system.check_objectives(item=item.id)

    def _check_objectives(self):
        """检查任务目标"""
        # 检查位置目标
        completed = self.mission_system.check_objectives(
            player_pos=(self.player.x, self.player.y),
            alive_count=self.enemy_manager.count_alive()
        )

        # 检查任务完成
        if self.mission_system.is_mission_complete():
            self.state = GameState.MISSION_COMPLETE
            self.mission_system.complete_mission()
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)

    def _draw(self):
        """渲染画面"""
        if self.state == GameState.MENU:
            self.main_menu.draw()

        elif self.state == GameState.WEAPON_SELECT:
            self.mission_select.draw()

        elif self.state == GameState.MISSION_BRIEFING:
            self._draw_playing()  # 显示游戏画面作为背景
            self.mission_briefing.draw(self.mission_system.current_mission)

        elif self.state == GameState.PLAYING:
            self._draw_playing()

        elif self.state == GameState.PAUSED:
            self._draw_playing()  # 显示游戏画面作为背景
            self.pause_menu.draw()

        elif self.state == GameState.GAME_OVER:
            self.game_over_screen.draw(False, self.stats)

        elif self.state == GameState.MISSION_COMPLETE:
            self.game_over_screen.draw(True, self.stats)

    def _draw_playing(self):
        """渲染游戏画面"""
        # 应用屏幕抖动
        shake_x = random.randint(-int(self.screen_shake * 10), int(self.screen_shake * 10)) if self.screen_shake > 0 else 0
        shake_y = random.randint(-int(self.screen_shake * 10), int(self.screen_shake * 10)) if self.screen_shake > 0 else 0

        # 光线投射渲染
        self.raycaster.cast_rays(
            self.player.x + shake_x * 0.01,
            self.player.y + shake_y * 0.01,
            self.player.angle
        )

        # 渲染精灵 (敌人和物品)
        sprites = []

        # 添加敌人
        for enemy in self.enemy_manager.enemies:
            if enemy.is_alive or enemy.death_timer < 2:
                sprites.append(enemy)

        # 添加物品
        for item in self.item_manager.get_active_items():
            sprites.append(item)

        self.raycaster.render_sprites(sprites, self.player.x, self.player.y, self.player.angle)

        # 渲染武器
        weapon = self.player.get_current_weapon()
        if weapon:
            if self.player.is_aiming and weapon.has_scope:
                self.weapon_renderer.draw_scope()
            else:
                self.weapon_renderer.draw_weapon(
                    weapon,
                    self.player.is_aiming,
                    weapon.recoil_offset
                )

        # 枪口火焰
        if self.muzzle_flash_timer > 0:
            self._draw_muzzle_flash()

        # HUD
        self.hud.draw(self.player, weapon, self.mission_system)

        # 对话框
        self.dialogue_box.draw()

        # 受伤效果
        if self.player.damage_flash > 0:
            self._draw_damage_effect()

    def _draw_muzzle_flash(self):
        """绘制枪口火焰"""
        weapon = self.player.get_current_weapon()
        if not weapon:
            return

        if self.player.is_aiming and weapon.has_scope:
            # 瞄准镜时不显示
            return

        # 火焰位置
        flash_x = SCREEN_WIDTH - 100
        flash_y = SCREEN_HEIGHT - 120

        size = int(40 * (self.muzzle_flash_timer / 0.05))
        pygame.draw.circle(self.screen, (255, 200, 50), (flash_x, flash_y), size)
        pygame.draw.circle(self.screen, (255, 255, 200), (flash_x, flash_y), size // 2)

    def _draw_damage_effect(self):
        """绘制受伤效果"""
        alpha = int(150 * (self.player.damage_flash / 0.5))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # 红色边框效果
        for i in range(50):
            a = int(alpha * (1 - i / 50))
            pygame.draw.rect(overlay, (200, 0, 0, a), (i, i, SCREEN_WIDTH - i * 2, SCREEN_HEIGHT - i * 2), 1)

        self.screen.blit(overlay, (0, 0))


def main():
    """主函数"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
