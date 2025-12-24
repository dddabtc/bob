"""
Black Ops - 高画质光线投射渲染引擎
实现类似COD的伪3D效果
"""

import pygame
import math
import random
from settings import *


class Raycaster:
    """高画质光线投射渲染器"""

    def __init__(self, screen, game_map):
        self.screen = screen
        self.game_map = game_map
        self.z_buffer = [0] * NUM_RAYS

        # 预计算
        self.screen_dist = (SCREEN_WIDTH // 2) / math.tan(HALF_FOV)

        # 生成高质量纹理
        self.textures = self._generate_hd_textures()

        # 预渲染天空
        self.sky_surface = self._create_sky()

        # 预渲染地面
        self.floor_surface = self._create_floor()

    def _create_sky(self):
        """创建高质量天空"""
        sky = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT // 2))

        # 渐变天空
        for y in range(SCREEN_HEIGHT // 2):
            ratio = y / (SCREEN_HEIGHT // 2)
            r = int(40 + 80 * (1 - ratio))
            g = int(80 + 100 * (1 - ratio))
            b = int(120 + 100 * (1 - ratio))
            pygame.draw.line(sky, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # 添加云彩
        random.seed(12345)  # 固定种子保证一致性
        for _ in range(15):
            cx = random.randint(0, SCREEN_WIDTH)
            cy = random.randint(20, SCREEN_HEIGHT // 3)
            for i in range(5):
                offset_x = random.randint(-40, 40)
                offset_y = random.randint(-10, 10)
                size = random.randint(20, 50)
                alpha = random.randint(30, 80)
                cloud = pygame.Surface((size * 2, size), pygame.SRCALPHA)
                pygame.draw.ellipse(cloud, (255, 255, 255, alpha), (0, 0, size * 2, size))
                sky.blit(cloud, (cx + offset_x - size, cy + offset_y - size // 2))

        return sky

    def _create_floor(self):
        """创建高质量地面"""
        floor = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT // 2))

        for y in range(SCREEN_HEIGHT // 2):
            ratio = y / (SCREEN_HEIGHT // 2)
            # 距离感渐变
            shade = int(30 + 40 * (1 - ratio * 0.5))
            # 添加一点颜色变化
            r = shade
            g = int(shade * 0.9)
            b = int(shade * 0.8)
            pygame.draw.line(floor, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        return floor

    def _generate_hd_textures(self):
        """生成简单纹理（快速加载）"""
        textures = {}
        size = TEXTURE_SIZE

        # 纹理1: 灰色混凝土
        tex1 = pygame.Surface((size, size))
        tex1.fill((110, 110, 115))
        for y in range(0, size, 4):
            shade = 100 + (y % 20)
            pygame.draw.line(tex1, (shade, shade, shade), (0, y), (size, y))
        textures[1] = tex1

        # 纹理2: 木墙
        tex2 = pygame.Surface((size, size))
        tex2.fill((120, 75, 45))
        plank_h = size // 4
        for py in range(0, size, plank_h):
            pygame.draw.rect(tex2, (110, 65, 35), (0, py, size, plank_h - 2))
            pygame.draw.line(tex2, (40, 25, 15), (0, py + plank_h - 1), (size, py + plank_h - 1), 2)
        textures[2] = tex2

        # 纹理3: 金属墙
        tex3 = pygame.Surface((size, size))
        tex3.fill((80, 85, 95))
        panel = size // 2
        for py in range(0, size, panel):
            for px in range(0, size, panel):
                pygame.draw.rect(tex3, (90, 95, 105), (px + 4, py + 4, panel - 8, panel - 8))
                pygame.draw.rect(tex3, (60, 65, 75), (px + 4, py + 4, panel - 8, panel - 8), 2)
        textures[3] = tex3

        # 纹理4: 军事绿
        tex4 = pygame.Surface((size, size))
        tex4.fill((70, 85, 55))
        pygame.draw.rect(tex4, (200, 180, 50), (size // 2 - 20, size // 2 - 20, 40, 40), 3)
        pygame.draw.line(tex4, (200, 180, 50), (size // 2 - 15, size // 2), (size // 2 + 15, size // 2), 2)
        pygame.draw.line(tex4, (200, 180, 50), (size // 2, size // 2 - 15), (size // 2, size // 2 + 15), 2)
        textures[4] = tex4

        # 纹理5: 红砖
        tex5 = pygame.Surface((size, size))
        tex5.fill((65, 65, 65))
        brick_w, brick_h = max(16, size // 4), max(8, size // 8)
        for row in range(size // brick_h + 1):
            offset = (brick_w // 2) if row % 2 else 0
            for col in range(-1, size // brick_w + 2):
                bx = col * brick_w + offset
                by = row * brick_h
                pygame.draw.rect(tex5, (150, 60, 45), (bx + 1, by + 1, brick_w - 2, brick_h - 2))
        textures[5] = tex5

        # 纹理6: 门
        tex6 = pygame.Surface((size, size))
        tex6.fill((60, 40, 25))
        pygame.draw.rect(tex6, (40, 25, 15), (0, 0, size, size), 8)
        pygame.draw.rect(tex6, (70, 50, 35), (15, 15, size - 30, size // 2 - 20))
        pygame.draw.rect(tex6, (70, 50, 35), (15, size // 2 + 5, size - 30, size // 2 - 20))
        pygame.draw.circle(tex6, (180, 160, 60), (size - 25, size // 2), 8)
        textures[6] = tex6

        return textures

    def cast_rays(self, player_x, player_y, player_angle):
        """高质量光线投射渲染"""
        # 绘制天空和地面
        self.screen.blit(self.sky_surface, (0, 0))
        self.screen.blit(self.floor_surface, (0, SCREEN_HEIGHT // 2))

        ray_angle = player_angle - HALF_FOV

        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # 垂直墙壁检测
            x_vert, y_vert, depth_vert, texture_vert = self._cast_ray_vertical(
                player_x, player_y, sin_a, cos_a
            )

            # 水平墙壁检测
            x_horiz, y_horiz, depth_horiz, texture_horiz = self._cast_ray_horizontal(
                player_x, player_y, sin_a, cos_a
            )

            # 选择更近的
            if depth_vert < depth_horiz:
                depth = depth_vert
                texture = texture_vert
                offset = y_vert % 1
                is_vertical = True
            else:
                depth = depth_horiz
                texture = texture_horiz
                offset = x_horiz % 1
                is_vertical = False

            # 修正鱼眼效果
            depth *= math.cos(player_angle - ray_angle)

            # 存储深度
            self.z_buffer[ray] = depth

            # 计算墙壁高度
            if depth > 0.001:
                wall_height = self.screen_dist / depth
            else:
                wall_height = SCREEN_HEIGHT

            # 绘制墙壁
            self._draw_wall_stripe_hd(ray, wall_height, texture, offset, depth, is_vertical)

            ray_angle += DELTA_ANGLE

    def _cast_ray_vertical(self, px, py, sin_a, cos_a):
        """垂直墙壁检测"""
        texture = 1

        if cos_a > 0:
            x = int(px) + 1
            dx = 1
        elif cos_a < 0:
            x = int(px) - 0.000001
            dx = -1
        else:
            return px, py, MAX_DEPTH, texture

        depth = (x - px) / cos_a
        y = py + depth * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for _ in range(MAX_DEPTH):
            tile_x = int(x)
            tile_y = int(y)

            if 0 <= tile_x < self.game_map.width and 0 <= tile_y < self.game_map.height:
                tile = self.game_map.get_tile(tile_x, tile_y)
                if tile > 0:
                    texture = tile
                    return x, y, depth, texture

            x += dx
            y += dy
            depth += delta_depth

        return x, y, MAX_DEPTH, texture

    def _cast_ray_horizontal(self, px, py, sin_a, cos_a):
        """水平墙壁检测"""
        texture = 1

        if sin_a > 0:
            y = int(py) + 1
            dy = 1
        elif sin_a < 0:
            y = int(py) - 0.000001
            dy = -1
        else:
            return px, py, MAX_DEPTH, texture

        depth = (y - py) / sin_a
        x = px + depth * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for _ in range(MAX_DEPTH):
            tile_x = int(x)
            tile_y = int(y)

            if 0 <= tile_x < self.game_map.width and 0 <= tile_y < self.game_map.height:
                tile = self.game_map.get_tile(tile_x, tile_y)
                if tile > 0:
                    texture = tile
                    return x, y, depth, texture

            x += dx
            y += dy
            depth += delta_depth

        return x, y, MAX_DEPTH, texture

    def _draw_wall_stripe_hd(self, ray, wall_height, texture_id, offset, depth, is_vertical):
        """高质量墙壁渲染"""
        wall_height = min(wall_height, SCREEN_HEIGHT * 2)

        wall_top = int((SCREEN_HEIGHT - wall_height) / 2)
        x = ray * SCALE

        # 获取纹理
        texture = self.textures.get(texture_id, self.textures[1])

        # 计算纹理列
        tex_x = int(offset * TEXTURE_SIZE)
        if tex_x >= TEXTURE_SIZE:
            tex_x = TEXTURE_SIZE - 1

        # 提取纹理列
        tex_column = texture.subsurface((tex_x, 0, 1, TEXTURE_SIZE))

        if wall_height > 0:
            # 缩放纹理列
            column_width = max(1, SCALE)
            scaled_column = pygame.transform.scale(tex_column, (column_width, int(wall_height)))

            # 计算光照
            # 距离衰减 (更平滑的曲线)
            distance_shade = max(0.15, 1 - (depth / MAX_DEPTH) ** 0.6)

            # 垂直墙壁稍暗 (模拟侧光)
            if is_vertical:
                distance_shade *= 0.75

            # 环境光
            final_shade = AMBIENT_LIGHT + (1 - AMBIENT_LIGHT) * distance_shade

            # 雾效果
            if ENABLE_FOG and depth > FOG_START:
                fog_ratio = min(1, (depth - FOG_START) / (FOG_END - FOG_START))
                fog_color = (90, 100, 120)  # 蓝灰色雾

                # 混合雾色
                fog_surface = pygame.Surface(scaled_column.get_size())
                fog_surface.fill(fog_color)
                fog_surface.set_alpha(int(fog_ratio * 220))
                scaled_column.blit(fog_surface, (0, 0))

            # 应用阴影
            if final_shade < 1:
                dark_surface = pygame.Surface(scaled_column.get_size())
                dark_surface.fill((0, 0, 0))
                dark_surface.set_alpha(int((1 - final_shade) * 255))
                scaled_column.blit(dark_surface, (0, 0))

            self.screen.blit(scaled_column, (x, wall_top))

    def render_sprites(self, sprites, player_x, player_y, player_angle):
        """渲染精灵"""
        sprites_to_render = []

        for sprite in sprites:
            dx = sprite.x - player_x
            dy = sprite.y - player_y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < 0.5:
                continue

            theta = math.atan2(dy, dx)
            delta = theta - player_angle

            while delta > math.pi:
                delta -= 2 * math.pi
            while delta < -math.pi:
                delta += 2 * math.pi

            if abs(delta) > HALF_FOV + 0.3:
                continue

            sprites_to_render.append({
                'sprite': sprite,
                'distance': distance,
                'delta': delta,
            })

        sprites_to_render.sort(key=lambda s: -s['distance'])

        for data in sprites_to_render:
            self._draw_sprite_hd(data, player_x, player_y)

    def _draw_sprite_hd(self, data, player_x, player_y):
        """高质量精灵渲染"""
        sprite = data['sprite']
        distance = data['distance']
        delta = data['delta']

        screen_x = int((delta / FOV + 0.5) * SCREEN_WIDTH)

        sprite_height = min(int(self.screen_dist / distance * 1.2), SCREEN_HEIGHT)
        sprite_width = sprite_height

        draw_x = screen_x - sprite_width // 2
        draw_y = (SCREEN_HEIGHT - sprite_height) // 2

        # 深度测试
        center_ray = int(screen_x / max(1, SCALE))
        if 0 <= center_ray < NUM_RAYS:
            if self.z_buffer[center_ray] < distance * 0.9:
                return

        # 获取精灵图像
        sprite_surface = sprite.get_sprite_surface(sprite_width, sprite_height)

        # 应用光照和雾
        darkness = max(0.2, 1 - (distance / MAX_DEPTH) ** 0.6)

        if ENABLE_FOG and distance > FOG_START:
            fog_ratio = min(1, (distance - FOG_START) / (FOG_END - FOG_START))
            fog_surface = pygame.Surface(sprite_surface.get_size())
            fog_surface.fill((90, 100, 120))
            fog_surface.set_alpha(int(fog_ratio * 180))
            sprite_surface.blit(fog_surface, (0, 0))

        dark_overlay = pygame.Surface(sprite_surface.get_size())
        dark_overlay.fill((0, 0, 0))
        dark_overlay.set_alpha(int((1 - darkness) * 200))
        sprite_surface.blit(dark_overlay, (0, 0))

        self.screen.blit(sprite_surface, (draw_x, draw_y))


class GameMap:
    """游戏地图"""

    def __init__(self):
        self.width = 0
        self.height = 0
        self.tiles = []
        self.player_start = (2, 2)
        self.player_angle = 0
        self.enemies_data = []
        self.items_data = []

    def load_from_string(self, map_string):
        """从字符串加载地图"""
        lines = [line for line in map_string.strip().split('\n')
                 if line and not line.startswith('# ')]
        self.height = len(lines)
        self.width = max(len(line) for line in lines) if lines else 0

        self.tiles = []
        for y, line in enumerate(lines):
            row = []
            for x, char in enumerate(line):
                tile_value = MAP_SYMBOLS.get(char, 0)
                row.append(tile_value)

                if char == 'S':
                    self.player_start = (x + 0.5, y + 0.5)
                elif char == 'E':
                    self.enemies_data.append((x + 0.5, y + 0.5))
                elif char == 'I':
                    self.items_data.append((x + 0.5, y + 0.5))

            while len(row) < self.width:
                row.append(0)
            self.tiles.append(row)

    def load_from_file(self, filepath):
        """从文件加载地图"""
        try:
            with open(filepath, 'r') as f:
                self.load_from_string(f.read())
        except FileNotFoundError:
            print(f"地图文件未找到: {filepath}")
            self._create_default_map()

    def _create_default_map(self):
        """创建默认地图"""
        default_map = """
################################
#S.............................#
#......##########..............#
#......#........#..............#
#......#........#....##########
#......#........#....#........#
#......##########....#........#
#....................#........#
#########............##########                     
#.......#......................#                   
#.......#....##########........#                    
#.......#....#........#........#                    
#.......#....#........#........#                  
#.......#....#........##########                    
#.......#....#..................#                   
#.......#....##########........#                    
#.......#......................#                    
#.......#....###################                   
#..............................#
#.......#......................#
###############################
"""
        self.load_from_string(default_map)

    def get_tile(self, x, y):
        """获取瓦片"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return 1

    def is_wall(self, x, y):
        """检查墙壁"""
        return self.get_tile(int(x), int(y)) > 0

    def is_walkable(self, x, y, radius=0.2):
        """检查可行走"""
        for dx in [-radius, radius]:
            for dy in [-radius, radius]:
                if self.is_wall(x + dx, y + dy):
                    return False
        return True
