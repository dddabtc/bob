"""
物品数据 - 材料和魔药定义
"""

# 材料品质
QUALITY_COMMON = "common"      # 普通
QUALITY_UNCOMMON = "uncommon"  # 优质
QUALITY_RARE = "rare"          # 稀有
QUALITY_EPIC = "epic"          # 史诗
QUALITY_LEGENDARY = "legendary"  # 传说

# 品质颜色
QUALITY_COLORS = {
    QUALITY_COMMON: (200, 200, 200),     # 灰白
    QUALITY_UNCOMMON: (100, 255, 100),   # 绿色
    QUALITY_RARE: (100, 150, 255),       # 蓝色
    QUALITY_EPIC: (200, 100, 255),       # 紫色
    QUALITY_LEGENDARY: (255, 200, 50),   # 金色
}

# 材料类型
MATERIAL_TYPES = {
    "植物": "plant",
    "矿石": "mineral",
    "动物": "animal",
    "灵性": "spiritual",
    "炼金": "alchemy",
}

# ==================== 基础材料 ====================
MATERIALS = {
    # === 普通材料 (序列9魔药) ===
    "夜香花": {
        "type": "plant",
        "quality": QUALITY_COMMON,
        "desc": "夜间盛开的神秘花朵，散发幽香",
        "drop_rate": 0.3,
        "drop_from": ["低级邪灵", "活尸"],
    },
    "冷杉精华": {
        "type": "plant",
        "quality": QUALITY_COMMON,
        "desc": "从古老冷杉树中提取的精华",
        "drop_rate": 0.3,
        "drop_from": ["低级邪灵", "活尸"],
    },
    "紫月花": {
        "type": "plant",
        "quality": QUALITY_COMMON,
        "desc": "在紫月光芒下生长的稀有花朵",
        "drop_rate": 0.25,
        "drop_from": ["低级邪灵", "梦魇"],
    },
    "黑曜石粉": {
        "type": "mineral",
        "quality": QUALITY_COMMON,
        "desc": "研磨成粉的黑曜石，蕴含微弱灵性",
        "drop_rate": 0.3,
        "drop_from": ["活尸", "低级邪灵"],
    },
    "蒸馏水": {
        "type": "alchemy",
        "quality": QUALITY_COMMON,
        "desc": "经过多次蒸馏的纯净水",
        "drop_rate": 0.4,
        "drop_from": ["低级邪灵", "活尸"],
    },
    "星辰草": {
        "type": "plant",
        "quality": QUALITY_COMMON,
        "desc": "吸收星光生长的草药",
        "drop_rate": 0.25,
        "drop_from": ["梦魇", "低级邪灵"],
    },

    # === 优质材料 (序列8魔药) ===
    "魔鬼蛆": {
        "type": "animal",
        "quality": QUALITY_UNCOMMON,
        "desc": "寄生于腐肉中的特殊蛆虫",
        "drop_rate": 0.2,
        "drop_from": ["活尸", "梦魇"],
    },
    "九叶莲": {
        "type": "plant",
        "quality": QUALITY_UNCOMMON,
        "desc": "拥有九片叶子的神秘莲花",
        "drop_rate": 0.15,
        "drop_from": ["梦魇", "堕落非凡者"],
    },
    "梦境尘埃": {
        "type": "spiritual",
        "quality": QUALITY_UNCOMMON,
        "desc": "从梦境中凝结的灵性粉尘",
        "drop_rate": 0.15,
        "drop_from": ["梦魇"],
    },
    "银月草汁": {
        "type": "plant",
        "quality": QUALITY_UNCOMMON,
        "desc": "银月草榨取的汁液",
        "drop_rate": 0.2,
        "drop_from": ["低级邪灵", "梦魇"],
    },
    "红蛛浆液": {
        "type": "animal",
        "quality": QUALITY_UNCOMMON,
        "desc": "红色蜘蛛的毒液",
        "drop_rate": 0.15,
        "drop_from": ["活尸", "堕落非凡者"],
    },
    "灵银粉": {
        "type": "mineral",
        "quality": QUALITY_UNCOMMON,
        "desc": "灵银研磨成的细粉",
        "drop_rate": 0.15,
        "drop_from": ["堕落非凡者", "梦魇"],
    },

    # === 稀有材料 (序列7魔药) ===
    "深红月晶": {
        "type": "mineral",
        "quality": QUALITY_RARE,
        "desc": "深红之月力量凝聚的晶石",
        "drop_rate": 0.08,
        "drop_from": ["堕落非凡者", "极光会主教"],
    },
    "命运之弦": {
        "type": "spiritual",
        "quality": QUALITY_RARE,
        "desc": "命运的具象化丝线",
        "drop_rate": 0.05,
        "drop_from": ["极光会主教"],
    },
    "太阳圣水": {
        "type": "alchemy",
        "quality": QUALITY_RARE,
        "desc": "经太阳照耀祝福的圣水",
        "drop_rate": 0.08,
        "drop_from": ["堕落非凡者", "极光会主教"],
    },
    "风暴精华": {
        "type": "spiritual",
        "quality": QUALITY_RARE,
        "desc": "从暴风中凝聚的纯粹力量",
        "drop_rate": 0.06,
        "drop_from": ["极光会主教"],
    },
    "隐者之眼": {
        "type": "animal",
        "quality": QUALITY_RARE,
        "desc": "隐者蜘蛛的复眼",
        "drop_rate": 0.06,
        "drop_from": ["堕落非凡者", "极光会主教"],
    },
    "死者耳语": {
        "type": "spiritual",
        "quality": QUALITY_RARE,
        "desc": "死者残留的最后执念",
        "drop_rate": 0.07,
        "drop_from": ["活尸", "堕落非凡者"],
    },

    # === 史诗材料 (Boss掉落) ===
    "腐化之心": {
        "type": "spiritual",
        "quality": QUALITY_EPIC,
        "desc": "堕落非凡者的核心",
        "drop_rate": 0.3,
        "drop_from": ["极光会主教"],
    },
    "极光碎片": {
        "type": "spiritual",
        "quality": QUALITY_EPIC,
        "desc": "极光力量的结晶",
        "drop_rate": 0.25,
        "drop_from": ["极光会主教"],
    },
}

# ==================== 魔药配方 ====================
# 每个途径每个序列的魔药配方
POTION_RECIPES = {
    # === 水手途径 ===
    "水手": {
        9: {
            "name": "水手魔药",
            "materials": {"蒸馏水": 2, "冷杉精华": 1, "黑曜石粉": 1},
            "desc": "服用后成为序列9水手",
        },
        8: {
            "name": "溺水者魔药",
            "materials": {"银月草汁": 2, "魔鬼蛆": 1, "蒸馏水": 2},
            "desc": "服用后晋升为序列8溺水者",
        },
        7: {
            "name": "航海士魔药",
            "materials": {"风暴精华": 1, "深红月晶": 1, "银月草汁": 3},
            "desc": "服用后晋升为序列7航海士",
        },
    },

    # === 暴君途径 ===
    "暴君": {
        9: {
            "name": "猎手魔药",
            "materials": {"星辰草": 2, "黑曜石粉": 2, "蒸馏水": 1},
            "desc": "服用后成为序列9猎手",
        },
        8: {
            "name": "挑衅者魔药",
            "materials": {"红蛛浆液": 2, "灵银粉": 1, "星辰草": 2},
            "desc": "服用后晋升为序列8挑衅者",
        },
        7: {
            "name": "咆哮者魔药",
            "materials": {"风暴精华": 2, "腐化之心": 1, "灵银粉": 2},
            "desc": "服用后晋升为序列7咆哮者",
        },
    },

    # === 愚者途径 ===
    "愚者": {
        9: {
            "name": "占卜师魔药",
            "materials": {"紫月花": 2, "星辰草": 1, "蒸馏水": 1},
            "desc": "服用后成为序列9占卜师",
        },
        8: {
            "name": "小丑魔药",
            "materials": {"梦境尘埃": 2, "九叶莲": 1, "紫月花": 2},
            "desc": "服用后晋升为序列8小丑",
        },
        7: {
            "name": "魔术师魔药",
            "materials": {"命运之弦": 1, "梦境尘埃": 3, "极光碎片": 1},
            "desc": "服用后晋升为序列7魔术师",
        },
    },

    # === 红祭司途径 ===
    "红祭司": {
        9: {
            "name": "药剂师魔药",
            "materials": {"夜香花": 2, "冷杉精华": 1, "蒸馏水": 1},
            "desc": "服用后成为序列9药剂师",
        },
        8: {
            "name": "驯兽师魔药",
            "materials": {"魔鬼蛆": 2, "红蛛浆液": 1, "夜香花": 2},
            "desc": "服用后晋升为序列8驯兽师",
        },
        7: {
            "name": "猎巫人魔药",
            "materials": {"太阳圣水": 2, "隐者之眼": 1, "红蛛浆液": 2},
            "desc": "服用后晋升为序列7猎巫人",
        },
    },

    # === 黑夜途径 ===
    "黑夜": {
        9: {
            "name": "守夜人魔药",
            "materials": {"夜香花": 3, "黑曜石粉": 1, "蒸馏水": 1},
            "desc": "服用后成为序列9守夜人",
        },
        8: {
            "name": "隐修士魔药",
            "materials": {"梦境尘埃": 2, "夜香花": 2, "灵银粉": 1},
            "desc": "服用后晋升为序列8隐修士",
        },
        7: {
            "name": "祈光者魔药",
            "materials": {"深红月晶": 2, "死者耳语": 1, "梦境尘埃": 2},
            "desc": "服用后晋升为序列7祈光者",
        },
    },

    # === 太阳途径 ===
    "太阳": {
        9: {
            "name": "阳光少年魔药",
            "materials": {"星辰草": 3, "蒸馏水": 2},
            "desc": "服用后成为序列9阳光少年",
        },
        8: {
            "name": "阳光祭司魔药",
            "materials": {"九叶莲": 2, "星辰草": 2, "灵银粉": 1},
            "desc": "服用后晋升为序列8阳光祭司",
        },
        7: {
            "name": "阳光圣者魔药",
            "materials": {"太阳圣水": 3, "极光碎片": 1, "九叶莲": 2},
            "desc": "服用后晋升为序列7阳光圣者",
        },
    },

    # === 命运途径 ===
    "命运": {
        9: {
            "name": "墨者魔药",
            "materials": {"紫月花": 2, "黑曜石粉": 1, "蒸馏水": 1},
            "desc": "服用后成为序列9墨者",
        },
        8: {
            "name": "预言家魔药",
            "materials": {"梦境尘埃": 3, "紫月花": 2},
            "desc": "服用后晋升为序列8预言家",
        },
        7: {
            "name": "幸运者魔药",
            "materials": {"命运之弦": 2, "极光碎片": 1, "梦境尘埃": 2},
            "desc": "服用后晋升为序列7幸运者",
        },
    },

    # === 死神途径 ===
    "死神": {
        9: {
            "name": "掘墓人魔药",
            "materials": {"夜香花": 2, "黑曜石粉": 2, "蒸馏水": 1},
            "desc": "服用后成为序列9掘墓人",
        },
        8: {
            "name": "灵巫魔药",
            "materials": {"梦境尘埃": 2, "魔鬼蛆": 2, "夜香花": 1},
            "desc": "服用后晋升为序列8灵巫",
        },
        7: {
            "name": "通灵人魔药",
            "materials": {"死者耳语": 2, "深红月晶": 1, "梦境尘埃": 2},
            "desc": "服用后晋升为序列7通灵人",
        },
    },

    # === 战神途径 ===
    "战神": {
        9: {
            "name": "战士魔药",
            "materials": {"冷杉精华": 2, "黑曜石粉": 2, "蒸馏水": 1},
            "desc": "服用后成为序列9战士",
        },
        8: {
            "name": "格斗家魔药",
            "materials": {"红蛛浆液": 2, "魔鬼蛆": 1, "冷杉精华": 2},
            "desc": "服用后晋升为序列8格斗家",
        },
        7: {
            "name": "武器大师魔药",
            "materials": {"腐化之心": 1, "风暴精华": 1, "红蛛浆液": 3},
            "desc": "服用后晋升为序列7武器大师",
        },
    },

    # === 审判途径 ===
    "审判": {
        9: {
            "name": "律师魔药",
            "materials": {"星辰草": 2, "蒸馏水": 2, "冷杉精华": 1},
            "desc": "服用后成为序列9律师",
        },
        8: {
            "name": "调解人魔药",
            "materials": {"灵银粉": 2, "星辰草": 2, "九叶莲": 1},
            "desc": "服用后晋升为序列8调解人",
        },
        7: {
            "name": "裁决者魔药",
            "materials": {"太阳圣水": 2, "命运之弦": 1, "灵银粉": 2},
            "desc": "服用后晋升为序列7裁决者",
        },
    },

    # === 隐者途径 ===
    "隐者": {
        9: {
            "name": "窃贼魔药",
            "materials": {"夜香花": 2, "黑曜石粉": 1, "蒸馏水": 1},
            "desc": "服用后成为序列9窃贼",
        },
        8: {
            "name": "蝗人魔药",
            "materials": {"魔鬼蛆": 3, "夜香花": 2},
            "desc": "服用后晋升为序列8蝗人",
        },
        7: {
            "name": "铁面人魔药",
            "materials": {"隐者之眼": 2, "深红月晶": 1, "魔鬼蛆": 2},
            "desc": "服用后晋升为序列7铁面人",
        },
    },

    # === 白塔途径 ===
    "白塔": {
        9: {
            "name": "读者魔药",
            "materials": {"紫月花": 2, "星辰草": 1, "蒸馏水": 1},
            "desc": "服用后成为序列9读者",
        },
        8: {
            "name": "机关术士魔药",
            "materials": {"灵银粉": 2, "九叶莲": 1, "紫月花": 2},
            "desc": "服用后晋升为序列8机关术士",
        },
        7: {
            "name": "考古学家魔药",
            "materials": {"深红月晶": 2, "死者耳语": 1, "灵银粉": 2},
            "desc": "服用后晋升为序列7考古学家",
        },
    },

    # === 巨人途径 ===
    "巨人": {
        9: {
            "name": "感知者魔药",
            "materials": {"冷杉精华": 2, "星辰草": 2, "蒸馏水": 1},
            "desc": "服用后成为序列9感知者",
        },
        8: {
            "name": "粉碎者魔药",
            "materials": {"红蛛浆液": 2, "冷杉精华": 2, "魔鬼蛆": 1},
            "desc": "服用后晋升为序列8粉碎者",
        },
        7: {
            "name": "守护者魔药",
            "materials": {"腐化之心": 1, "太阳圣水": 1, "红蛛浆液": 3},
            "desc": "服用后晋升为序列7守护者",
        },
    },

    # === 大地母神途径 ===
    "大地母神": {
        9: {
            "name": "种植者魔药",
            "materials": {"夜香花": 2, "冷杉精华": 2, "蒸馏水": 1},
            "desc": "服用后成为序列9种植者",
        },
        8: {
            "name": "牧人魔药",
            "materials": {"九叶莲": 2, "夜香花": 2, "银月草汁": 1},
            "desc": "服用后晋升为序列8牧人",
        },
        7: {
            "name": "收获者魔药",
            "materials": {"太阳圣水": 2, "九叶莲": 2, "极光碎片": 1},
            "desc": "服用后晋升为序列7收获者",
        },
    },

    # === 知识途径 ===
    "知识": {
        9: {
            "name": "学徒魔药",
            "materials": {"紫月花": 2, "蒸馏水": 2, "星辰草": 1},
            "desc": "服用后成为序列9学徒",
        },
        8: {
            "name": "巫师魔药",
            "materials": {"梦境尘埃": 2, "紫月花": 2, "灵银粉": 1},
            "desc": "服用后晋升为序列8巫师",
        },
        7: {
            "name": "咒术师魔药",
            "materials": {"命运之弦": 1, "深红月晶": 1, "梦境尘埃": 3},
            "desc": "服用后晋升为序列7咒术师",
        },
    },

    # === 猎人途径 ===
    "猎人": {
        9: {
            "name": "探险家魔药",
            "materials": {"冷杉精华": 3, "黑曜石粉": 1, "蒸馏水": 1},
            "desc": "服用后成为序列9探险家",
        },
        8: {
            "name": "陷阱师魔药",
            "materials": {"红蛛浆液": 2, "魔鬼蛆": 1, "冷杉精华": 2},
            "desc": "服用后晋升为序列8陷阱师",
        },
        7: {
            "name": "驯化者魔药",
            "materials": {"隐者之眼": 1, "风暴精华": 1, "红蛛浆液": 3},
            "desc": "服用后晋升为序列7驯化者",
        },
    },

    # === 深渊途径 ===
    "深渊": {
        9: {
            "name": "暗侍者魔药",
            "materials": {"夜香花": 3, "黑曜石粉": 2},
            "desc": "服用后成为序列9暗侍者",
        },
        8: {
            "name": "深渊信徒魔药",
            "materials": {"梦境尘埃": 2, "魔鬼蛆": 2, "夜香花": 1},
            "desc": "服用后晋升为序列8深渊信徒",
        },
        7: {
            "name": "深渊行者魔药",
            "materials": {"腐化之心": 1, "死者耳语": 2, "梦境尘埃": 2},
            "desc": "服用后晋升为序列7深渊行者",
        },
    },

    # === 永恒烈阳途径 ===
    "永恒烈阳": {
        9: {
            "name": "光启者魔药",
            "materials": {"星辰草": 3, "蒸馏水": 2},
            "desc": "服用后成为序列9光启者",
        },
        8: {
            "name": "圣职者魔药",
            "materials": {"九叶莲": 2, "银月草汁": 2, "星辰草": 1},
            "desc": "服用后晋升为序列8圣职者",
        },
        7: {
            "name": "太阳之子魔药",
            "materials": {"太阳圣水": 3, "极光碎片": 1, "九叶莲": 1},
            "desc": "服用后晋升为序列7太阳之子",
        },
    },

    # === 黑暗途径 ===
    "黑暗": {
        9: {
            "name": "拾荒者魔药",
            "materials": {"夜香花": 2, "黑曜石粉": 2, "蒸馏水": 1},
            "desc": "服用后成为序列9拾荒者",
        },
        8: {
            "name": "丧者魔药",
            "materials": {"魔鬼蛆": 2, "梦境尘埃": 1, "夜香花": 2},
            "desc": "服用后晋升为序列8丧者",
        },
        7: {
            "name": "死灵法师魔药",
            "materials": {"死者耳语": 3, "腐化之心": 1, "梦境尘埃": 1},
            "desc": "服用后晋升为序列7死灵法师",
        },
    },

    # === 原罪途径 ===
    "原罪": {
        9: {
            "name": "刺客魔药",
            "materials": {"夜香花": 2, "红蛛浆液": 1, "蒸馏水": 1},
            "desc": "服用后成为序列9刺客",
        },
        8: {
            "name": "中毒者魔药",
            "materials": {"红蛛浆液": 3, "魔鬼蛆": 1, "夜香花": 1},
            "desc": "服用后晋升为序列8中毒者",
        },
        7: {
            "name": "毒师魔药",
            "materials": {"隐者之眼": 2, "腐化之心": 1, "红蛛浆液": 2},
            "desc": "服用后晋升为序列7毒师",
        },
    },

    # === 梦境途径 ===
    "梦境": {
        9: {
            "name": "入梦者魔药",
            "materials": {"紫月花": 3, "蒸馏水": 2},
            "desc": "服用后成为序列9入梦者",
        },
        8: {
            "name": "梦行者魔药",
            "materials": {"梦境尘埃": 3, "紫月花": 2},
            "desc": "服用后晋升为序列8梦行者",
        },
        7: {
            "name": "编梦者魔药",
            "materials": {"命运之弦": 1, "梦境尘埃": 3, "深红月晶": 1},
            "desc": "服用后晋升为序列7编梦者",
        },
    },

    # === 神机途径 ===
    "神机": {
        9: {
            "name": "机械师魔药",
            "materials": {"黑曜石粉": 3, "冷杉精华": 1, "蒸馏水": 1},
            "desc": "服用后成为序列9机械师",
        },
        8: {
            "name": "工程师魔药",
            "materials": {"灵银粉": 3, "黑曜石粉": 2},
            "desc": "服用后晋升为序列8工程师",
        },
        7: {
            "name": "发明家魔药",
            "materials": {"极光碎片": 1, "风暴精华": 1, "灵银粉": 3},
            "desc": "服用后晋升为序列7发明家",
        },
    },
}

# 消耗品
CONSUMABLES = {
    "小型治疗药剂": {
        "type": "heal",
        "quality": QUALITY_COMMON,
        "effect": {"heal": 30},
        "desc": "恢复30点生命值",
    },
    "中型治疗药剂": {
        "type": "heal",
        "quality": QUALITY_UNCOMMON,
        "effect": {"heal": 60},
        "desc": "恢复60点生命值",
    },
    "大型治疗药剂": {
        "type": "heal",
        "quality": QUALITY_RARE,
        "effect": {"heal": 100},
        "desc": "恢复100点生命值",
    },
}

# 获取材料信息
def get_material_info(name):
    """获取材料信息"""
    return MATERIALS.get(name)

# 获取魔药配方
def get_potion_recipe(pathway_name, sequence):
    """获取指定途径和序列的魔药配方"""
    pathway_recipes = POTION_RECIPES.get(pathway_name, {})
    return pathway_recipes.get(sequence)

# 检查是否能炮制魔药
def can_craft_potion(inventory, pathway_name, sequence):
    """检查背包中材料是否足够炮制魔药"""
    recipe = get_potion_recipe(pathway_name, sequence)
    if not recipe:
        return False, "没有对应的魔药配方"

    for material, count in recipe["materials"].items():
        if inventory.get(material, 0) < count:
            return False, f"缺少材料: {material} (需要{count}个)"

    return True, "可以炮制"
