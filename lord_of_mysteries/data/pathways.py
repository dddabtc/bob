"""
途径数据 - 包含已有角色图片的途径
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
    # 占卜家途径技能
    "灵视": {"type": "buff", "cooldown": 10, "duration": 5, "desc": "开启灵视，看穿敌人弱点，增加20%暴击率"},
    "占卜": {"type": "buff", "cooldown": 15, "duration": 3, "desc": "预知危险，短暂无敌"},
    "纸牌投掷": {"type": "projectile", "cooldown": 2, "damage": 25, "desc": "投掷锋利纸牌，远程攻击"},
    "火焰跳跃": {"type": "dash", "cooldown": 8, "damage": 40, "desc": "化为火焰瞬移，对路径敌人造成伤害"},
    "空气炮": {"type": "projectile", "cooldown": 5, "damage": 60, "desc": "压缩空气形成炮弹"},
    "易容": {"type": "buff", "cooldown": 30, "duration": 10, "desc": "改变外貌，敌人不会主动攻击"},
    # 隐者途径技能
    "偷窃": {"type": "buff", "cooldown": 8, "duration": 0, "desc": "偷取敌人的物品或能力"},
    "闪现": {"type": "dash", "cooldown": 5, "damage": 0, "desc": "瞬间移动到目标位置"},
    "隐匿": {"type": "buff", "cooldown": 20, "duration": 8, "desc": "进入隐身状态"},
    # 观众途径技能
    "读心": {"type": "buff", "cooldown": 12, "duration": 6, "desc": "读取敌人意图，预判攻击"},
    "催眠": {"type": "control", "cooldown": 15, "duration": 4, "desc": "催眠敌人使其停止行动"},
    "心灵冲击": {"type": "projectile", "cooldown": 6, "damage": 45, "desc": "精神攻击造成伤害"},
    # 读者途径技能
    "博学": {"type": "buff", "cooldown": 0, "duration": 0, "desc": "被动提升所有属性"},
    "考古": {"type": "buff", "cooldown": 25, "duration": 10, "desc": "分析敌人弱点，增加伤害"},
    "知识投射": {"type": "projectile", "cooldown": 4, "damage": 35, "desc": "将知识化为攻击"},
    # 黑夜途径技能
    "暗影步": {"type": "dash", "cooldown": 6, "damage": 30, "desc": "在阴影中穿行"},
    "黑暗笼罩": {"type": "control", "cooldown": 18, "duration": 5, "desc": "制造黑暗区域"},
    "暗影刺杀": {"type": "projectile", "cooldown": 3, "damage": 50, "desc": "暗影形成的利刃"},
    # 死神途径技能
    "亡灵召唤": {"type": "summon", "cooldown": 20, "duration": 15, "desc": "召唤亡灵助战"},
    "死亡凝视": {"type": "projectile", "cooldown": 10, "damage": 80, "desc": "死亡的目光"},
    "灵魂收割": {"type": "buff", "cooldown": 25, "duration": 0, "desc": "收割敌人灵魂恢复生命"},
    # 红祭司途径技能
    "神圣之光": {"type": "projectile", "cooldown": 5, "damage": 40, "desc": "释放神圣光芒"},
    "治愈祷言": {"type": "heal", "cooldown": 15, "heal": 50, "desc": "治愈自身伤势"},
    "惩戒": {"type": "projectile", "cooldown": 8, "damage": 60, "desc": "神圣惩戒攻击"},
    # 水手途径技能
    "风暴召唤": {"type": "projectile", "cooldown": 12, "damage": 55, "desc": "召唤风暴攻击"},
    "水流操控": {"type": "control", "cooldown": 10, "duration": 4, "desc": "操控水流束缚敌人"},
    "闪电链": {"type": "projectile", "cooldown": 7, "damage": 45, "desc": "释放闪电链"},
    # 巨人途径技能
    "狂暴": {"type": "buff", "cooldown": 20, "duration": 10, "desc": "进入狂暴状态，攻击大幅提升"},
    "重击": {"type": "melee", "cooldown": 4, "damage": 70, "desc": "强力重击"},
    "地震": {"type": "projectile", "cooldown": 15, "damage": 50, "desc": "震击地面造成范围伤害"},
    # 吟游诗人途径技能
    "战歌": {"type": "buff", "cooldown": 18, "duration": 12, "desc": "演奏战歌提升属性"},
    "音波攻击": {"type": "projectile", "cooldown": 5, "damage": 35, "desc": "音波造成伤害"},
    "魅惑之歌": {"type": "control", "cooldown": 20, "duration": 5, "desc": "魅惑敌人"},
    # 学徒途径技能
    "火球术": {"type": "projectile", "cooldown": 4, "damage": 45, "desc": "释放火球"},
    "冰锥术": {"type": "projectile", "cooldown": 5, "damage": 40, "desc": "释放冰锥"},
    "魔法护盾": {"type": "buff", "cooldown": 15, "duration": 8, "desc": "生成魔法护盾"},
}

# 途径数据
PATHWAYS = {
    "占卜家": {
        "name": "占卜家途径",
        "god": "愚者",
        "type": "magic",
        "color": (218, 165, 32),  # 金色
        "desc": "占卜与欺诈之道，掌控命运的丝线",
        "sequences": {
            9: {"name": "占卜家", "skills": ["灵视", "占卜"], "hp": 100, "attack": 15, "defense": 5, "speed": 5},
            8: {"name": "小丑", "skills": ["灵视", "占卜", "纸牌投掷"], "hp": 150, "attack": 25, "defense": 8, "speed": 6},
            7: {"name": "魔术师", "skills": ["灵视", "占卜", "纸牌投掷", "火焰跳跃"], "hp": 200, "attack": 40, "defense": 12, "speed": 7},
            6: {"name": "无面人", "skills": ["灵视", "占卜", "纸牌投掷", "火焰跳跃", "易容"], "hp": 280, "attack": 60, "defense": 18, "speed": 8},
            5: {"name": "秘偶大师", "skills": ["灵视", "占卜", "纸牌投掷", "火焰跳跃", "易容", "空气炮"], "hp": 380, "attack": 85, "defense": 25, "speed": 9},
            4: {"name": "诡法师", "skills": ["灵视", "占卜", "纸牌投掷", "火焰跳跃", "易容", "空气炮"], "hp": 500, "attack": 120, "defense": 35, "speed": 10},
            3: {"name": "古代学者", "skills": ["灵视", "占卜", "纸牌投掷", "火焰跳跃", "易容", "空气炮"], "hp": 700, "attack": 180, "defense": 50, "speed": 12},
            2: {"name": "奇迹师", "skills": ["灵视", "占卜", "纸牌投掷", "火焰跳跃", "易容", "空气炮"], "hp": 1000, "attack": 280, "defense": 80, "speed": 15},
            1: {"name": "诡秘侍者", "skills": ["灵视", "占卜", "纸牌投掷", "火焰跳跃", "易容", "空气炮"], "hp": 1500, "attack": 450, "defense": 120, "speed": 18},
            0: {"name": "愚者", "skills": ["灵视", "占卜", "纸牌投掷", "火焰跳跃", "易容", "空气炮"], "hp": 3000, "attack": 800, "defense": 200, "speed": 25},
        }
    },
    "隐者": {
        "name": "隐者途径",
        "god": "隐秘者",
        "type": "special",
        "color": (128, 0, 128),  # 紫色
        "desc": "隐秘与窃取之道，在暗影中行动",
        "sequences": {
            9: {"name": "窃贼", "skills": ["偷窃", "闪现"], "hp": 90, "attack": 18, "defense": 4, "speed": 7},
            8: {"name": "纵火者", "skills": ["偷窃", "闪现", "隐匿"], "hp": 140, "attack": 28, "defense": 7, "speed": 8},
            7: {"name": "旅行家", "skills": ["偷窃", "闪现", "隐匿"], "hp": 190, "attack": 42, "defense": 10, "speed": 9},
            6: {"name": "探案者", "skills": ["偷窃", "闪现", "隐匿"], "hp": 260, "attack": 62, "defense": 15, "speed": 10},
            5: {"name": "掠夺者", "skills": ["偷窃", "闪现", "隐匿"], "hp": 350, "attack": 88, "defense": 22, "speed": 11},
            4: {"name": "万象之门", "skills": ["偷窃", "闪现", "隐匿"], "hp": 480, "attack": 125, "defense": 32, "speed": 13},
            3: {"name": "寄生者", "skills": ["偷窃", "闪现", "隐匿"], "hp": 680, "attack": 185, "defense": 48, "speed": 15},
            2: {"name": "偷盗者", "skills": ["偷窃", "闪现", "隐匿"], "hp": 980, "attack": 290, "defense": 75, "speed": 18},
            1: {"name": "错误", "skills": ["偷窃", "闪现", "隐匿"], "hp": 1450, "attack": 460, "defense": 115, "speed": 22},
            0: {"name": "隐秘者", "skills": ["偷窃", "闪现", "隐匿"], "hp": 2800, "attack": 820, "defense": 190, "speed": 28},
        }
    },
    "观众": {
        "name": "观众途径",
        "god": "隐秘者",
        "type": "control",
        "color": (75, 0, 130),  # 靛蓝色
        "desc": "心灵与操控之道，窥探他人思想",
        "sequences": {
            9: {"name": "观众", "skills": ["读心", "心灵冲击"], "hp": 95, "attack": 16, "defense": 5, "speed": 5},
            8: {"name": "感知者", "skills": ["读心", "心灵冲击", "催眠"], "hp": 145, "attack": 26, "defense": 8, "speed": 6},
            7: {"name": "催眠师", "skills": ["读心", "心灵冲击", "催眠"], "hp": 195, "attack": 40, "defense": 12, "speed": 7},
            6: {"name": "操纵者", "skills": ["读心", "心灵冲击", "催眠"], "hp": 270, "attack": 60, "defense": 18, "speed": 8},
            5: {"name": "黑暗主宰", "skills": ["读心", "心灵冲击", "催眠"], "hp": 370, "attack": 86, "defense": 25, "speed": 9},
            4: {"name": "傀儡", "skills": ["读心", "心灵冲击", "催眠"], "hp": 490, "attack": 122, "defense": 35, "speed": 10},
            3: {"name": "幽影之王", "skills": ["读心", "心灵冲击", "催眠"], "hp": 690, "attack": 182, "defense": 50, "speed": 12},
            2: {"name": "蝇王", "skills": ["读心", "心灵冲击", "催眠"], "hp": 990, "attack": 285, "defense": 78, "speed": 15},
            1: {"name": "心理病医师", "skills": ["读心", "心灵冲击", "催眠"], "hp": 1480, "attack": 455, "defense": 118, "speed": 18},
            0: {"name": "隐秘者", "skills": ["读心", "心灵冲击", "催眠"], "hp": 2900, "attack": 810, "defense": 195, "speed": 25},
        }
    },
    "读者": {
        "name": "读者途径",
        "god": "智慧之神",
        "type": "wisdom",
        "color": (70, 130, 180),  # 钢蓝色
        "desc": "知识与博学之道，以学识为武器",
        "sequences": {
            9: {"name": "读者", "skills": ["博学", "知识投射"], "hp": 100, "attack": 14, "defense": 6, "speed": 4},
            8: {"name": "博学家", "skills": ["博学", "知识投射", "考古"], "hp": 155, "attack": 24, "defense": 9, "speed": 5},
            7: {"name": "考古学家", "skills": ["博学", "知识投射", "考古"], "hp": 210, "attack": 38, "defense": 14, "speed": 6},
            6: {"name": "鉴定师", "skills": ["博学", "知识投射", "考古"], "hp": 290, "attack": 58, "defense": 20, "speed": 7},
            5: {"name": "博物学家", "skills": ["博学", "知识投射", "考古"], "hp": 400, "attack": 84, "defense": 28, "speed": 8},
            4: {"name": "秘修士", "skills": ["博学", "知识投射", "考古"], "hp": 530, "attack": 118, "defense": 38, "speed": 9},
            3: {"name": "圣贤", "skills": ["博学", "知识投射", "考古"], "hp": 740, "attack": 175, "defense": 55, "speed": 11},
            2: {"name": "智者", "skills": ["博学", "知识投射", "考古"], "hp": 1050, "attack": 275, "defense": 85, "speed": 14},
            1: {"name": "真知者", "skills": ["博学", "知识投射", "考古"], "hp": 1550, "attack": 440, "defense": 125, "speed": 17},
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
            9: {"name": "暗夜行者", "skills": ["暗影步", "暗影刺杀"], "hp": 95, "attack": 17, "defense": 5, "speed": 6},
            8: {"name": "秘祈人", "skills": ["暗影步", "暗影刺杀", "黑暗笼罩"], "hp": 145, "attack": 27, "defense": 8, "speed": 7},
            7: {"name": "黑夜眼", "skills": ["暗影步", "暗影刺杀", "黑暗笼罩"], "hp": 195, "attack": 42, "defense": 12, "speed": 8},
            6: {"name": "噩梦编织者", "skills": ["暗影步", "暗影刺杀", "黑暗笼罩"], "hp": 270, "attack": 62, "defense": 17, "speed": 9},
            5: {"name": "隐影", "skills": ["暗影步", "暗影刺杀", "黑暗笼罩"], "hp": 370, "attack": 88, "defense": 24, "speed": 10},
            4: {"name": "僵尸之亲", "skills": ["暗影步", "暗影刺杀", "黑暗笼罩"], "hp": 490, "attack": 124, "defense": 34, "speed": 12},
            3: {"name": "薄暮之王", "skills": ["暗影步", "暗影刺杀", "黑暗笼罩"], "hp": 690, "attack": 184, "defense": 49, "speed": 14},
            2: {"name": "暗影之王", "skills": ["暗影步", "暗影刺杀", "黑暗笼罩"], "hp": 990, "attack": 288, "defense": 77, "speed": 17},
            1: {"name": "黑暗天使", "skills": ["暗影步", "暗影刺杀", "黑暗笼罩"], "hp": 1470, "attack": 458, "defense": 117, "speed": 21},
            0: {"name": "永夜女神", "skills": ["暗影步", "暗影刺杀", "黑暗笼罩"], "hp": 2850, "attack": 815, "defense": 192, "speed": 27},
        }
    },
    "死神": {
        "name": "死神途径",
        "god": "死神",
        "type": "magic",
        "color": (47, 79, 79),  # 暗石板灰
        "desc": "死亡与灵魂之道，掌控生死轮回",
        "sequences": {
            9: {"name": "殡葬师", "skills": ["亡灵召唤", "死亡凝视"], "hp": 105, "attack": 16, "defense": 6, "speed": 4},
            8: {"name": "掘墓人", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 160, "attack": 26, "defense": 9, "speed": 5},
            7: {"name": "灵巫", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 215, "attack": 40, "defense": 13, "speed": 6},
            6: {"name": "亡灵法师", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 295, "attack": 60, "defense": 19, "speed": 7},
            5: {"name": "尸王", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 405, "attack": 86, "defense": 27, "speed": 8},
            4: {"name": "冥界吟游诗人", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 535, "attack": 120, "defense": 37, "speed": 9},
            3: {"name": "死亡执政官", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 745, "attack": 178, "defense": 53, "speed": 11},
            2: {"name": "死神代行者", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 1060, "attack": 278, "defense": 82, "speed": 14},
            1: {"name": "苍白死神", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 1560, "attack": 445, "defense": 122, "speed": 17},
            0: {"name": "死神", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 3050, "attack": 790, "defense": 205, "speed": 24},
        }
    },
    "红祭司": {
        "name": "红祭司途径",
        "god": "永恒烈阳",
        "type": "support",
        "color": (220, 20, 60),  # 猩红色
        "desc": "神圣与治愈之道，以信仰为力量",
        "sequences": {
            9: {"name": "红祭司", "skills": ["神圣之光", "治愈祷言"], "hp": 110, "attack": 14, "defense": 7, "speed": 4},
            8: {"name": "牧师", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 165, "attack": 24, "defense": 10, "speed": 5},
            7: {"name": "圣职者", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 220, "attack": 38, "defense": 15, "speed": 6},
            6: {"name": "审判官", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 300, "attack": 58, "defense": 22, "speed": 7},
            5: {"name": "裁决", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 410, "attack": 84, "defense": 30, "speed": 8},
            4: {"name": "神卫", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 540, "attack": 118, "defense": 40, "speed": 9},
            3: {"name": "战天使", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 750, "attack": 176, "defense": 58, "speed": 11},
            2: {"name": "圣光骑士", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 1070, "attack": 276, "defense": 88, "speed": 14},
            1: {"name": "天使之王", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 1570, "attack": 442, "defense": 128, "speed": 17},
            0: {"name": "永恒烈阳", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 3150, "attack": 785, "defense": 215, "speed": 24},
        }
    },
    "水手": {
        "name": "水手途径",
        "god": "风暴之主",
        "type": "magic",
        "color": (0, 105, 148),  # 深海蓝
        "desc": "风暴与海洋之道，驾驭自然之力",
        "sequences": {
            9: {"name": "水手", "skills": ["风暴召唤", "水流操控"], "hp": 100, "attack": 16, "defense": 5, "speed": 5},
            8: {"name": "航海士", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 155, "attack": 26, "defense": 8, "speed": 6},
            7: {"name": "海盗", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 210, "attack": 40, "defense": 12, "speed": 7},
            6: {"name": "冒险者", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 290, "attack": 60, "defense": 18, "speed": 8},
            5: {"name": "海王", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 400, "attack": 86, "defense": 25, "speed": 9},
            4: {"name": "潮汐掌控者", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 530, "attack": 122, "defense": 35, "speed": 10},
            3: {"name": "风暴使者", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 740, "attack": 182, "defense": 50, "speed": 12},
            2: {"name": "海神代理", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 1050, "attack": 285, "defense": 78, "speed": 15},
            1: {"name": "神风使者", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 1550, "attack": 455, "defense": 118, "speed": 18},
            0: {"name": "风暴之主", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 3100, "attack": 810, "defense": 195, "speed": 25},
        }
    },
    "巨人": {
        "name": "巨人途径",
        "god": "战争之神",
        "type": "melee",
        "color": (139, 69, 19),  # 鞍褐色
        "desc": "力量与战斗之道，以蛮力压制敌人",
        "sequences": {
            9: {"name": "战士", "skills": ["狂暴", "重击"], "hp": 130, "attack": 18, "defense": 8, "speed": 3},
            8: {"name": "角斗士", "skills": ["狂暴", "重击", "地震"], "hp": 195, "attack": 30, "defense": 12, "speed": 4},
            7: {"name": "武器大师", "skills": ["狂暴", "重击", "地震"], "hp": 260, "attack": 46, "defense": 18, "speed": 5},
            6: {"name": "黎明骑士", "skills": ["狂暴", "重击", "地震"], "hp": 350, "attack": 68, "defense": 26, "speed": 6},
            5: {"name": "白银骑士", "skills": ["狂暴", "重击", "地震"], "hp": 470, "attack": 96, "defense": 36, "speed": 7},
            4: {"name": "黄金骑士", "skills": ["狂暴", "重击", "地震"], "hp": 620, "attack": 135, "defense": 48, "speed": 8},
            3: {"name": "荣耀之星", "skills": ["狂暴", "重击", "地震"], "hp": 860, "attack": 200, "defense": 68, "speed": 9},
            2: {"name": "神之武器", "skills": ["狂暴", "重击", "地震"], "hp": 1220, "attack": 310, "defense": 100, "speed": 11},
            1: {"name": "战争骑士", "skills": ["狂暴", "重击", "地震"], "hp": 1800, "attack": 495, "defense": 145, "speed": 14},
            0: {"name": "战争之神", "skills": ["狂暴", "重击", "地震"], "hp": 3500, "attack": 880, "defense": 240, "speed": 20},
        }
    },
    "吟游诗人": {
        "name": "吟游诗人途径",
        "god": "命运女神",
        "type": "support",
        "color": (255, 182, 193),  # 浅粉色
        "desc": "音乐与祝福之道，以歌声改变命运",
        "sequences": {
            9: {"name": "吟游诗人", "skills": ["战歌", "音波攻击"], "hp": 95, "attack": 14, "defense": 5, "speed": 5},
            8: {"name": "乐手", "skills": ["战歌", "音波攻击", "魅惑之歌"], "hp": 145, "attack": 24, "defense": 8, "speed": 6},
            7: {"name": "舞者", "skills": ["战歌", "音波攻击", "魅惑之歌"], "hp": 195, "attack": 38, "defense": 12, "speed": 7},
            6: {"name": "祝福师", "skills": ["战歌", "音波攻击", "魅惑之歌"], "hp": 270, "attack": 58, "defense": 18, "speed": 8},
            5: {"name": "幸运者", "skills": ["战歌", "音波攻击", "魅惑之歌"], "hp": 370, "attack": 84, "defense": 25, "speed": 9},
            4: {"name": "灾难祭司", "skills": ["战歌", "音波攻击", "魅惑之歌"], "hp": 490, "attack": 118, "defense": 35, "speed": 10},
            3: {"name": "命运木偶师", "skills": ["战歌", "音波攻击", "魅惑之歌"], "hp": 690, "attack": 175, "defense": 50, "speed": 12},
            2: {"name": "幸运之子", "skills": ["战歌", "音波攻击", "魅惑之歌"], "hp": 990, "attack": 275, "defense": 78, "speed": 15},
            1: {"name": "命运掌控者", "skills": ["战歌", "音波攻击", "魅惑之歌"], "hp": 1470, "attack": 440, "defense": 118, "speed": 18},
            0: {"name": "命运女神", "skills": ["战歌", "音波攻击", "魅惑之歌"], "hp": 2900, "attack": 780, "defense": 195, "speed": 25},
        }
    },
    "学徒": {
        "name": "学徒途径",
        "god": "知识之神",
        "type": "magic",
        "color": (65, 105, 225),  # 皇家蓝
        "desc": "魔法与元素之道，以知识驾驭魔力",
        "sequences": {
            9: {"name": "学徒", "skills": ["火球术", "冰锥术"], "hp": 90, "attack": 18, "defense": 4, "speed": 4},
            8: {"name": "巫师", "skills": ["火球术", "冰锥术", "魔法护盾"], "hp": 140, "attack": 28, "defense": 7, "speed": 5},
            7: {"name": "法师", "skills": ["火球术", "冰锥术", "魔法护盾"], "hp": 190, "attack": 44, "defense": 10, "speed": 6},
            6: {"name": "星术师", "skills": ["火球术", "冰锥术", "魔法护盾"], "hp": 265, "attack": 65, "defense": 15, "speed": 7},
            5: {"name": "占星师", "skills": ["火球术", "冰锥术", "魔法护盾"], "hp": 365, "attack": 92, "defense": 22, "speed": 8},
            4: {"name": "秘法师", "skills": ["火球术", "冰锥术", "魔法护盾"], "hp": 485, "attack": 130, "defense": 32, "speed": 9},
            3: {"name": "贤者", "skills": ["火球术", "冰锥术", "魔法护盾"], "hp": 680, "attack": 192, "defense": 46, "speed": 11},
            2: {"name": "先知", "skills": ["火球术", "冰锥术", "魔法护盾"], "hp": 980, "attack": 300, "defense": 72, "speed": 14},
            1: {"name": "神谕者", "skills": ["火球术", "冰锥术", "魔法护盾"], "hp": 1450, "attack": 475, "defense": 110, "speed": 17},
            0: {"name": "知识之神", "skills": ["火球术", "冰锥术", "魔法护盾"], "hp": 2850, "attack": 845, "defense": 185, "speed": 24},
        }
    },
    "深渊": {
        "name": "深渊途径",
        "god": "真实造物主",
        "type": "magic",
        "color": (20, 20, 60),  # 深蓝黑
        "desc": "深渊与毁灭之道，掌控黑暗力量",
        "sequences": {
            9: {"name": "深渊追随者", "skills": ["深渊凝视", "黑暗侵蚀"], "hp": 100, "attack": 20, "defense": 4, "speed": 4},
            8: {"name": "深渊信徒", "skills": ["深渊凝视", "黑暗侵蚀"], "hp": 155, "attack": 32, "defense": 7, "speed": 5},
            7: {"name": "深渊行者", "skills": ["深渊凝视", "黑暗侵蚀"], "hp": 210, "attack": 48, "defense": 11, "speed": 6},
            6: {"name": "深渊使者", "skills": ["深渊凝视", "黑暗侵蚀"], "hp": 290, "attack": 70, "defense": 16, "speed": 7},
            5: {"name": "深渊主宰", "skills": ["深渊凝视", "黑暗侵蚀"], "hp": 400, "attack": 98, "defense": 24, "speed": 8},
            4: {"name": "虚空行者", "skills": ["深渊凝视", "黑暗侵蚀"], "hp": 530, "attack": 138, "defense": 34, "speed": 9},
            3: {"name": "毁灭者", "skills": ["深渊凝视", "黑暗侵蚀"], "hp": 740, "attack": 205, "defense": 50, "speed": 11},
            2: {"name": "末日使者", "skills": ["深渊凝视", "黑暗侵蚀"], "hp": 1060, "attack": 320, "defense": 78, "speed": 14},
            1: {"name": "深渊之王", "skills": ["深渊凝视", "黑暗侵蚀"], "hp": 1560, "attack": 510, "defense": 118, "speed": 17},
            0: {"name": "真实造物主", "skills": ["深渊凝视", "黑暗侵蚀"], "hp": 3200, "attack": 900, "defense": 200, "speed": 24},
        }
    },
    "黑皇帝": {
        "name": "黑皇帝途径",
        "god": "黑皇帝",
        "type": "control",
        "color": (30, 30, 30),  # 纯黑
        "desc": "权谋与统治之道，以黑暗手段掌控一切",
        "sequences": {
            9: {"name": "律师", "skills": ["威压", "契约"], "hp": 105, "attack": 14, "defense": 6, "speed": 5},
            8: {"name": "野心家", "skills": ["威压", "契约"], "hp": 160, "attack": 24, "defense": 9, "speed": 6},
            7: {"name": "谋士", "skills": ["威压", "契约"], "hp": 215, "attack": 38, "defense": 14, "speed": 7},
            6: {"name": "幕后黑手", "skills": ["威压", "契约"], "hp": 295, "attack": 58, "defense": 20, "speed": 8},
            5: {"name": "野心执政官", "skills": ["威压", "契约"], "hp": 405, "attack": 84, "defense": 28, "speed": 9},
            4: {"name": "独裁者", "skills": ["威压", "契约"], "hp": 535, "attack": 118, "defense": 38, "speed": 10},
            3: {"name": "魔鬼", "skills": ["威压", "契约"], "hp": 745, "attack": 176, "defense": 55, "speed": 12},
            2: {"name": "契约之王", "skills": ["威压", "契约"], "hp": 1060, "attack": 276, "defense": 85, "speed": 15},
            1: {"name": "暗帝", "skills": ["威压", "契约"], "hp": 1560, "attack": 442, "defense": 125, "speed": 18},
            0: {"name": "黑皇帝", "skills": ["威压", "契约"], "hp": 3150, "attack": 785, "defense": 210, "speed": 25},
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
    "隐士": {
        "name": "隐士途径",
        "god": "隐士",
        "type": "wisdom",
        "color": (139, 119, 101),  # 灰褐色
        "desc": "隐居与洞察之道，在孤独中寻找真理",
        "sequences": {
            9: {"name": "隐士", "skills": ["洞察", "冥想"], "hp": 95, "attack": 14, "defense": 5, "speed": 4},
            8: {"name": "苦行者", "skills": ["洞察", "冥想"], "hp": 145, "attack": 24, "defense": 8, "speed": 5},
            7: {"name": "修行者", "skills": ["洞察", "冥想"], "hp": 195, "attack": 38, "defense": 12, "speed": 6},
            6: {"name": "悟道者", "skills": ["洞察", "冥想"], "hp": 270, "attack": 58, "defense": 18, "speed": 7},
            5: {"name": "真人", "skills": ["洞察", "冥想"], "hp": 370, "attack": 84, "defense": 25, "speed": 8},
            4: {"name": "圣人", "skills": ["洞察", "冥想"], "hp": 490, "attack": 118, "defense": 35, "speed": 9},
            3: {"name": "天人", "skills": ["洞察", "冥想"], "hp": 690, "attack": 176, "defense": 50, "speed": 11},
            2: {"name": "超脱者", "skills": ["洞察", "冥想"], "hp": 990, "attack": 276, "defense": 78, "speed": 14},
            1: {"name": "至高隐士", "skills": ["洞察", "冥想"], "hp": 1470, "attack": 442, "defense": 118, "speed": 17},
            0: {"name": "隐士", "skills": ["洞察", "冥想"], "hp": 2900, "attack": 785, "defense": 195, "speed": 24},
        }
    },
    "审判官": {
        "name": "审判官途径",
        "god": "审判之神",
        "type": "melee",
        "color": (192, 192, 192),  # 银色
        "desc": "审判与正义之道，以神圣之力惩戒邪恶",
        "sequences": {
            9: {"name": "审判官", "skills": ["神圣审判", "正义之锤"], "hp": 115, "attack": 16, "defense": 8, "speed": 4},
            8: {"name": "裁决者", "skills": ["神圣审判", "正义之锤"], "hp": 175, "attack": 26, "defense": 12, "speed": 5},
            7: {"name": "执法者", "skills": ["神圣审判", "正义之锤"], "hp": 235, "attack": 40, "defense": 18, "speed": 6},
            6: {"name": "圣裁骑士", "skills": ["神圣审判", "正义之锤"], "hp": 320, "attack": 60, "defense": 26, "speed": 7},
            5: {"name": "审判长", "skills": ["神圣审判", "正义之锤"], "hp": 435, "attack": 86, "defense": 36, "speed": 8},
            4: {"name": "正义执行者", "skills": ["神圣审判", "正义之锤"], "hp": 575, "attack": 120, "defense": 48, "speed": 9},
            3: {"name": "天罚使者", "skills": ["神圣审判", "正义之锤"], "hp": 800, "attack": 180, "defense": 68, "speed": 10},
            2: {"name": "审判天使", "skills": ["神圣审判", "正义之锤"], "hp": 1150, "attack": 280, "defense": 100, "speed": 12},
            1: {"name": "至高审判者", "skills": ["神圣审判", "正义之锤"], "hp": 1700, "attack": 450, "defense": 145, "speed": 15},
            0: {"name": "审判之神", "skills": ["神圣审判", "正义之锤"], "hp": 3400, "attack": 800, "defense": 240, "speed": 22},
        }
    },
    "月亮": {
        "name": "月亮途径",
        "god": "月之女神",
        "type": "magic",
        "color": (200, 200, 230),  # 月白色
        "desc": "月光与变化之道，借月之力量转化形态",
        "sequences": {
            9: {"name": "月亮侍者", "skills": ["月光祝福", "月影步"], "hp": 95, "attack": 16, "defense": 5, "speed": 6},
            8: {"name": "银月骑士", "skills": ["月光祝福", "月影步"], "hp": 145, "attack": 26, "defense": 8, "speed": 7},
            7: {"name": "月影", "skills": ["月光祝福", "月影步"], "hp": 195, "attack": 40, "defense": 12, "speed": 8},
            6: {"name": "月之猎手", "skills": ["月光祝福", "月影步"], "hp": 270, "attack": 60, "defense": 18, "speed": 9},
            5: {"name": "银月使者", "skills": ["月光祝福", "月影步"], "hp": 370, "attack": 86, "defense": 25, "speed": 10},
            4: {"name": "月之牧师", "skills": ["月光祝福", "月影步"], "hp": 490, "attack": 122, "defense": 35, "speed": 12},
            3: {"name": "月之骑士", "skills": ["月光祝福", "月影步"], "hp": 690, "attack": 182, "defense": 50, "speed": 14},
            2: {"name": "银月圣女", "skills": ["月光祝福", "月影步"], "hp": 990, "attack": 285, "defense": 78, "speed": 17},
            1: {"name": "月之化身", "skills": ["月光祝福", "月影步"], "hp": 1470, "attack": 455, "defense": 118, "speed": 21},
            0: {"name": "月之女神", "skills": ["月光祝福", "月影步"], "hp": 2900, "attack": 810, "defense": 195, "speed": 28},
        }
    },
    "母亲": {
        "name": "母亲途径",
        "god": "大地之母",
        "type": "support",
        "color": (139, 90, 43),  # 大地棕
        "desc": "生命与大地之道，孕育万物的力量",
        "sequences": {
            9: {"name": "大地之子", "skills": ["大地祝福", "生命治愈"], "hp": 120, "attack": 12, "defense": 8, "speed": 4},
            8: {"name": "农夫", "skills": ["大地祝福", "生命治愈"], "hp": 180, "attack": 20, "defense": 12, "speed": 5},
            7: {"name": "德鲁伊", "skills": ["大地祝福", "生命治愈"], "hp": 240, "attack": 32, "defense": 18, "speed": 6},
            6: {"name": "自然守卫", "skills": ["大地祝福", "生命治愈"], "hp": 330, "attack": 48, "defense": 26, "speed": 7},
            5: {"name": "生命导师", "skills": ["大地祝福", "生命治愈"], "hp": 450, "attack": 70, "defense": 36, "speed": 8},
            4: {"name": "大地之心", "skills": ["大地祝福", "生命治愈"], "hp": 600, "attack": 100, "defense": 48, "speed": 9},
            3: {"name": "万物之母", "skills": ["大地祝福", "生命治愈"], "hp": 840, "attack": 150, "defense": 68, "speed": 10},
            2: {"name": "生命源泉", "skills": ["大地祝福", "生命治愈"], "hp": 1200, "attack": 235, "defense": 100, "speed": 12},
            1: {"name": "大地化身", "skills": ["大地祝福", "生命治愈"], "hp": 1780, "attack": 375, "defense": 145, "speed": 15},
            0: {"name": "大地之母", "skills": ["大地祝福", "生命治愈"], "hp": 3600, "attack": 670, "defense": 250, "speed": 22},
        }
    },
    "完美者": {
        "name": "完美者途径",
        "god": "完美之神",
        "type": "special",
        "color": (255, 215, 0),  # 金色
        "desc": "完美与极致之道，追求绝对的完美",
        "sequences": {
            9: {"name": "完美主义者", "skills": ["精确打击", "完美防御"], "hp": 100, "attack": 16, "defense": 6, "speed": 5},
            8: {"name": "艺术家", "skills": ["精确打击", "完美防御"], "hp": 155, "attack": 26, "defense": 9, "speed": 6},
            7: {"name": "大师", "skills": ["精确打击", "完美防御"], "hp": 210, "attack": 40, "defense": 14, "speed": 7},
            6: {"name": "宗师", "skills": ["精确打击", "完美防御"], "hp": 290, "attack": 60, "defense": 20, "speed": 8},
            5: {"name": "完美战士", "skills": ["精确打击", "完美防御"], "hp": 400, "attack": 86, "defense": 28, "speed": 9},
            4: {"name": "无瑕者", "skills": ["精确打击", "完美防御"], "hp": 530, "attack": 122, "defense": 38, "speed": 10},
            3: {"name": "完美化身", "skills": ["精确打击", "完美防御"], "hp": 740, "attack": 182, "defense": 55, "speed": 12},
            2: {"name": "至臻者", "skills": ["精确打击", "完美防御"], "hp": 1060, "attack": 285, "defense": 85, "speed": 15},
            1: {"name": "完美使者", "skills": ["精确打击", "完美防御"], "hp": 1560, "attack": 455, "defense": 125, "speed": 18},
            0: {"name": "完美之神", "skills": ["精确打击", "完美防御"], "hp": 3150, "attack": 810, "defense": 210, "speed": 25},
        }
    },
    "命运之轮": {
        "name": "命运之轮途径",
        "god": "命运女神",
        "type": "control",
        "color": (148, 0, 211),  # 紫罗兰
        "desc": "命运与因果之道，操控命运的齿轮",
        "sequences": {
            9: {"name": "幸运儿", "skills": ["命运转轮", "因果操控"], "hp": 95, "attack": 15, "defense": 5, "speed": 5},
            8: {"name": "赌徒", "skills": ["命运转轮", "因果操控"], "hp": 145, "attack": 25, "defense": 8, "speed": 6},
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
