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

        # 启用面剔除
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

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

        # 简单光照
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [0.5, 1.0, 0.3, 0.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.4, 0.4, 0.4, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])

        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        # 雾效果 (远处渐隐)
        glEnable(GL_FOG)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogfv(GL_FOG_COLOR, [0.53, 0.81, 0.92, 1.0])
        glFogf(GL_FOG_START, RENDER_DISTANCE * CHUNK_SIZE * 0.6)
        glFogf(GL_FOG_END, RENDER_DISTANCE * CHUNK_SIZE)

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

        self.set_camera(player)

        # 获取玩家所在区块
        player_chunk_x = int(player.x) // CHUNK_SIZE
        player_chunk_z = int(player.z) // CHUNK_SIZE

        # 渲染周围区块
        chunks = world.get_chunks_around(player_chunk_x, player_chunk_z, RENDER_DISTANCE)

        # 先渲染不透明方块
        for chunk in chunks:
            self._render_chunk(chunk, world, transparent=False)

        # 再渲染透明方块
        glDepthMask(GL_FALSE)
        for chunk in chunks:
            self._render_chunk(chunk, world, transparent=True)
        glDepthMask(GL_TRUE)

        # 渲染选中方块高亮
        self._render_block_highlight(player, world)

    def _render_chunk(self, chunk, world, transparent=False):
        """渲染单个区块"""
        if chunk.dirty:
            self._build_chunk_mesh(chunk, world)
            chunk.dirty = False

        if chunk.vertex_count == 0:
            return

        world_x = chunk.chunk_x * CHUNK_SIZE
        world_z = chunk.chunk_z * CHUNK_SIZE

        glPushMatrix()
        glTranslatef(world_x, 0, world_z)

        # 使用顶点数组渲染
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)

        if transparent:
            if hasattr(chunk, 'trans_vertices') and chunk.trans_vertex_count > 0:
                glVertexPointer(3, GL_FLOAT, 0, chunk.trans_vertices)
                glColorPointer(4, GL_FLOAT, 0, chunk.trans_colors)
                glNormalPointer(GL_FLOAT, 0, chunk.trans_normals)
                glDrawArrays(GL_QUADS, 0, chunk.trans_vertex_count)
        else:
            if chunk.vertex_count > 0:
                glVertexPointer(3, GL_FLOAT, 0, chunk.mesh_vertices)
                glColorPointer(4, GL_FLOAT, 0, chunk.mesh_colors)
                glNormalPointer(GL_FLOAT, 0, chunk.mesh_normals)
                glDrawArrays(GL_QUADS, 0, chunk.vertex_count)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)

        glPopMatrix()

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
        glEnable(GL_LIGHTING)
        glEnable(GL_FOG)


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
