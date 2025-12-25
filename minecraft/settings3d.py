# Minecraft 3D 游戏设置

# 窗口设置
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
TITLE = "Minecraft 3D"

# 方块设置
BLOCK_SIZE = 1.0

# 区块设置
CHUNK_SIZE = 16  # 16x16x128 方块
RENDER_DISTANCE = 2  # 渲染距离（区块数）- 降低以提高性能

# 世界设置
WORLD_HEIGHT = 128
SEA_LEVEL = 32
GROUND_LEVEL = 40

# 玩家设置
PLAYER_HEIGHT = 1.8
PLAYER_WIDTH = 0.6
PLAYER_SPEED = 5.0
SPRINT_SPEED = 8.0
JUMP_FORCE = 8.0
GRAVITY = 25.0
MAX_FALL_SPEED = 50.0

# 鼠标灵敏度
MOUSE_SENSITIVITY = 0.002

# 视野
FOV = 70.0
NEAR_PLANE = 0.1
FAR_PLANE = 1000.0

# 挖掘设置
MINING_RANGE = 5.0
PLACE_RANGE = 5.0

# 背包设置
HOTBAR_SLOTS = 9
INVENTORY_ROWS = 3
INVENTORY_COLS = 9


# 方块类型
class BlockType:
    AIR = 0
    GRASS = 1
    DIRT = 2
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
    GLASS = 15
    BRICK = 16
    SNOW = 17
    ICE = 18
    GRAVEL = 19


# 方块颜色 (R, G, B) - 每个面可以不同
BLOCK_COLORS = {
    BlockType.GRASS: {
        'top': (0.4, 0.8, 0.3),
        'bottom': (0.55, 0.35, 0.17),
        'side': (0.5, 0.4, 0.25),  # 棕绿混合色
    },
    BlockType.DIRT: {
        'all': (0.55, 0.35, 0.17),
    },
    BlockType.STONE: {
        'all': (0.5, 0.5, 0.5),
    },
    BlockType.COBBLESTONE: {
        'all': (0.4, 0.4, 0.4),
    },
    BlockType.WOOD: {
        'top': (0.6, 0.5, 0.3),
        'bottom': (0.6, 0.5, 0.3),
        'side': (0.4, 0.26, 0.13),
    },
    BlockType.LEAVES: {
        'all': (0.2, 0.6, 0.2),
    },
    BlockType.SAND: {
        'all': (0.82, 0.7, 0.55),
    },
    BlockType.WATER: {
        'all': (0.2, 0.4, 0.8),
    },
    BlockType.COAL_ORE: {
        'all': (0.3, 0.3, 0.3),
    },
    BlockType.IRON_ORE: {
        'all': (0.6, 0.55, 0.5),
    },
    BlockType.GOLD_ORE: {
        'all': (0.8, 0.7, 0.2),
    },
    BlockType.DIAMOND_ORE: {
        'all': (0.3, 0.8, 0.85),
    },
    BlockType.BEDROCK: {
        'all': (0.15, 0.15, 0.15),
    },
    BlockType.PLANKS: {
        'all': (0.7, 0.55, 0.35),
    },
    BlockType.GLASS: {
        'all': (0.8, 0.9, 1.0),
    },
    BlockType.BRICK: {
        'all': (0.6, 0.3, 0.25),
    },
    BlockType.SNOW: {
        'all': (0.95, 0.95, 0.98),
    },
    BlockType.ICE: {
        'all': (0.7, 0.85, 0.95),
    },
    BlockType.GRAVEL: {
        'all': (0.5, 0.48, 0.45),
    },
}

# 方块属性
BLOCK_DATA = {
    BlockType.AIR: {'name': '空气', 'solid': False, 'transparent': True, 'hardness': 0},
    BlockType.GRASS: {'name': '草方块', 'solid': True, 'transparent': False, 'hardness': 0.6},
    BlockType.DIRT: {'name': '泥土', 'solid': True, 'transparent': False, 'hardness': 0.5},
    BlockType.STONE: {'name': '石头', 'solid': True, 'transparent': False, 'hardness': 1.5},
    BlockType.COBBLESTONE: {'name': '圆石', 'solid': True, 'transparent': False, 'hardness': 2.0},
    BlockType.WOOD: {'name': '原木', 'solid': True, 'transparent': False, 'hardness': 2.0},
    BlockType.LEAVES: {'name': '树叶', 'solid': True, 'transparent': True, 'hardness': 0.2},
    BlockType.SAND: {'name': '沙子', 'solid': True, 'transparent': False, 'hardness': 0.5},
    BlockType.WATER: {'name': '水', 'solid': False, 'transparent': True, 'hardness': -1},
    BlockType.COAL_ORE: {'name': '煤矿石', 'solid': True, 'transparent': False, 'hardness': 3.0},
    BlockType.IRON_ORE: {'name': '铁矿石', 'solid': True, 'transparent': False, 'hardness': 3.0},
    BlockType.GOLD_ORE: {'name': '金矿石', 'solid': True, 'transparent': False, 'hardness': 3.0},
    BlockType.DIAMOND_ORE: {'name': '钻石矿石', 'solid': True, 'transparent': False, 'hardness': 3.0},
    BlockType.BEDROCK: {'name': '基岩', 'solid': True, 'transparent': False, 'hardness': -1},
    BlockType.PLANKS: {'name': '木板', 'solid': True, 'transparent': False, 'hardness': 2.0},
    BlockType.GLASS: {'name': '玻璃', 'solid': True, 'transparent': True, 'hardness': 0.3},
    BlockType.BRICK: {'name': '砖块', 'solid': True, 'transparent': False, 'hardness': 2.0},
    BlockType.SNOW: {'name': '雪块', 'solid': True, 'transparent': False, 'hardness': 0.2},
    BlockType.ICE: {'name': '冰块', 'solid': True, 'transparent': True, 'hardness': 0.5},
    BlockType.GRAVEL: {'name': '砂砾', 'solid': True, 'transparent': False, 'hardness': 0.6},
}

# 方块掉落
BLOCK_DROPS = {
    BlockType.GRASS: BlockType.DIRT,
    BlockType.DIRT: BlockType.DIRT,
    BlockType.STONE: BlockType.COBBLESTONE,
    BlockType.COBBLESTONE: BlockType.COBBLESTONE,
    BlockType.WOOD: BlockType.WOOD,
    BlockType.LEAVES: BlockType.LEAVES,
    BlockType.SAND: BlockType.SAND,
    BlockType.COAL_ORE: BlockType.COAL_ORE,
    BlockType.IRON_ORE: BlockType.IRON_ORE,
    BlockType.GOLD_ORE: BlockType.GOLD_ORE,
    BlockType.DIAMOND_ORE: BlockType.DIAMOND_ORE,
    BlockType.PLANKS: BlockType.PLANKS,
    BlockType.GLASS: BlockType.AIR,  # 玻璃破碎不掉落
    BlockType.BRICK: BlockType.BRICK,
    BlockType.SNOW: BlockType.SNOW,
    BlockType.ICE: BlockType.ICE,
    BlockType.GRAVEL: BlockType.GRAVEL,
}
