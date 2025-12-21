"""
游戏HUD界面
"""

import pygame
from settings import *


class GameHUD:
    """游戏HUD"""

    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts

    def draw(self, player, pathway_name):
        """绘制完整HUD"""
        self._draw_hp_bar(player)
        self._draw_player_info(player, pathway_name)
        self._draw_skills(player)
        self._draw_controls()

    def _draw_hp_bar(self, player):
        """绘制血条"""
        # 血条背景
        hp_bar_bg = pygame.Rect(20, 20, 220, 28)
        pygame.draw.rect(self.screen, HP_BG, hp_bar_bg, border_radius=5)

        # 血条
        hp_ratio = player.hp / player.max_hp
        hp_width = int(216 * hp_ratio)
        if hp_width > 0:
            hp_bar = pygame.Rect(22, 22, hp_width, 24)
            hp_color = HP_GREEN if hp_ratio > 0.3 else HP_RED
            pygame.draw.rect(self.screen, hp_color, hp_bar, border_radius=4)

        # 血条边框
        pygame.draw.rect(self.screen, WHITE, hp_bar_bg, 2, border_radius=5)

        # 血量文字
        hp_text = self.fonts["tiny"].render(
            f"HP: {player.hp}/{player.max_hp}",
            True, WHITE
        )
        self.screen.blit(hp_text, (25, 24))

    def _draw_player_info(self, player, pathway_name):
        """绘制玩家信息"""
        # 序列显示
        seq_text = self.fonts["small"].render(
            f"序列{player.sequence} - {player.name}",
            True, player.color
        )
        self.screen.blit(seq_text, (20, 55))

        # 途径名
        pathway_text = self.fonts["tiny"].render(pathway_name, True, GRAY)
        self.screen.blit(pathway_text, (20, 85))

        # 属性显示
        attr_y = 110
        attrs = [
            ("攻击", player.attack, CRIMSON),
            ("防御", player.defense, (100, 150, 255)),
            ("速度", player.speed, (255, 200, 100)),
        ]

        for attr_name, value, color in attrs:
            # 属性名
            name_text = self.fonts["tiny"].render(f"{attr_name}:", True, GRAY)
            self.screen.blit(name_text, (20, attr_y))
            # 属性值
            value_text = self.fonts["tiny"].render(str(value), True, color)
            self.screen.blit(value_text, (70, attr_y))
            attr_y += 22

        # 魔药消化进度
        if hasattr(player, 'is_digesting') and player.is_digesting:
            digest_y = attr_y + 5
            digest_text = self.fonts["tiny"].render("消化中:", True, (200, 150, 100))
            self.screen.blit(digest_text, (20, digest_y))

            # 进度条背景
            bar_bg = pygame.Rect(20, digest_y + 18, 100, 8)
            pygame.draw.rect(self.screen, (40, 40, 50), bar_bg, border_radius=3)

            # 进度条
            progress_width = int(100 * player.digest_progress / 100)
            if progress_width > 0:
                bar = pygame.Rect(20, digest_y + 18, progress_width, 8)
                pygame.draw.rect(self.screen, (200, 150, 100), bar, border_radius=3)

            # 百分比文字
            pct_text = self.fonts["tiny"].render(f"{player.digest_progress:.0f}%", True, (200, 150, 100))
            self.screen.blit(pct_text, (125, digest_y + 14))

    def _draw_skills(self, player):
        """绘制技能栏"""
        skill_y = 190
        skill_title = self.fonts["small"].render("技能", True, GOLD)
        self.screen.blit(skill_title, (20, skill_y))
        skill_y += 28

        skill_names = player.get_skill_list()

        for i, skill_name in enumerate(skill_names):
            skill = player.skills.get(skill_name, {})
            cooldown = skill.get("current_cooldown", 0)
            max_cooldown = skill.get("cooldown", 1)

            # 技能槽背景
            slot_rect = pygame.Rect(20, skill_y, 180, 35)
            pygame.draw.rect(self.screen, (40, 40, 60), slot_rect, border_radius=5)

            # 冷却覆盖
            if cooldown > 0:
                cooldown_ratio = cooldown / max_cooldown
                cooldown_width = int(180 * cooldown_ratio)
                cooldown_rect = pygame.Rect(20, skill_y, cooldown_width, 35)
                pygame.draw.rect(self.screen, (80, 40, 40), cooldown_rect, border_radius=5)

            # 边框
            border_color = GOLD if cooldown <= 0 else GRAY
            pygame.draw.rect(self.screen, border_color, slot_rect, 2, border_radius=5)

            # 技能编号
            num_text = self.fonts["small"].render(str(i + 1), True, GOLD)
            self.screen.blit(num_text, (25, skill_y + 5))

            # 技能名称
            name_color = WHITE if cooldown <= 0 else GRAY
            name_text = self.fonts["tiny"].render(skill_name, True, name_color)
            self.screen.blit(name_text, (50, skill_y + 8))

            # 冷却时间显示
            if cooldown > 0:
                cd_text = self.fonts["tiny"].render(f"{cooldown:.1f}s", True, WHITE)
                self.screen.blit(cd_text, (155, skill_y + 8))

            skill_y += 40

        # 如果技能不足4个，显示空槽
        for i in range(len(skill_names), 4):
            slot_rect = pygame.Rect(20, skill_y, 180, 35)
            pygame.draw.rect(self.screen, (30, 30, 40), slot_rect, border_radius=5)
            pygame.draw.rect(self.screen, DARK_GRAY, slot_rect, 1, border_radius=5)

            num_text = self.fonts["small"].render(str(i + 1), True, DARK_GRAY)
            self.screen.blit(num_text, (25, skill_y + 5))

            lock_text = self.fonts["tiny"].render("未解锁", True, DARK_GRAY)
            self.screen.blit(lock_text, (50, skill_y + 8))

            skill_y += 40

    def _draw_controls(self):
        """绘制操作提示"""
        controls = [
            "WASD - 移动",
            "J - 攻击",
            "K - 闪避",
            "1-4 - 技能",
            "I - 背包/炮制",
            "E - 武器",
            "Q - 任务",
            "ESC - 暂停"
        ]

        y = SCREEN_HEIGHT - 175
        for text in controls:
            hint = self.fonts["tiny"].render(text, True, GRAY)
            self.screen.blit(hint, (20, y))
            y += 22


class DamageNumber:
    """伤害数字显示"""

    def __init__(self, x, y, damage, color=WHITE, is_crit=False):
        self.x = x
        self.y = y
        self.damage = damage
        self.color = color
        self.is_crit = is_crit
        self.lifetime = 1.0
        self.vy = -2  # 向上飘动

    def update(self, dt):
        """更新位置"""
        self.y += self.vy
        self.lifetime -= dt
        return self.lifetime > 0

    def draw(self, screen, fonts):
        """绘制伤害数字"""
        alpha = int(255 * min(1, self.lifetime * 2))

        if self.is_crit:
            text = fonts["medium"].render(f"{self.damage}!", True, self.color)
        else:
            text = fonts["small"].render(str(self.damage), True, self.color)

        # 创建带透明度的surface
        text_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
        text_surface.blit(text, (0, 0))
        text_surface.set_alpha(alpha)

        text_rect = text_surface.get_rect(center=(self.x, self.y))
        screen.blit(text_surface, text_rect)


class FloatingText:
    """浮动文字（用于显示buff、状态等）"""

    def __init__(self, x, y, text, color=WHITE):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = 1.5
        self.vy = -1

    def update(self, dt):
        """更新位置"""
        self.y += self.vy
        self.lifetime -= dt
        return self.lifetime > 0

    def draw(self, screen, fonts):
        """绘制文字"""
        alpha = int(255 * min(1, self.lifetime))

        text = fonts["tiny"].render(self.text, True, self.color)
        text_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
        text_surface.blit(text, (0, 0))
        text_surface.set_alpha(alpha)

        text_rect = text_surface.get_rect(center=(self.x, self.y))
        screen.blit(text_surface, text_rect)
