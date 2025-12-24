"""
狙击枪射击游戏 - Snipe the Bad Guys
使用纯 Pygame 实现伪3D效果
"""

import pygame
import math
import random

# 初始化
pygame.init()

# 屏幕设置
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("狙击手 - Snipe the Bad Guys")

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 200)
YELLOW = (255, 255, 0)
DARK_GREEN = (30, 80, 30)
SKY_BLUE = (135, 180, 250)
BROWN = (139, 90, 43)
GRAY = (100, 100, 100)
SKIN = (255, 200, 150)


class Enemy:
    """敌人"""
    def __init__(self):
        self.reset()

    def reset(self):
        """重置位置"""
        self.x = random.randint(-400, 400)  # 水平位置
        self.distance = random.randint(50, 200)  # 距离
        self.alive = True
        self.color = (random.randint(50, 150), random.randint(30, 80), random.randint(30, 80))
        self.speed_x = random.uniform(-30, 30)
        self.move_timer = 0

    def update(self, dt):
        if not self.alive:
            return

        self.move_timer += dt
        if self.move_timer > 2:
            self.speed_x = random.uniform(-30, 30)
            self.move_timer = 0

        self.x += self.speed_x * dt
        self.x = max(-400, min(400, self.x))

    def get_screen_pos(self, camera_x, camera_y):
        """获取屏幕位置和大小"""
        # 相对于摄像机的位置
        rel_x = self.x - camera_x

        # 透视投影
        scale = 500 / self.distance
        screen_x = SCREEN_WIDTH // 2 + int(rel_x * scale)
        screen_y = SCREEN_HEIGHT // 2 + int(camera_y * scale)

        # 大小随距离变化
        width = int(40 * scale)
        height = int(80 * scale)

        return screen_x, screen_y, width, height

    def draw(self, surface, camera_x, camera_y):
        if not self.alive:
            return

        sx, sy, w, h = self.get_screen_pos(camera_x, camera_y)

        # 检查是否在屏幕内
        if sx < -100 or sx > SCREEN_WIDTH + 100:
            return

        # 身体
        body_rect = pygame.Rect(sx - w//2, sy - h//2, w, h * 2 // 3)
        pygame.draw.rect(surface, self.color, body_rect)

        # 头
        head_size = w // 2
        head_rect = pygame.Rect(sx - head_size//2, sy - h//2 - head_size, head_size, head_size)
        pygame.draw.rect(surface, SKIN, head_rect)

        # 腿
        leg_w = w // 4
        leg_h = h // 3
        pygame.draw.rect(surface, GRAY, (sx - w//3, sy + h//6, leg_w, leg_h))
        pygame.draw.rect(surface, GRAY, (sx + w//6, sy + h//6, leg_w, leg_h))

    def check_hit(self, click_x, click_y, camera_x, camera_y):
        """检查是否被击中"""
        if not self.alive:
            return False

        sx, sy, w, h = self.get_screen_pos(camera_x, camera_y)

        # 扩大点击范围
        hit_rect = pygame.Rect(sx - w, sy - h, w * 2, h * 2)
        return hit_rect.collidepoint(click_x, click_y)


class Game:
    def __init__(self):
        self.camera_x = 0
        self.camera_y = 0  # 上下瞄准
        self.enemies = []
        self.score = 0
        self.kills = 0
        self.ammo = 10
        self.max_ammo = 10
        self.wave = 1
        self.reloading = False
        self.reload_timer = 0
        self.shoot_cooldown = 0
        self.scoped = False
        self.hit_flash = 0
        self.game_over = False

        # 字体
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)

        # 生成敌人
        self.spawn_enemies()

    def spawn_enemies(self):
        """生成敌人"""
        self.enemies.clear()
        count = 5 + self.wave * 2
        for _ in range(count):
            self.enemies.append(Enemy())

    def shoot(self, mx, my):
        """射击"""
        if self.ammo <= 0 or self.reloading or self.shoot_cooldown > 0:
            return

        self.ammo -= 1
        self.shoot_cooldown = 0.3

        # 瞄准镜时点击中心
        if self.scoped:
            mx, my = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        # 检查命中
        for enemy in sorted(self.enemies, key=lambda e: e.distance):
            if enemy.check_hit(mx, my, self.camera_x, self.camera_y):
                enemy.alive = False
                self.kills += 1
                self.score += 100 * self.wave
                self.hit_flash = 0.2
                break

    def reload(self):
        if not self.reloading and self.ammo < self.max_ammo:
            self.reloading = True
            self.reload_timer = 1.5

    def update(self, dt):
        if self.game_over:
            return

        # 冷却
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
        if self.hit_flash > 0:
            self.hit_flash -= dt

        # 换弹
        if self.reloading:
            self.reload_timer -= dt
            if self.reload_timer <= 0:
                self.ammo = self.max_ammo
                self.reloading = False

        # 更新敌人
        for enemy in self.enemies:
            enemy.update(dt)

        # 检查波次
        alive = sum(1 for e in self.enemies if e.alive)
        if alive == 0:
            self.wave += 1
            self.spawn_enemies()
            self.ammo = self.max_ammo

    def draw(self):
        # 天空
        screen.fill(SKY_BLUE)

        # 地面
        pygame.draw.rect(screen, DARK_GREEN, (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))

        # 绘制敌人 (按距离排序，远的先画)
        for enemy in sorted(self.enemies, key=lambda e: -e.distance):
            enemy.draw(screen, self.camera_x, self.camera_y)

        # 瞄准镜效果
        if self.scoped:
            self.draw_scope()
        else:
            self.draw_crosshair()

        # 命中闪烁
        if self.hit_flash > 0:
            self.draw_hit_marker()

        # HUD
        self.draw_hud()

    def draw_crosshair(self):
        """绘制准心"""
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        color = GREEN

        pygame.draw.line(screen, color, (cx - 20, cy), (cx - 5, cy), 2)
        pygame.draw.line(screen, color, (cx + 5, cy), (cx + 20, cy), 2)
        pygame.draw.line(screen, color, (cx, cy - 20), (cx, cy - 5), 2)
        pygame.draw.line(screen, color, (cx, cy + 5), (cx, cy + 20), 2)

    def draw_scope(self):
        """绘制瞄准镜"""
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        radius = 200

        # 黑色遮罩
        mask = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 200))
        pygame.draw.circle(mask, (0, 0, 0, 0), (cx, cy), radius)
        screen.blit(mask, (0, 0))

        # 圆环
        pygame.draw.circle(screen, BLACK, (cx, cy), radius, 3)

        # 十字线
        pygame.draw.line(screen, BLACK, (cx - radius, cy), (cx - 10, cy), 2)
        pygame.draw.line(screen, BLACK, (cx + 10, cy), (cx + radius, cy), 2)
        pygame.draw.line(screen, BLACK, (cx, cy - radius), (cx, cy - 10), 2)
        pygame.draw.line(screen, BLACK, (cx, cy + 10), (cx, cy + radius), 2)

        # 刻度
        for i in range(1, 5):
            y = cy + i * 30
            pygame.draw.line(screen, BLACK, (cx - 5, y), (cx + 5, y), 1)

    def draw_hit_marker(self):
        """绘制命中标记"""
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        pygame.draw.line(screen, RED, (cx - 15, cy - 15), (cx - 5, cy - 5), 3)
        pygame.draw.line(screen, RED, (cx + 15, cy - 15), (cx + 5, cy - 5), 3)
        pygame.draw.line(screen, RED, (cx - 15, cy + 15), (cx - 5, cy + 5), 3)
        pygame.draw.line(screen, RED, (cx + 15, cy + 15), (cx + 5, cy + 5), 3)

    def draw_hud(self):
        """绘制HUD"""
        # 弹药
        ammo_color = RED if self.ammo == 0 else WHITE
        ammo_text = self.font.render(f"弹药: {self.ammo}/{self.max_ammo}", True, ammo_color)
        screen.blit(ammo_text, (50, SCREEN_HEIGHT - 50))

        # 换弹提示
        if self.reloading:
            reload_text = self.font.render("换弹中...", True, YELLOW)
            screen.blit(reload_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50))
            # 进度条
            progress = 1 - (self.reload_timer / 1.5)
            pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 80, 100, 10))
            pygame.draw.rect(screen, YELLOW, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 80, int(100 * progress), 10))

        # 分数
        score_text = self.font.render(f"分数: {self.score}", True, WHITE)
        screen.blit(score_text, (50, 30))

        # 击杀
        kills_text = self.font.render(f"击杀: {self.kills}", True, WHITE)
        screen.blit(kills_text, (50, 60))

        # 波次
        wave_text = self.font.render(f"波次: {self.wave}", True, YELLOW)
        screen.blit(wave_text, (50, 90))

        # 剩余敌人
        alive = sum(1 for e in self.enemies if e.alive)
        enemy_text = self.font.render(f"剩余敌人: {alive}", True, (255, 150, 0))
        screen.blit(enemy_text, (SCREEN_WIDTH - 180, 30))

        # 操作提示
        help_text = self.font.render("J键/左键:射击 | 右键:瞄准 | R:换弹 | WASD:移动视角", True, (180, 180, 180))
        screen.blit(help_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT - 30))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_r:
                self.reload()
            elif event.key == pygame.K_j:
                mx, my = pygame.mouse.get_pos()
                self.shoot(mx, my)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键
                mx, my = pygame.mouse.get_pos()
                self.shoot(mx, my)
            elif event.button == 3:  # 右键
                self.scoped = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                self.scoped = False

        return True

    def run(self):
        clock = pygame.time.Clock()
        running = True

        print("=" * 50)
        print("   狙击手 - Snipe the Bad Guys")
        print("=" * 50)
        print("\n操作说明:")
        print("  鼠标移动 - 瞄准")
        print("  J键/鼠标左键 - 射击")
        print("  鼠标右键(按住) - 开镜")
        print("  R键 - 换弹")
        print("  WASD - 移动视角")
        print("  ESC - 退出")
        print("\n目标: 消灭所有坏蛋!")
        print("=" * 50)

        while running:
            dt = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if not self.handle_event(event):
                    running = False

            # 持续按键检测
            keys = pygame.key.get_pressed()
            move_speed = 200 * dt
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.camera_x -= move_speed
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.camera_x += move_speed
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.camera_y += move_speed * 0.5
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.camera_y -= move_speed * 0.5

            # 限制视角
            self.camera_x = max(-300, min(300, self.camera_x))
            self.camera_y = max(-100, min(100, self.camera_y))

            self.update(dt)
            self.draw()

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
