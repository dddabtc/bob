"""
精灵图系统 - 加载和管理角色图片
支持从单独文件加载每个途径的角色图片
"""

import pygame
import os


# 途径名称到英文文件名的映射
PATHWAY_FILE_NAMES = {
    # 原有11条途径
    "占卜家": "Seer",
    "隐者": "Marauder",
    "观众": "spectator",
    "读者": "Reader",
    "黑夜": "Darkness",
    "死神": "Death",
    "红祭司": "RedPriest",
    "水手": "Sailor",
    "巨人": "Giant",
    "吟游诗人": "Bard",
    "学徒": "Apprentice",
    # 新增11条途径
    "深渊": "ABYSS",
    "黑皇帝": "BLACK EMPEROR",
    "囚徒": "CHAINED",
    "隐士": "Hermit",
    "审判官": "JUSTICIAR",
    "月亮": "MOON",
    "母亲": "MOTHER",
    "完美者": "PERFECTIONIST",
    "命运之轮": "THE WHEEL OF FORTUNE",
    "女巫": "Witch",
}

# 序列号到序列名称的映射（占卜家途径）
SEER_SEQUENCE_NAMES = {
    9: "占卜家",
    8: "小丑",
    7: "魔术师",
    6: "无面人",
    5: "秘偶大师",
    4: "诡法师",
    3: "古代学者",
    2: "奇迹师",
    1: "诡秘侍者",
    0: "愚者",
}


class SpriteManager:
    """精灵图管理器"""

    def __init__(self):
        self.base_path = None
        self.pathway_sprites = {}  # 按途径存储的精灵图集 {pathway_name: sprite_sheet}
        self.sequence_sprites = {}  # 按序列存储的角色图片 {sequence: sprite}
        self.current_pathway = "占卜家"  # 当前途径

    def init(self, base_path):
        """初始化精灵图系统"""
        self.base_path = base_path
        self._load_all_pathways()

    def _load_all_pathways(self):
        """加载所有可用的途径图片"""
        if not self.base_path:
            return

        img_dir = os.path.join(self.base_path, "img", "charactor")
        if not os.path.exists(img_dir):
            print(f"角色图片目录不存在: {img_dir}")
            return

        # 遍历所有途径，尝试加载对应的图片
        for pathway_name, file_name in PATHWAY_FILE_NAMES.items():
            file_path = os.path.join(img_dir, f"{file_name}.png")
            if os.path.exists(file_path):
                try:
                    sprite_sheet = pygame.image.load(file_path).convert_alpha()
                    self.pathway_sprites[pathway_name] = sprite_sheet
                    print(f"加载途径图片成功: {pathway_name} ({file_name}.png)")
                except Exception as e:
                    print(f"加载途径图片失败 {pathway_name}: {e}")

        # 默认加载占卜家途径的序列图片
        if "占卜家" in self.pathway_sprites:
            self._split_pathway_sheet("占卜家")

    def set_current_pathway(self, pathway_name):
        """设置当前途径并加载对应的序列图片"""
        if pathway_name == self.current_pathway:
            return

        self.current_pathway = pathway_name
        if pathway_name in self.pathway_sprites:
            self._split_pathway_sheet(pathway_name)

    def _split_pathway_sheet(self, pathway_name):
        """将途径图集分割为单个序列图片"""
        if pathway_name not in self.pathway_sprites:
            return

        sprite_sheet = self.pathway_sprites[pathway_name]
        sheet_width = sprite_sheet.get_width()
        sheet_height = sprite_sheet.get_height()

        # 图片布局: 2行5列，每个角色图片
        cols = 5
        rows = 2
        char_width = sheet_width // cols
        char_height = sheet_height // rows

        # 序列对应位置 (行, 列) - 从序列9开始，到序列0
        # 第一行: 序列9, 8, 7, 6, 5
        # 第二行: 序列4, 3, 2, 1, 0
        sequence_positions = {
            9: (0, 0),
            8: (0, 1),
            7: (0, 2),
            6: (0, 3),
            5: (0, 4),
            4: (1, 0),
            3: (1, 1),
            2: (1, 2),
            1: (1, 3),
            0: (1, 4),
        }

        self.sequence_sprites.clear()
        for sequence, (row, col) in sequence_positions.items():
            x = col * char_width
            y = row * char_height

            # 裁剪出单个角色
            sprite = pygame.Surface((char_width, char_height), pygame.SRCALPHA)
            sprite.blit(sprite_sheet, (0, 0), (x, y, char_width, char_height))

            self.sequence_sprites[sequence] = sprite

    def get_character_sprite(self, sequence, size=None):
        """获取指定序列的角色图片"""
        if sequence in self.sequence_sprites:
            sprite = self.sequence_sprites[sequence]
            if size:
                return pygame.transform.scale(sprite, size)
            return sprite
        return None

    def get_character_portrait(self, sequence, size=(80, 100)):
        """获取角色头像（用于HUD等）"""
        sprite = self.get_character_sprite(sequence)
        if sprite:
            # 裁剪上半部分作为头像
            portrait_height = sprite.get_height() // 2
            portrait = pygame.Surface((sprite.get_width(), portrait_height), pygame.SRCALPHA)
            portrait.blit(sprite, (0, 0))
            return pygame.transform.scale(portrait, size)
        return None

    def get_available_pathways(self):
        """获取已加载的途径列表"""
        return list(self.pathway_sprites.keys())

    def has_pathway_sprites(self, pathway_name):
        """检查途径是否有对应的图片"""
        return pathway_name in self.pathway_sprites


# 全局精灵管理器实例
sprite_manager = SpriteManager()


def init_sprites(base_path):
    """初始化精灵图系统"""
    sprite_manager.init(base_path)
    return len(sprite_manager.pathway_sprites) > 0


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
