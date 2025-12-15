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
from ui.boss_ui import BossUI
from ui.weapon_ui import WeaponUI, WeaponHUD
from entities.player import Player
from entities.enemy import Enemy
from data.pathways import PATHWAYS
from data.enemies import get_enemy_data, get_wave_enemies
from data.items import MATERIALS, QUALITY_COLORS
from data.weapons import WEAPONS, get_weapon_data, get_all_droppable_weapons
from systems.inventory import Inventory
from systems.potion import PotionSystem
from systems.quest import QuestSystem
from systems.lighting import LightingSystem, Light, TorchLight
from systems.sprites import init_sprites, set_pathway
from systems.save_system import SaveSystem, collect_game_data, apply_save_data
from ui.save_ui import SaveLoadUI, ContinueButton


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
        self.boss_ui = BossUI(self.fonts)
        self.weapon_ui = WeaponUI(self.screen, self.fonts)
        self.weapon_hud = WeaponHUD(self.fonts)

        # 存档系统
        import os
        save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saves")
        self.save_system = SaveSystem(save_dir)
        self.save_ui = SaveLoadUI(self.screen, self.fonts, self.save_system)
        self.continue_button = ContinueButton(self.save_system)

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

        # Boss战斗
        self.current_boss = None
        self.is_boss_wave = False

        # 统计
        self.kill_count = 0
        self.total_exp = 0
        self.playtime = 0  # 游戏时间（秒）
        self.total_kills = 0
        self.max_wave_reached = 0
        self.max_combo = 0
        self.bosses_killed = 0
        self.deaths = 0
        self.score = 0

        # 背包和炮制系统
        self.inventory = Inventory()
        self.potion_system = PotionSystem()

        # 任务系统
        self.quest_system = QuestSystem()

        # 光影系统
        self.lighting = LightingSystem(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.lighting.set_ambient(50)  # 设置较暗的环境光
        self._init_background_lights()

        # 加载精灵图
        import os
        base_path = os.path.dirname(os.path.abspath(__file__))
        init_sprites(base_path)

        # 帧时间
        self.dt = 0

        # 事件缓存
        self.events = []

    def _init_background_lights(self):
        """初始化背景光源（街灯等）"""
        # 添加街灯
        street_lamp_positions = [150, 400, 650, 900]
        for x in street_lamp_positions:
            lamp = TorchLight(x, SCREEN_HEIGHT - 180)
            lamp.radius = 120
            lamp.color = (255, 180, 80)
            lamp.intensity = 0.5
            self.lighting.add_light(lamp)

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
            # 检查是否有存档可继续
            self.main_menu.has_continue = self.continue_button.is_available()

            action = self.main_menu.update(mouse_pos, mouse_clicked)
            if action == "start":
                self.state = GameState.PATHWAY_SELECT
                self.pathway_select_ui = PathwaySelectUI(self.screen, self.fonts, PATHWAYS)
            elif action == "continue":
                # 继续游戏 - 加载最新存档
                latest = self.continue_button.get_continue_slot()
                if latest:
                    self._load_game(latest)
            elif action == "load":
                # 打开读档界面
                self.save_ui.show("load")
                self.state = "save_load"
            elif action == "quit":
                self.running = False

        elif self.state == "save_load":
            # 存档/读档界面
            for event in self.events:
                result = self.save_ui.handle_event(event)
                if result:
                    action = result[0] if isinstance(result, tuple) else result
                    if action == "close":
                        self.state = GameState.MENU if not self.player else GameState.PAUSED
                    elif action == "save":
                        slot = result[1]
                        self._save_game(slot)
                        self.save_ui._refresh_saves()
                        self.floating_texts.append(FloatingText(
                            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                            "游戏已保存!", GOLD
                        ))
                    elif action == "load":
                        slot = result[1]
                        self._load_game(slot)
                    elif action == "deleted":
                        pass  # 已删除存档

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
            elif action == "save":
                # 打开存档界面
                self.save_ui.show("save")
                self.state = "save_load"
            elif action == "load":
                # 打开读档界面
                self.save_ui.show("load")
                self.state = "save_load"
            elif action == "main_menu":
                # 自动存档后返回主菜单
                self._auto_save()
                self.state = GameState.MENU
                self._reset_game()
            elif action == "quit":
                # 自动存档后退出
                self._auto_save()
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

            # 处理武器UI
            if self.weapon_ui.visible:
                for event in self.events:
                    if self.weapon_ui.handle_event(event):
                        pass
                return  # 武器UI打开时不处理其他输入

            for event in self.events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.PAUSED
                    elif event.key == pygame.K_i:
                        self.inventory_ui.toggle()
                    elif event.key == pygame.K_q:
                        self.quest_ui.toggle()
                    elif event.key == pygame.K_w and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        # Shift+W 打开武器背包
                        self.weapon_ui.toggle()

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

        # 切换到选中途径的角色图片
        set_pathway(pathway_id)

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

        # 设置武器UI引用
        self.weapon_ui.set_references(self.inventory, self.player)

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

        # 创建玩家光源
        pathway_color = PATHWAYS[pathway_id].get("color", GOLD)
        self.lighting.create_player_light(self.player.x, self.player.y, pathway_color)

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
        self.playtime = 0
        self.current_boss = None
        self.is_boss_wave = False
        self.boss_ui.current_boss = None
        self.boss_ui.show_intro = False
        self.boss_ui.show_victory = False

    def _save_game(self, slot):
        """保存游戏"""
        if not self.player:
            return False, "没有可保存的游戏"

        game_data = collect_game_data(self)
        game_data["player"]["pathway"] = self.player_pathway
        success, msg = self.save_system.save_game(slot, game_data)
        return success, msg

    def _load_game(self, slot):
        """读取存档"""
        success, result = self.save_system.load_game(slot)
        if not success:
            self.floating_texts.append(FloatingText(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                f"读档失败: {result}", CRIMSON
            ))
            return False

        # 获取存档数据
        data = result.get("data", {})
        player_data = data.get("player", {})
        pathway_id = player_data.get("pathway", "fool")

        # 确保途径有效
        if pathway_id not in PATHWAYS:
            pathway_id = "fool"

        # 启动游戏
        self._start_game(pathway_id)

        # 应用存档数据
        apply_save_data(self, result)

        # 更新波次（不重新开始）
        self.wave_complete = True
        self.wave_timer = 2.0

        self.save_ui.hide()
        self.state = GameState.PLAYING

        self.floating_texts.append(FloatingText(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
            "读档成功!", (100, 255, 100)
        ))
        return True

    def _auto_save(self):
        """自动存档"""
        if self.player:
            self._save_game("auto")

    def _update(self):
        """更新游戏状态"""
        if self.state == GameState.PLAYING:
            self._update_playing()

    def _update_playing(self):
        """更新游戏中状态"""
        if not self.player:
            return

        # 更新游戏时间
        self.playtime += self.dt

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

        # 更新任务通知
        self.quest_notification.update(self.dt)

        # 更新对话框
        self.dialogue_box.update(self.dt)

        # 更新Boss UI
        self.boss_ui.update(self.dt)

        # 检查Boss战斗中的特殊伤害
        if self.current_boss and self.current_boss.is_alive():
            self._check_boss_damage()

        # 更新光影系统
        self.lighting.update(self.dt)
        if self.lighting.player_light:
            self.lighting.player_light.set_position(self.player.x, self.player.y)

        # 检查玩家是否死亡
        if not self.player.is_alive():
            self._handle_player_death()

    def _update_enemies(self):
        """更新所有敌人"""
        for enemy in self.enemies[:]:
            enemy.update(self.dt, self.player)

            # 更新敌人光源位置
            if hasattr(enemy, 'light') and enemy.light:
                enemy.light.set_position(enemy.x, enemy.y)

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

        # 通知任务系统
        updates = self.quest_system.on_wave_reached(self.current_wave)
        for quest_id, obj_desc, current, required in updates:
            if current >= required:
                self.quest_notification.add(f"目标完成: {obj_desc}", (100, 255, 100), 2.0)

        wave_config = get_wave_enemies(self.current_wave)
        self.is_boss_wave = wave_config.get("is_boss_wave", False)

        if self.is_boss_wave:
            # Boss波次特殊提示
            boss_name = wave_config.get("boss_name", "BOSS")
            self.floating_texts.append(FloatingText(
                SCREEN_WIDTH // 2,
                150,
                f"! BOSS战 !",
                CRIMSON
            ))
            self.floating_texts.append(FloatingText(
                SCREEN_WIDTH // 2,
                200,
                boss_name,
                (255, 200, 100)
            ))
        else:
            self.floating_texts.append(FloatingText(
                SCREEN_WIDTH // 2,
                150,
                f"波次 {self.current_wave}",
                GOLD
            ))

        # 生成敌人位置
        for enemy_type, count in wave_config["enemies"]:
            for _ in range(count):
                if self.is_boss_wave:
                    # Boss在屏幕中央上方生成
                    x = SCREEN_WIDTH // 2
                    y = 150
                else:
                    # 普通敌人在屏幕边缘生成
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

        # 为精英和BOSS添加光源
        if enemy.enemy_type in ["elite", "boss"]:
            light = Light(x, y, radius=100 if enemy.enemy_type == "boss" else 60,
                         color=enemy.color, intensity=0.6, flicker=True)
            enemy.light = light
            self.lighting.add_light(light)

            # 如果是Boss，设置当前Boss并启动Boss UI
            if enemy.enemy_type == "boss":
                self.current_boss = enemy
                self.boss_ui.set_boss(enemy)
        else:
            enemy.light = None

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
                    damage_result = self.player.get_attack_damage()

                    # 处理武器系统返回的元组 (damage, is_crit, effects) 或单一数值
                    is_crit = False
                    weapon_effects = {}
                    if isinstance(damage_result, tuple):
                        damage = damage_result[0]
                        is_crit = damage_result[1] if len(damage_result) > 1 else False
                        weapon_effects = damage_result[2] if len(damage_result) > 2 else {}
                    else:
                        damage = damage_result

                    result = enemy.take_damage(damage)

                    # 攻击命中光效
                    pathway_color = PATHWAYS[self.player_pathway].get("color", GOLD)
                    self.lighting.add_skill_light(
                        enemy.x, enemy.y,
                        pathway_color,
                        radius=60,
                        duration=0.2
                    )

                    # 处理不同的伤害结果
                    if result == "evaded":
                        self.floating_texts.append(FloatingText(
                            enemy.x, enemy.y - 20,
                            "闪避!",
                            (150, 150, 255)
                        ))
                    elif result == 0:
                        self.floating_texts.append(FloatingText(
                            enemy.x, enemy.y - 20,
                            "无敌!",
                            (200, 200, 200)
                        ))
                    elif isinstance(result, tuple) and result[0] == "damage_reflect":
                        actual_damage, reflect_damage = result[1], result[2]
                        self.damage_numbers.append(DamageNumber(
                            enemy.x, enemy.y - 20,
                            actual_damage,
                            GOLD
                        ))
                        # 反弹伤害给玩家
                        self.player.take_damage(reflect_damage)
                        self.damage_numbers.append(DamageNumber(
                            self.player.x, self.player.y - 20,
                            reflect_damage,
                            (100, 200, 255)
                        ))
                        self.floating_texts.append(FloatingText(
                            self.player.x, self.player.y - 40,
                            "反弹!",
                            (100, 200, 255)
                        ))
                    else:
                        # 显示伤害数字，暴击用特殊颜色
                        damage_color = (255, 100, 100) if is_crit else GOLD
                        self.damage_numbers.append(DamageNumber(
                            enemy.x, enemy.y - 20,
                            result,
                            damage_color
                        ))

                        # 显示暴击文字
                        if is_crit:
                            self.floating_texts.append(FloatingText(
                                enemy.x, enemy.y - 40,
                                "暴击!",
                                (255, 100, 100)
                            ))

                        # 处理武器特殊效果
                        if weapon_effects:
                            if weapon_effects.get("stun"):
                                self.floating_texts.append(FloatingText(
                                    enemy.x, enemy.y - 50,
                                    "眩晕!",
                                    (255, 255, 100)
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

                    # 投射物命中光效
                    self.lighting.add_skill_light(
                        enemy.x, enemy.y,
                        self.player.color,
                        radius=50,
                        duration=0.15
                    )

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

        # 移除敌人光源
        if hasattr(enemy, 'light') and enemy.light:
            self.lighting.remove_light(enemy.light)

        # 添加死亡爆炸光效
        self.lighting.add_explosion_light(
            enemy.x, enemy.y,
            enemy.color,
            max_radius=80 if enemy.enemy_type == "boss" else 50,
            duration=0.4
        )

        # 通知任务系统
        updates = self.quest_system.on_enemy_killed(enemy.name)
        for quest_id, obj_desc, current, required in updates:
            if current >= required:
                self.quest_notification.add(f"目标完成: {obj_desc}", (100, 255, 100), 2.0)

        # 显示经验
        self.floating_texts.append(FloatingText(
            enemy.x, enemy.y,
            f"+{enemy.exp} EXP",
            (100, 255, 100)
        ))

        # Boss死亡特殊处理
        if enemy.enemy_type == "boss":
            self.current_boss = None
            self.is_boss_wave = False
            self.boss_ui.clear_boss()

            # Boss击败特殊提示
            self.floating_texts.append(FloatingText(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 50,
                f"击败 {enemy.name}!",
                GOLD
            ))

            # 通知任务系统Boss击杀
            boss_updates = self.quest_system.on_enemy_killed(f"BOSS:{enemy.name}")
            for quest_id, obj_desc, current, required in boss_updates:
                if current >= required:
                    self.quest_notification.add(f"目标完成: {obj_desc}", (100, 255, 100), 2.0)

        # 生成掉落物
        drops = enemy.get_drops()
        for drop in drops:
            self.drops.append({
                "x": enemy.x + random.randint(-20, 20),
                "y": enemy.y + random.randint(-20, 20),
                "item": drop["item"],
                "count": drop["count"],
                "type": "material",  # 材料类型
                "lifetime": 10.0  # 10秒后消失
            })

        # 武器掉落判定
        self._try_drop_weapon(enemy)

    def _try_drop_weapon(self, enemy):
        """尝试从敌人掉落武器"""
        enemy_type = getattr(enemy, 'enemy_type', enemy.name)

        # 遍历所有武器检查是否可从该敌人掉落
        for weapon_name, weapon_data in WEAPONS.items():
            drop_from = weapon_data.get("drop_from", [])
            drop_rate = weapon_data.get("drop_rate", 0)

            if enemy_type in drop_from and drop_rate > 0:
                if random.random() < drop_rate:
                    # 武器掉落!
                    self.drops.append({
                        "x": enemy.x + random.randint(-15, 15),
                        "y": enemy.y + random.randint(-15, 15),
                        "item": weapon_name,
                        "count": 1,
                        "type": "weapon",
                        "quality": weapon_data.get("quality", "common"),
                        "lifetime": 15.0  # 武器15秒消失
                    })

    def _check_boss_damage(self):
        """检查Boss特殊技能对玩家的伤害"""
        if not self.current_boss or not self.player:
            return

        boss = self.current_boss

        # 检查技能预警执行后的伤害
        if boss.skill_warning is None and hasattr(boss, '_pending_skill_damage'):
            damage_result = boss._pending_skill_damage
            del boss._pending_skill_damage
            if damage_result and not self.player.is_invincible:
                _, damage, skill_name = damage_result
                actual_damage = self.player.take_damage(int(damage))
                self.damage_numbers.append(DamageNumber(
                    self.player.x, self.player.y - 20,
                    actual_damage,
                    CRIMSON
                ))
                self.floating_texts.append(FloatingText(
                    self.player.x, self.player.y - 50,
                    skill_name,
                    (255, 100, 100)
                ))

        # 检查地面效果和分身伤害
        damages = boss.get_boss_effects_damage(self.player)
        for damage_type, damage, source in damages:
            if not self.player.is_invincible:
                actual_damage = self.player.take_damage(int(damage))
                self.damage_numbers.append(DamageNumber(
                    self.player.x, self.player.y - 20,
                    actual_damage,
                    CRIMSON
                ))
                if damage_type == "dot":
                    pass  # 持续伤害不显示文字
                else:
                    self.floating_texts.append(FloatingText(
                        self.player.x, self.player.y - 50,
                        source if isinstance(source, str) else "技能",
                        (255, 150, 100)
                    ))

        # 检查沉默效果（禁用玩家技能）
        for effect in boss.ground_effects:
            if effect["type"] == "silence":
                self.player.is_silenced = True
                break
        else:
            if hasattr(self.player, 'is_silenced'):
                self.player.is_silenced = False

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
                item_name = drop["item"]
                item_count = drop["count"]
                drop_type = drop.get("type", "material")

                if drop_type == "weapon":
                    # 武器拾取 - 直接装备或存入背包
                    weapon_data = get_weapon_data(item_name)
                    quality = weapon_data.get("quality", "common")
                    color = QUALITY_COLORS.get(quality, (255, 215, 0))

                    # 添加到背包武器栏
                    self.inventory.add_weapon(item_name)

                    self.floating_texts.append(FloatingText(
                        self.player.x, self.player.y - 40,
                        f"获得武器: {item_name}",
                        color
                    ))

                    # 右上角通知（武器用特殊颜色）
                    self.drop_notification.add(f"★ 武器: {item_name}", color, duration=3.0)

                else:
                    # 材料/消耗品拾取
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

                    # 通知任务系统收集
                    updates = self.quest_system.on_item_collected(item_name, item_count)
                    for quest_id, obj_desc, current, required in updates:
                        if current >= required:
                            self.quest_notification.add(f"目标完成: {obj_desc}", (100, 255, 100), 2.0)

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
            # 绘制任务追踪
            self.quest_tracker.draw(self.quest_system)
            # 绘制任务通知
            self.quest_notification.draw(self.screen, self.fonts)
            # 绘制背包UI（如果打开）
            if self.inventory_ui.is_open:
                self.inventory_ui.draw(self.inventory, self.player, self.potion_system)
            # 绘制任务UI（如果打开）
            if self.quest_ui.is_open:
                self.quest_ui.draw(self.quest_system, self.player)
            # 绘制武器UI（如果打开）
            if self.weapon_ui.visible:
                self.weapon_ui.draw()
            # 绘制炮制结果
            self.craft_result_ui.draw()
            # 绘制对话框
            self.dialogue_box.draw()

        elif self.state == GameState.PAUSED:
            self._draw_playing()
            self.pause_menu.draw()

        elif self.state == "save_load":
            # 如果有游戏在进行，先绘制游戏画面
            if self.player:
                self._draw_playing()
            else:
                self.screen.fill(MIDNIGHT_BLUE)
            self.save_ui.draw()

        elif self.state == GameState.GAME_OVER:
            self._draw_playing()
            self._draw_game_over()

        pygame.display.flip()

    def _draw_playing(self):
        """绘制游戏画面"""
        self.screen.fill(MIDNIGHT_BLUE)
        self._draw_street_background()

        # 绘制掉落物（带发光效果）
        for drop in self.drops:
            alpha = int(255 * min(1, drop["lifetime"]))
            drop_type = drop.get("type", "material")

            if drop_type == "weapon":
                # 武器掉落 - 用品质颜色和剑形图标
                quality = drop.get("quality", "common")
                quality_color = QUALITY_COLORS.get(quality, (255, 215, 0))

                # 绘制光晕（更大更亮）
                glow_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
                glow_alpha = int(100 * min(1, drop["lifetime"]))
                pygame.draw.circle(glow_surface, (*quality_color, glow_alpha), (25, 25), 22)
                pygame.draw.circle(glow_surface, (*quality_color, glow_alpha // 2), (25, 25), 15)
                self.screen.blit(glow_surface, (drop["x"] - 25, drop["y"] - 25))

                # 绘制武器图标（剑形）
                weapon_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
                # 剑身
                pygame.draw.line(weapon_surface, (*quality_color, alpha), (10, 2), (10, 14), 3)
                # 剑柄
                pygame.draw.line(weapon_surface, (150, 100, 50, alpha), (10, 14), (10, 18), 2)
                # 护手
                pygame.draw.line(weapon_surface, (*quality_color, alpha), (5, 12), (15, 12), 2)
                self.screen.blit(weapon_surface, (drop["x"] - 10, drop["y"] - 10))
            else:
                # 材料掉落 - 原有效果
                glow_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
                glow_alpha = int(80 * min(1, drop["lifetime"]))
                pygame.draw.circle(glow_surface, (255, 215, 0, glow_alpha), (20, 20), 18)
                pygame.draw.circle(glow_surface, (255, 230, 100, glow_alpha // 2), (20, 20), 12)
                self.screen.blit(glow_surface, (drop["x"] - 20, drop["y"] - 20))
                # 绘制物品
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

        # 渲染光影效果
        self.lighting.render(self.screen)

        # 绘制HUD
        if self.player:
            pathway_name = PATHWAYS[self.player_pathway]["name"]
            self.game_hud.draw(self.player, pathway_name)
            # 绘制武器HUD
            self.weapon_hud.draw(self.screen, self.player)

        # 绘制波次信息
        self._draw_wave_info()

        # 绘制掉落通知
        self.drop_notification.draw(self.screen, self.fonts)

        # 绘制Boss UI
        self.boss_ui.draw(self.screen)

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

        # 绘制建筑和窗户
        for x, y, w, h in buildings:
            pygame.draw.rect(self.screen, (30, 30, 50), (x, y, w, h))

            for wy in range(y + 20, y + h - 40, 50):
                for wx in range(x + 15, x + w - 20, 35):
                    if (wx + wy) % 100 < 70:
                        # 根据位置确定窗户是否亮灯
                        seed = (wx * 1000 + wy) % 100
                        if seed < 40:  # 40%的窗户亮着
                            # 暖色灯光
                            window_color = (255, 200, 100)
                            # 绘制窗户光晕
                            glow = pygame.Surface((30, 40), pygame.SRCALPHA)
                            pygame.draw.rect(glow, (255, 180, 80, 60), (0, 0, 30, 40))
                            self.screen.blit(glow, (wx - 5, wy - 5))
                        else:
                            window_color = (40, 35, 25)

                        pygame.draw.rect(self.screen, window_color, (wx, wy, 20, 30))

        # 绘制街灯
        lamp_positions = [150, 400, 650, 900]
        for lx in lamp_positions:
            # 灯柱
            pygame.draw.rect(self.screen, (60, 60, 70), (lx - 3, SCREEN_HEIGHT - 230, 6, 80))
            # 灯头
            pygame.draw.rect(self.screen, (80, 80, 90), (lx - 10, SCREEN_HEIGHT - 235, 20, 10))
            # 灯光效果
            lamp_glow = pygame.Surface((80, 60), pygame.SRCALPHA)
            pygame.draw.ellipse(lamp_glow, (255, 200, 100, 40), (0, 0, 80, 60))
            self.screen.blit(lamp_glow, (lx - 40, SCREEN_HEIGHT - 260))

        fog = pygame.Surface((SCREEN_WIDTH, 100))
        fog.fill((40, 40, 60))
        fog.set_alpha(50)
        self.screen.blit(fog, (0, SCREEN_HEIGHT - 200))


if __name__ == "__main__":
    game = Game()
    game.run()
