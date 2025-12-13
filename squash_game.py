"""
壁球游戏 - Squash Game
使用 Pygame 实现的简单壁球游戏
"""

import pygame
import sys
import random

# 初始化 Pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (50, 100, 255)
GREEN = (50, 255, 50)
GRAY = (100, 100, 100)

# 球拍设置
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 8

# 球设置
BALL_SIZE = 15
BALL_SPEED_X = 6
BALL_SPEED_Y = 6


class Paddle:
    """球拍类"""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED
        self.score = 0

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)


class Ball:
    """球类"""
    def __init__(self):
        self.reset()

    def reset(self):
        """重置球的位置和速度"""
        self.rect = pygame.Rect(
            SCREEN_WIDTH // 2 - BALL_SIZE // 2,
            SCREEN_HEIGHT // 2 - BALL_SIZE // 2,
            BALL_SIZE,
            BALL_SIZE
        )
        # 随机方向
        self.speed_x = BALL_SPEED_X * random.choice([-1, 1])
        self.speed_y = BALL_SPEED_Y * random.choice([-1, 1])

    def move(self):
        """移动球"""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 上下边界反弹
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y = -self.speed_y
            return "wall"

        # 右边墙壁反弹（壁球的墙）
        if self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
            return "wall"

        return None

    def check_paddle_collision(self, paddle):
        """检查与球拍的碰撞"""
        if self.rect.colliderect(paddle.rect):
            if self.speed_x < 0:  # 只有球向左移动时才反弹
                self.speed_x = -self.speed_x
                # 将球移到球拍右侧，防止重复碰撞
                self.rect.left = paddle.rect.right + 1
                # 根据击球位置调整垂直速度
                relative_hit = (self.rect.centery - paddle.rect.centery) / (PADDLE_HEIGHT / 2)
                self.speed_y = relative_hit * BALL_SPEED_Y
                # 稍微加速
                self.speed_x *= 1.02
                return True
        return False

    def is_out(self):
        """检查球是否出界（左边界）"""
        return self.rect.left <= 0

    def draw(self, screen):
        pygame.draw.ellipse(screen, RED, self.rect)
        pygame.draw.ellipse(screen, WHITE, self.rect, 2)


class Game:
    """游戏主类"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("壁球游戏 - Squash Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

        # 游戏对象
        self.paddle = Paddle(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball()

        # 游戏状态
        self.running = True
        self.paused = False
        self.game_over = False
        self.hits = 0
        self.best_score = 0

    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.restart()
                    else:
                        self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.restart()

    def handle_input(self):
        """处理持续按键输入"""
        if self.paused or self.game_over:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.paddle.move_up()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.paddle.move_down()

    def update(self):
        """更新游戏状态"""
        if self.paused or self.game_over:
            return

        # 移动球
        self.ball.move()

        # 检查球拍碰撞
        if self.ball.check_paddle_collision(self.paddle):
            self.hits += 1

        # 检查是否出界
        if self.ball.is_out():
            self.game_over = True
            if self.hits > self.best_score:
                self.best_score = self.hits

    def draw_court(self):
        """绘制球场"""
        # 背景
        self.screen.fill(BLACK)

        # 右边墙壁
        pygame.draw.rect(self.screen, GRAY, (SCREEN_WIDTH - 10, 0, 10, SCREEN_HEIGHT))

        # 上下边界线
        pygame.draw.line(self.screen, WHITE, (0, 0), (SCREEN_WIDTH, 0), 3)
        pygame.draw.line(self.screen, WHITE, (0, SCREEN_HEIGHT - 1), (SCREEN_WIDTH, SCREEN_HEIGHT - 1), 3)

    def draw_ui(self):
        """绘制用户界面"""
        # 当前得分
        score_text = self.font.render(str(self.hits), True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

        # 最高分
        best_text = self.small_font.render(f"Best: {self.best_score}", True, GREEN)
        self.screen.blit(best_text, (SCREEN_WIDTH - 150, 20))

        # 暂停提示
        if self.paused:
            pause_text = self.font.render("PAUSED", True, WHITE)
            self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2,
                                          SCREEN_HEIGHT // 2 - pause_text.get_height() // 2))
            hint_text = self.small_font.render("Press SPACE to continue", True, WHITE)
            self.screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 + 50))

        # 游戏结束
        if self.game_over:
            over_text = self.font.render("GAME OVER", True, RED)
            self.screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 - over_text.get_height() // 2))
            score_text = self.small_font.render(f"Score: {self.hits}", True, WHITE)
            self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                                          SCREEN_HEIGHT // 2 + 50))
            hint_text = self.small_font.render("Press SPACE to restart", True, WHITE)
            self.screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 + 90))

    def draw_instructions(self):
        """绘制操作说明"""
        instructions = [
            "W/↑: Move Up",
            "S/↓: Move Down",
            "SPACE: Pause",
            "R: Restart",
            "ESC: Quit"
        ]
        y = SCREEN_HEIGHT - 30
        for text in reversed(instructions):
            inst_text = self.small_font.render(text, True, GRAY)
            self.screen.blit(inst_text, (10, y))
            y -= 25

    def draw(self):
        """绘制所有内容"""
        self.draw_court()
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.draw_ui()
        self.draw_instructions()
        pygame.display.flip()

    def restart(self):
        """重新开始游戏"""
        self.paddle = Paddle(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball()
        self.hits = 0
        self.game_over = False
        self.paused = False

    def run(self):
        """游戏主循环"""
        while self.running:
            self.handle_events()
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """主函数"""
    print("=" * 40)
    print("    壁球游戏 - Squash Game")
    print("=" * 40)
    print("\n操作说明:")
    print("  W / ↑  : 向上移动球拍")
    print("  S / ↓  : 向下移动球拍")
    print("  SPACE  : 暂停游戏")
    print("  R      : 重新开始")
    print("  ESC    : 退出游戏")
    print("\n游戏目标: 用球拍击球，不让球从左边出界！")
    print("-" * 40)

    game = Game()
    game.run()


if __name__ == "__main__":
    main()
