"""
Black Ops - 关卡数据定义
"""

MISSIONS = {
    "mission1": {
        "name": "第一章：黎明突袭",
        "subtitle": "Operation: Dawn Strike",
        "map": "mission1.txt",
        "briefing": [
            "Mason，这是你的首次任务。",
            "目标：潜入古巴军事基地，获取机密情报。",
            "情报显示基地内有重要的导弹计划文件。",
            "消灭指挥官，带回文件，然后撤离。",
            "祝你好运，士兵。"
        ],
        "objectives": [
            {
                "id": "infiltrate",
                "type": "reach",
                "target": (25, 15),
                "description": "潜入基地核心区域",
                "required": True,
            },
            {
                "id": "intel",
                "type": "collect",
                "item": "intel_file",
                "description": "获取机密文件",
                "required": True,
            },
            {
                "id": "commander",
                "type": "kill",
                "target": "commander",
                "description": "消灭指挥官",
                "required": True,
            },
            {
                "id": "extract",
                "type": "reach",
                "target": (3, 3),
                "description": "返回撤离点",
                "required": True,
            },
        ],
        "player_start": (2, 2),
        "player_angle": 0,
        "enemies": [
            {"type": "soldier", "x": 8, "y": 5},
            {"type": "soldier", "x": 12, "y": 8, "patrol": [(12, 8), (18, 8)]},
            {"type": "soldier", "x": 15, "y": 12},
            {"type": "soldier", "x": 20, "y": 6, "patrol": [(20, 6), (20, 12)]},
            {"type": "elite", "x": 22, "y": 15},
            {"type": "sniper", "x": 28, "y": 3},
            {"type": "commander", "x": 26, "y": 14, "is_target": True},
        ],
        "items": [
            {"type": "intel", "id": "intel_file", "x": 27, "y": 15},
            {"type": "ammo", "ammo_type": "assault_rifle", "x": 10, "y": 10},
            {"type": "health", "amount": 30, "x": 15, "y": 5},
            {"type": "armor", "amount": 25, "x": 18, "y": 14},
        ],
        "dialogue": {
            "start": ["控制中心：Mason，你已进入敌方领土。保持无线电静默。"],
            "infiltrate": ["控制中心：干得好。情报室就在附近。"],
            "intel": ["Mason：找到文件了。", "控制中心：很好，现在去解决指挥官。"],
            "commander": ["控制中心：目标已消灭。返回撤离点。"],
            "extract": ["控制中心：直升机已就位。任务完成！"],
        },
        "loadout": {
            "primary": "m16",
            "secondary": "m1911",
            "grenades": 2,
        },
        "time_limit": None,  # 无时间限制
        "next_mission": "mission2",
    },

    "mission2": {
        "name": "第二章：丛林猎杀",
        "subtitle": "Operation: Jungle Hunt",
        "map": "mission2.txt",
        "briefing": [
            "上次任务的情报揭示了一个秘密研究设施。",
            "位于越南丛林深处。",
            "你的任务是摧毁那里的化学武器研究。",
            "预计会遭遇重兵防守。",
            "小心行动。"
        ],
        "objectives": [
            {
                "id": "locate",
                "type": "reach",
                "target": (30, 20),
                "description": "找到研究设施",
                "required": True,
            },
            {
                "id": "destroy",
                "type": "interact",
                "target": "lab_console",
                "description": "摧毁研究数据",
                "required": True,
            },
            {
                "id": "eliminate",
                "type": "kill_all",
                "description": "消灭所有敌人",
                "required": False,
            },
            {
                "id": "extract",
                "type": "reach",
                "target": (5, 25),
                "description": "前往撤离点",
                "required": True,
            },
        ],
        "player_start": (3, 3),
        "player_angle": 1.57,
        "enemies": [
            {"type": "soldier", "x": 10, "y": 8},
            {"type": "soldier", "x": 15, "y": 10, "patrol": [(15, 10), (20, 10), (20, 15)]},
            {"type": "rusher", "x": 18, "y": 12},
            {"type": "rusher", "x": 22, "y": 8},
            {"type": "shotgunner", "x": 25, "y": 18},
            {"type": "elite", "x": 28, "y": 20},
            {"type": "sniper", "x": 32, "y": 5},
            {"type": "heavy", "x": 30, "y": 22},
        ],
        "items": [
            {"type": "weapon", "weapon_id": "ak47", "x": 12, "y": 12},
            {"type": "ammo", "ammo_type": "assault_rifle", "x": 20, "y": 15},
            {"type": "ammo", "ammo_type": "smg", "x": 25, "y": 10},
            {"type": "health", "amount": 50, "x": 28, "y": 18},
            {"type": "armor", "amount": 30, "x": 15, "y": 20},
        ],
        "dialogue": {
            "start": ["控制中心：丛林里小心，敌人可能隐藏在任何地方。"],
            "locate": ["Mason：找到设施了，这地方规模不小。"],
            "destroy": ["Mason：数据已清除。", "控制中心：现在离开那里！"],
            "extract": ["控制中心：做得好，Mason。欢迎回来。"],
        },
        "loadout": {
            "primary": "commando",
            "secondary": "python",
            "grenades": 3,
        },
        "time_limit": None,
        "next_mission": "mission3",
    },

    "mission3": {
        "name": "第三章：冰封地狱",
        "subtitle": "Operation: Frozen Hell",
        "map": "mission3.txt",
        "briefing": [
            "情报指向西伯利亚的一个古拉格集中营。",
            "据信那里关押着一名叛逃的苏联科学家。",
            "营救他，他掌握着关键情报。",
            "注意：这是敌人的大本营，做好苦战准备。"
        ],
        "objectives": [
            {
                "id": "enter",
                "type": "reach",
                "target": (20, 10),
                "description": "进入集中营",
                "required": True,
            },
            {
                "id": "rescue",
                "type": "interact",
                "target": "prisoner",
                "description": "营救科学家",
                "required": True,
            },
            {
                "id": "boss",
                "type": "kill",
                "target": "general",
                "description": "击败苏联将军",
                "required": True,
            },
            {
                "id": "escape",
                "type": "reach",
                "target": (2, 28),
                "description": "带领科学家逃离",
                "required": True,
            },
        ],
        "player_start": (2, 2),
        "player_angle": 0.78,
        "enemies": [
            {"type": "soldier", "x": 8, "y": 5},
            {"type": "soldier", "x": 12, "y": 8},
            {"type": "soldier", "x": 15, "y": 5, "patrol": [(15, 5), (20, 5)]},
            {"type": "elite", "x": 18, "y": 10},
            {"type": "elite", "x": 22, "y": 12},
            {"type": "sniper", "x": 25, "y": 3},
            {"type": "sniper", "x": 28, "y": 8},
            {"type": "heavy", "x": 20, "y": 15},
            {"type": "heavy", "x": 25, "y": 18},
            {"type": "commander", "x": 28, "y": 20},
            {"type": "general", "x": 30, "y": 25, "is_target": True},
        ],
        "items": [
            {"type": "weapon", "weapon_id": "l96", "x": 15, "y": 12},
            {"type": "ammo", "ammo_type": "sniper", "x": 18, "y": 8},
            {"type": "ammo", "ammo_type": "assault_rifle", "x": 22, "y": 15},
            {"type": "health", "amount": 40, "x": 10, "y": 10},
            {"type": "health", "amount": 60, "x": 25, "y": 22},
            {"type": "armor", "amount": 50, "x": 20, "y": 20},
        ],
        "dialogue": {
            "start": ["控制中心：西伯利亚，全年冰封。保持体温，保持警惕。"],
            "enter": ["Mason：我进去了。这地方戒备森严。"],
            "rescue": ["科学家：感谢上帝！快带我离开这里！"],
            "boss": ["将军：你以为能带走他？做梦！", "Mason：任务完成。"],
            "escape": ["控制中心：科学家已安全。干得漂亮，Mason！"],
        },
        "loadout": {
            "primary": "ak47",
            "secondary": "m1911",
            "grenades": 4,
        },
        "time_limit": None,
        "next_mission": None,  # 最后一关
    },
}

# 任务完成奖励
MISSION_REWARDS = {
    "mission1": {
        "unlock_weapon": "mp5",
        "bonus_points": 1000,
    },
    "mission2": {
        "unlock_weapon": "spas12",
        "bonus_points": 1500,
    },
    "mission3": {
        "unlock_weapon": "dragunov",
        "bonus_points": 2500,
    },
}
