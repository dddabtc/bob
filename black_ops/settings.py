"""
Black Ops - 游戏配置
"""

import math
from enum import Enum, auto

# 屏幕设置
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
TITLE = "Black Ops - 黑色行动"

# 光线投射设置 (平衡画质和性能)
FOV = math.pi / 3  # 60度视野
HALF_FOV = FOV / 2
NUM_RAYS = 320  # 平衡画质和性能
MAX_DEPTH = 20  # 渲染距离
DELTA_ANGLE = FOV / NUM_RAYS
SCALE = max(1, SCREEN_WIDTH // NUM_RAYS)  # 每条光线的宽度

# 纹理设置
TEXTURE_SIZE = 128  # 纹理大小
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

# 画质增强
ENABLE_SHADOWS = True
ENABLE_FOG = True
FOG_START = 8
FOG_END = 30
AMBIENT_LIGHT = 0.3

# 玩家设置
PLAYER_SPEED = 3.0
PLAYER_SPRINT_SPEED = 5.0
PLAYER_ROT_SPEED = 2.5
PLAYER_SIZE = 0.3  # 碰撞半径
MOUSE_SENSITIVITY = 0.002
MOUSE_MAX_REL = 40

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 200)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (180, 180, 180)

# 天空和地面颜色
SKY_COLOR = (100, 150, 200)
FLOOR_COLOR = (50, 50, 50)

# 墙壁颜色 (用于不同类型的墙)
WALL_COLORS = {
    1: (150, 150, 150),  # 灰色混凝土
    2: (139, 90, 43),    # 棕色木墙
    3: (100, 100, 120),  # 蓝灰色金属
    4: (80, 120, 80),    # 绿色军事
    5: (120, 60, 60),    # 红砖
}

# HUD颜色
HUD_BG = (0, 0, 0, 180)
HUD_TEXT = (255, 255, 255)
HUD_HEALTH = (200, 50, 50)
HUD_ARMOR = (50, 100, 200)
HUD_AMMO = (255, 200, 0)

# 游戏状态
class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    MISSION_BRIEFING = auto()
    MISSION_COMPLETE = auto()
    GAME_OVER = auto()
    SETTINGS = auto()
    WEAPON_SELECT = auto()

# 字体大小
FONT_SIZES = {
    "small": 18,
    "medium": 24,
    "large": 36,
    "title": 48,
    "huge": 72,
}

# 武器类型
class WeaponType(Enum):
    PISTOL = "pistol"
    SMG = "smg"
    ASSAULT_RIFLE = "assault_rifle"
    SNIPER = "sniper"
    SHOTGUN = "shotgun"
    KNIFE = "knife"

# 敌人状态
class EnemyState(Enum):
    IDLE = auto()
    PATROL = auto()
    ALERT = auto()
    COMBAT = auto()
    DEAD = auto()

# 地图符号
MAP_SYMBOLS = {
    '.': 0,   # 空地
    '#': 1,   # 墙壁类型1
    'W': 2,   # 墙壁类型2
    'M': 3,   # 墙壁类型3
    'G': 4,   # 墙壁类型4
    'B': 5,   # 墙壁类型5
    'S': 0,   # 玩家起点 (空地)
    'E': 0,   # 敌人位置 (空地)
    'I': 0,   # 物品位置 (空地)
    'X': 0,   # 出口 (空地)
    'D': 6,   # 门
}

# 物品类型
class ItemType(Enum):
    HEALTH = "health"
    ARMOR = "armor"
    AMMO = "ammo"
    WEAPON = "weapon"
    INTEL = "intel"
    KEY = "key"
