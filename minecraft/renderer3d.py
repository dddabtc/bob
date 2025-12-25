# 3D OpenGL 渲染器
import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from settings3d import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FOV, NEAR_PLANE, FAR_PLANE,
    CHUNK_SIZE, WORLD_HEIGHT, RENDER_DISTANCE, BLOCK_SIZE,
    BlockType, BLOCK_DATA, BLOCK_COLORS
)


class Renderer:
    """OpenGL 3D渲染器"""

    def __init__(self):
        self._init_opengl()

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

        # 背景色 (天空)
        glClearColor(0.53, 0.81, 0.92, 1.0)

        # 设置透视投影
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(FOV, WINDOW_WIDTH / WINDOW_HEIGHT, NEAR_PLANE, FAR_PLANE)
        glMatrixMode(GL_MODELVIEW)

        # 禁用光照（使用顶点颜色）
        glDisable(GL_LIGHTING)

        # 禁用雾效果
        glDisable(GL_FOG)

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

    def render_world(self, world, player):
        """渲染世界"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 确保正确的渲染状态
        glDisable(GL_LIGHTING)
        glDisable(GL_FOG)
        glEnable(GL_DEPTH_TEST)

        self.set_camera(player)

        # 获取玩家所在区块
        player_chunk_x = math.floor(player.x / CHUNK_SIZE)
        player_chunk_z = math.floor(player.z / CHUNK_SIZE)

        # 渲染周围区块
        for dx in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
            for dz in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
                chunk_x = player_chunk_x + dx
                chunk_z = player_chunk_z + dz
                key = (chunk_x, chunk_z)
                if key in world.chunks:
                    chunk = world.chunks[key]
                    self._render_chunk_cached(chunk, world)

        # 渲染选中方块高亮
        self._render_block_highlight(player, world)

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
