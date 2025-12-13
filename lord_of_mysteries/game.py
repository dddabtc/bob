"""
游戏主类
"""

import pygame
import sys
import random
from settings import *
from ui.menu import MainMenu, PauseMenu
from ui.pathway_select import PathwaySelectUI, PathwayConfirmUI
from ui.hud import GameHUD, DamageNumber, FloatingText
from ui.inventory_ui import InventoryUI, DropNotification, CraftResultUI
from ui.quest_ui import QuestUI, QuestTracker, QuestNotification
from ui.dialogue import DialogueBox
from entities.player import Player
from entities.enemy import Enemy
from data.pathways import PATHWAYS
from data.enemies import get_enemy_data, get_wave_enemies
from data.items import MATERIALS, QUALITY_COLORS
from systems.inventory import Inventory
from systems.potion import PotionSystem
from systems.quest import QuestSystem


class Game:
    """游戏主类"""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # 加载字体
        self.fonts = self._load_fonts()

        # 游戏状态
        self.state = GameState.MENU
        self.running = True

        # 菜单和UI
        self.main_menu = MainMenu(self.screen, self.fonts)
        self.pause_menu = PauseMenu(self.screen, self.fonts)
        self.pathway_select_ui = PathwaySelectUI(self.screen, self.fonts, PATHWAYS)
        self.pathway_confirm_ui = None
        self.game_hud = GameHUD(self.screen, self.fonts)
        self.inventory_ui = InventoryUI(self.screen, self.fonts)
        self.drop_notification = DropNotification()
        self.craft_result_ui = CraftResultUI(self.screen, self.fonts)
        self.quest_ui = QuestUI(self.screen, self.fonts)
        self.quest_tracker = QuestTracker(self.screen, self.fonts)
        self.quest_notification = QuestNotification()
        self.dialogue_box = DialogueBox(self.screen, self.fonts)

        # 玩家
        self.player = None
        self.player_pathway = None

        # 游戏对象
        self.enemies = []
        self.damage_numbers = []
        self.floating_texts = []
        self.drops = []  # 掉落物

        # 波次系统
        self.current_wave = 0
        self.wave_timer = 0
        self.wave_spawn_queue = []
        self.wave_spawn_delay = 0
        self.wave_complete = True
        self.wave_cooldown = 3.0  # 波次间隔

        # 统计
        self.kill_count = 0
        self.total_exp = 0

        # 背包和炮制系统
        self.inventory = Inventory()
        self.potion_system = PotionSystem()

        # 任务系统
        self.quest_system = QuestSystem()

        # 帧时间
        self.dt = 0

        # 事件缓存
        self.events = []

    def _load_fonts(self):
        """加载字体"""
        fonts = {}
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
            None
        ]

        font_path = None
        for path in font_paths:
            if path is None:
                break
            try:
                pygame.font.Font(path, 24)
                font_path = path
                break
            except (FileNotFoundError, OSError):
                continue

        for name, size in FONT_SIZES.items():
            try:
                if font_path:
                    fonts[name] = pygame.font.Font(font_path, size)
                else:
                    fonts[name] = pygame.font.Font(None, size)
            except Exception:
                fonts[name] = pygame.font.Font(None, size)

        return fonts

    def run(self):
        """游戏主循环"""
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0
            self._handle_events()
            self._update()
            self._draw()

        pygame.quit()
        sys.exit()

    def _handle_events(self):
        """处理事件"""
        self.events = pygame.event.get()
        mouse_clicked = False

        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True

        mouse_pos = pygame.mouse.get_pos()
        self._handle_state_input(mouse_pos, mouse_clicked)

    def _handle_state_input(self, mouse_pos, mouse_clicked):
        """处理各状态的输入"""
        if self.state == GameState.MENU:
            action = self.main_menu.update(mouse_pos, mouse_clicked)
            if action == "start":
                self.state = GameState.PATHWAY_SELECT
                self.pathway_select_ui = PathwaySelectUI(self.screen, self.fonts, PATHWAYS)
            elif action == "continue":
                pass
            elif action == "quit":
                self.running = False

        elif self.state == GameState.PATHWAY_SELECT:
            action, pathway_id = self.pathway_select_ui.update(mouse_pos, mouse_clicked, self.events)
            if action == "confirm" and pathway_id:
                self.pathway_confirm_ui = PathwayConfirmUI(
                    self.screen, self.fonts,
                    pathway_id, PATHWAYS[pathway_id]
                )
                self.state = "pathway_confirm"
            elif action == "back":
                self.state = GameState.MENU

        elif self.state == "pathway_confirm":
            action, pathway_id = self.pathway_confirm_ui.update(mouse_pos, mouse_clicked, self.events)
            if action == "start" and pathway_id:
                self._start_game(pathway_id)
            elif action == "back":
                self.state = GameState.PATHWAY_SELECT

        elif self.state == GameState.PAUSED:
            action = self.pause_menu.update(mouse_pos, mouse_clicked)
            if action == "resume":
                self.state = GameState.PLAYING
            elif action == "main_menu":
                self.state = GameState.MENU
                self._reset_game()
            elif action == "quit":
                self.running = False

        elif self.state == GameState.PLAYING:
            # 先处理对话框
            if self.dialogue_box.is_active():
                for event in self.events:
                    self.dialogue_box.handle_event(event)
                return  # 对话时不处理其他输入

            # 处理任务UI
            if self.quest_ui.is_open:
                for event in self.events:
                    result = self.quest_ui.handle_event(
                        event, self.quest_system, self.inventory, self.player
                    )
                    if result:
                        action = result[0] if isinstance(result, tuple) else result
                        if action == "accept":
                            quest_id = result[1]
                            self.quest_notification.add(f"接受任务: {result[2]}", GOLD)
                            # 检查是否有对话
                            dialogue = self.quest_system.get_pending_dialogue()
                            if dialogue:
                                self.dialogue_box.start(dialogue["dialogues"])
                        elif action == "complete":
                            quest_id, msg, rewards = result[1], result[2], result[3]
                            self.quest_notification.add(msg, (100, 255, 100))
                            if rewards:
                                self.quest_notification.add(f"奖励: {rewards['reward_text']}", GOLD)
                                self.total_exp += rewards.get("exp", 0)
                            # 检查是否有对话
                            dialogue = self.quest_system.get_pending_dialogue()
                            if dialogue:
                                self.dialogue_box.start(dialogue["dialogues"])
                return  # 任务UI打开时不处理其他输入

            # 处理背包UI
            if self.inventory_ui.is_open:
                for event in self.events:
                    result = self.inventory_ui.handle_event(
                        event, self.inventory, self.player, self.potion_system
                    )
                    if result:
                        action = result[0] if isinstance(result, tuple) else result
                        if action == "close":
                            pass  # 背包已关闭
                        elif action == "use":
                            success, msg = result[1], result[2]
                            self.craft_result_ui.show(msg, success, 2.0)
                        elif action == "craft":
                            success, msg = result[1], result[2]
                            self.craft_result_ui.show(msg, success, 3.0)
                            if success:
                                self.floating_texts.append(FloatingText(
                                    SCREEN_WIDTH // 2,
                                    SCREEN_HEIGHT // 2 - 50,
                                    "晋升成功！",
                                    GOLD
                                ))
                                # 通知任务系统晋升
                                self.quest_system.on_sequence_advanced(self.player.sequence)
                return  # 背包打开时不处理其他输入

            for event in self.events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.PAUSED
                    elif event.key == pygame.K_i:
                        self.inventory_ui.toggle()
                    elif event.key == pygame.K_q:
                        self.quest_ui.toggle()

        elif self.state == GameState.GAME_OVER:
            for event in self.events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self._start_game(self.player_pathway)
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                        self._reset_game()

    def _start_game(self, pathway_id):
        """开始游戏"""
        self.player_pathway = pathway_id

        self.player = Player(
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 100,
            pathway_id=pathway_id,
            pathway_data=PATHWAYS[pathway_id],
            sequence=9
        )

        self.enemies = []
        self.damage_numbers = []
        self.floating_texts = []
        self.drops = []
        self.inventory = Inventory()

        self.current_wave = 0
        self.wave_timer = 2.0  # 开始前等待
        self.wave_spawn_queue = []
        self.wave_complete = True
        self.kill_count = 0
        self.total_exp = 0

        self.floating_texts.append(FloatingText(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            f"欢迎，{self.player.name}！",
            GOLD
        ))

        # 重置任务系统
        self.quest_system = QuestSystem()

        self.state = GameState.PLAYING

    def _reset_game(self):
        """重置游戏"""
        self.player = None
        self.player_pathway = None
        self.enemies = []
        self.damage_numbers = []
        self.floating_texts = []
        self.drops = []
        self.inventory = Inventory()
        self.current_wave = 0
        self.kill_count = 0
        self.total_exp = 0

    def _update(self):
        """更新游戏状态"""
        if self.state == GameState.PLAYING:
            self._update_playing()

    def _update_playing(self):
        """更新游戏中状态"""
        if not self.player:
            return

        keys = pygame.key.get_pressed()

        # 更新玩家
        self.player.update(self.dt, keys, self.events)

        # 更新敌人
        self._update_enemies()

        # 更新波次
        self._update_waves()

        # 检查战斗碰撞
        self._check_combat()

        # 更新掉落物
        self._update_drops()

        # 更新伤害数字
        self.damage_numbers = [d for d in self.damage_numbers if d.update(self.dt)]

        # 更新浮动文字
        self.floating_texts = [f for f in self.floating_texts if f.update(self.dt)]

        # 更新掉落通知
        self.drop_notification.update(self.dt)

        # 更新炮制结果UI
        self.craft_result_ui.update(self.dt)

        # 检查玩家是否死亡
        if not self.player.is_alive():
            self._handle_player_death()

    def _update_enemies(self):
        """更新所有敌人"""
        for enemy in self.enemies[:]:
            enemy.update(self.dt, self.player)

            # 处理敌人召唤
            for summon in enemy.summons_to_spawn:
                self._spawn_enemy(summon["type"], summon["x"], summon["y"])
            enemy.summons_to_spawn = []

            # 移除死亡敌人
            if not enemy.is_alive():
                self._handle_enemy_death(enemy)
                self.enemies.remove(enemy)

    def _update_waves(self):
        """更新波次系统"""
        # 生成队列中的敌人
        if self.wave_spawn_queue and self.wave_spawn_delay <= 0:
            enemy_type, x, y = self.wave_spawn_queue.pop(0)
            self._spawn_enemy(enemy_type, x, y)

            if self.wave_spawn_queue:
                wave_config = get_wave_enemies(self.current_wave)
                self.wave_spawn_delay = wave_config.get("spawn_delay", 0.5)
        else:
            self.wave_spawn_delay -= self.dt

        # 检查波次完成
        if not self.wave_spawn_queue and not self.enemies:
            if not self.wave_complete:
                self.wave_complete = True
                self.wave_timer = self.wave_cooldown

                self.floating_texts.append(FloatingText(
                    SCREEN_WIDTH // 2,
                    200,
                    f"波次 {self.current_wave} 完成！",
                    GOLD
                ))

        # 开始新波次
        if self.wave_complete:
            self.wave_timer -= self.dt
            if self.wave_timer <= 0:
                self._start_next_wave()

    def _start_next_wave(self):
        """开始下一波"""
        self.current_wave += 1
        self.wave_complete = False

        wave_config = get_wave_enemies(self.current_wave)

        self.floating_texts.append(FloatingText(
            SCREEN_WIDTH // 2,
            150,
            f"波次 {self.current_wave}",
            CRIMSON if wave_config.get("is_boss_wave") else GOLD
        ))

        # 生成敌人位置
        for enemy_type, count in wave_config["enemies"]:
            for _ in range(count):
                # 在屏幕边缘生成
                side = random.randint(0, 3)
                if side == 0:  # 上
                    x = random.randint(100, SCREEN_WIDTH - 100)
                    y = 50
                elif side == 1:  # 右
                    x = SCREEN_WIDTH - 50
                    y = random.randint(100, SCREEN_HEIGHT - 200)
                elif side == 2:  # 下
                    x = random.randint(100, SCREEN_WIDTH - 100)
                    y = SCREEN_HEIGHT - 200
                else:  # 左
                    x = 50
                    y = random.randint(100, SCREEN_HEIGHT - 200)

                self.wave_spawn_queue.append((enemy_type, x, y))

        self.wave_spawn_delay = wave_config.get("spawn_delay", 0.5)

    def _spawn_enemy(self, enemy_type, x, y):
        """生成敌人"""
        enemy_data = get_enemy_data(enemy_type)

        # 根据波次增加难度
        difficulty_mult = 1 + (self.current_wave - 1) * 0.1
        enemy_data["hp"] = int(enemy_data["hp"] * difficulty_mult)
        enemy_data["attack"] = int(enemy_data["attack"] * difficulty_mult)

        enemy = Enemy(x, y, enemy_data)
        self.enemies.append(enemy)

    def _check_combat(self):
        """检查战斗碰撞"""
        if not self.player:
            return

        player_rect = self.player.get_rect()

        # 玩家攻击命中敌人
        if self.player.is_attacking and self.player.attack_hitbox:
            for enemy in self.enemies:
                enemy_rect = enemy.get_rect()
                if self.player.attack_hitbox.colliderect(enemy_rect):
                    damage = self.player.get_attack_damage()
                    actual_damage = enemy.take_damage(damage)

                    self.damage_numbers.append(DamageNumber(
                        enemy.x, enemy.y - 20,
                        actual_damage,
                        GOLD
                    ))

        # 玩家投射物命中敌人
        for proj in self.player.projectiles[:]:
            proj_rect = pygame.Rect(
                proj["x"] - proj["size"],
                proj["y"] - proj["size"],
                proj["size"] * 2,
                proj["size"] * 2
            )
            for enemy in self.enemies:
                enemy_rect = enemy.get_rect()
                if proj_rect.colliderect(enemy_rect):
                    actual_damage = enemy.take_damage(proj["damage"])
                    self.damage_numbers.append(DamageNumber(
                        enemy.x, enemy.y - 20,
                        actual_damage,
                        self.player.color
                    ))
                    if proj in self.player.projectiles:
                        self.player.projectiles.remove(proj)
                    break

        # 敌人攻击命中玩家
        for enemy in self.enemies:
            # 近战攻击
            if enemy.is_attacking:
                attack_rect = enemy.get_attack_rect()
                if attack_rect and attack_rect.colliderect(player_rect):
                    if not self.player.is_invincible:
                        actual_damage = self.player.take_damage(enemy.attack)
                        self.damage_numbers.append(DamageNumber(
                            self.player.x, self.player.y - 20,
                            actual_damage,
                            CRIMSON
                        ))

            # 敌人投射物
            for proj in enemy.projectiles[:]:
                proj_rect = pygame.Rect(
                    proj["x"] - proj["size"],
                    proj["y"] - proj["size"],
                    proj["size"] * 2,
                    proj["size"] * 2
                )
                if proj_rect.colliderect(player_rect):
                    if not self.player.is_invincible:
                        actual_damage = self.player.take_damage(proj["damage"])
                        self.damage_numbers.append(DamageNumber(
                            self.player.x, self.player.y - 20,
                            actual_damage,
                            CRIMSON
                        ))
                    enemy.projectiles.remove(proj)

            # 接触伤害
            enemy_rect = enemy.get_rect()
            if enemy_rect.colliderect(player_rect):
                if not self.player.is_invincible and not self.player.is_dodging:
                    actual_damage = self.player.take_damage(enemy.attack // 2)
                    self.damage_numbers.append(DamageNumber(
                        self.player.x, self.player.y - 20,
                        actual_damage,
                        CRIMSON
                    ))

    def _handle_enemy_death(self, enemy):
        """处理敌人死亡"""
        self.kill_count += 1
        self.total_exp += enemy.exp

        # 显示经验
        self.floating_texts.append(FloatingText(
            enemy.x, enemy.y,
            f"+{enemy.exp} EXP",
            (100, 255, 100)
        ))

        # 生成掉落物
        drops = enemy.get_drops()
        for drop in drops:
            self.drops.append({
                "x": enemy.x + random.randint(-20, 20),
                "y": enemy.y + random.randint(-20, 20),
                "item": drop["item"],
                "count": drop["count"],
                "lifetime": 10.0  # 10秒后消失
            })

    def _update_drops(self):
        """更新掉落物"""
        if not self.player:
            return

        player_rect = self.player.get_rect()

        for drop in self.drops[:]:
            drop["lifetime"] -= self.dt

            if drop["lifetime"] <= 0:
                self.drops.remove(drop)
                continue

            # 检查玩家拾取
            drop_rect = pygame.Rect(drop["x"] - 10, drop["y"] - 10, 20, 20)
            if drop_rect.colliderect(player_rect):
                # 添加到背包
                item_name = drop["item"]
                item_count = drop["count"]

                # 判断是材料还是消耗品
                if item_name in MATERIALS:
                    self.inventory.add_material(item_name, item_count)
                else:
                    self.inventory.add_consumable(item_name, item_count)

                # 获取品质颜色
                material_info = MATERIALS.get(item_name, {})
                quality = material_info.get("quality", "common")
                color = QUALITY_COLORS.get(quality, (200, 200, 100))

                self.floating_texts.append(FloatingText(
                    self.player.x, self.player.y - 40,
                    f"+{item_count} {item_name}",
                    color
                ))

                # 右上角通知
                self.drop_notification.add(f"获得 {item_name} x{item_count}", color)

                self.drops.remove(drop)

    def _handle_player_death(self):
        """处理玩家死亡"""
        self.state = GameState.GAME_OVER

    def _draw(self):
        """绘制画面"""
        if self.state == GameState.MENU:
            self.main_menu.draw()

        elif self.state == GameState.PATHWAY_SELECT:
            self.pathway_select_ui.draw()

        elif self.state == "pathway_confirm":
            self.pathway_confirm_ui.draw()

        elif self.state == GameState.PLAYING:
            self._draw_playing()
            # 绘制背包UI（如果打开）
            if self.inventory_ui.is_open:
                self.inventory_ui.draw(self.inventory, self.player, self.potion_system)
            # 绘制炮制结果
            self.craft_result_ui.draw()

        elif self.state == GameState.PAUSED:
            self._draw_playing()
            self.pause_menu.draw()

        elif self.state == GameState.GAME_OVER:
            self._draw_playing()
            self._draw_game_over()

        pygame.display.flip()

    def _draw_playing(self):
        """绘制游戏画面"""
        self.screen.fill(MIDNIGHT_BLUE)
        self._draw_street_background()

        # 绘制掉落物
        for drop in self.drops:
            alpha = int(255 * min(1, drop["lifetime"]))
            drop_surface = pygame.Surface((16, 16), pygame.SRCALPHA)
            pygame.draw.rect(drop_surface, (255, 215, 0, alpha), (0, 0, 16, 16), border_radius=3)
            pygame.draw.rect(drop_surface, (255, 255, 255, alpha), (0, 0, 16, 16), 1, border_radius=3)
            self.screen.blit(drop_surface, (drop["x"] - 8, drop["y"] - 8))

        # 绘制敌人
        for enemy in self.enemies:
            enemy.draw(self.screen, self.fonts)

        # 绘制玩家
        if self.player:
            self.player.draw(self.screen, self.fonts)

        # 绘制伤害数字
        for damage_num in self.damage_numbers:
            damage_num.draw(self.screen, self.fonts)

        # 绘制浮动文字
        for float_text in self.floating_texts:
            float_text.draw(self.screen, self.fonts)

        # 绘制HUD
        if self.player:
            pathway_name = PATHWAYS[self.player_pathway]["name"]
            self.game_hud.draw(self.player, pathway_name)

        # 绘制波次信息
        self._draw_wave_info()

        # 绘制掉落通知
        self.drop_notification.draw(self.screen, self.fonts)

    def _draw_wave_info(self):
        """绘制波次信息"""
        # 右上角显示波次和击杀数
        wave_text = self.fonts["small"].render(f"波次: {self.current_wave}", True, GOLD)
        self.screen.blit(wave_text, (SCREEN_WIDTH - 150, 20))

        kill_text = self.fonts["tiny"].render(f"击杀: {self.kill_count}", True, WHITE)
        self.screen.blit(kill_text, (SCREEN_WIDTH - 150, 55))

        enemy_text = self.fonts["tiny"].render(f"敌人: {len(self.enemies)}", True, GRAY)
        self.screen.blit(enemy_text, (SCREEN_WIDTH - 150, 80))

        # 显示即将开始的波次倒计时
        if self.wave_complete and self.wave_timer > 0:
            countdown = self.fonts["medium"].render(
                f"下一波: {self.wave_timer:.1f}s",
                True, GOLD
            )
            countdown_rect = countdown.get_rect(center=(SCREEN_WIDTH // 2, 50))
            self.screen.blit(countdown, countdown_rect)

    def _draw_game_over(self):
        """绘制游戏结束界面"""
        # 半透明遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))

        # 游戏结束文字
        title = self.fonts["title"].render("游戏结束", True, CRIMSON)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)

        # 统计
        stats = [
            f"到达波次: {self.current_wave}",
            f"击杀敌人: {self.kill_count}",
            f"获得经验: {self.total_exp}",
        ]

        y = 300
        for stat in stats:
            text = self.fonts["medium"].render(stat, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 50

        # 提示
        hint1 = self.fonts["small"].render("按 SPACE 重新开始", True, GOLD)
        hint1_rect = hint1.get_rect(center=(SCREEN_WIDTH // 2, 500))
        self.screen.blit(hint1, hint1_rect)

        hint2 = self.fonts["small"].render("按 ESC 返回主菜单", True, GRAY)
        hint2_rect = hint2.get_rect(center=(SCREEN_WIDTH // 2, 540))
        self.screen.blit(hint2, hint2_rect)

    def _draw_street_background(self):
        """绘制街道背景"""
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - 150, SCREEN_WIDTH, 150)
        pygame.draw.rect(self.screen, DARK_GRAY, ground_rect)

        pygame.draw.line(
            self.screen, GRAY,
            (0, SCREEN_HEIGHT - 150),
            (SCREEN_WIDTH, SCREEN_HEIGHT - 150), 3
        )

        buildings = [
            (50, 200, 120, 350),
            (200, 250, 100, 300),
            (330, 180, 140, 370),
            (500, 220, 110, 330),
            (640, 190, 130, 360),
            (800, 240, 120, 310),
            (950, 200, 100, 350),
        ]

        for x, y, w, h in buildings:
            pygame.draw.rect(self.screen, (30, 30, 50), (x, y, w, h))
            window_color = (60, 50, 30)
            for wy in range(y + 20, y + h - 40, 50):
                for wx in range(x + 15, x + w - 20, 35):
                    if (wx + wy) % 100 < 70:
                        pygame.draw.rect(self.screen, window_color, (wx, wy, 20, 30))

        fog = pygame.Surface((SCREEN_WIDTH, 100))
        fog.fill((40, 40, 60))
        fog.set_alpha(50)
        self.screen.blit(fog, (0, SCREEN_HEIGHT - 200))
