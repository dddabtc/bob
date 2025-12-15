"""
敌人数据
"""

# 敌人类型
ENEMY_TYPES = {
    # ===== 普通怪物 =====
    "低级邪灵": {
        "name": "低级邪灵",
        "type": "normal",
        "hp": 50,
        "attack": 8,
        "defense": 2,
        "speed": 3,
        "size": 30,
        "color": (100, 150, 200),
        "exp": 10,
        "behavior": "chase",  # 追逐玩家
        "attack_range": 40,
        "attack_cooldown": 1.5,
        "drops": [
            {"item": "灵性碎片", "chance": 0.5, "count": (1, 2)},
            {"item": "邪灵精华", "chance": 0.2, "count": (1, 1)},
        ]
    },

    "活尸": {
        "name": "活尸",
        "type": "normal",
        "hp": 80,
        "attack": 15,
        "defense": 5,
        "speed": 1.5,
        "size": 35,
        "color": (80, 100, 80),
        "exp": 15,
        "behavior": "chase",
        "attack_range": 50,
        "attack_cooldown": 2.0,
        "drops": [
            {"item": "腐烂之心", "chance": 0.4, "count": (1, 1)},
            {"item": "尸体残骸", "chance": 0.6, "count": (1, 3)},
        ]
    },

    "梦魇": {
        "name": "梦魇",
        "type": "normal",
        "hp": 40,
        "attack": 12,
        "defense": 1,
        "speed": 4,
        "size": 28,
        "color": (150, 100, 180),
        "exp": 12,
        "behavior": "ranged",  # 远程攻击
        "attack_range": 200,
        "attack_cooldown": 2.5,
        "projectile_speed": 6,
        "drops": [
            {"item": "梦魇精华", "chance": 0.4, "count": (1, 2)},
            {"item": "深蓝梦魇花", "chance": 0.3, "count": (1, 1)},
        ]
    },

    "疯狂信徒": {
        "name": "疯狂信徒",
        "type": "normal",
        "hp": 60,
        "attack": 10,
        "defense": 3,
        "speed": 3.5,
        "size": 32,
        "color": (180, 80, 80),
        "exp": 14,
        "behavior": "chase",
        "attack_range": 45,
        "attack_cooldown": 1.2,
        "drops": [
            {"item": "邪教徽章", "chance": 0.3, "count": (1, 1)},
            {"item": "血色布料", "chance": 0.5, "count": (1, 2)},
        ]
    },

    # ===== 精英怪物 =====
    "堕落非凡者": {
        "name": "堕落非凡者",
        "type": "elite",
        "hp": 200,
        "attack": 25,
        "defense": 10,
        "speed": 3,
        "size": 45,
        "color": (200, 50, 50),
        "exp": 50,
        "behavior": "smart",  # 智能行为
        "attack_range": 60,
        "attack_cooldown": 1.0,
        "skills": ["冲锋", "重击"],
        "drops": [
            {"item": "非凡特性", "chance": 0.8, "count": (1, 1)},
            {"item": "灵性水晶", "chance": 0.5, "count": (1, 2)},
            {"item": "序列材料", "chance": 0.3, "count": (1, 1)},
        ]
    },

    "暗影猎手": {
        "name": "暗影猎手",
        "type": "elite",
        "hp": 150,
        "attack": 30,
        "defense": 5,
        "speed": 5,
        "size": 40,
        "color": (50, 50, 80),
        "exp": 45,
        "behavior": "assassin",  # 刺客行为
        "attack_range": 50,
        "attack_cooldown": 0.8,
        "can_stealth": True,
        "drops": [
            {"item": "暗影精华", "chance": 0.6, "count": (1, 2)},
            {"item": "隐匿之心", "chance": 0.3, "count": (1, 1)},
        ]
    },

    "邪灵领主": {
        "name": "邪灵领主",
        "type": "elite",
        "hp": 180,
        "attack": 20,
        "defense": 8,
        "speed": 2.5,
        "size": 50,
        "color": (80, 120, 200),
        "exp": 55,
        "behavior": "summoner",  # 召唤行为
        "attack_range": 150,
        "attack_cooldown": 2.0,
        "summon_cooldown": 8.0,
        "summon_type": "低级邪灵",
        "drops": [
            {"item": "邪灵之心", "chance": 0.7, "count": (1, 1)},
            {"item": "灵性水晶", "chance": 0.8, "count": (2, 4)},
        ]
    },

    # ===== BOSS =====
    "极光会主教": {
        "name": "极光会主教",
        "type": "boss",
        "hp": 500,
        "attack": 35,
        "defense": 15,
        "speed": 3,
        "size": 60,
        "color": (255, 100, 100),
        "exp": 200,
        "behavior": "boss",
        "attack_range": 80,
        "attack_cooldown": 1.5,
        "skills": ["火焰风暴", "召唤信徒", "狂暴", "十字火焰", "神圣审判"],
        "phases": 3,
        "phase_skills": {
            1: ["火焰风暴", "召唤信徒"],
            2: ["火焰风暴", "十字火焰", "召唤信徒"],
            3: ["狂暴", "十字火焰", "神圣审判"],
        },
        "drops": [
            {"item": "极光会圣物", "chance": 1.0, "count": (1, 1)},
            {"item": "序列魔药配方", "chance": 0.5, "count": (1, 1)},
            {"item": "非凡特性", "chance": 1.0, "count": (2, 3)},
        ]
    },

    "愚者之影": {
        "name": "愚者之影",
        "type": "boss",
        "hp": 800,
        "attack": 50,
        "defense": 20,
        "speed": 4,
        "size": 55,
        "color": (100, 100, 150),
        "exp": 300,
        "behavior": "boss",
        "attack_range": 100,
        "attack_cooldown": 1.2,
        "skills": ["命运逆转", "欺诈迷雾", "纸牌风暴", "时间回溯", "分身术"],
        "phases": 3,
        "phase_skills": {
            1: ["欺诈迷雾", "纸牌风暴"],
            2: ["命运逆转", "纸牌风暴", "分身术"],
            3: ["时间回溯", "纸牌风暴", "分身术"],
        },
        "evasion": 0.3,  # 30%闪避率
        "drops": [
            {"item": "愚者权杖", "chance": 1.0, "count": (1, 1)},
            {"item": "命运之线", "chance": 0.6, "count": (1, 2)},
            {"item": "非凡特性", "chance": 1.0, "count": (3, 4)},
        ]
    },

    "永暗巨兽": {
        "name": "永暗巨兽",
        "type": "boss",
        "hp": 1200,
        "attack": 40,
        "defense": 30,
        "speed": 2,
        "size": 80,
        "color": (30, 30, 50),
        "exp": 350,
        "behavior": "boss",
        "attack_range": 120,
        "attack_cooldown": 2.0,
        "skills": ["黑暗吞噬", "亡灵召唤", "死亡凝视", "不死之躯", "黑暗领域"],
        "phases": 4,
        "phase_skills": {
            1: ["黑暗吞噬", "亡灵召唤"],
            2: ["黑暗吞噬", "死亡凝视", "亡灵召唤"],
            3: ["黑暗领域", "死亡凝视", "亡灵召唤"],
            4: ["不死之躯", "黑暗领域", "死亡凝视"],
        },
        "can_revive": True,  # 可以复活一次
        "drops": [
            {"item": "永暗之心", "chance": 1.0, "count": (1, 1)},
            {"item": "死亡精华", "chance": 0.8, "count": (2, 3)},
            {"item": "非凡特性", "chance": 1.0, "count": (3, 5)},
        ]
    },

    "原初魔女": {
        "name": "原初魔女",
        "type": "boss",
        "hp": 600,
        "attack": 60,
        "defense": 15,
        "speed": 3.5,
        "size": 50,
        "color": (180, 50, 120),
        "exp": 280,
        "behavior": "boss",
        "attack_range": 150,
        "attack_cooldown": 1.0,
        "skills": ["诅咒之触", "魅惑", "瘟疫爆发", "灵魂收割", "灾祸降临"],
        "phases": 3,
        "phase_skills": {
            1: ["诅咒之触", "魅惑"],
            2: ["瘟疫爆发", "诅咒之触", "魅惑"],
            3: ["灵魂收割", "灾祸降临", "瘟疫爆发"],
        },
        "dot_damage": 5,  # 持续伤害
        "drops": [
            {"item": "魔女之冠", "chance": 1.0, "count": (1, 1)},
            {"item": "诅咒宝石", "chance": 0.7, "count": (1, 2)},
            {"item": "非凡特性", "chance": 1.0, "count": (2, 4)},
        ]
    },

    "知识妖鬼": {
        "name": "知识妖鬼",
        "type": "boss",
        "hp": 700,
        "attack": 55,
        "defense": 18,
        "speed": 3,
        "size": 55,
        "color": (200, 180, 100),
        "exp": 320,
        "behavior": "boss",
        "attack_range": 180,
        "attack_cooldown": 1.3,
        "skills": ["疯狂低语", "知识压制", "卷轴轰炸", "真实之眼", "禁忌知识"],
        "phases": 3,
        "phase_skills": {
            1: ["疯狂低语", "卷轴轰炸"],
            2: ["知识压制", "卷轴轰炸", "疯狂低语"],
            3: ["真实之眼", "禁忌知识", "知识压制"],
        },
        "can_silence": True,  # 可以封印玩家技能
        "drops": [
            {"item": "知识结晶", "chance": 1.0, "count": (1, 1)},
            {"item": "禁忌卷轴", "chance": 0.6, "count": (1, 2)},
            {"item": "非凡特性", "chance": 1.0, "count": (3, 4)},
        ]
    },
}

# 波次配置
WAVE_CONFIG = {
    1: {
        "enemies": [("低级邪灵", 3)],
        "spawn_delay": 1.0,
    },
    2: {
        "enemies": [("低级邪灵", 2), ("活尸", 2)],
        "spawn_delay": 0.8,
    },
    3: {
        "enemies": [("低级邪灵", 3), ("梦魇", 2)],
        "spawn_delay": 0.8,
    },
    4: {
        "enemies": [("活尸", 3), ("梦魇", 2), ("疯狂信徒", 2)],
        "spawn_delay": 0.6,
    },
    5: {
        "enemies": [("堕落非凡者", 1), ("低级邪灵", 4)],
        "spawn_delay": 0.5,
        "is_elite_wave": True,
    },
    6: {
        "enemies": [("梦魇", 4), ("暗影猎手", 1)],
        "spawn_delay": 0.5,
    },
    7: {
        "enemies": [("疯狂信徒", 5), ("活尸", 3)],
        "spawn_delay": 0.4,
    },
    8: {
        "enemies": [("邪灵领主", 1), ("低级邪灵", 5)],
        "spawn_delay": 0.5,
        "is_elite_wave": True,
    },
    9: {
        "enemies": [("堕落非凡者", 2), ("暗影猎手", 2)],
        "spawn_delay": 0.4,
    },
    10: {
        "enemies": [("极光会主教", 1)],
        "spawn_delay": 0,
        "is_boss_wave": True,
        "boss_name": "极光会主教",
    },
}

# Boss波次配置（每10波循环一个Boss）
BOSS_ROTATION = [
    "极光会主教",   # 波次10
    "愚者之影",     # 波次20
    "原初魔女",     # 波次30
    "知识妖鬼",     # 波次40
    "永暗巨兽",     # 波次50（最难）
]


def get_enemy_data(enemy_type):
    """获取敌人数据"""
    return ENEMY_TYPES.get(enemy_type, ENEMY_TYPES["低级邪灵"]).copy()


def get_wave_enemies(wave_number):
    """获取波次敌人配置"""
    # 循环波次，难度递增
    base_wave = ((wave_number - 1) % 10) + 1
    multiplier = (wave_number - 1) // 10 + 1

    wave = WAVE_CONFIG.get(base_wave, WAVE_CONFIG[1]).copy()

    # Boss波次处理：根据波次选择不同Boss
    if base_wave == 10:
        boss_index = (multiplier - 1) % len(BOSS_ROTATION)
        boss_name = BOSS_ROTATION[boss_index]
        wave["enemies"] = [(boss_name, 1)]
        wave["boss_name"] = boss_name
        wave["is_boss_wave"] = True
        return wave

    # 增加敌人数量
    if multiplier > 1:
        new_enemies = []
        for enemy_type, count in wave["enemies"]:
            new_count = int(count * (1 + 0.2 * (multiplier - 1)))
            new_enemies.append((enemy_type, new_count))
        wave["enemies"] = new_enemies

    return wave


def get_boss_data(boss_name):
    """获取Boss数据"""
    if boss_name in ENEMY_TYPES and ENEMY_TYPES[boss_name].get("type") == "boss":
        return ENEMY_TYPES[boss_name].copy()
    return None


def get_all_bosses():
    """获取所有Boss列表"""
    return [name for name, data in ENEMY_TYPES.items() if data.get("type") == "boss"]
