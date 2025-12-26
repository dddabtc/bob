#!/usr/bin/env python3
"""
Minecraft 3D - 一个用Python、Pygame和OpenGL制作的3D Minecraft风格游戏

控制方式:
    WASD: 移动
    空格: 跳跃
    Shift: 冲刺
    Ctrl: 潜行
    鼠标移动: 视角
    左键: 挖掘方块/攻击僵尸
    右键: 放置方块
    滚轮/1-9: 选择物品
    E: 打开背包
    ESC: 暂停/菜单
    F3: 调试信息
    F5: 保存游戏
    F6: 加载游戏
    T: 跳到白天 (调试)
    N: 跳到夜晚 (调试)
"""

import sys
import os
import math

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from settings3d import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE,
    RENDER_DISTANCE, CHUNK_SIZE, FOV, NEAR_PLANE, FAR_PLANE
)
from world3d import World
from player3d import Player
from renderer3d import Renderer
from hud3d import HUD, PauseMenu, InventoryScreen
from save_system import save_game, load_game, has_save
from daynight import DayNightCycle
from zombie import ZombieManager
from village3d import generate_fortress


class Game:
    """Minecraft 3D 主游戏类"""

    def __init__(self):
        # 初始化Pygame
        pygame.init()
        pygame.display.set_caption(TITLE)

        # 创建OpenGL窗口
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                               DOUBLEBUF | OPENGL)

        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.inventory_open = False
        self.debug_mode = False

        # 鼠标锁定
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        # HUD 使用2D表面
        self.hud_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        # 显示加载画面
        self._show_loading()

        # 创建世界
        print("正在生成世界...")
        self.world = World()
        print(f"世界种子: {self.world.seed}")

        # 预加载出生点周围的区块
        spawn = self.world.find_spawn_point()
        spawn_chunk_x = int(spawn[0]) // CHUNK_SIZE
        spawn_chunk_z = int(spawn[2]) // CHUNK_SIZE
        print("正在加载区块...")
        self.world.get_chunks_around(spawn_chunk_x, spawn_chunk_z, RENDER_DISTANCE)

        # 创建玩家
        self.player = Player(spawn[0], spawn[1], spawn[2])
        print(f"出生点: ({spawn[0]:.1f}, {spawn[1]:.1f}, {spawn[2]:.1f})")

        # 创建渲染器
        self.renderer = Renderer()

        # 创建HUD
        self.hud = HUD()
        self.pause_menu = PauseMenu()
        self.inventory_screen = InventoryScreen()

        # 创建昼夜循环系统 (从早晨开始)
        self.day_night = DayNightCycle(start_time=0.2)

        # 创建僵尸管理器
        self.zombie_manager = ZombieManager()

        print("游戏启动完成!")
        print("提示: 你有一把无限弹药的枪！左键射击")
        print("提示: 夜晚会有僵尸出没！按T跳到白天，按N跳到夜晚")

    def _show_loading(self):
        """显示加载画面"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        pygame.display.flip()

    def run(self):
        """主游戏循环"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            self._handle_events()

            if not self.paused and not self.inventory_open:
                self._update(dt)

            self._render()

        self._cleanup()

    def _handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

            elif event.type == KEYDOWN:
                self._handle_keydown(event)

            elif event.type == MOUSEBUTTONDOWN:
                if self.inventory_open:
                    mx, my = pygame.mouse.get_pos()
                    self.inventory_screen.handle_click(mx, my, self.player)
                elif not self.paused:
                    self._handle_mousedown(event)

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.player.stop_mining()

            elif event.type == MOUSEMOTION:
                if not self.paused and not self.inventory_open:
                    self.player.handle_mouse_motion(event.rel[0], event.rel[1])

            elif event.type == MOUSEWHEEL:
                if not self.paused:
                    self.player.scroll_slot(event.y)

    def _handle_keydown(self, event):
        """处理按键"""
        if event.key == K_ESCAPE:
            if self.inventory_open:
                self.inventory_open = False
                pygame.mouse.set_visible(False)
                pygame.event.set_grab(True)
            elif self.paused:
                self.paused = False
                pygame.mouse.set_visible(False)
                pygame.event.set_grab(True)
            else:
                self.paused = True
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)

        elif event.key == K_e:
            # 打开/关闭背包
            if not self.paused:
                self.inventory_open = not self.inventory_open
                if self.inventory_open:
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)
                else:
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)

        elif event.key == K_q and self.paused:
            self.running = False

        elif event.key == K_F3:
            self.debug_mode = not self.debug_mode

        elif event.key == K_F5:
            # 保存游戏
            save_game(self.world, self.player)

        elif event.key == K_F6:
            # 加载游戏
            if has_save():
                load_game(self.world, self.player)
                # 重新加载周围区块
                player_chunk_x = math.floor(self.player.x / CHUNK_SIZE)
                player_chunk_z = math.floor(self.player.z / CHUNK_SIZE)
                self.world.get_chunks_around(player_chunk_x, player_chunk_z, RENDER_DISTANCE)
            else:
                print("没有找到存档文件")

        # 数字键选择快捷栏
        elif K_1 <= event.key <= K_9:
            self.player.select_slot(event.key - K_1)

        # 调试：跳到白天
        elif event.key == K_t:
            self.day_night.skip_to_day()
            self.zombie_manager.clear_all()
            print("跳到白天")

        # 调试：跳到夜晚
        elif event.key == K_n:
            self.day_night.skip_to_night()
            print("跳到夜晚 - 小心僵尸！")

    def _handle_mousedown(self, event):
        """处理鼠标按下"""
        target, place_pos = self.player.raycast(self.world)

        if event.button == 1:  # 左键 - 射击
            # 使用枪射击
            self.player.attack(self.zombie_manager)

        elif event.button == 3:  # 右键 - 放置方块（如果有的话）
            self.player.place_block(place_pos, self.world)

    def _update(self, dt):
        """更新游戏状态"""
        keys = pygame.key.get_pressed()

        # 更新昼夜循环
        self.day_night.update(dt)
        self.renderer.update_day_night(self.day_night)

        # 更新玩家
        self.player.update(self.world, keys, dt)

        # 更新僵尸
        self.zombie_manager.update(self.world, self.player, self.day_night, dt)

        # 更新枪和子弹
        self.player.update_gun(self.world, self.zombie_manager, dt)

        # 检查玩家是否死亡
        if self.player.is_dead():
            print("你被僵尸杀死了！正在重生...")
            self.player.respawn(self.world)
            self.zombie_manager.clear_all()

        # 持续射击（按住左键）
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            self.player.attack(self.zombie_manager)

        # 加载新区块
        player_chunk_x = math.floor(self.player.x / CHUNK_SIZE)
        player_chunk_z = math.floor(self.player.z / CHUNK_SIZE)
        self.world.get_chunks_around(player_chunk_x, player_chunk_z, RENDER_DISTANCE)

    def _render(self):
        """渲染画面"""
        # 确保正确的 OpenGL 状态用于 3D 渲染
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(FOV, WINDOW_WIDTH / WINDOW_HEIGHT, NEAR_PLANE, FAR_PLANE)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDisable(GL_FOG)

        # 3D渲染（包含僵尸和子弹）
        bullets = self.player.gun.get_bullets()
        self.renderer.render_world(self.world, self.player, self.zombie_manager.get_zombies(), bullets)

        # 切换到2D模式渲染HUD
        self._setup_2d()

        # 清除HUD表面
        self.hud_surface.fill((0, 0, 0, 0))

        # 渲染HUD
        fps = self.clock.get_fps()
        zombie_count = len(self.zombie_manager.get_zombies())
        self.hud.render(self.hud_surface, self.player, fps, self.debug_mode, self.world,
                       self.day_night, zombie_count)

        # 挖掘进度
        if self.player.is_mining:
            self.hud.render_mining_progress(self.hud_surface, self.player.mining_progress)

        # 背包界面
        if self.inventory_open:
            self.inventory_screen.render(self.hud_surface, self.player)

        # 暂停菜单
        if self.paused:
            self.pause_menu.render(self.hud_surface)

        # 将HUD绘制到屏幕
        self._draw_hud_surface()

        # 恢复3D模式
        self._setup_3d()

        pygame.display.flip()

    def _setup_2d(self):
        """设置2D渲染模式"""
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, WINDOW_WIDTH, WINDOW_HEIGHT, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDisable(GL_FOG)

    def _setup_3d(self):
        """恢复3D渲染模式"""
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        glEnable(GL_DEPTH_TEST)
        # 不启用光照和雾 - 我们使用顶点颜色
        glDisable(GL_LIGHTING)
        glDisable(GL_FOG)

    def _draw_hud_surface(self):
        """将pygame表面绘制到OpenGL"""
        # 获取表面数据 (False = 不翻转)
        texture_data = pygame.image.tostring(self.hud_surface, "RGBA", False)

        # 创建纹理
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, WINDOW_WIDTH, WINDOW_HEIGHT,
                    0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        # 绘制全屏四边形
        glColor4f(1, 1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(0, 0)
        glTexCoord2f(1, 0); glVertex2f(WINDOW_WIDTH, 0)
        glTexCoord2f(1, 1); glVertex2f(WINDOW_WIDTH, WINDOW_HEIGHT)
        glTexCoord2f(0, 1); glVertex2f(0, WINDOW_HEIGHT)
        glEnd()

        # 清理
        glDeleteTextures([texture_id])
        glDisable(GL_TEXTURE_2D)

    def _cleanup(self):
        """清理资源"""
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        pygame.quit()


def main():
    """游戏入口"""
    print("=" * 50)
    print("  Minecraft 3D - 射击版")
    print("=" * 50)
    print()
    print("控制方式:")
    print("  WASD: 移动")
    print("  空格: 跳跃")
    print("  Shift: 冲刺")
    print("  鼠标: 视角")
    print("  左键: 射击（无限弹药）")
    print("  E: 背包")
    print("  ESC: 暂停")
    print("  F3: 调试信息")
    print("  F5: 保存游戏")
    print("  F6: 加载游戏")
    print("  T: 跳到白天")
    print("  N: 跳到夜晚（僵尸出没）")
    print()

    game = Game()
    game.run()


if __name__ == "__main__":
    main()
