"""
Black Ops - 主菜单界面
"""

import pygame
import math
from settings import *


def get_font(size):
    """获取支持中文的字体"""
    # 尝试系统中文字体
    chinese_fonts = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
    ]
    for font_path in chinese_fonts:
        try:
            return pygame.font.Font(font_path, size)
        except:
            continue
    # 回退到默认字体
    return pygame.font.Font(None, size)


class MainMenu:
    """主菜单"""

    def __init__(self, screen):
        self.screen = screen

        # 字体 - 支持中文
        pygame.font.init()
        self.font_title = pygame.font.Font(None, FONT_SIZES['huge'])
        self.font_subtitle = get_font(FONT_SIZES['large'])
        self.font_menu = pygame.font.Font(None, FONT_SIZES['medium'])

        # 菜单选项
        self.menu_items = [
            {'text': 'NEW GAME', 'action': 'new_game'},
            {'text': 'SELECT MISSION', 'action': 'select_mission'},
            {'text': 'SETTINGS', 'action': 'settings'},
            {'text': 'QUIT', 'action': 'quit'},
        ]
        self.selected_index = 0

        # 动画
        self.time = 0
        self.particles = self._create_particles()

    def _create_particles(self):
        """创建背景粒子效果"""
        import random
        particles = []
        for _ in range(50):
            particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(20, 50),
                'size': random.randint(1, 3),
                'alpha': random.randint(50, 150),
            })
        return particles

    def update(self, dt):
        """更新菜单动画"""
        self.time += dt

        # 更新粒子
        for p in self.particles:
            p['y'] += p['speed'] * dt
            if p['y'] > SCREEN_HEIGHT:
                p['y'] = 0
                p['x'] = pygame.time.get_ticks() % SCREEN_WIDTH

    def handle_event(self, event):
        """处理输入事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.menu_items[self.selected_index]['action']
            elif event.key == pygame.K_ESCAPE:
                return 'quit'

        elif event.type == pygame.MOUSEMOTION:
            # 鼠标悬停选择
            mouse_y = event.pos[1]
            menu_start_y = SCREEN_HEIGHT // 2
            for i, item in enumerate(self.menu_items):
                item_y = menu_start_y + i * 50
                if item_y - 20 < mouse_y < item_y + 20:
                    self.selected_index = i
                    break

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self.menu_items[self.selected_index]['action']

        return None

    def draw(self):
        """绘制主菜单"""
        # 背景
        self.screen.fill((10, 10, 15))

        # 粒子效果
        for p in self.particles:
            pygame.draw.circle(
                self.screen,
                (p['alpha'], p['alpha'], p['alpha']),
                (int(p['x']), int(p['y'])),
                p['size']
            )

        # 标题
        title_y = 150 + math.sin(self.time * 2) * 5
        title = self.font_title.render("BLACK OPS", True, (200, 50, 50))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, title_y))

        # 标题阴影
        shadow = self.font_title.render("BLACK OPS", True, (50, 10, 10))
        shadow_rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + 3, title_y + 3))
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, title_rect)

        # 副标题
        subtitle = self.font_subtitle.render("黑色行动", True, LIGHT_GRAY)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, title_y + 60))
        self.screen.blit(subtitle, subtitle_rect)

        # 菜单选项
        menu_start_y = SCREEN_HEIGHT // 2
        for i, item in enumerate(self.menu_items):
            is_selected = i == self.selected_index

            # 选中效果
            if is_selected:
                color = YELLOW
                prefix = "> "
                # 选中指示器动画
                indicator_x = SCREEN_WIDTH // 2 - 120 + math.sin(self.time * 5) * 5
                pygame.draw.polygon(
                    self.screen,
                    YELLOW,
                    [
                        (indicator_x, menu_start_y + i * 50 - 8),
                        (indicator_x + 15, menu_start_y + i * 50),
                        (indicator_x, menu_start_y + i * 50 + 8),
                    ]
                )
            else:
                color = WHITE
                prefix = "  "

            text = self.font_menu.render(prefix + item['text'], True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, menu_start_y + i * 50))
            self.screen.blit(text, text_rect)

        # 版本信息
        version = self.font_menu.render("v1.0 - Pygame Edition", True, GRAY)
        self.screen.blit(version, (20, SCREEN_HEIGHT - 40))

        # 控制提示
        controls = self.font_menu.render("Arrow Keys: Navigate  |  Enter: Select  |  Esc: Quit", True, GRAY)
        controls_rect = controls.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        self.screen.blit(controls, controls_rect)


class MissionSelectMenu:
    """关卡选择菜单"""

    def __init__(self, screen, mission_system):
        self.screen = screen
        self.mission_system = mission_system

        self.font_title = pygame.font.Font(None, FONT_SIZES['title'])
        self.font_menu = pygame.font.Font(None, FONT_SIZES['medium'])
        self.font_small = pygame.font.Font(None, FONT_SIZES['small'])

        self.missions = mission_system.get_available_missions()
        self.selected_index = 0

    def handle_event(self, event):
        """处理输入"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.missions)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.missions)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return ('start_mission', self.missions[self.selected_index]['id'])
            elif event.key == pygame.K_ESCAPE:
                return ('back', None)

        return None

    def draw(self):
        """绘制关卡选择"""
        # 背景
        self.screen.fill((15, 15, 20))

        # 标题
        title = self.font_title.render("SELECT MISSION", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)

        # 关卡列表
        y = 180
        for i, mission in enumerate(self.missions):
            is_selected = i == self.selected_index

            # 背景框
            box_color = (60, 60, 70) if is_selected else (30, 30, 35)
            pygame.draw.rect(self.screen, box_color, (100, y - 20, SCREEN_WIDTH - 200, 70))

            if is_selected:
                pygame.draw.rect(self.screen, YELLOW, (100, y - 20, SCREEN_WIDTH - 200, 70), 2)

            # 关卡名称
            name_color = WHITE if not mission['completed'] else GREEN
            name = self.font_menu.render(mission['name'], True, name_color)
            self.screen.blit(name, (120, y))

            # 副标题
            subtitle = self.font_small.render(mission['subtitle'], True, GRAY)
            self.screen.blit(subtitle, (120, y + 25))

            # 完成标记
            if mission['completed']:
                complete = self.font_small.render("[COMPLETED]", True, GREEN)
                self.screen.blit(complete, (SCREEN_WIDTH - 220, y + 10))

            y += 90

        # 返回提示
        back_hint = self.font_small.render("Press ESC to go back", True, GRAY)
        self.screen.blit(back_hint, (20, SCREEN_HEIGHT - 40))


class PauseMenu:
    """暂停菜单"""

    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, FONT_SIZES['title'])
        self.font_menu = pygame.font.Font(None, FONT_SIZES['medium'])

        self.menu_items = [
            {'text': 'RESUME', 'action': 'resume'},
            {'text': 'RESTART MISSION', 'action': 'restart'},
            {'text': 'SETTINGS', 'action': 'settings'},
            {'text': 'QUIT TO MENU', 'action': 'quit_menu'},
        ]
        self.selected_index = 0

    def handle_event(self, event):
        """处理输入"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.menu_items[self.selected_index]['action']
            elif event.key == pygame.K_ESCAPE:
                return 'resume'

        return None

    def draw(self):
        """绘制暂停菜单"""
        # 半透明背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # 标题
        title = self.font_title.render("PAUSED", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)

        # 菜单选项
        y = 320
        for i, item in enumerate(self.menu_items):
            is_selected = i == self.selected_index
            color = YELLOW if is_selected else WHITE
            prefix = "> " if is_selected else "  "

            text = self.font_menu.render(prefix + item['text'], True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 50


class GameOverScreen:
    """游戏结束画面"""

    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, FONT_SIZES['huge'])
        self.font_menu = pygame.font.Font(None, FONT_SIZES['medium'])
        self.font_stats = pygame.font.Font(None, FONT_SIZES['large'])

    def draw(self, is_victory, stats=None):
        """绘制游戏结束画面"""
        # 背景
        color = (20, 50, 20) if is_victory else (50, 20, 20)
        self.screen.fill(color)

        # 标题
        title_text = "MISSION COMPLETE" if is_victory else "MISSION FAILED"
        title_color = GREEN if is_victory else RED
        title = self.font_title.render(title_text, True, title_color)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        # 统计数据
        if stats:
            y = 280
            for key, value in stats.items():
                stat_text = self.font_stats.render(f"{key}: {value}", True, WHITE)
                stat_rect = stat_text.get_rect(center=(SCREEN_WIDTH // 2, y))
                self.screen.blit(stat_text, stat_rect)
                y += 50

        # 提示
        y = SCREEN_HEIGHT - 100
        if is_victory:
            hint = self.font_menu.render("Press SPACE to continue", True, WHITE)
        else:
            hint = self.font_menu.render("Press R to retry  |  Press ESC to quit", True, WHITE)

        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.screen.blit(hint, hint_rect)
