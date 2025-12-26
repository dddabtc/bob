# 3D OpenGL 渲染器
import math
import random
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from settings3d import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FOV, NEAR_PLANE, FAR_PLANE,
    CHUNK_SIZE, WORLD_HEIGHT, RENDER_DISTANCE, BLOCK_SIZE,
    BlockType, BLOCK_DATA, BLOCK_COLORS
)

# 雾效果设置
FOG_START = 30.0  # 雾开始距离
FOG_END = 80.0    # 雾结束距离（完全不透明）
FOG_COLOR = (0.75, 0.85, 0.95, 1.0)  # 淡蓝色天空雾（默认白天）

# 云层设置
CLOUD_HEIGHT = 100  # 云的高度
CLOUD_SIZE = 8      # 每朵云的大小

# 当前光照强度（由昼夜循环更新）
current_ambient_light = 1.0


class Renderer:
    """OpenGL 3D渲染器"""

    def __init__(self):
        self._init_opengl()
        self._init_clouds()
        self.ambient_light = 1.0
        self.sky_color = (0.53, 0.81, 0.92)
        self.fog_color = FOG_COLOR

    def _init_opengl(self):
        """初始化OpenGL设置"""
        # 启用深度测试
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        # 禁用面剔除（调试用）
        glDisable(GL_CULL_FACE)

        # 启用混合 (透明)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # 背景色 (天空) - 更接近Minecraft的蓝天
        glClearColor(0.53, 0.81, 0.92, 1.0)

        # 设置透视投影
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(FOV, WINDOW_WIDTH / WINDOW_HEIGHT, NEAR_PLANE, FAR_PLANE)
        glMatrixMode(GL_MODELVIEW)

        # 禁用光照（使用顶点颜色）
        glDisable(GL_LIGHTING)

        # 启用雾效果 - 创建大气透视感
        self._setup_fog()

    def _setup_fog(self):
        """设置雾效果"""
        glEnable(GL_FOG)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogfv(GL_FOG_COLOR, FOG_COLOR)
        glFogf(GL_FOG_START, FOG_START)
        glFogf(GL_FOG_END, FOG_END)
        glHint(GL_FOG_HINT, GL_NICEST)

    def _init_clouds(self):
        """初始化云层数据"""
        self.clouds = []
        cloud_rng = random.Random(12345)  # 固定种子保持一致性

        # 生成云朵位置 - 大范围分布
        for _ in range(50):
            cx = cloud_rng.uniform(-200, 200)
            cz = cloud_rng.uniform(-200, 200)
            # 云的形状 - 由多个方块组成
            cloud_blocks = []
            cloud_width = cloud_rng.randint(4, 12)
            cloud_length = cloud_rng.randint(4, 12)

            for dx in range(cloud_width):
                for dz in range(cloud_length):
                    # 使用噪声让云有不规则形状
                    if cloud_rng.random() < 0.7:
                        cloud_blocks.append((dx, dz))

            self.clouds.append({
                'x': cx,
                'z': cz,
                'blocks': cloud_blocks
            })

    def _render_clouds(self, player):
        """渲染云层"""
        glDisable(GL_FOG)  # 云不受雾影响
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # 云的颜色 - 半透明白色
        glColor4f(1.0, 1.0, 1.0, 0.85)

        glBegin(GL_QUADS)
        for cloud in self.clouds:
            # 云跟随玩家移动（视觉上保持在天空）
            base_x = cloud['x'] + int(player.x / 100) * 100
            base_z = cloud['z'] + int(player.z / 100) * 100

            for dx, dz in cloud['blocks']:
                x = base_x + dx
                z = base_z + dz
                y = CLOUD_HEIGHT

                # 渲染云块的顶面（主要可见面）
                glVertex3f(x, y, z)
                glVertex3f(x + 1, y, z)
                glVertex3f(x + 1, y, z + 1)
                glVertex3f(x, y, z + 1)

                # 底面
                glColor4f(0.9, 0.9, 0.9, 0.7)
                glVertex3f(x, y - 1, z + 1)
                glVertex3f(x + 1, y - 1, z + 1)
                glVertex3f(x + 1, y - 1, z)
                glVertex3f(x, y - 1, z)
                glColor4f(1.0, 1.0, 1.0, 0.85)

        glEnd()
        glEnable(GL_FOG)

    def set_camera(self, player):
        """设置摄像机"""
        glLoadIdentity()

        # 获取摄像机位置和方向
        cam_x, cam_y, cam_z = player.get_camera_position()
        dir_x, dir_y, dir_z = player.get_look_direction()

        # 看向的点
        look_x = cam_x + dir_x
        look_y = cam_y + dir_y
        look_z = cam_z + dir_z

        gluLookAt(
            cam_x, cam_y, cam_z,
            look_x, look_y, look_z,
            0, 1, 0
        )

    def update_day_night(self, day_night):
        """更新昼夜循环效果"""
        self.sky_color = day_night.get_sky_color()
        self.fog_color = day_night.get_fog_color()
        self.ambient_light = day_night.get_ambient_light()

        # 更新天空颜色
        glClearColor(self.sky_color[0], self.sky_color[1], self.sky_color[2], 1.0)

        # 更新雾颜色
        glFogfv(GL_FOG_COLOR, self.fog_color)

    def render_world(self, world, player, zombies=None, bullets=None):
        """渲染世界"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 确保正确的渲染状态
        glDisable(GL_LIGHTING)
        glEnable(GL_FOG)  # 启用雾效果
        glEnable(GL_DEPTH_TEST)

        self.set_camera(player)

        # 渲染云层（先渲染远处的对象）
        self._render_clouds(player)

        # 获取玩家所在区块
        player_chunk_x = math.floor(player.x / CHUNK_SIZE)
        player_chunk_z = math.floor(player.z / CHUNK_SIZE)

        # 渲染周围区块
        glEnable(GL_FOG)  # 确保雾效果启用
        for dx in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
            for dz in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
                chunk_x = player_chunk_x + dx
                chunk_z = player_chunk_z + dz
                key = (chunk_x, chunk_z)
                if key in world.chunks:
                    chunk = world.chunks[key]
                    self._render_chunk_cached(chunk, world)

        # 渲染僵尸
        if zombies:
            self._render_zombies(zombies)

        # 渲染子弹
        if bullets:
            self._render_bullets(bullets)

        # 渲染选中方块高亮
        self._render_block_highlight(player, world)

    def _render_bullets(self, bullets):
        """渲染所有子弹"""
        glDisable(GL_FOG)
        glDisable(GL_DEPTH_TEST)  # 子弹总是可见
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)  # 加法混合，发光效果

        for bullet in bullets:
            self._render_bullet(bullet)

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_FOG)

    def _render_bullet(self, bullet):
        """渲染单个子弹"""
        x, y, z = bullet.get_position()

        # 子弹核心 - 黄色发光
        glPointSize(8.0)
        glBegin(GL_POINTS)
        glColor4f(1.0, 0.9, 0.3, 1.0)
        glVertex3f(x, y, z)
        glEnd()

        # 子弹轨迹
        trail = bullet.get_trail()
        if len(trail) > 1:
            glLineWidth(3.0)
            glBegin(GL_LINE_STRIP)
            for i, (tx, ty, tz) in enumerate(trail):
                alpha = (i + 1) / len(trail) * 0.8
                glColor4f(1.0, 0.7, 0.2, alpha)
                glVertex3f(tx, ty, tz)
            # 连接到当前位置
            glColor4f(1.0, 0.9, 0.3, 1.0)
            glVertex3f(x, y, z)
            glEnd()

        glPointSize(1.0)
        glLineWidth(1.0)

    def _render_zombies(self, zombies):
        """渲染所有僵尸"""
        glDisable(GL_FOG)  # 僵尸不受雾影响（保持可见性）

        for zombie in zombies:
            self._render_zombie(zombie)

        glEnable(GL_FOG)

    def _render_zombie(self, zombie):
        """渲染单个僵尸"""
        x, y, z = zombie.get_position()
        color = zombie.get_render_color()

        # 应用环境光
        r = color[0] * self.ambient_light
        g = color[1] * self.ambient_light
        b = color[2] * self.ambient_light

        # 简单的盒子模型表示僵尸
        glBegin(GL_QUADS)

        # 身体 (0.6 x 1.2 x 0.3)
        body_width = 0.3
        body_height = 0.8
        body_depth = 0.2
        body_y = y + 0.6

        # 身体颜色 - 深绿色衣服
        body_r, body_g, body_b = 0.2 * self.ambient_light, 0.35 * self.ambient_light, 0.2 * self.ambient_light

        # 上面
        glColor3f(body_r, body_g, body_b)
        glVertex3f(x - body_width, body_y + body_height, z - body_depth)
        glVertex3f(x + body_width, body_y + body_height, z - body_depth)
        glVertex3f(x + body_width, body_y + body_height, z + body_depth)
        glVertex3f(x - body_width, body_y + body_height, z + body_depth)

        # 下面
        glColor3f(body_r * 0.6, body_g * 0.6, body_b * 0.6)
        glVertex3f(x - body_width, body_y, z + body_depth)
        glVertex3f(x + body_width, body_y, z + body_depth)
        glVertex3f(x + body_width, body_y, z - body_depth)
        glVertex3f(x - body_width, body_y, z - body_depth)

        # 前后左右面
        glColor3f(body_r * 0.8, body_g * 0.8, body_b * 0.8)
        # 前
        glVertex3f(x - body_width, body_y, z - body_depth)
        glVertex3f(x + body_width, body_y, z - body_depth)
        glVertex3f(x + body_width, body_y + body_height, z - body_depth)
        glVertex3f(x - body_width, body_y + body_height, z - body_depth)
        # 后
        glVertex3f(x + body_width, body_y, z + body_depth)
        glVertex3f(x - body_width, body_y, z + body_depth)
        glVertex3f(x - body_width, body_y + body_height, z + body_depth)
        glVertex3f(x + body_width, body_y + body_height, z + body_depth)
        # 左
        glColor3f(body_r * 0.7, body_g * 0.7, body_b * 0.7)
        glVertex3f(x - body_width, body_y, z + body_depth)
        glVertex3f(x - body_width, body_y, z - body_depth)
        glVertex3f(x - body_width, body_y + body_height, z - body_depth)
        glVertex3f(x - body_width, body_y + body_height, z + body_depth)
        # 右
        glVertex3f(x + body_width, body_y, z - body_depth)
        glVertex3f(x + body_width, body_y, z + body_depth)
        glVertex3f(x + body_width, body_y + body_height, z + body_depth)
        glVertex3f(x + body_width, body_y + body_height, z - body_depth)

        # 头部 (0.4 x 0.4 x 0.4)
        head_size = 0.25
        head_y = body_y + body_height

        # 头部颜色 - 僵尸绿皮肤
        glColor3f(r, g, b)

        # 上面
        glVertex3f(x - head_size, head_y + head_size * 2, z - head_size)
        glVertex3f(x + head_size, head_y + head_size * 2, z - head_size)
        glVertex3f(x + head_size, head_y + head_size * 2, z + head_size)
        glVertex3f(x - head_size, head_y + head_size * 2, z + head_size)

        # 下面
        glColor3f(r * 0.6, g * 0.6, b * 0.6)
        glVertex3f(x - head_size, head_y, z + head_size)
        glVertex3f(x + head_size, head_y, z + head_size)
        glVertex3f(x + head_size, head_y, z - head_size)
        glVertex3f(x - head_size, head_y, z - head_size)

        # 前面 - 脸
        glColor3f(r * 0.85, g * 0.85, b * 0.85)
        glVertex3f(x - head_size, head_y, z - head_size)
        glVertex3f(x + head_size, head_y, z - head_size)
        glVertex3f(x + head_size, head_y + head_size * 2, z - head_size)
        glVertex3f(x - head_size, head_y + head_size * 2, z - head_size)

        # 其他面
        glColor3f(r * 0.75, g * 0.75, b * 0.75)
        # 后
        glVertex3f(x + head_size, head_y, z + head_size)
        glVertex3f(x - head_size, head_y, z + head_size)
        glVertex3f(x - head_size, head_y + head_size * 2, z + head_size)
        glVertex3f(x + head_size, head_y + head_size * 2, z + head_size)
        # 左
        glVertex3f(x - head_size, head_y, z + head_size)
        glVertex3f(x - head_size, head_y, z - head_size)
        glVertex3f(x - head_size, head_y + head_size * 2, z - head_size)
        glVertex3f(x - head_size, head_y + head_size * 2, z + head_size)
        # 右
        glVertex3f(x + head_size, head_y, z - head_size)
        glVertex3f(x + head_size, head_y, z + head_size)
        glVertex3f(x + head_size, head_y + head_size * 2, z + head_size)
        glVertex3f(x + head_size, head_y + head_size * 2, z - head_size)

        # 腿部 (两条腿)
        leg_width = 0.12
        leg_height = 0.6

        # 腿的动画偏移
        leg_swing = math.sin(zombie.animation_time * 5) * 0.2 if zombie.state == 'chase' else 0

        # 蓝色裤子
        glColor3f(0.15 * self.ambient_light, 0.15 * self.ambient_light, 0.3 * self.ambient_light)

        for leg_offset in [-0.15, 0.15]:
            leg_x = x + leg_offset
            swing = leg_swing if leg_offset > 0 else -leg_swing

            # 腿的六个面
            # 上
            glVertex3f(leg_x - leg_width, y + leg_height, z - leg_width + swing)
            glVertex3f(leg_x + leg_width, y + leg_height, z - leg_width + swing)
            glVertex3f(leg_x + leg_width, y + leg_height, z + leg_width + swing)
            glVertex3f(leg_x - leg_width, y + leg_height, z + leg_width + swing)
            # 下
            glVertex3f(leg_x - leg_width, y, z + leg_width + swing)
            glVertex3f(leg_x + leg_width, y, z + leg_width + swing)
            glVertex3f(leg_x + leg_width, y, z - leg_width + swing)
            glVertex3f(leg_x - leg_width, y, z - leg_width + swing)
            # 前后左右
            glVertex3f(leg_x - leg_width, y, z - leg_width + swing)
            glVertex3f(leg_x + leg_width, y, z - leg_width + swing)
            glVertex3f(leg_x + leg_width, y + leg_height, z - leg_width + swing)
            glVertex3f(leg_x - leg_width, y + leg_height, z - leg_width + swing)

        glEnd()

    def _render_chunk_cached(self, chunk, world):
        """使用缓存渲染区块"""
        # 如果区块是脏的，重建显示列表
        if chunk.dirty or not hasattr(chunk, 'display_list') or chunk.display_list is None:
            self._build_chunk_display_list(chunk, world)
            chunk.dirty = False

        # 调用显示列表
        if hasattr(chunk, 'display_list') and chunk.display_list is not None:
            glCallList(chunk.display_list)

    def _build_chunk_display_list(self, chunk, world):
        """构建区块的显示列表"""
        # 删除旧的显示列表
        if hasattr(chunk, 'display_list') and chunk.display_list is not None:
            glDeleteLists(chunk.display_list, 1)

        chunk.display_list = glGenLists(1)
        glNewList(chunk.display_list, GL_COMPILE)

        world_x = chunk.chunk_x * CHUNK_SIZE
        world_z = chunk.chunk_z * CHUNK_SIZE

        glBegin(GL_QUADS)
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                for y in range(WORLD_HEIGHT):
                    block = chunk.blocks[x][y][z]
                    if block == BlockType.AIR or block == BlockType.WATER:
                        continue

                    wx, wz = world_x + x, world_z + z

                    # 检查6个面
                    # 上面
                    if y == WORLD_HEIGHT - 1 or chunk.blocks[x][y+1][z] == BlockType.AIR or chunk.blocks[x][y+1][z] == BlockType.WATER:
                        self._add_face_vertices(wx, y, wz, 'top', block)
                    # 下面
                    if y == 0 or chunk.blocks[x][y-1][z] == BlockType.AIR or chunk.blocks[x][y-1][z] == BlockType.WATER:
                        self._add_face_vertices(wx, y, wz, 'bottom', block)
                    # 前面 (Z-)
                    if z == 0:
                        neighbor = world.get_block(wx, y, wz - 1)
                    else:
                        neighbor = chunk.blocks[x][y][z-1]
                    if neighbor == BlockType.AIR or neighbor == BlockType.WATER:
                        self._add_face_vertices(wx, y, wz, 'front', block)
                    # 后面 (Z+)
                    if z == CHUNK_SIZE - 1:
                        neighbor = world.get_block(wx, y, wz + 1)
                    else:
                        neighbor = chunk.blocks[x][y][z+1]
                    if neighbor == BlockType.AIR or neighbor == BlockType.WATER:
                        self._add_face_vertices(wx, y, wz, 'back', block)
                    # 左面 (X-)
                    if x == 0:
                        neighbor = world.get_block(wx - 1, y, wz)
                    else:
                        neighbor = chunk.blocks[x-1][y][z]
                    if neighbor == BlockType.AIR or neighbor == BlockType.WATER:
                        self._add_face_vertices(wx, y, wz, 'left', block)
                    # 右面 (X+)
                    if x == CHUNK_SIZE - 1:
                        neighbor = world.get_block(wx + 1, y, wz)
                    else:
                        neighbor = chunk.blocks[x+1][y][z]
                    if neighbor == BlockType.AIR or neighbor == BlockType.WATER:
                        self._add_face_vertices(wx, y, wz, 'right', block)

        glEnd()
        glEndList()

    def _add_face_vertices(self, x, y, z, face, block_type):
        """添加一个面的顶点到当前GL_QUADS"""
        colors = BLOCK_COLORS.get(block_type, {'all': (0.5, 0.5, 0.5)})
        if 'all' in colors:
            c = colors['all'][:3]
        else:
            if face == 'top':
                c = colors.get('top', (0.5, 0.5, 0.5))[:3]
            elif face == 'bottom':
                c = colors.get('bottom', colors.get('top', (0.5, 0.5, 0.5)))[:3]
            else:
                c = colors.get('side', colors.get('top', (0.5, 0.5, 0.5)))[:3]

        # 光照调整
        if face == 'top':
            light = 1.0
        elif face == 'bottom':
            light = 0.5
        elif face in ('front', 'back'):
            light = 0.85
        else:
            light = 0.7

        glColor3f(c[0] * light, c[1] * light, c[2] * light)

        if face == 'top':
            glVertex3f(x, y+1, z)
            glVertex3f(x+1, y+1, z)
            glVertex3f(x+1, y+1, z+1)
            glVertex3f(x, y+1, z+1)
        elif face == 'bottom':
            glVertex3f(x, y, z+1)
            glVertex3f(x+1, y, z+1)
            glVertex3f(x+1, y, z)
            glVertex3f(x, y, z)
        elif face == 'front':
            glVertex3f(x, y, z)
            glVertex3f(x+1, y, z)
            glVertex3f(x+1, y+1, z)
            glVertex3f(x, y+1, z)
        elif face == 'back':
            glVertex3f(x+1, y, z+1)
            glVertex3f(x, y, z+1)
            glVertex3f(x, y+1, z+1)
            glVertex3f(x+1, y+1, z+1)
        elif face == 'left':
            glVertex3f(x, y, z+1)
            glVertex3f(x, y, z)
            glVertex3f(x, y+1, z)
            glVertex3f(x, y+1, z+1)
        elif face == 'right':
            glVertex3f(x+1, y, z)
            glVertex3f(x+1, y, z+1)
            glVertex3f(x+1, y+1, z+1)
            glVertex3f(x+1, y+1, z)

    def _render_block(self, x, y, z, block_type):
        """渲染单个方块"""
        colors = BLOCK_COLORS.get(block_type, {'all': (0.5, 0.5, 0.5)})

        if 'all' in colors:
            top_color = side_color = bottom_color = colors['all'][:3]
        else:
            top_color = colors.get('top', (0.5, 0.5, 0.5))[:3]
            bottom_color = colors.get('bottom', top_color)[:3]
            side_color = colors.get('side', top_color)[:3]

        glBegin(GL_QUADS)

        # 上面 - 亮度 1.0
        glColor3f(top_color[0], top_color[1], top_color[2])
        glVertex3f(x, y+1, z)
        glVertex3f(x+1, y+1, z)
        glVertex3f(x+1, y+1, z+1)
        glVertex3f(x, y+1, z+1)

        # 下面 - 亮度 0.5
        glColor3f(bottom_color[0]*0.5, bottom_color[1]*0.5, bottom_color[2]*0.5)
        glVertex3f(x, y, z+1)
        glVertex3f(x+1, y, z+1)
        glVertex3f(x+1, y, z)
        glVertex3f(x, y, z)

        # 前面 (Z-) - 亮度 0.85
        glColor3f(side_color[0]*0.85, side_color[1]*0.85, side_color[2]*0.85)
        glVertex3f(x, y, z)
        glVertex3f(x+1, y, z)
        glVertex3f(x+1, y+1, z)
        glVertex3f(x, y+1, z)

        # 后面 (Z+) - 亮度 0.85
        glColor3f(side_color[0]*0.85, side_color[1]*0.85, side_color[2]*0.85)
        glVertex3f(x+1, y, z+1)
        glVertex3f(x, y, z+1)
        glVertex3f(x, y+1, z+1)
        glVertex3f(x+1, y+1, z+1)

        # 左面 (X-) - 亮度 0.7
        glColor3f(side_color[0]*0.7, side_color[1]*0.7, side_color[2]*0.7)
        glVertex3f(x, y, z+1)
        glVertex3f(x, y, z)
        glVertex3f(x, y+1, z)
        glVertex3f(x, y+1, z+1)

        # 右面 (X+) - 亮度 0.75
        glColor3f(side_color[0]*0.75, side_color[1]*0.75, side_color[2]*0.75)
        glVertex3f(x+1, y, z)
        glVertex3f(x+1, y, z+1)
        glVertex3f(x+1, y+1, z+1)
        glVertex3f(x+1, y+1, z)

        glEnd()

    def _render_test_cube(self, x, y, z):
        """渲染测试立方体 - 草方块样式"""
        glBegin(GL_QUADS)
        # 上面 - 草绿色
        glColor3f(0.4, 0.75, 0.25)
        glVertex3f(x, y+1, z)
        glVertex3f(x+1, y+1, z)
        glVertex3f(x+1, y+1, z+1)
        glVertex3f(x, y+1, z+1)
        # 下面 - 泥土
        glColor3f(0.55, 0.35, 0.18)
        glVertex3f(x, y, z+1)
        glVertex3f(x+1, y, z+1)
        glVertex3f(x+1, y, z)
        glVertex3f(x, y, z)
        # 前面 (Z-) - 泥土带草边
        glColor3f(0.5, 0.32, 0.15)
        glVertex3f(x, y, z)
        glVertex3f(x+1, y, z)
        glVertex3f(x+1, y+1, z)
        glVertex3f(x, y+1, z)
        # 后面 (Z+)
        glColor3f(0.48, 0.3, 0.14)
        glVertex3f(x+1, y, z+1)
        glVertex3f(x, y, z+1)
        glVertex3f(x, y+1, z+1)
        glVertex3f(x+1, y+1, z+1)
        # 左面 (X-)
        glColor3f(0.45, 0.28, 0.13)
        glVertex3f(x, y, z+1)
        glVertex3f(x, y, z)
        glVertex3f(x, y+1, z)
        glVertex3f(x, y+1, z+1)
        # 右面 (X+)
        glColor3f(0.52, 0.33, 0.16)
        glVertex3f(x+1, y, z)
        glVertex3f(x+1, y, z+1)
        glVertex3f(x+1, y+1, z+1)
        glVertex3f(x+1, y+1, z)
        glEnd()

    def _render_chunk(self, chunk, world, transparent=False):
        """渲染单个区块"""
        if chunk.dirty:
            self._build_chunk_mesh(chunk, world)
            self._build_display_list(chunk)
            chunk.dirty = False

        # 使用显示列表渲染
        if transparent:
            if hasattr(chunk, 'trans_display_list') and chunk.trans_display_list:
                glCallList(chunk.trans_display_list)
        else:
            if hasattr(chunk, 'display_list') and chunk.display_list:
                glCallList(chunk.display_list)

    def _build_display_list(self, chunk):
        """构建显示列表"""
        world_x = chunk.chunk_x * CHUNK_SIZE
        world_z = chunk.chunk_z * CHUNK_SIZE

        # 不透明方块显示列表
        if chunk.vertex_count > 0:
            chunk.display_list = glGenLists(1)
            glNewList(chunk.display_list, GL_COMPILE)

            glPushMatrix()
            glTranslatef(world_x, 0, world_z)
            glBegin(GL_QUADS)
            for i in range(0, chunk.vertex_count * 3, 3):
                ci = (i // 3) * 4
                glColor4f(chunk.mesh_colors[ci], chunk.mesh_colors[ci+1],
                         chunk.mesh_colors[ci+2], chunk.mesh_colors[ci+3])
                glVertex3f(chunk.mesh_vertices[i], chunk.mesh_vertices[i+1],
                          chunk.mesh_vertices[i+2])
            glEnd()
            glPopMatrix()

            glEndList()
        else:
            chunk.display_list = None

        # 透明方块显示列表
        if chunk.trans_vertex_count > 0:
            chunk.trans_display_list = glGenLists(1)
            glNewList(chunk.trans_display_list, GL_COMPILE)

            glPushMatrix()
            glTranslatef(world_x, 0, world_z)
            glBegin(GL_QUADS)
            for i in range(0, chunk.trans_vertex_count * 3, 3):
                ci = (i // 3) * 4
                glColor4f(chunk.trans_colors[ci], chunk.trans_colors[ci+1],
                         chunk.trans_colors[ci+2], chunk.trans_colors[ci+3])
                glVertex3f(chunk.trans_vertices[i], chunk.trans_vertices[i+1],
                          chunk.trans_vertices[i+2])
            glEnd()
            glPopMatrix()

            glEndList()
        else:
            chunk.trans_display_list = None

    def _build_chunk_mesh(self, chunk, world):
        """构建区块网格"""
        vertices = []
        colors = []
        normals = []
        trans_vertices = []
        trans_colors = []
        trans_normals = []

        world_x = chunk.chunk_x * CHUNK_SIZE
        world_z = chunk.chunk_z * CHUNK_SIZE

        for x in range(CHUNK_SIZE):
            for y in range(WORLD_HEIGHT):
                for z in range(CHUNK_SIZE):
                    block = chunk.blocks[x][y][z]
                    if block == BlockType.AIR:
                        continue

                    data = BLOCK_DATA.get(block, {})
                    is_transparent = data.get('transparent', False)

                    # 获取方块颜色
                    block_colors = BLOCK_COLORS.get(block, {'all': (0.5, 0.5, 0.5)})

                    # 检查每个面是否需要渲染
                    # 上面 (Y+)
                    if not self._is_opaque(chunk, world, x, y + 1, z, world_x, world_z):
                        color = self._get_face_color(block_colors, 'top')
                        self._add_face(
                            x, y, z, 'top', color, is_transparent,
                            vertices, colors, normals,
                            trans_vertices, trans_colors, trans_normals
                        )

                    # 下面 (Y-)
                    if not self._is_opaque(chunk, world, x, y - 1, z, world_x, world_z):
                        color = self._get_face_color(block_colors, 'bottom')
                        self._add_face(
                            x, y, z, 'bottom', color, is_transparent,
                            vertices, colors, normals,
                            trans_vertices, trans_colors, trans_normals
                        )

                    # 前面 (Z-)
                    if not self._is_opaque(chunk, world, x, y, z - 1, world_x, world_z):
                        color = self._get_face_color(block_colors, 'side')
                        self._add_face(
                            x, y, z, 'front', color, is_transparent,
                            vertices, colors, normals,
                            trans_vertices, trans_colors, trans_normals
                        )

                    # 后面 (Z+)
                    if not self._is_opaque(chunk, world, x, y, z + 1, world_x, world_z):
                        color = self._get_face_color(block_colors, 'side')
                        self._add_face(
                            x, y, z, 'back', color, is_transparent,
                            vertices, colors, normals,
                            trans_vertices, trans_colors, trans_normals
                        )

                    # 左面 (X-)
                    if not self._is_opaque(chunk, world, x - 1, y, z, world_x, world_z):
                        color = self._get_face_color(block_colors, 'side')
                        self._add_face(
                            x, y, z, 'left', color, is_transparent,
                            vertices, colors, normals,
                            trans_vertices, trans_colors, trans_normals
                        )

                    # 右面 (X+)
                    if not self._is_opaque(chunk, world, x + 1, y, z, world_x, world_z):
                        color = self._get_face_color(block_colors, 'side')
                        self._add_face(
                            x, y, z, 'right', color, is_transparent,
                            vertices, colors, normals,
                            trans_vertices, trans_colors, trans_normals
                        )

        # 转换为numpy数组
        chunk.mesh_vertices = np.array(vertices, dtype=np.float32)
        chunk.mesh_colors = np.array(colors, dtype=np.float32)
        chunk.mesh_normals = np.array(normals, dtype=np.float32)
        chunk.vertex_count = len(vertices) // 3

        chunk.trans_vertices = np.array(trans_vertices, dtype=np.float32)
        chunk.trans_colors = np.array(trans_colors, dtype=np.float32)
        chunk.trans_normals = np.array(trans_normals, dtype=np.float32)
        chunk.trans_vertex_count = len(trans_vertices) // 3

    def _is_opaque(self, chunk, world, x, y, z, world_x, world_z):
        """检查方块是否不透明"""
        if y < 0 or y >= WORLD_HEIGHT:
            return False

        if 0 <= x < CHUNK_SIZE and 0 <= z < CHUNK_SIZE:
            block = chunk.blocks[x][y][z]
        else:
            block = world.get_block(world_x + x, y, world_z + z)

        if block == BlockType.AIR:
            return False

        return not BLOCK_DATA.get(block, {}).get('transparent', False)

    def _get_face_color(self, block_colors, face):
        """获取面的颜色"""
        if 'all' in block_colors:
            color = block_colors['all']
        elif face in block_colors:
            color = block_colors[face]
        else:
            color = (0.5, 0.5, 0.5)

        # 确保是RGB
        if len(color) >= 3:
            return color[:3]
        return color

    def _add_face(self, x, y, z, face, color, is_transparent,
                  vertices, colors, normals,
                  trans_vertices, trans_colors, trans_normals):
        """添加一个面的顶点"""
        # 面的顶点定义
        face_vertices = {
            'top': [
                (x, y + 1, z), (x + 1, y + 1, z),
                (x + 1, y + 1, z + 1), (x, y + 1, z + 1)
            ],
            'bottom': [
                (x, y, z + 1), (x + 1, y, z + 1),
                (x + 1, y, z), (x, y, z)
            ],
            'front': [
                (x, y, z), (x + 1, y, z),
                (x + 1, y + 1, z), (x, y + 1, z)
            ],
            'back': [
                (x + 1, y, z + 1), (x, y, z + 1),
                (x, y + 1, z + 1), (x + 1, y + 1, z + 1)
            ],
            'left': [
                (x, y, z + 1), (x, y, z),
                (x, y + 1, z), (x, y + 1, z + 1)
            ],
            'right': [
                (x + 1, y, z), (x + 1, y, z + 1),
                (x + 1, y + 1, z + 1), (x + 1, y + 1, z)
            ],
        }

        face_normals = {
            'top': (0, 1, 0),
            'bottom': (0, -1, 0),
            'front': (0, 0, -1),
            'back': (0, 0, 1),
            'left': (-1, 0, 0),
            'right': (1, 0, 0),
        }

        verts = face_vertices[face]
        normal = face_normals[face]

        # 光照调整
        light_factors = {
            'top': 1.0,
            'bottom': 0.5,
            'front': 0.8,
            'back': 0.8,
            'left': 0.7,
            'right': 0.7,
        }
        light = light_factors[face]

        # 调整颜色
        r, g, b = color[0] * light, color[1] * light, color[2] * light
        alpha = 0.7 if is_transparent else 1.0

        target_v = trans_vertices if is_transparent else vertices
        target_c = trans_colors if is_transparent else colors
        target_n = trans_normals if is_transparent else normals

        for vx, vy, vz in verts:
            target_v.extend([vx, vy, vz])
            target_c.extend([r, g, b, alpha])
            target_n.extend(normal)

    def _render_block_highlight(self, player, world):
        """渲染方块选中高亮"""
        target, _ = player.raycast(world)
        if target is None:
            return

        bx, by, bz = target

        # 禁用光照
        glDisable(GL_LIGHTING)
        glDisable(GL_FOG)

        # 线框模式
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glLineWidth(2.0)

        glColor4f(0.1, 0.1, 0.1, 0.8)

        # 绘制立方体线框
        glBegin(GL_QUADS)
        # 稍微放大一点避免z-fighting
        offset = 0.002
        x0, y0, z0 = bx - offset, by - offset, bz - offset
        x1, y1, z1 = bx + 1 + offset, by + 1 + offset, bz + 1 + offset

        # 上
        glVertex3f(x0, y1, z0); glVertex3f(x1, y1, z0)
        glVertex3f(x1, y1, z1); glVertex3f(x0, y1, z1)
        # 下
        glVertex3f(x0, y0, z1); glVertex3f(x1, y0, z1)
        glVertex3f(x1, y0, z0); glVertex3f(x0, y0, z0)
        # 前
        glVertex3f(x0, y0, z0); glVertex3f(x1, y0, z0)
        glVertex3f(x1, y1, z0); glVertex3f(x0, y1, z0)
        # 后
        glVertex3f(x1, y0, z1); glVertex3f(x0, y0, z1)
        glVertex3f(x0, y1, z1); glVertex3f(x1, y1, z1)
        # 左
        glVertex3f(x0, y0, z1); glVertex3f(x0, y0, z0)
        glVertex3f(x0, y1, z0); glVertex3f(x0, y1, z1)
        # 右
        glVertex3f(x1, y0, z0); glVertex3f(x1, y0, z1)
        glVertex3f(x1, y1, z1); glVertex3f(x1, y1, z0)
        glEnd()

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        # 保持光照和雾禁用（我们使用顶点颜色）


def render_crosshair(screen):
    """渲染准星"""
    cx = WINDOW_WIDTH // 2
    cy = WINDOW_HEIGHT // 2
    size = 15
    thickness = 2

    # 白色准星
    color = (255, 255, 255)
    pygame.draw.line(screen, color, (cx - size, cy), (cx + size, cy), thickness)
    pygame.draw.line(screen, color, (cx, cy - size), (cx, cy + size), thickness)
