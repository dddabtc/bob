"""
Black Ops - 敌人数据定义
"""

ENEMY_TYPES = {
    # 普通士兵
    "soldier": {
        "name": "苏联士兵",
        "hp": 50,
        "damage": 15,
        "fire_rate": 2.0,
        "accuracy": 0.6,
        "speed": 1.5,
        "view_distance": 8,
        "view_angle": 90,
        "attack_range": 10,
        "color": (100, 120, 80),  # 军绿色
        "points": 100,
        "drops": [
            {"type": "ammo", "ammo_type": "assault_rifle", "chance": 0.5},
            {"type": "health", "amount": 15, "chance": 0.2},
        ],
    },

    # 精英士兵
    "elite": {
        "name": "精英士兵",
        "hp": 80,
        "damage": 25,
        "fire_rate": 3.0,
        "accuracy": 0.75,
        "speed": 1.8,
        "view_distance": 10,
        "view_angle": 100,
        "attack_range": 12,
        "color": (60, 60, 80),  # 深蓝色
        "points": 200,
        "drops": [
            {"type": "ammo", "ammo_type": "assault_rifle", "chance": 0.7},
            {"type": "health", "amount": 25, "chance": 0.3},
            {"type": "armor", "amount": 15, "chance": 0.2},
        ],
    },

    # 狙击手
    "sniper": {
        "name": "狙击手",
        "hp": 40,
        "damage": 60,
        "fire_rate": 0.8,
        "accuracy": 0.9,
        "speed": 1.0,
        "view_distance": 15,
        "view_angle": 60,
        "attack_range": 20,
        "color": (80, 80, 60),  # 迷彩色
        "points": 250,
        "drops": [
            {"type": "ammo", "ammo_type": "sniper", "chance": 0.8},
            {"type": "health", "amount": 20, "chance": 0.2},
        ],
    },

    # 霰弹兵
    "shotgunner": {
        "name": "霰弹兵",
        "hp": 70,
        "damage": 35,
        "fire_rate": 1.0,
        "accuracy": 0.5,
        "speed": 1.6,
        "view_distance": 6,
        "view_angle": 100,
        "attack_range": 5,
        "color": (100, 80, 60),  # 棕色
        "points": 180,
        "drops": [
            {"type": "ammo", "ammo_type": "shotgun", "chance": 0.7},
            {"type": "health", "amount": 20, "chance": 0.25},
        ],
    },

    # 冲锋手
    "rusher": {
        "name": "冲锋手",
        "hp": 45,
        "damage": 12,
        "fire_rate": 8.0,
        "accuracy": 0.4,
        "speed": 2.5,
        "view_distance": 7,
        "view_angle": 110,
        "attack_range": 6,
        "color": (80, 60, 60),  # 暗红色
        "points": 150,
        "drops": [
            {"type": "ammo", "ammo_type": "smg", "chance": 0.6},
            {"type": "health", "amount": 15, "chance": 0.3},
        ],
    },

    # 重装兵
    "heavy": {
        "name": "重装兵",
        "hp": 150,
        "damage": 20,
        "fire_rate": 6.0,
        "accuracy": 0.5,
        "speed": 0.8,
        "view_distance": 8,
        "view_angle": 80,
        "attack_range": 10,
        "color": (60, 80, 100),  # 钢蓝色
        "points": 350,
        "drops": [
            {"type": "ammo", "ammo_type": "assault_rifle", "chance": 0.8},
            {"type": "health", "amount": 40, "chance": 0.4},
            {"type": "armor", "amount": 30, "chance": 0.3},
        ],
    },

    # 指挥官 (小Boss)
    "commander": {
        "name": "指挥官",
        "hp": 200,
        "damage": 30,
        "fire_rate": 3.5,
        "accuracy": 0.8,
        "speed": 1.2,
        "view_distance": 12,
        "view_angle": 120,
        "attack_range": 15,
        "color": (150, 50, 50),  # 红色
        "points": 500,
        "is_boss": True,
        "drops": [
            {"type": "ammo", "ammo_type": "assault_rifle", "chance": 1.0},
            {"type": "health", "amount": 50, "chance": 0.5},
            {"type": "armor", "amount": 50, "chance": 0.4},
        ],
    },

    # 终极Boss
    "general": {
        "name": "将军",
        "hp": 500,
        "damage": 40,
        "fire_rate": 4.0,
        "accuracy": 0.85,
        "speed": 1.0,
        "view_distance": 15,
        "view_angle": 150,
        "attack_range": 18,
        "color": (200, 180, 50),  # 金色
        "points": 2000,
        "is_boss": True,
        "drops": [
            {"type": "health", "amount": 100, "chance": 1.0},
            {"type": "armor", "amount": 100, "chance": 1.0},
        ],
    },
}

# 敌人行为参数
ENEMY_BEHAVIOR = {
    "patrol_wait_time": 2.0,      # 巡逻点等待时间
    "alert_duration": 5.0,        # 警戒持续时间
    "search_duration": 8.0,       # 搜索持续时间
    "reaction_time": 0.3,         # 反应时间
    "accuracy_penalty_moving": 0.3,  # 移动时精度惩罚
}
