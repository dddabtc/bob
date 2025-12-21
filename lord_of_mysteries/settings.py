"""
游戏配置文件
"""

# 窗口设置
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
TITLE = "诡秘之主 - Lord of Mysteries"

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# 主题色
GOLD = (218, 165, 32)
DARK_GOLD = (184, 134, 11)
CRIMSON = (220, 20, 60)
DARK_BLUE = (25, 25, 112)
MIDNIGHT_BLUE = (15, 15, 60)
PURPLE = (128, 0, 128)
DARK_PURPLE = (75, 0, 130)

# UI颜色
MENU_BG = (20, 20, 35)
MENU_TEXT = (200, 180, 140)
MENU_HIGHLIGHT = (255, 215, 0)
BUTTON_NORMAL = (60, 50, 80)
BUTTON_HOVER = (80, 70, 110)
BUTTON_CLICK = (100, 90, 130)

# 血条颜色
HP_RED = (200, 50, 50)
HP_GREEN = (50, 200, 50)
HP_BG = (40, 40, 40)

# 游戏状态
class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    INVENTORY = "inventory"
    DIALOG = "dialog"
    PATHWAY_SELECT = "pathway_select"
    POTION_CRAFT = "potion_craft"
    GAME_OVER = "game_over"

# 玩家设置
PLAYER_SPEED = 5
PLAYER_SIZE = 40

# 字体设置（将在游戏中加载）
FONT_SIZES = {
    "title": 72,
    "large": 48,
    "medium": 32,
    "small": 24,
    "tiny": 18
}

# 语言设置
DEFAULT_LANGUAGE = "zh_CN"  # 默认语言: zh_CN (简体中文), en_US (English)
