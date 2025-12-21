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
            {"item": "紫月花", "chance": 0.3, "count": (1, 1)},
            {"item": "梦境尘埃", "chance": 0.2, "count": (1, 1)},
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
            {"item": "夜香花", "chance": 0.3, "count": (1, 1)},
            {"item": "黑曜石粉", "chance": 0.2, "count": (1, 1)},
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
            {"item": "梦境尘埃", "chance": 0.5, "count": (1, 2)},
            {"item": "九叶莲", "chance": 0.25, "count": (1, 1)},
            {"item": "星辰草", "chance": 0.2, "count": (1, 1)},
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
            {"item": "灵银粉", "chance": 0.3, "count": (1, 1)},
            {"item": "冷杉精华", "chance": 0.3, "count": (1, 1)},
            {"item": "蒸馏水", "chance": 0.4, "count": (1, 2)},
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
            {"item": "命运之弦", "chance": 0.2, "count": (1, 1)},
            {"item": "深红月晶", "chance": 0.15, "count": (1, 1)},
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
            {"item": "命运之弦", "chance": 0.15, "count": (1, 1)},
            {"item": "隐者之眼", "chance": 0.2, "count": (1, 1)},
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
            {"item": "命运之弦", "chance": 0.25, "count": (1, 1)},
            {"item": "死者耳语", "chance": 0.3, "count": (1, 1)},
        ]
    },

    # ===== BOSS =====
    "极光会主教": {
        "name": "极光会主教",
        "type": "boss",
        "hp": 150,           # 大幅降低HP，序列9玩家可击败
        "attack": 10,        # 大幅降低攻击力
        "defense": 3,        # 大幅降低防御
        "speed": 1.5,        # 降低移动速度
        "size": 60,
        "color": (255, 100, 100),
        "exp": 200,
        "behavior": "boss",
        "attack_range": 60,  # 缩小攻击范围
        "attack_cooldown": 2.5,  # 攻击间隔更长
        "skills": ["火焰风暴"],  # 只保留火焰风暴
        "phases": 1,         # 单阶段，简化战斗
        "phase_skills": {
            1: ["火焰风暴"],
        },
        "drops": [
            # 晋升材料（序列8需要）
            {"item": "梦境尘埃", "chance": 1.0, "count": (2, 4)},
            {"item": "九叶莲", "chance": 1.0, "count": (1, 2)},
            {"item": "紫月花", "chance": 1.0, "count": (2, 3)},
            {"item": "灵银粉", "chance": 0.8, "count": (1, 2)},
            # 序列7材料
            {"item": "命运之弦", "chance": 1.0, "count": (1, 2)},
            {"item": "深红月晶", "chance": 1.0, "count": (1, 2)},
            {"item": "太阳圣水", "chance": 0.8, "count": (1, 2)},
            # Boss专属材料
            {"item": "极光碎片", "chance": 1.0, "count": (1, 2)},
        ]
    },

    "愚者之影": {
        "name": "愚者之影",
        "type": "boss",
        "hp": 250,           # 大幅降低 (原800)
        "attack": 15,        # 大幅降低 (原50)
        "defense": 5,        # 大幅降低 (原20)
        "speed": 2.5,        # 降低速度 (原4)
        "size": 55,
        "color": (100, 100, 150),
        "exp": 300,
        "behavior": "boss",
        "attack_range": 70,  # 缩小范围 (原100)
        "attack_cooldown": 2.0,  # 攻击更慢 (原1.2)
        "skills": ["欺诈迷雾", "纸牌风暴"],  # 减少技能
        "phases": 2,         # 减少阶段 (原3)
        "phase_skills": {
            1: ["欺诈迷雾"],
            2: ["纸牌风暴", "欺诈迷雾"],
        },
        "evasion": 0.15,     # 降低闪避 (原0.3)
        "drops": [
            {"item": "千面之种", "chance": 1.0, "count": (1, 2)},
            {"item": "虚空精华", "chance": 1.0, "count": (1, 2)},
            {"item": "命运之弦", "chance": 1.0, "count": (2, 3)},
            {"item": "极光碎片", "chance": 1.0, "count": (1, 2)},
        ]
    },

    "永暗巨兽": {
        "name": "永暗巨兽",
        "type": "boss",
        "hp": 400,           # 大幅降低 (原1200)
        "attack": 18,        # 大幅降低 (原40)
        "defense": 8,        # 大幅降低 (原30)
        "speed": 1.5,        # 降低速度 (原2)
        "size": 80,
        "color": (30, 30, 50),
        "exp": 350,
        "behavior": "boss",
        "attack_range": 80,  # 缩小范围 (原120)
        "attack_cooldown": 2.5,  # 攻击更慢 (原2.0)
        "skills": ["黑暗吞噬", "死亡凝视"],  # 减少技能
        "phases": 2,         # 减少阶段 (原4)
        "phase_skills": {
            1: ["黑暗吞噬"],
            2: ["黑暗吞噬", "死亡凝视"],
        },
        "can_revive": False,  # 取消复活 (原True)
        "drops": [
            {"item": "深渊之泪", "chance": 1.0, "count": (1, 2)},
            {"item": "灵魂水晶", "chance": 1.0, "count": (1, 2)},
            {"item": "虚空精华", "chance": 1.0, "count": (1, 2)},
            {"item": "死者耳语", "chance": 1.0, "count": (2, 3)},
        ]
    },

    "原初魔女": {
        "name": "原初魔女",
        "type": "boss",
        "hp": 200,           # 大幅降低 (原600)
        "attack": 18,        # 大幅降低 (原60)
        "defense": 4,        # 大幅降低 (原15)
        "speed": 2.5,        # 降低速度 (原3.5)
        "size": 50,
        "color": (180, 50, 120),
        "exp": 280,
        "behavior": "boss",
        "attack_range": 90,  # 缩小范围 (原150)
        "attack_cooldown": 2.0,  # 攻击更慢 (原1.0)
        "skills": ["诅咒之触", "瘟疫爆发"],  # 减少技能
        "phases": 2,         # 减少阶段 (原3)
        "phase_skills": {
            1: ["诅咒之触"],
            2: ["瘟疫爆发", "诅咒之触"],
        },
        "dot_damage": 2,     # 降低持续伤害 (原5)
        "drops": [
            {"item": "灵魂水晶", "chance": 1.0, "count": (1, 2)},
            {"item": "腐化之心", "chance": 1.0, "count": (2, 3)},
            {"item": "隐者之眼", "chance": 1.0, "count": (1, 2)},
            {"item": "深红月晶", "chance": 1.0, "count": (1, 2)},
        ]
    },

    "知识妖鬼": {
        "name": "知识妖鬼",
        "type": "boss",
        "hp": 280,           # 大幅降低 (原700)
        "attack": 16,        # 大幅降低 (原55)
        "defense": 5,        # 大幅降低 (原18)
        "speed": 2,          # 降低速度 (原3)
        "size": 55,
        "color": (200, 180, 100),
        "exp": 320,
        "behavior": "boss",
        "attack_range": 100, # 缩小范围 (原180)
        "attack_cooldown": 2.2,  # 攻击更慢 (原1.3)
        "skills": ["疯狂低语", "卷轴轰炸"],  # 减少技能
        "phases": 2,         # 减少阶段 (原3)
        "phase_skills": {
            1: ["疯狂低语"],
            2: ["卷轴轰炸", "疯狂低语"],
        },
        "can_silence": False,  # 取消封印 (原True)
        "drops": [
            {"item": "知识之书", "chance": 1.0, "count": (1, 2)},
            {"item": "深红月晶", "chance": 1.0, "count": (2, 3)},
            {"item": "灵银粉", "chance": 1.0, "count": (2, 3)},
            {"item": "梦境尘埃", "chance": 1.0, "count": (2, 3)},
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
        wave["stat_multiplier"] = 1.0 + 0.3 * (multiplier - 1)  # Boss也增强属性
        return wave

    # 增加敌人数量和属性
    if multiplier > 1:
        new_enemies = []
        for enemy_type, count in wave["enemies"]:
            new_count = int(count * (1 + 0.2 * (multiplier - 1)))
            new_enemies.append((enemy_type, new_count))
        wave["enemies"] = new_enemies
        # 属性增强倍率：每轮增加30%
        wave["stat_multiplier"] = 1.0 + 0.3 * (multiplier - 1)
    else:
        wave["stat_multiplier"] = 1.0

    return wave


def get_boss_data(boss_name):
    """获取Boss数据"""
    if boss_name in ENEMY_TYPES and ENEMY_TYPES[boss_name].get("type") == "boss":
        return ENEMY_TYPES[boss_name].copy()
    return None


def get_all_bosses():
    """获取所有Boss列表"""
    return [name for name, data in ENEMY_TYPES.items() if data.get("type") == "boss"]
