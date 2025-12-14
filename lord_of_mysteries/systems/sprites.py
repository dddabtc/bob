"""
精灵图系统 - 加载和管理角色图片
支持从单独文件加载每个途径的角色图片
启动时显示进度条，预缩放常用尺寸
"""

import pygame
import os


# 途径名称到英文文件名的映射（基于img/charactor目录下的实际文件）
# 22条途径对应22个图片文件
PATHWAY_FILE_NAMES = {
    # 诡秘之主组
    "占卜家": "Seer",                    # The Seer
    "学徒": "Apprentice",                # The Apprentice
    "偷盗者": "Marauder",                # The Marauder
    # 上帝组
    "观众": "spectator",                 # The Spectator
    "秘祈人": "SECRETS SUPPLICANT",      # The Secrets Supplicant
    "歌颂者": "Bard",                    # The Bard
    "水手": "Sailor",                    # The Sailor
    "阅读者": "Reader",                  # The Reader
    # 永暗组
    "不眠者": "Darkness",                # The Sleepless
    "收尸人": "Death",                   # The Corpse Collector
    "战士": "Giant",                     # The Warrior
    # 灾祸组
    "猎人": "RedPriest",                 # The Hunter
    "刺客": "Witch",                     # The Assassin
    # 根源组
    "耕种者": "MOTHER",                  # The Planter
    "药师": "MOON",                      # The Apothecary
    # 无序组
    "律师": "BLACK EMPEROR",             # The Lawyer
    "仲裁人": "JUSTICIAR",               # The Arbiter
    # 知识妖鬼组
    "通识者": "PERFECTIONIST",           # The Savant
    "窥秘人": "Hermit",                  # The Mystery Pryer
    # 恶魔之父组
    "罪犯": "ABYSS",                     # The Criminal
    "囚犯": "CHAINED",                   # The Prisoner
    # 光之钥组
    "怪物": "THE WHEEL OF FORTUNE",      # The Monster
}

# 预缩放的常用尺寸
PRESET_SIZES = {
    "tiny": (50, 65),      # 序列预览小图标
    "small": (60, 80),     # 游戏中角色
    "medium": (120, 160),  # 途径详情
    "large": (180, 240),   # 确认界面大图
}


class SpriteManager:
    """精灵图管理器"""

    def __init__(self):
        self.base_path = None
        self.all_sequence_sprites = {}  # {pathway_name: {sequence: {size_name: sprite}}}
        self.current_pathway = "占卜家"
        self.loading_progress = 0
        self.loading_total = 0
        self.loading_current = ""

    def init_with_progress(self, base_path, screen):
        """带进度条的初始化"""
        self.base_path = base_path
        self._load_all_pathways_with_progress(screen)

    def _draw_loading_screen(self, screen, progress, total, current_name):
        """绘制加载进度界面"""
        screen.fill((20, 20, 30))

        # 使用系统中文字体
        try:
            font_path = "/System/Library/Fonts/PingFang.ttc"
            font_large = pygame.font.Font(font_path, 36)
            font_small = pygame.font.Font(font_path, 20)
        except:
            font_large = pygame.font.Font(None, 48)
            font_small = pygame.font.Font(None, 24)

        # 标题
        title = font_large.render("正在加载...", True, (218, 165, 32))
        title_rect = title.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 60))
        screen.blit(title, title_rect)

        # 当前加载项
        if current_name:
            current = font_small.render(f"加载途径: {current_name}", True, (150, 150, 150))
            current_rect = current.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))
            screen.blit(current, current_rect)

        # 进度条背景
        bar_width = 400
        bar_height = 20
        bar_x = (screen.get_width() - bar_width) // 2
        bar_y = screen.get_height() // 2 + 20
        pygame.draw.rect(screen, (50, 50, 60), (bar_x, bar_y, bar_width, bar_height), border_radius=10)

        # 进度条填充
        if total > 0:
            fill_width = int((progress / total) * bar_width)
            if fill_width > 0:
                pygame.draw.rect(screen, (100, 180, 100), (bar_x, bar_y, fill_width, bar_height), border_radius=10)

        # 进度文字
        percent = int((progress / total) * 100) if total > 0 else 0
        progress_text = font_small.render(f"{progress}/{total} ({percent}%)", True, (200, 200, 200))
        progress_rect = progress_text.get_rect(center=(screen.get_width() // 2, bar_y + 45))
        screen.blit(progress_text, progress_rect)

        pygame.display.flip()

    def _load_all_pathways_with_progress(self, screen):
        """带进度条加载所有途径图片"""
        if not self.base_path:
            return

        img_dir = os.path.join(self.base_path, "img", "charactor")
        if not os.path.exists(img_dir):
            print(f"角色图片目录不存在: {img_dir}")
            return

        # 计算总数
        valid_pathways = []
        for pathway_name, file_name in PATHWAY_FILE_NAMES.items():
            file_path = os.path.join(img_dir, f"{file_name}.png")
            if os.path.exists(file_path):
                valid_pathways.append((pathway_name, file_name, file_path))

        total = len(valid_pathways)

        # 加载每个途径
        for i, (pathway_name, file_name, file_path) in enumerate(valid_pathways):
            # 更新进度显示
            self._draw_loading_screen(screen, i, total, pathway_name)

            try:
                # 加载原图
                sprite_sheet = pygame.image.load(file_path).convert_alpha()
                # 分割并预缩放
                self._split_and_prescale(pathway_name, sprite_sheet)
                print(f"加载途径图片成功: {pathway_name} ({file_name}.png)")
            except Exception as e:
                print(f"加载途径图片失败 {pathway_name}: {e}")

            # 处理事件防止无响应
            pygame.event.pump()

        # 完成
        self._draw_loading_screen(screen, total, total, "加载完成!")
        pygame.time.wait(300)

    def _split_and_prescale(self, pathway_name, sprite_sheet):
        """分割图集并预缩放到常用尺寸"""
        sheet_width = sprite_sheet.get_width()
        sheet_height = sprite_sheet.get_height()

        cols = 5
        rows = 2
        char_width = sheet_width // cols
        char_height = sheet_height // rows

        sequence_positions = {
            9: (0, 0), 8: (0, 1), 7: (0, 2), 6: (0, 3), 5: (0, 4),
            4: (1, 0), 3: (1, 1), 2: (1, 2), 1: (1, 3), 0: (1, 4),
        }

        self.all_sequence_sprites[pathway_name] = {}

        for sequence, (row, col) in sequence_positions.items():
            x = col * char_width
            y = row * char_height

            # 裁剪原始尺寸
            original = pygame.Surface((char_width, char_height), pygame.SRCALPHA)
            original.blit(sprite_sheet, (0, 0), (x, y, char_width, char_height))

            # 预缩放到各种常用尺寸
            self.all_sequence_sprites[pathway_name][sequence] = {
                "original": original,
            }
            for size_name, size in PRESET_SIZES.items():
                scaled = pygame.transform.smoothscale(original, size)
                self.all_sequence_sprites[pathway_name][sequence][size_name] = scaled

    def set_current_pathway(self, pathway_name):
        """设置当前途径"""
        if pathway_name in self.all_sequence_sprites:
            self.current_pathway = pathway_name

    def get_character_sprite(self, sequence, size=None):
        """获取角色图片（优先使用预缩放版本）"""
        if self.current_pathway not in self.all_sequence_sprites:
            return None

        pathway_sprites = self.all_sequence_sprites[self.current_pathway]
        if sequence not in pathway_sprites:
            return None

        sprites = pathway_sprites[sequence]

        if size is None:
            return sprites.get("original")

        # 查找匹配的预缩放尺寸
        for size_name, preset_size in PRESET_SIZES.items():
            if size == preset_size:
                return sprites.get(size_name)

        # 找不到预设尺寸，动态缩放（较少发生）
        original = sprites.get("original")
        if original:
            return pygame.transform.smoothscale(original, size)
        return None

    def get_character_portrait(self, sequence, size=(80, 100)):
        """获取角色头像"""
        sprite = self.get_character_sprite(sequence)
        if sprite:
            portrait_height = sprite.get_height() // 2
            portrait = pygame.Surface((sprite.get_width(), portrait_height), pygame.SRCALPHA)
            portrait.blit(sprite, (0, 0))
            return pygame.transform.smoothscale(portrait, size)
        return None

    def get_available_pathways(self):
        """获取已加载的途径列表"""
        return list(self.all_sequence_sprites.keys())

    def has_pathway_sprites(self, pathway_name):
        """检查途径是否有对应的图片"""
        return pathway_name in self.all_sequence_sprites


# 全局精灵管理器实例
sprite_manager = SpriteManager()


def init_sprites_with_progress(base_path, screen):
    """带进度条初始化精灵图系统"""
    sprite_manager.init_with_progress(base_path, screen)
    return len(sprite_manager.all_sequence_sprites) > 0


def init_sprites(base_path):
    """初始化精灵图系统（无进度条，兼容旧接口）"""
    # 创建临时窗口显示进度
    screen = pygame.display.get_surface()
    if screen:
        sprite_manager.init_with_progress(base_path, screen)
    return len(sprite_manager.all_sequence_sprites) > 0


def set_pathway(pathway_name):
    """设置当前途径"""
    sprite_manager.set_current_pathway(pathway_name)


def get_sequence_sprite(sequence, size=None):
    """获取序列对应的角色图片"""
    return sprite_manager.get_character_sprite(sequence, size)


def get_sequence_portrait(sequence, size=(80, 100)):
    """获取序列对应的角色头像"""
    return sprite_manager.get_character_portrait(sequence, size)


def get_available_pathways():
    """获取已加载的途径列表"""
    return sprite_manager.get_available_pathways()


def has_pathway_sprites(pathway_name):
    """检查途径是否有对应的图片"""
    return sprite_manager.has_pathway_sprites(pathway_name)
