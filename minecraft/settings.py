# Minecraft 游戏设置

# 窗口设置
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60
TITLE = "Minecraft 2D"

# 方块设置
BLOCK_SIZE = 32
CHUNK_WIDTH = 16
CHUNK_HEIGHT = 128
WORLD_WIDTH = 256  # 方块数

# 世界生成
SEA_LEVEL = 64
GROUND_LEVEL = 70
CAVE_THRESHOLD = 0.4

# 玩家设置
PLAYER_WIDTH = 24
PLAYER_HEIGHT = 48
PLAYER_SPEED = 5
JUMP_FORCE = 12
GRAVITY = 0.5
MAX_FALL_SPEED = 15

# 挖掘设置
MINING_RANGE = 4  # 方块距离
PLACE_RANGE = 5

# 背包设置
HOTBAR_SLOTS = 9
INVENTORY_ROWS = 3
INVENTORY_COLS = 9

# 颜色
COLORS = {
    'sky_day': (135, 206, 235),
    'sky_night': (25, 25, 112),
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'gray': (128, 128, 128),
    'dark_gray': (64, 64, 64),
    'brown': (139, 69, 19),
    'green': (34, 139, 34),
    'dark_green': (0, 100, 0),
    'blue': (0, 0, 255),
    'light_blue': (173, 216, 230),
    'yellow': (255, 255, 0),
    'red': (255, 0, 0),
    'orange': (255, 165, 0),
}

# 方块类型
class BlockType:
    AIR = 0
    DIRT = 1
    GRASS = 2
    STONE = 3
    COBBLESTONE = 4
    WOOD = 5
    LEAVES = 6
    SAND = 7
    WATER = 8
    COAL_ORE = 9
    IRON_ORE = 10
    GOLD_ORE = 11
    DIAMOND_ORE = 12
    BEDROCK = 13
    PLANKS = 14
    CRAFTING_TABLE = 15
    FURNACE = 16
    CHEST = 17
    GLASS = 18
    BRICK = 19
    OBSIDIAN = 20
    GRAVEL = 21
    TNT = 22
    BOOKSHELF = 23
    TORCH = 24

# 方块属性
BLOCK_DATA = {
    BlockType.AIR: {'name': '空气', 'hardness': 0, 'solid': False, 'transparent': True, 'color': None},
    BlockType.DIRT: {'name': '泥土', 'hardness': 0.5, 'solid': True, 'transparent': False, 'color': (139, 90, 43)},
    BlockType.GRASS: {'name': '草方块', 'hardness': 0.6, 'solid': True, 'transparent': False, 'color': (86, 125, 70), 'top_color': (86, 170, 70)},
    BlockType.STONE: {'name': '石头', 'hardness': 1.5, 'solid': True, 'transparent': False, 'color': (128, 128, 128)},
    BlockType.COBBLESTONE: {'name': '圆石', 'hardness': 2.0, 'solid': True, 'transparent': False, 'color': (100, 100, 100)},
    BlockType.WOOD: {'name': '原木', 'hardness': 2.0, 'solid': True, 'transparent': False, 'color': (101, 67, 33)},
    BlockType.LEAVES: {'name': '树叶', 'hardness': 0.2, 'solid': True, 'transparent': True, 'color': (34, 139, 34)},
    BlockType.SAND: {'name': '沙子', 'hardness': 0.5, 'solid': True, 'transparent': False, 'color': (210, 180, 140)},
    BlockType.WATER: {'name': '水', 'hardness': 100, 'solid': False, 'transparent': True, 'color': (64, 164, 223, 180)},
    BlockType.COAL_ORE: {'name': '煤矿石', 'hardness': 3.0, 'solid': True, 'transparent': False, 'color': (60, 60, 60)},
    BlockType.IRON_ORE: {'name': '铁矿石', 'hardness': 3.0, 'solid': True, 'transparent': False, 'color': (136, 119, 102)},
    BlockType.GOLD_ORE: {'name': '金矿石', 'hardness': 3.0, 'solid': True, 'transparent': False, 'color': (143, 131, 87)},
    BlockType.DIAMOND_ORE: {'name': '钻石矿石', 'hardness': 3.0, 'solid': True, 'transparent': False, 'color': (70, 200, 200)},
    BlockType.BEDROCK: {'name': '基岩', 'hardness': -1, 'solid': True, 'transparent': False, 'color': (40, 40, 40)},
    BlockType.PLANKS: {'name': '木板', 'hardness': 2.0, 'solid': True, 'transparent': False, 'color': (188, 152, 98)},
    BlockType.CRAFTING_TABLE: {'name': '工作台', 'hardness': 2.5, 'solid': True, 'transparent': False, 'color': (139, 90, 43)},
    BlockType.FURNACE: {'name': '熔炉', 'hardness': 3.5, 'solid': True, 'transparent': False, 'color': (100, 100, 100)},
    BlockType.CHEST: {'name': '箱子', 'hardness': 2.5, 'solid': True, 'transparent': False, 'color': (139, 90, 43)},
    BlockType.GLASS: {'name': '玻璃', 'hardness': 0.3, 'solid': True, 'transparent': True, 'color': (200, 220, 255, 100)},
    BlockType.BRICK: {'name': '砖块', 'hardness': 2.0, 'solid': True, 'transparent': False, 'color': (150, 74, 63)},
    BlockType.OBSIDIAN: {'name': '黑曜石', 'hardness': 50, 'solid': True, 'transparent': False, 'color': (20, 18, 29)},
    BlockType.GRAVEL: {'name': '砂砾', 'hardness': 0.6, 'solid': True, 'transparent': False, 'color': (136, 126, 126)},
    BlockType.TNT: {'name': 'TNT', 'hardness': 0, 'solid': True, 'transparent': False, 'color': (200, 50, 50)},
    BlockType.BOOKSHELF: {'name': '书架', 'hardness': 1.5, 'solid': True, 'transparent': False, 'color': (188, 152, 98)},
    BlockType.TORCH: {'name': '火把', 'hardness': 0, 'solid': False, 'transparent': True, 'color': (255, 200, 50)},
}

# 掉落物
BLOCK_DROPS = {
    BlockType.DIRT: [(BlockType.DIRT, 1)],
    BlockType.GRASS: [(BlockType.DIRT, 1)],
    BlockType.STONE: [(BlockType.COBBLESTONE, 1)],
    BlockType.COBBLESTONE: [(BlockType.COBBLESTONE, 1)],
    BlockType.WOOD: [(BlockType.WOOD, 1)],
    BlockType.LEAVES: [(BlockType.LEAVES, 1)],  # 有几率掉树苗
    BlockType.SAND: [(BlockType.SAND, 1)],
    BlockType.COAL_ORE: [(BlockType.COAL_ORE, 1)],
    BlockType.IRON_ORE: [(BlockType.IRON_ORE, 1)],
    BlockType.GOLD_ORE: [(BlockType.GOLD_ORE, 1)],
    BlockType.DIAMOND_ORE: [(BlockType.DIAMOND_ORE, 1)],
    BlockType.PLANKS: [(BlockType.PLANKS, 1)],
    BlockType.CRAFTING_TABLE: [(BlockType.CRAFTING_TABLE, 1)],
    BlockType.FURNACE: [(BlockType.FURNACE, 1)],
    BlockType.CHEST: [(BlockType.CHEST, 1)],
    BlockType.GLASS: [],  # 玻璃破碎不掉落
    BlockType.BRICK: [(BlockType.BRICK, 1)],
    BlockType.GRAVEL: [(BlockType.GRAVEL, 1)],
    BlockType.TNT: [(BlockType.TNT, 1)],
    BlockType.BOOKSHELF: [(BlockType.PLANKS, 6)],
}

# 合成配方
RECIPES = {
    # 木板 (1原木 = 4木板)
    'planks': {
        'ingredients': {BlockType.WOOD: 1},
        'result': (BlockType.PLANKS, 4)
    },
    # 工作台
    'crafting_table': {
        'ingredients': {BlockType.PLANKS: 4},
        'result': (BlockType.CRAFTING_TABLE, 1)
    },
    # 熔炉
    'furnace': {
        'ingredients': {BlockType.COBBLESTONE: 8},
        'result': (BlockType.FURNACE, 1)
    },
    # 箱子
    'chest': {
        'ingredients': {BlockType.PLANKS: 8},
        'result': (BlockType.CHEST, 1)
    },
    # 火把
    'torch': {
        'ingredients': {BlockType.COAL_ORE: 1, BlockType.PLANKS: 1},
        'result': (BlockType.TORCH, 4)
    },
}
