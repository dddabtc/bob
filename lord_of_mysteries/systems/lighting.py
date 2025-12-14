"""
光影系统 - 动态光照效果
"""

import pygame
import math


class Light:
    """单个光源"""

    def __init__(self, x, y, radius, color, intensity=1.0, flicker=False):
        self.x = x
        self.y = y
        self.radius = radius
        self.base_radius = radius
        self.color = color
        self.intensity = intensity
        self.flicker = flicker
        self.flicker_timer = 0
        self.flicker_offset = 0

    def update(self, dt):
        """更新光源"""
        if self.flicker:
            self.flicker_timer += dt * 8
            self.flicker_offset = math.sin(self.flicker_timer) * 0.15
            self.radius = self.base_radius * (1 + self.flicker_offset)

    def set_position(self, x, y):
        """设置位置"""
        self.x = x
        self.y = y


class LightingSystem:
    """光影系统"""

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 光照表面（用于混合）
        self.light_surface = pygame.Surface(
            (screen_width, screen_height),
            pygame.SRCALPHA
        )

        # 环境光强度（0-255，越低越暗）
        self.ambient_light = 40

        # 光源列表
        self.lights = []

        # 玩家光源（始终存在）
        self.player_light = None

        # 预渲染的光照贴图缓存
        self._light_cache = {}

    def set_ambient(self, level):
        """设置环境光强度 (0-255)"""
        self.ambient_light = max(0, min(255, level))

    def add_light(self, light):
        """添加光源"""
        self.lights.append(light)
        return light

    def remove_light(self, light):
        """移除光源"""
        if light in self.lights:
            self.lights.remove(light)

    def clear_lights(self):
        """清除所有临时光源"""
        self.lights.clear()

    def create_player_light(self, x, y, pathway_color):
        """创建玩家光源"""
        # 玩家有一个较大的主光源和一个小的核心光源
        self.player_light = Light(
            x, y,
            radius=180,
            color=pathway_color,
            intensity=0.8,
            flicker=True
        )
        return self.player_light

    def add_skill_light(self, x, y, color, radius=100, duration=0.5):
        """添加技能光效"""
        light = SkillLight(x, y, radius, color, duration)
        self.lights.append(light)
        return light

    def add_explosion_light(self, x, y, color, max_radius=200, duration=0.3):
        """添加爆炸光效"""
        light = ExplosionLight(x, y, max_radius, color, duration)
        self.lights.append(light)
        return light

    def update(self, dt):
        """更新所有光源"""
        # 更新玩家光源
        if self.player_light:
            self.player_light.update(dt)

        # 更新临时光源
        for light in self.lights[:]:
            light.update(dt)
            # 移除已结束的光源
            if hasattr(light, 'is_finished') and light.is_finished():
                self.lights.remove(light)

    def _get_light_surface(self, radius, color, intensity):
        """获取或创建光照贴图"""
        # 使用缓存避免重复创建
        cache_key = (int(radius), color, int(intensity * 100))

        if cache_key not in self._light_cache:
            size = int(radius * 2)
            if size <= 0:
                return None

            surface = pygame.Surface((size, size), pygame.SRCALPHA)
            center = radius

            # 创建渐变光照
            for r in range(int(radius), 0, -2):
                alpha = int(255 * intensity * (r / radius) ** 0.5)
                alpha = min(255, max(0, alpha))

                # 混合颜色
                light_color = (
                    min(255, color[0]),
                    min(255, color[1]),
                    min(255, color[2]),
                    alpha
                )
                pygame.draw.circle(surface, light_color, (center, center), r)

            self._light_cache[cache_key] = surface

            # 限制缓存大小
            if len(self._light_cache) > 50:
                # 移除最旧的缓存
                oldest_key = next(iter(self._light_cache))
                del self._light_cache[oldest_key]

        return self._light_cache[cache_key]

    def render(self, screen):
        """渲染光影效果"""
        # 创建暗色遮罩
        self.light_surface.fill((0, 0, 0, 255 - self.ambient_light))

        # 渲染玩家光源
        if self.player_light:
            self._render_light(self.player_light)

        # 渲染其他光源
        for light in self.lights:
            self._render_light(light)

        # 将光照层混合到屏幕
        screen.blit(self.light_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def _render_light(self, light):
        """渲染单个光源"""
        if light.radius <= 0:
            return

        # 获取光照贴图
        light_tex = self._create_radial_gradient(light)
        if light_tex is None:
            return

        # 计算绘制位置
        x = int(light.x - light.radius)
        y = int(light.y - light.radius)

        # 使用加法混合
        self.light_surface.blit(
            light_tex,
            (x, y),
            special_flags=pygame.BLEND_RGBA_ADD
        )

    def _create_radial_gradient(self, light):
        """创建径向渐变光照"""
        size = int(light.radius * 2)
        if size <= 0:
            return None

        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = light.radius

        # 分层渐变以获得更平滑的效果
        layers = min(int(light.radius / 3), 30)
        for i in range(layers, 0, -1):
            ratio = i / layers
            r = int(light.radius * ratio)

            # 使用平方根衰减获得更自然的效果
            alpha = int(255 * light.intensity * (1 - ratio ** 2))
            alpha = min(255, max(0, alpha))

            color = (
                min(255, light.color[0] + 30),
                min(255, light.color[1] + 30),
                min(255, light.color[2] + 30),
                alpha
            )
            pygame.draw.circle(surface, color, (int(center), int(center)), r)

        return surface


class SkillLight(Light):
    """技能光效"""

    def __init__(self, x, y, radius, color, duration):
        super().__init__(x, y, radius, color, intensity=1.0)
        self.duration = duration
        self.elapsed = 0
        self.max_radius = radius

    def update(self, dt):
        self.elapsed += dt
        # 光效逐渐减弱
        progress = self.elapsed / self.duration
        self.intensity = 1.0 - progress
        self.radius = self.max_radius * (1.0 - progress * 0.5)

    def is_finished(self):
        return self.elapsed >= self.duration


class ExplosionLight(Light):
    """爆炸光效"""

    def __init__(self, x, y, max_radius, color, duration):
        super().__init__(x, y, 0, color, intensity=1.5)
        self.max_radius = max_radius
        self.duration = duration
        self.elapsed = 0

    def update(self, dt):
        self.elapsed += dt
        progress = self.elapsed / self.duration

        if progress < 0.3:
            # 快速扩张
            self.radius = self.max_radius * (progress / 0.3)
            self.intensity = 1.5
        else:
            # 逐渐消退
            fade = (progress - 0.3) / 0.7
            self.radius = self.max_radius
            self.intensity = 1.5 * (1 - fade)

    def is_finished(self):
        return self.elapsed >= self.duration


class WindowLight(Light):
    """窗户光效（用于背景建筑）"""

    def __init__(self, x, y, width, height, color=(255, 200, 100)):
        super().__init__(x + width / 2, y + height / 2, max(width, height), color, intensity=0.3)
        self.width = width
        self.height = height
        self.on = True
        self.flicker_chance = 0.001  # 闪烁概率

    def update(self, dt):
        import random
        # 随机闪烁
        if random.random() < self.flicker_chance:
            self.on = not self.on

        self.intensity = 0.3 if self.on else 0


class TorchLight(Light):
    """火把光效"""

    def __init__(self, x, y):
        super().__init__(
            x, y,
            radius=80,
            color=(255, 150, 50),
            intensity=0.7,
            flicker=True
        )
