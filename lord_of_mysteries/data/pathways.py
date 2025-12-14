"""
途径数据 - 基于《诡秘之主》的22条途径
"""

# 途径类型
PATHWAY_TYPES = {
    "melee": "近战物理",
    "magic": "魔法远程",
    "control": "辅助控制",
    "special": "特殊能力",
    "support": "生存支援",
    "wisdom": "智慧研究"
}

# 技能数据
SKILLS = {
    # 愚者途径技能
    "灵视": {"type": "buff", "cooldown": 10, "duration": 5, "desc": "开启灵视，看穿敌人弱点，增加20%暴击率"},
    "占卜": {"type": "buff", "cooldown": 15, "duration": 3, "desc": "预知危险，短暂无敌"},
    "纸牌投掷": {"type": "projectile", "cooldown": 2, "damage": 25, "desc": "投掷锋利纸牌，远程攻击"},
    "火焰跳跃": {"type": "dash", "cooldown": 8, "damage": 40, "desc": "化为火焰瞬移，对路径敌人造成伤害"},
    "空气炮": {"type": "projectile", "cooldown": 5, "damage": 60, "desc": "压缩空气形成炮弹"},
    "易容": {"type": "buff", "cooldown": 30, "duration": 10, "desc": "改变外貌，敌人不会主动攻击"},
    # 门途径技能
    "偷窃": {"type": "buff", "cooldown": 8, "duration": 0, "desc": "偷取敌人的物品或能力"},
    "闪现": {"type": "dash", "cooldown": 5, "damage": 0, "desc": "瞬间移动到目标位置"},
    "隐匿": {"type": "buff", "cooldown": 20, "duration": 8, "desc": "进入隐身状态"},
    "空间切割": {"type": "projectile", "cooldown": 10, "damage": 70, "desc": "切割空间造成伤害"},
    # 隐秘途径技能
    "读心": {"type": "buff", "cooldown": 12, "duration": 6, "desc": "读取敌人意图，预判攻击"},
    "催眠": {"type": "control", "cooldown": 15, "duration": 4, "desc": "催眠敌人使其停止行动"},
    "心灵冲击": {"type": "projectile", "cooldown": 6, "damage": 45, "desc": "精神攻击造成伤害"},
    "梦境入侵": {"type": "control", "cooldown": 20, "duration": 6, "desc": "入侵敌人梦境使其混乱"},
    # 智慧途径技能
    "博学": {"type": "buff", "cooldown": 0, "duration": 0, "desc": "被动提升所有属性"},
    "考古": {"type": "buff", "cooldown": 25, "duration": 10, "desc": "分析敌人弱点，增加伤害"},
    "知识投射": {"type": "projectile", "cooldown": 4, "damage": 35, "desc": "将知识化为攻击"},
    # 黑夜途径技能
    "暗影步": {"type": "dash", "cooldown": 6, "damage": 30, "desc": "在阴影中穿行"},
    "黑暗笼罩": {"type": "control", "cooldown": 18, "duration": 5, "desc": "制造黑暗区域"},
    "暗影刺杀": {"type": "projectile", "cooldown": 3, "damage": 50, "desc": "暗影形成的利刃"},
    # 死亡途径技能
    "亡灵召唤": {"type": "summon", "cooldown": 20, "duration": 15, "desc": "召唤亡灵助战"},
    "死亡凝视": {"type": "projectile", "cooldown": 10, "damage": 80, "desc": "死亡的目光"},
    "灵魂收割": {"type": "buff", "cooldown": 25, "duration": 0, "desc": "收割敌人灵魂恢复生命"},
    # 猎人途径技能
    "猎杀标记": {"type": "buff", "cooldown": 15, "duration": 20, "desc": "标记敌人，增加对其伤害"},
    "嗜血": {"type": "buff", "cooldown": 20, "duration": 10, "desc": "进入嗜血状态，攻击吸血"},
    "血之利刃": {"type": "projectile", "cooldown": 5, "damage": 55, "desc": "血液形成的利刃"},
    # 暴风途径技能
    "风暴召唤": {"type": "projectile", "cooldown": 12, "damage": 55, "desc": "召唤风暴攻击"},
    "水流操控": {"type": "control", "cooldown": 10, "duration": 4, "desc": "操控水流束缚敌人"},
    "闪电链": {"type": "projectile", "cooldown": 7, "damage": 45, "desc": "释放闪电链"},
    # 战争途径技能
    "狂暴": {"type": "buff", "cooldown": 20, "duration": 10, "desc": "进入狂暴状态，攻击大幅提升"},
    "重击": {"type": "melee", "cooldown": 4, "damage": 70, "desc": "强力重击"},
    "地震": {"type": "projectile", "cooldown": 15, "damage": 50, "desc": "震击地面造成范围伤害"},
    # 命运途径技能
    "幸运加持": {"type": "buff", "cooldown": 18, "duration": 12, "desc": "增加暴击和闪避"},
    "厄运诅咒": {"type": "control", "cooldown": 20, "duration": 8, "desc": "诅咒敌人降低其属性"},
    "命运逆转": {"type": "buff", "cooldown": 30, "duration": 0, "desc": "逆转即将受到的致命伤害"},
    # 炼药途径技能
    "火球术": {"type": "projectile", "cooldown": 4, "damage": 45, "desc": "释放火球"},
    "冰锥术": {"type": "projectile", "cooldown": 5, "damage": 40, "desc": "释放冰锥"},
    "魔法护盾": {"type": "buff", "cooldown": 15, "duration": 8, "desc": "生成魔法护盾"},
    "变形术": {"type": "buff", "cooldown": 25, "duration": 15, "desc": "变形增强能力"},
    # 错误途径技能
    "混乱领域": {"type": "control", "cooldown": 20, "duration": 8, "desc": "创造混乱区域"},
    "感染": {"type": "projectile", "cooldown": 8, "damage": 40, "desc": "感染敌人造成持续伤害"},
    "错误扭曲": {"type": "buff", "cooldown": 25, "duration": 0, "desc": "扭曲规则获得优势"},
    # 黑皇帝途径技能
    "威压": {"type": "control", "cooldown": 15, "duration": 5, "desc": "释放威压使敌人恐惧"},
    "契约": {"type": "buff", "cooldown": 30, "duration": 0, "desc": "强制签订契约"},
    "黑暗统治": {"type": "buff", "cooldown": 25, "duration": 15, "desc": "统治领域内的一切"},
    # 刺客途径技能
    "潜行": {"type": "buff", "cooldown": 12, "duration": 10, "desc": "进入潜行状态"},
    "致命一击": {"type": "melee", "cooldown": 8, "damage": 100, "desc": "从背后发动致命攻击"},
    "毒刃": {"type": "projectile", "cooldown": 5, "damage": 35, "desc": "投掷淬毒的飞刀"},
    # 审判途径技能
    "神圣审判": {"type": "projectile", "cooldown": 10, "damage": 60, "desc": "神圣之力审判敌人"},
    "正义之锤": {"type": "melee", "cooldown": 6, "damage": 55, "desc": "以正义之名重击"},
    "庇护": {"type": "buff", "cooldown": 20, "duration": 8, "desc": "获得神圣庇护"},
    # 太阳途径技能
    "神圣之光": {"type": "projectile", "cooldown": 5, "damage": 40, "desc": "释放神圣光芒"},
    "治愈祷言": {"type": "heal", "cooldown": 15, "heal": 50, "desc": "治愈自身伤势"},
    "惩戒": {"type": "projectile", "cooldown": 8, "damage": 60, "desc": "神圣惩戒攻击"},
    # 驭兽途径技能
    "召唤野兽": {"type": "summon", "cooldown": 20, "duration": 20, "desc": "召唤野兽助战"},
    "自然治愈": {"type": "heal", "cooldown": 15, "heal": 40, "desc": "自然之力治愈"},
    "野性之力": {"type": "buff", "cooldown": 18, "duration": 12, "desc": "获得野兽之力"},
    # 其他途径技能
    "完美打击": {"type": "melee", "cooldown": 5, "damage": 50, "desc": "完美的攻击"},
    "完美防御": {"type": "buff", "cooldown": 15, "duration": 5, "desc": "完美的防御姿态"},
    "秘密感知": {"type": "buff", "cooldown": 12, "duration": 10, "desc": "感知隐藏的秘密"},
    "祈祷": {"type": "heal", "cooldown": 20, "heal": 60, "desc": "向神明祈祷获得治愈"},
    "命运转轮": {"type": "buff", "cooldown": 25, "duration": 0, "desc": "转动命运之轮改变局势"},
    "因果操控": {"type": "control", "cooldown": 18, "duration": 6, "desc": "操控因果关系"},
    "魅惑术": {"type": "control", "cooldown": 15, "duration": 8, "desc": "魅惑敌人使其听从命令"},
    "诅咒": {"type": "projectile", "cooldown": 10, "damage": 45, "desc": "释放恶毒的诅咒"},
    "挣脱": {"type": "buff", "cooldown": 20, "duration": 0, "desc": "挣脱一切束缚"},
    "锁链攻击": {"type": "projectile", "cooldown": 6, "damage": 40, "desc": "以锁链攻击敌人"},
}

# 途径数据 - 22条途径
PATHWAYS = {
    "愚者": {
        "name": "愚者途径",
        "god": "愚者",
        "type": "magic",
        "color": (218, 165, 32),  # 金色
        "desc": "占卜与欺诈之道，掌控命运的丝线",
        "sequences": {
            9: {"name": "占卜家", "skills": ["灵视", "占卜"], "hp": 100, "attack": 15, "defense": 5, "speed": 5},
            8: {"name": "小丑", "skills": ["灵视", "占卜", "纸牌投掷"], "hp": 150, "attack": 25, "defense": 8, "speed": 6},
            7: {"name": "魔术师", "skills": ["灵视", "占卜", "纸牌投掷", "火焰跳跃"], "hp": 200, "attack": 40, "defense": 12, "speed": 7},
            6: {"name": "驭火者", "skills": ["灵视", "占卜", "纸牌投掷", "火焰跳跃", "易容"], "hp": 280, "attack": 60, "defense": 18, "speed": 8},
            5: {"name": "无面人", "skills": ["灵视", "占卜", "纸牌投掷", "火焰跳跃", "易容", "空气炮"], "hp": 380, "attack": 85, "defense": 25, "speed": 9},
            4: {"name": "马戏团长", "skills": ["灵视", "占卜", "纸牌投掷", "火焰跳跃", "易容", "空气炮"], "hp": 500, "attack": 120, "defense": 35, "speed": 10},
            3: {"name": "诡秘侍者", "skills": ["灵视", "占卜", "纸牌投掷", "火焰跳跃", "易容", "空气炮"], "hp": 700, "attack": 180, "defense": 50, "speed": 12},
            2: {"name": "奇迹师", "skills": ["灵视", "占卜", "纸牌投掷", "火焰跳跃", "易容", "空气炮"], "hp": 1000, "attack": 280, "defense": 80, "speed": 15},
            1: {"name": "愚者代行者", "skills": ["灵视", "占卜", "纸牌投掷", "火焰跳跃", "易容", "空气炮"], "hp": 1500, "attack": 450, "defense": 120, "speed": 18},
            0: {"name": "愚者", "skills": ["灵视", "占卜", "纸牌投掷", "火焰跳跃", "易容", "空气炮"], "hp": 3000, "attack": 800, "defense": 200, "speed": 25},
        }
    },
    "门": {
        "name": "门途径",
        "god": "门",
        "type": "special",
        "color": (128, 0, 128),  # 紫色
        "desc": "空间与盗窃之道，穿梭于不同位面",
        "sequences": {
            9: {"name": "偷盗者", "skills": ["偷窃", "闪现"], "hp": 90, "attack": 18, "defense": 4, "speed": 7},
            8: {"name": "尸体收集者", "skills": ["偷窃", "闪现", "隐匿"], "hp": 140, "attack": 28, "defense": 7, "speed": 8},
            7: {"name": "窃贼", "skills": ["偷窃", "闪现", "隐匿", "空间切割"], "hp": 190, "attack": 42, "defense": 10, "speed": 9},
            6: {"name": "旅法者", "skills": ["偷窃", "闪现", "隐匿", "空间切割"], "hp": 260, "attack": 62, "defense": 15, "speed": 10},
            5: {"name": "守秘人", "skills": ["偷窃", "闪现", "隐匿", "空间切割"], "hp": 350, "attack": 88, "defense": 22, "speed": 11},
            4: {"name": "传送师", "skills": ["偷窃", "闪现", "隐匿", "空间切割"], "hp": 480, "attack": 125, "defense": 32, "speed": 13},
            3: {"name": "空间行者", "skills": ["偷窃", "闪现", "隐匿", "空间切割"], "hp": 680, "attack": 185, "defense": 48, "speed": 15},
            2: {"name": "星之门", "skills": ["偷窃", "闪现", "隐匿", "空间切割"], "hp": 980, "attack": 290, "defense": 75, "speed": 18},
            1: {"name": "诸界行者", "skills": ["偷窃", "闪现", "隐匿", "空间切割"], "hp": 1450, "attack": 460, "defense": 115, "speed": 22},
            0: {"name": "门", "skills": ["偷窃", "闪现", "隐匿", "空间切割"], "hp": 2800, "attack": 820, "defense": 190, "speed": 28},
        }
    },
    "隐秘": {
        "name": "隐秘途径",
        "god": "隐秘侍者",
        "type": "control",
        "color": (75, 0, 130),  # 靛蓝色
        "desc": "心灵与操控之道，窥探他人思想",
        "sequences": {
            9: {"name": "读心者", "skills": ["读心", "心灵冲击"], "hp": 95, "attack": 16, "defense": 5, "speed": 5},
            8: {"name": "推演家", "skills": ["读心", "心灵冲击", "催眠"], "hp": 145, "attack": 26, "defense": 8, "speed": 6},
            7: {"name": "催眠师", "skills": ["读心", "心灵冲击", "催眠", "梦境入侵"], "hp": 195, "attack": 40, "defense": 12, "speed": 7},
            6: {"name": "操控师", "skills": ["读心", "心灵冲击", "催眠", "梦境入侵"], "hp": 270, "attack": 60, "defense": 18, "speed": 8},
            5: {"name": "梦行者", "skills": ["读心", "心灵冲击", "催眠", "梦境入侵"], "hp": 370, "attack": 86, "defense": 25, "speed": 9},
            4: {"name": "噩梦", "skills": ["读心", "心灵冲击", "催眠", "梦境入侵"], "hp": 490, "attack": 122, "defense": 35, "speed": 10},
            3: {"name": "预言家", "skills": ["读心", "心灵冲击", "催眠", "梦境入侵"], "hp": 690, "attack": 182, "defense": 50, "speed": 12},
            2: {"name": "隐秘祈祷者", "skills": ["读心", "心灵冲击", "催眠", "梦境入侵"], "hp": 990, "attack": 285, "defense": 78, "speed": 15},
            1: {"name": "隐秘代行者", "skills": ["读心", "心灵冲击", "催眠", "梦境入侵"], "hp": 1480, "attack": 455, "defense": 118, "speed": 18},
            0: {"name": "隐秘侍者", "skills": ["读心", "心灵冲击", "催眠", "梦境入侵"], "hp": 2900, "attack": 810, "defense": 195, "speed": 25},
        }
    },
    "智慧": {
        "name": "智慧途径",
        "god": "智慧之神",
        "type": "wisdom",
        "color": (70, 130, 180),  # 钢蓝色
        "desc": "知识与博学之道，以学识为武器",
        "sequences": {
            9: {"name": "鉴定师", "skills": ["博学", "知识投射"], "hp": 100, "attack": 14, "defense": 6, "speed": 4},
            8: {"name": "考古学家", "skills": ["博学", "知识投射", "考古"], "hp": 155, "attack": 24, "defense": 9, "speed": 5},
            7: {"name": "大学者", "skills": ["博学", "知识投射", "考古"], "hp": 210, "attack": 38, "defense": 14, "speed": 6},
            6: {"name": "博学者", "skills": ["博学", "知识投射", "考古"], "hp": 290, "attack": 58, "defense": 20, "speed": 7},
            5: {"name": "预言家", "skills": ["博学", "知识投射", "考古"], "hp": 400, "attack": 84, "defense": 28, "speed": 8},
            4: {"name": "探秘者", "skills": ["博学", "知识投射", "考古"], "hp": 530, "attack": 118, "defense": 38, "speed": 9},
            3: {"name": "智者", "skills": ["博学", "知识投射", "考古"], "hp": 740, "attack": 175, "defense": 55, "speed": 11},
            2: {"name": "真知者", "skills": ["博学", "知识投射", "考古"], "hp": 1050, "attack": 275, "defense": 85, "speed": 14},
            1: {"name": "智慧天使", "skills": ["博学", "知识投射", "考古"], "hp": 1550, "attack": 440, "defense": 125, "speed": 17},
            0: {"name": "智慧之神", "skills": ["博学", "知识投射", "考古"], "hp": 3100, "attack": 780, "defense": 210, "speed": 24},
        }
    },
    "黑夜": {
        "name": "黑夜途径",
        "god": "永夜女神",
        "type": "special",
        "color": (25, 25, 112),  # 午夜蓝
        "desc": "黑暗与隐匿之道，在永夜中潜行",
        "sequences": {
            9: {"name": "祈密师", "skills": ["暗影步", "暗影刺杀"], "hp": 95, "attack": 17, "defense": 5, "speed": 6},
            8: {"name": "惊悚者", "skills": ["暗影步", "暗影刺杀", "黑暗笼罩"], "hp": 145, "attack": 27, "defense": 8, "speed": 7},
            7: {"name": "黑夜之眼", "skills": ["暗影步", "暗影刺杀", "黑暗笼罩"], "hp": 195, "attack": 42, "defense": 12, "speed": 8},
            6: {"name": "隐影者", "skills": ["暗影步", "暗影刺杀", "黑暗笼罩"], "hp": 270, "attack": 62, "defense": 17, "speed": 9},
            5: {"name": "半影人", "skills": ["暗影步", "暗影刺杀", "黑暗笼罩"], "hp": 370, "attack": 88, "defense": 24, "speed": 10},
            4: {"name": "影行者", "skills": ["暗影步", "暗影刺杀", "黑暗笼罩"], "hp": 490, "attack": 124, "defense": 34, "speed": 12},
            3: {"name": "暗夜之子", "skills": ["暗影步", "暗影刺杀", "黑暗笼罩"], "hp": 690, "attack": 184, "defense": 49, "speed": 14},
            2: {"name": "夜之女巫", "skills": ["暗影步", "暗影刺杀", "黑暗笼罩"], "hp": 990, "attack": 288, "defense": 77, "speed": 17},
            1: {"name": "黑暗圣者", "skills": ["暗影步", "暗影刺杀", "黑暗笼罩"], "hp": 1470, "attack": 458, "defense": 117, "speed": 21},
            0: {"name": "永夜女神", "skills": ["暗影步", "暗影刺杀", "黑暗笼罩"], "hp": 2850, "attack": 815, "defense": 192, "speed": 27},
        }
    },
    "死亡": {
        "name": "死亡途径",
        "god": "死神",
        "type": "magic",
        "color": (47, 79, 79),  # 暗石板灰
        "desc": "死亡与灵魂之道，掌控生死轮回",
        "sequences": {
            9: {"name": "尸巫", "skills": ["亡灵召唤", "死亡凝视"], "hp": 105, "attack": 16, "defense": 6, "speed": 4},
            8: {"name": "掘墓人", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 160, "attack": 26, "defense": 9, "speed": 5},
            7: {"name": "灵魂操纵师", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 215, "attack": 40, "defense": 13, "speed": 6},
            6: {"name": "尸骨召唤师", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 295, "attack": 60, "defense": 19, "speed": 7},
            5: {"name": "死亡预兆者", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 405, "attack": 86, "defense": 27, "speed": 8},
            4: {"name": "死神使者", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 535, "attack": 120, "defense": 37, "speed": 9},
            3: {"name": "亡灵天灾", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 745, "attack": 178, "defense": 53, "speed": 11},
            2: {"name": "死神代言者", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 1060, "attack": 278, "defense": 82, "speed": 14},
            1: {"name": "死亡执政官", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 1560, "attack": 445, "defense": 122, "speed": 17},
            0: {"name": "死神", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 3050, "attack": 790, "defense": 205, "speed": 24},
        }
    },
    "猎人": {
        "name": "猎人途径",
        "god": "红祭司",
        "type": "melee",
        "color": (220, 20, 60),  # 猩红色
        "desc": "猎杀与鲜血之道，以猎物之血为食",
        "sequences": {
            9: {"name": "猎人", "skills": ["猎杀标记", "血之利刃"], "hp": 110, "attack": 18, "defense": 6, "speed": 5},
            8: {"name": "挑衅者", "skills": ["猎杀标记", "血之利刃", "嗜血"], "hp": 165, "attack": 28, "defense": 9, "speed": 6},
            7: {"name": "复仇者", "skills": ["猎杀标记", "血之利刃", "嗜血"], "hp": 220, "attack": 44, "defense": 14, "speed": 7},
            6: {"name": "嗜血者", "skills": ["猎杀标记", "血之利刃", "嗜血"], "hp": 300, "attack": 66, "defense": 20, "speed": 8},
            5: {"name": "血法师", "skills": ["猎杀标记", "血之利刃", "嗜血"], "hp": 410, "attack": 94, "defense": 28, "speed": 9},
            4: {"name": "血族", "skills": ["猎杀标记", "血之利刃", "嗜血"], "hp": 540, "attack": 132, "defense": 38, "speed": 10},
            3: {"name": "血族公爵", "skills": ["猎杀标记", "血之利刃", "嗜血"], "hp": 750, "attack": 196, "defense": 55, "speed": 12},
            2: {"name": "血族亲王", "skills": ["猎杀标记", "血之利刃", "嗜血"], "hp": 1070, "attack": 306, "defense": 85, "speed": 15},
            1: {"name": "血族始祖", "skills": ["猎杀标记", "血之利刃", "嗜血"], "hp": 1570, "attack": 490, "defense": 125, "speed": 18},
            0: {"name": "红祭司", "skills": ["猎杀标记", "血之利刃", "嗜血"], "hp": 3150, "attack": 870, "defense": 210, "speed": 25},
        }
    },
    "暴风": {
        "name": "暴风途径",
        "god": "风暴之主",
        "type": "magic",
        "color": (0, 105, 148),  # 深海蓝
        "desc": "风暴与海洋之道，驾驭自然之力",
        "sequences": {
            9: {"name": "水手", "skills": ["风暴召唤", "水流操控"], "hp": 100, "attack": 16, "defense": 5, "speed": 5},
            8: {"name": "航海士", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 155, "attack": 26, "defense": 8, "speed": 6},
            7: {"name": "海难求生者", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 210, "attack": 40, "defense": 12, "speed": 7},
            6: {"name": "风眷者", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 290, "attack": 60, "defense": 18, "speed": 8},
            5: {"name": "御风者", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 400, "attack": 86, "defense": 25, "speed": 9},
            4: {"name": "暴风祭司", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 530, "attack": 122, "defense": 35, "speed": 10},
            3: {"name": "海王", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 740, "attack": 182, "defense": 50, "speed": 12},
            2: {"name": "暴风之灵", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 1050, "attack": 285, "defense": 78, "speed": 15},
            1: {"name": "风暴天使", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 1550, "attack": 455, "defense": 118, "speed": 18},
            0: {"name": "风暴之主", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 3100, "attack": 810, "defense": 195, "speed": 25},
        }
    },
    "战争": {
        "name": "战争途径",
        "god": "战神",
        "type": "melee",
        "color": (139, 69, 19),  # 鞍褐色
        "desc": "力量与战斗之道，以蛮力压制敌人",
        "sequences": {
            9: {"name": "战士", "skills": ["狂暴", "重击"], "hp": 130, "attack": 18, "defense": 8, "speed": 3},
            8: {"name": "武器大师", "skills": ["狂暴", "重击", "地震"], "hp": 195, "attack": 30, "defense": 12, "speed": 4},
            7: {"name": "雇佣兵", "skills": ["狂暴", "重击", "地震"], "hp": 260, "attack": 46, "defense": 18, "speed": 5},
            6: {"name": "黎明骑士", "skills": ["狂暴", "重击", "地震"], "hp": 350, "attack": 68, "defense": 26, "speed": 6},
            5: {"name": "守护者", "skills": ["狂暴", "重击", "地震"], "hp": 470, "attack": 96, "defense": 36, "speed": 7},
            4: {"name": "不败军", "skills": ["狂暴", "重击", "地震"], "hp": 620, "attack": 135, "defense": 48, "speed": 8},
            3: {"name": "战争领主", "skills": ["狂暴", "重击", "地震"], "hp": 860, "attack": 200, "defense": 68, "speed": 9},
            2: {"name": "神之武器", "skills": ["狂暴", "重击", "地震"], "hp": 1220, "attack": 310, "defense": 100, "speed": 11},
            1: {"name": "战争天使", "skills": ["狂暴", "重击", "地震"], "hp": 1800, "attack": 495, "defense": 145, "speed": 14},
            0: {"name": "战神", "skills": ["狂暴", "重击", "地震"], "hp": 3500, "attack": 880, "defense": 240, "speed": 20},
        }
    },
    "命运": {
        "name": "命运途径",
        "god": "命运",
        "type": "support",
        "color": (255, 182, 193),  # 浅粉色
        "desc": "幸运与厄运之道，以概率改变命运",
        "sequences": {
            9: {"name": "幸运儿", "skills": ["幸运加持", "厄运诅咒"], "hp": 95, "attack": 14, "defense": 5, "speed": 5},
            8: {"name": "作祟者", "skills": ["幸运加持", "厄运诅咒", "命运逆转"], "hp": 145, "attack": 24, "defense": 8, "speed": 6},
            7: {"name": "概率学者", "skills": ["幸运加持", "厄运诅咒", "命运逆转"], "hp": 195, "attack": 38, "defense": 12, "speed": 7},
            6: {"name": "赐运者", "skills": ["幸运加持", "厄运诅咒", "命运逆转"], "hp": 270, "attack": 58, "defense": 18, "speed": 8},
            5: {"name": "灾难祭司", "skills": ["幸运加持", "厄运诅咒", "命运逆转"], "hp": 370, "attack": 84, "defense": 25, "speed": 9},
            4: {"name": "胜负师", "skills": ["幸运加持", "厄运诅咒", "命运逆转"], "hp": 490, "attack": 118, "defense": 35, "speed": 10},
            3: {"name": "命运木偶师", "skills": ["幸运加持", "厄运诅咒", "命运逆转"], "hp": 690, "attack": 175, "defense": 50, "speed": 12},
            2: {"name": "命运织者", "skills": ["幸运加持", "厄运诅咒", "命运逆转"], "hp": 990, "attack": 275, "defense": 78, "speed": 15},
            1: {"name": "命运之子", "skills": ["幸运加持", "厄运诅咒", "命运逆转"], "hp": 1470, "attack": 440, "defense": 118, "speed": 18},
            0: {"name": "命运", "skills": ["幸运加持", "厄运诅咒", "命运逆转"], "hp": 2900, "attack": 780, "defense": 195, "speed": 25},
        }
    },
    "炼药": {
        "name": "炼药途径",
        "god": "神母",
        "type": "magic",
        "color": (65, 105, 225),  # 皇家蓝
        "desc": "魔法与炼药之道，以药剂增强自身",
        "sequences": {
            9: {"name": "炼药师", "skills": ["火球术", "冰锥术"], "hp": 90, "attack": 18, "defense": 4, "speed": 4},
            8: {"name": "药剂师", "skills": ["火球术", "冰锥术", "魔法护盾"], "hp": 140, "attack": 28, "defense": 7, "speed": 5},
            7: {"name": "生物学家", "skills": ["火球术", "冰锥术", "魔法护盾", "变形术"], "hp": 190, "attack": 44, "defense": 10, "speed": 6},
            6: {"name": "狂人", "skills": ["火球术", "冰锥术", "魔法护盾", "变形术"], "hp": 265, "attack": 65, "defense": 15, "speed": 7},
            5: {"name": "怪物", "skills": ["火球术", "冰锥术", "魔法护盾", "变形术"], "hp": 365, "attack": 92, "defense": 22, "speed": 8},
            4: {"name": "畸变", "skills": ["火球术", "冰锥术", "魔法护盾", "变形术"], "hp": 485, "attack": 130, "defense": 32, "speed": 9},
            3: {"name": "神体", "skills": ["火球术", "冰锥术", "魔法护盾", "变形术"], "hp": 680, "attack": 192, "defense": 46, "speed": 11},
            2: {"name": "神子", "skills": ["火球术", "冰锥术", "魔法护盾", "变形术"], "hp": 980, "attack": 300, "defense": 72, "speed": 14},
            1: {"name": "神母代行者", "skills": ["火球术", "冰锥术", "魔法护盾", "变形术"], "hp": 1450, "attack": 475, "defense": 110, "speed": 17},
            0: {"name": "神母", "skills": ["火球术", "冰锥术", "魔法护盾", "变形术"], "hp": 2850, "attack": 845, "defense": 185, "speed": 24},
        }
    },
    "错误": {
        "name": "错误途径",
        "god": "错误",
        "type": "special",
        "color": (20, 20, 60),  # 深蓝黑
        "desc": "混乱与错误之道，在混沌中获得力量",
        "sequences": {
            9: {"name": "罪犯", "skills": ["混乱领域", "感染"], "hp": 100, "attack": 17, "defense": 5, "speed": 5},
            8: {"name": "仲裁人", "skills": ["混乱领域", "感染", "错误扭曲"], "hp": 155, "attack": 27, "defense": 8, "speed": 6},
            7: {"name": "混乱行者", "skills": ["混乱领域", "感染", "错误扭曲"], "hp": 210, "attack": 42, "defense": 12, "speed": 7},
            6: {"name": "变异师", "skills": ["混乱领域", "感染", "错误扭曲"], "hp": 290, "attack": 62, "defense": 18, "speed": 8},
            5: {"name": "染疫者", "skills": ["混乱领域", "感染", "错误扭曲"], "hp": 400, "attack": 88, "defense": 25, "speed": 9},
            4: {"name": "行尸", "skills": ["混乱领域", "感染", "错误扭曲"], "hp": 530, "attack": 124, "defense": 35, "speed": 10},
            3: {"name": "错误使者", "skills": ["混乱领域", "感染", "错误扭曲"], "hp": 740, "attack": 184, "defense": 50, "speed": 12},
            2: {"name": "错误之子", "skills": ["混乱领域", "感染", "错误扭曲"], "hp": 1060, "attack": 288, "defense": 78, "speed": 15},
            1: {"name": "错误代行者", "skills": ["混乱领域", "感染", "错误扭曲"], "hp": 1560, "attack": 460, "defense": 118, "speed": 18},
            0: {"name": "错误", "skills": ["混乱领域", "感染", "错误扭曲"], "hp": 3100, "attack": 815, "defense": 195, "speed": 25},
        }
    },
    "黑皇帝": {
        "name": "黑皇帝途径",
        "god": "黑皇帝",
        "type": "control",
        "color": (30, 30, 30),  # 纯黑
        "desc": "权谋与统治之道，以黑暗手段掌控一切",
        "sequences": {
            9: {"name": "强权者", "skills": ["威压", "契约"], "hp": 105, "attack": 14, "defense": 6, "speed": 5},
            8: {"name": "独裁者", "skills": ["威压", "契约", "黑暗统治"], "hp": 160, "attack": 24, "defense": 9, "speed": 6},
            7: {"name": "阴谋家", "skills": ["威压", "契约", "黑暗统治"], "hp": 215, "attack": 38, "defense": 14, "speed": 7},
            6: {"name": "征服者", "skills": ["威压", "契约", "黑暗统治"], "hp": 295, "attack": 58, "defense": 20, "speed": 8},
            5: {"name": "野蛮人首领", "skills": ["威压", "契约", "黑暗统治"], "hp": 405, "attack": 84, "defense": 28, "speed": 9},
            4: {"name": "暴君", "skills": ["威压", "契约", "黑暗统治"], "hp": 535, "attack": 118, "defense": 38, "speed": 10},
            3: {"name": "魔鬼", "skills": ["威压", "契约", "黑暗统治"], "hp": 745, "attack": 176, "defense": 55, "speed": 12},
            2: {"name": "契约之王", "skills": ["威压", "契约", "黑暗统治"], "hp": 1060, "attack": 276, "defense": 85, "speed": 15},
            1: {"name": "暗帝", "skills": ["威压", "契约", "黑暗统治"], "hp": 1560, "attack": 442, "defense": 125, "speed": 18},
            0: {"name": "黑皇帝", "skills": ["威压", "契约", "黑暗统治"], "hp": 3150, "attack": 785, "defense": 210, "speed": 25},
        }
    },
    "刺客": {
        "name": "刺客途径",
        "god": "隐者",
        "type": "melee",
        "color": (64, 64, 64),  # 深灰
        "desc": "暗杀与隐匿之道，在暗影中夺人性命",
        "sequences": {
            9: {"name": "刺客", "skills": ["潜行", "致命一击"], "hp": 85, "attack": 20, "defense": 3, "speed": 7},
            8: {"name": "绝命人", "skills": ["潜行", "致命一击", "毒刃"], "hp": 130, "attack": 32, "defense": 6, "speed": 8},
            7: {"name": "无面人", "skills": ["潜行", "致命一击", "毒刃"], "hp": 175, "attack": 48, "defense": 9, "speed": 9},
            6: {"name": "歌剧演员", "skills": ["潜行", "致命一击", "毒刃"], "hp": 245, "attack": 70, "defense": 14, "speed": 10},
            5: {"name": "魔女", "skills": ["潜行", "致命一击", "毒刃"], "hp": 335, "attack": 98, "defense": 20, "speed": 11},
            4: {"name": "祈祷者", "skills": ["潜行", "致命一击", "毒刃"], "hp": 450, "attack": 138, "defense": 29, "speed": 13},
            3: {"name": "隐者", "skills": ["潜行", "致命一击", "毒刃"], "hp": 630, "attack": 204, "defense": 43, "speed": 15},
            2: {"name": "暗影公爵", "skills": ["潜行", "致命一击", "毒刃"], "hp": 910, "attack": 318, "defense": 68, "speed": 18},
            1: {"name": "暗影之王", "skills": ["潜行", "致命一击", "毒刃"], "hp": 1350, "attack": 508, "defense": 105, "speed": 22},
            0: {"name": "隐者", "skills": ["潜行", "致命一击", "毒刃"], "hp": 2650, "attack": 900, "defense": 175, "speed": 30},
        }
    },
    "审判": {
        "name": "审判途径",
        "god": "战神",
        "type": "melee",
        "color": (192, 192, 192),  # 银色
        "desc": "审判与正义之道，以神圣之力惩戒邪恶",
        "sequences": {
            9: {"name": "仲裁者", "skills": ["神圣审判", "正义之锤"], "hp": 115, "attack": 16, "defense": 8, "speed": 4},
            8: {"name": "铁血骑士", "skills": ["神圣审判", "正义之锤", "庇护"], "hp": 175, "attack": 26, "defense": 12, "speed": 5},
            7: {"name": "绝望骑士", "skills": ["神圣审判", "正义之锤", "庇护"], "hp": 235, "attack": 40, "defense": 18, "speed": 6},
            6: {"name": "惩罚骑士", "skills": ["神圣审判", "正义之锤", "庇护"], "hp": 320, "attack": 60, "defense": 26, "speed": 7},
            5: {"name": "沉默骑士", "skills": ["神圣审判", "正义之锤", "庇护"], "hp": 435, "attack": 86, "defense": 36, "speed": 8},
            4: {"name": "死亡执事", "skills": ["神圣审判", "正义之锤", "庇护"], "hp": 575, "attack": 120, "defense": 48, "speed": 9},
            3: {"name": "审判官", "skills": ["神圣审判", "正义之锤", "庇护"], "hp": 800, "attack": 180, "defense": 68, "speed": 10},
            2: {"name": "审判天使", "skills": ["神圣审判", "正义之锤", "庇护"], "hp": 1150, "attack": 280, "defense": 100, "speed": 12},
            1: {"name": "至高审判者", "skills": ["神圣审判", "正义之锤", "庇护"], "hp": 1700, "attack": 450, "defense": 145, "speed": 15},
            0: {"name": "战神", "skills": ["神圣审判", "正义之锤", "庇护"], "hp": 3400, "attack": 800, "defense": 240, "speed": 22},
        }
    },
    "太阳": {
        "name": "太阳途径",
        "god": "永恒烈阳",
        "type": "support",
        "color": (255, 200, 50),  # 金黄色
        "desc": "光明与治愈之道，以信仰为力量",
        "sequences": {
            9: {"name": "拜祭师", "skills": ["神圣之光", "治愈祷言"], "hp": 110, "attack": 14, "defense": 7, "speed": 4},
            8: {"name": "光辉骑士", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 165, "attack": 24, "defense": 10, "speed": 5},
            7: {"name": "阳光祭司", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 220, "attack": 38, "defense": 15, "speed": 6},
            6: {"name": "驱魔人", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 300, "attack": 58, "defense": 22, "speed": 7},
            5: {"name": "牧师", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 410, "attack": 84, "defense": 30, "speed": 8},
            4: {"name": "光之隐修士", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 540, "attack": 118, "defense": 40, "speed": 9},
            3: {"name": "照明者", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 750, "attack": 176, "defense": 58, "speed": 11},
            2: {"name": "光辉之主", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 1070, "attack": 276, "defense": 88, "speed": 14},
            1: {"name": "圣者", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 1570, "attack": 442, "defense": 128, "speed": 17},
            0: {"name": "永恒烈阳", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 3150, "attack": 785, "defense": 215, "speed": 24},
        }
    },
    "驭兽": {
        "name": "驭兽途径",
        "god": "神母",
        "type": "support",
        "color": (34, 139, 34),  # 森林绿
        "desc": "自然与生命之道，与野兽为伴",
        "sequences": {
            9: {"name": "驭兽师", "skills": ["召唤野兽", "自然治愈"], "hp": 105, "attack": 15, "defense": 6, "speed": 5},
            8: {"name": "医生", "skills": ["召唤野兽", "自然治愈", "野性之力"], "hp": 160, "attack": 25, "defense": 9, "speed": 6},
            7: {"name": "变形师", "skills": ["召唤野兽", "自然治愈", "野性之力"], "hp": 215, "attack": 40, "defense": 14, "speed": 7},
            6: {"name": "精灵使", "skills": ["召唤野兽", "自然治愈", "野性之力"], "hp": 295, "attack": 60, "defense": 20, "speed": 8},
            5: {"name": "天灾召唤者", "skills": ["召唤野兽", "自然治愈", "野性之力"], "hp": 405, "attack": 86, "defense": 28, "speed": 9},
            4: {"name": "精灵王", "skills": ["召唤野兽", "自然治愈", "野性之力"], "hp": 535, "attack": 120, "defense": 38, "speed": 10},
            3: {"name": "自然之子", "skills": ["召唤野兽", "自然治愈", "野性之力"], "hp": 745, "attack": 178, "defense": 55, "speed": 12},
            2: {"name": "万物之灵", "skills": ["召唤野兽", "自然治愈", "野性之力"], "hp": 1060, "attack": 278, "defense": 85, "speed": 15},
            1: {"name": "自然化身", "skills": ["召唤野兽", "自然治愈", "野性之力"], "hp": 1560, "attack": 445, "defense": 125, "speed": 18},
            0: {"name": "神母", "skills": ["召唤野兽", "自然治愈", "野性之力"], "hp": 3150, "attack": 790, "defense": 210, "speed": 25},
        }
    },
    "囚徒": {
        "name": "囚徒途径",
        "god": "被囚禁者",
        "type": "melee",
        "color": (100, 80, 60),  # 锈棕色
        "desc": "束缚与挣脱之道，在枷锁中获得力量",
        "sequences": {
            9: {"name": "囚徒", "skills": ["挣脱", "锁链攻击"], "hp": 120, "attack": 16, "defense": 8, "speed": 4},
            8: {"name": "逃脱者", "skills": ["挣脱", "锁链攻击"], "hp": 180, "attack": 26, "defense": 12, "speed": 5},
            7: {"name": "自由行者", "skills": ["挣脱", "锁链攻击"], "hp": 240, "attack": 40, "defense": 18, "speed": 6},
            6: {"name": "束缚者", "skills": ["挣脱", "锁链攻击"], "hp": 330, "attack": 60, "defense": 26, "speed": 7},
            5: {"name": "锁链大师", "skills": ["挣脱", "锁链攻击"], "hp": 450, "attack": 86, "defense": 36, "speed": 8},
            4: {"name": "监狱长", "skills": ["挣脱", "锁链攻击"], "hp": 600, "attack": 120, "defense": 48, "speed": 9},
            3: {"name": "枷锁之王", "skills": ["挣脱", "锁链攻击"], "hp": 840, "attack": 178, "defense": 68, "speed": 10},
            2: {"name": "自由化身", "skills": ["挣脱", "锁链攻击"], "hp": 1200, "attack": 278, "defense": 100, "speed": 12},
            1: {"name": "解放者", "skills": ["挣脱", "锁链攻击"], "hp": 1780, "attack": 445, "defense": 145, "speed": 15},
            0: {"name": "被囚禁者", "skills": ["挣脱", "锁链攻击"], "hp": 3500, "attack": 790, "defense": 240, "speed": 22},
        }
    },
    "完美者": {
        "name": "完美者途径",
        "god": "完美之神",
        "type": "special",
        "color": (255, 215, 0),  # 金色
        "desc": "完美与极致之道，追求绝对的完美",
        "sequences": {
            9: {"name": "完美主义者", "skills": ["完美打击", "完美防御"], "hp": 100, "attack": 16, "defense": 6, "speed": 5},
            8: {"name": "艺术家", "skills": ["完美打击", "完美防御"], "hp": 155, "attack": 26, "defense": 9, "speed": 6},
            7: {"name": "大师", "skills": ["完美打击", "完美防御"], "hp": 210, "attack": 40, "defense": 14, "speed": 7},
            6: {"name": "宗师", "skills": ["完美打击", "完美防御"], "hp": 290, "attack": 60, "defense": 20, "speed": 8},
            5: {"name": "完美战士", "skills": ["完美打击", "完美防御"], "hp": 400, "attack": 86, "defense": 28, "speed": 9},
            4: {"name": "无瑕者", "skills": ["完美打击", "完美防御"], "hp": 530, "attack": 122, "defense": 38, "speed": 10},
            3: {"name": "完美化身", "skills": ["完美打击", "完美防御"], "hp": 740, "attack": 182, "defense": 55, "speed": 12},
            2: {"name": "至臻者", "skills": ["完美打击", "完美防御"], "hp": 1060, "attack": 285, "defense": 85, "speed": 15},
            1: {"name": "完美使者", "skills": ["完美打击", "完美防御"], "hp": 1560, "attack": 455, "defense": 125, "speed": 18},
            0: {"name": "完美之神", "skills": ["完美打击", "完美防御"], "hp": 3150, "attack": 810, "defense": 210, "speed": 25},
        }
    },
    "秘祈人": {
        "name": "秘祈人途径",
        "god": "隐秘之神",
        "type": "wisdom",
        "color": (100, 60, 120),  # 深紫
        "desc": "秘密与祈祷之道，探寻隐藏的真理",
        "sequences": {
            9: {"name": "秘祈人", "skills": ["秘密感知", "祈祷"], "hp": 95, "attack": 15, "defense": 5, "speed": 5},
            8: {"name": "窥秘者", "skills": ["秘密感知", "祈祷"], "hp": 145, "attack": 25, "defense": 8, "speed": 6},
            7: {"name": "解谜者", "skills": ["秘密感知", "祈祷"], "hp": 195, "attack": 39, "defense": 12, "speed": 7},
            6: {"name": "密语者", "skills": ["秘密感知", "祈祷"], "hp": 270, "attack": 59, "defense": 18, "speed": 8},
            5: {"name": "秘密守护者", "skills": ["秘密感知", "祈祷"], "hp": 370, "attack": 85, "defense": 25, "speed": 9},
            4: {"name": "神秘学家", "skills": ["秘密感知", "祈祷"], "hp": 490, "attack": 120, "defense": 35, "speed": 10},
            3: {"name": "秘密主宰", "skills": ["秘密感知", "祈祷"], "hp": 690, "attack": 178, "defense": 50, "speed": 12},
            2: {"name": "隐秘使者", "skills": ["秘密感知", "祈祷"], "hp": 990, "attack": 280, "defense": 78, "speed": 15},
            1: {"name": "秘密化身", "skills": ["秘密感知", "祈祷"], "hp": 1470, "attack": 448, "defense": 118, "speed": 18},
            0: {"name": "隐秘之神", "skills": ["秘密感知", "祈祷"], "hp": 2900, "attack": 795, "defense": 195, "speed": 25},
        }
    },
    "命运之轮": {
        "name": "命运之轮途径",
        "god": "命运女神",
        "type": "control",
        "color": (148, 0, 211),  # 紫罗兰
        "desc": "命运与因果之道，操控命运的齿轮",
        "sequences": {
            9: {"name": "赌徒", "skills": ["命运转轮", "因果操控"], "hp": 95, "attack": 15, "defense": 5, "speed": 5},
            8: {"name": "幸运儿", "skills": ["命运转轮", "因果操控"], "hp": 145, "attack": 25, "defense": 8, "speed": 6},
            7: {"name": "命运触手", "skills": ["命运转轮", "因果操控"], "hp": 195, "attack": 39, "defense": 12, "speed": 7},
            6: {"name": "因果编织者", "skills": ["命运转轮", "因果操控"], "hp": 270, "attack": 59, "defense": 18, "speed": 8},
            5: {"name": "命运操手", "skills": ["命运转轮", "因果操控"], "hp": 370, "attack": 85, "defense": 25, "speed": 9},
            4: {"name": "时运大师", "skills": ["命运转轮", "因果操控"], "hp": 490, "attack": 120, "defense": 35, "speed": 10},
            3: {"name": "命运织者", "skills": ["命运转轮", "因果操控"], "hp": 690, "attack": 178, "defense": 50, "speed": 12},
            2: {"name": "因果之主", "skills": ["命运转轮", "因果操控"], "hp": 990, "attack": 280, "defense": 78, "speed": 15},
            1: {"name": "命运化身", "skills": ["命运转轮", "因果操控"], "hp": 1470, "attack": 448, "defense": 118, "speed": 18},
            0: {"name": "命运女神", "skills": ["命运转轮", "因果操控"], "hp": 2900, "attack": 795, "defense": 195, "speed": 25},
        }
    },
    "女巫": {
        "name": "女巫途径",
        "god": "原罪之母",
        "type": "magic",
        "color": (128, 0, 64),  # 暗紫红
        "desc": "诅咒与欲望之道，以情感为武器",
        "sequences": {
            9: {"name": "女巫", "skills": ["魅惑术", "诅咒"], "hp": 90, "attack": 17, "defense": 4, "speed": 5},
            8: {"name": "诱惑者", "skills": ["魅惑术", "诅咒"], "hp": 140, "attack": 27, "defense": 7, "speed": 6},
            7: {"name": "恶魔女", "skills": ["魅惑术", "诅咒"], "hp": 190, "attack": 42, "defense": 10, "speed": 7},
            6: {"name": "欲望主宰", "skills": ["魅惑术", "诅咒"], "hp": 265, "attack": 62, "defense": 15, "speed": 8},
            5: {"name": "诅咒师", "skills": ["魅惑术", "诅咒"], "hp": 365, "attack": 88, "defense": 22, "speed": 9},
            4: {"name": "黑巫", "skills": ["魅惑术", "诅咒"], "hp": 485, "attack": 124, "defense": 32, "speed": 10},
            3: {"name": "原罪之女", "skills": ["魅惑术", "诅咒"], "hp": 680, "attack": 184, "defense": 46, "speed": 12},
            2: {"name": "欲望化身", "skills": ["魅惑术", "诅咒"], "hp": 980, "attack": 288, "defense": 72, "speed": 15},
            1: {"name": "罪恶之母", "skills": ["魅惑术", "诅咒"], "hp": 1450, "attack": 462, "defense": 110, "speed": 18},
            0: {"name": "原罪之母", "skills": ["魅惑术", "诅咒"], "hp": 2850, "attack": 820, "defense": 185, "speed": 25},
        }
    },
}


# 获取途径列表（按类型分组）
def get_pathways_by_type():
    """获取按类型分组的途径"""
    result = {}
    for pathway_id, data in PATHWAYS.items():
        ptype = data["type"]
        if ptype not in result:
            result[ptype] = []
        result[ptype].append((pathway_id, data))
    return result


# 获取所有途径名称列表
def get_pathway_names():
    """获取所有途径名称"""
    return list(PATHWAYS.keys())
