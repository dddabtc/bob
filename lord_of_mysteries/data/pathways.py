"""
途径数据 - 基于《诡秘之主》的22条途径
根据序列.xlsx正确数据生成
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
    # 学徒途径技能
    "戏法": {"type": "projectile", "cooldown": 3, "damage": 30, "desc": "释放魔法戏法"},
    "星象": {"type": "buff", "cooldown": 20, "duration": 10, "desc": "观测星象获得加成"},
    "传送": {"type": "dash", "cooldown": 12, "damage": 0, "desc": "短距离传送"},
    # 偷盗者途径技能
    "偷窃": {"type": "buff", "cooldown": 8, "duration": 0, "desc": "偷取敌人的物品或能力"},
    "闪现": {"type": "dash", "cooldown": 5, "damage": 0, "desc": "瞬间移动到目标位置"},
    "解密": {"type": "buff", "cooldown": 15, "duration": 8, "desc": "解密敌人弱点"},
    # 观众途径技能
    "读心": {"type": "buff", "cooldown": 12, "duration": 6, "desc": "读取敌人意图，预判攻击"},
    "催眠": {"type": "control", "cooldown": 15, "duration": 4, "desc": "催眠敌人使其停止行动"},
    "心灵冲击": {"type": "projectile", "cooldown": 6, "damage": 45, "desc": "精神攻击造成伤害"},
    "梦境入侵": {"type": "control", "cooldown": 20, "duration": 6, "desc": "入侵敌人梦境使其混乱"},
    # 秘祈人途径技能
    "祈祷": {"type": "heal", "cooldown": 20, "heal": 60, "desc": "向神明祈祷获得治愈"},
    "倾听": {"type": "buff", "cooldown": 15, "duration": 10, "desc": "倾听秘密获得情报"},
    "秘密感知": {"type": "buff", "cooldown": 12, "duration": 10, "desc": "感知隐藏的秘密"},
    # 歌颂者途径技能
    "神圣之光": {"type": "projectile", "cooldown": 5, "damage": 40, "desc": "释放神圣光芒"},
    "治愈祷言": {"type": "heal", "cooldown": 15, "heal": 50, "desc": "治愈自身伤势"},
    "惩戒": {"type": "projectile", "cooldown": 8, "damage": 60, "desc": "神圣惩戒攻击"},
    # 水手途径技能
    "风暴召唤": {"type": "projectile", "cooldown": 12, "damage": 55, "desc": "召唤风暴攻击"},
    "水流操控": {"type": "control", "cooldown": 10, "duration": 4, "desc": "操控水流束缚敌人"},
    "闪电链": {"type": "projectile", "cooldown": 7, "damage": 45, "desc": "释放闪电链"},
    # 阅读者途径技能
    "博学": {"type": "buff", "cooldown": 0, "duration": 0, "desc": "被动提升所有属性"},
    "知识投射": {"type": "projectile", "cooldown": 4, "damage": 35, "desc": "将知识化为攻击"},
    "考古": {"type": "buff", "cooldown": 25, "duration": 10, "desc": "分析敌人弱点，增加伤害"},
    # 不眠者途径技能
    "暗影步": {"type": "dash", "cooldown": 6, "damage": 30, "desc": "在阴影中穿行"},
    "黑暗笼罩": {"type": "control", "cooldown": 18, "duration": 5, "desc": "制造黑暗区域"},
    "噩梦释放": {"type": "projectile", "cooldown": 10, "damage": 55, "desc": "释放噩梦攻击敌人"},
    # 收尸人途径技能
    "亡灵召唤": {"type": "summon", "cooldown": 20, "duration": 15, "desc": "召唤亡灵助战"},
    "死亡凝视": {"type": "projectile", "cooldown": 10, "damage": 80, "desc": "死亡的目光"},
    "灵魂收割": {"type": "buff", "cooldown": 25, "duration": 0, "desc": "收割敌人灵魂恢复生命"},
    # 战士途径技能
    "狂暴": {"type": "buff", "cooldown": 20, "duration": 10, "desc": "进入狂暴状态，攻击大幅提升"},
    "重击": {"type": "melee", "cooldown": 4, "damage": 70, "desc": "强力重击"},
    "地震": {"type": "projectile", "cooldown": 15, "damage": 50, "desc": "震击地面造成范围伤害"},
    # 猎人途径技能
    "猎杀标记": {"type": "buff", "cooldown": 15, "duration": 20, "desc": "标记敌人，增加对其伤害"},
    "嗜血": {"type": "buff", "cooldown": 20, "duration": 10, "desc": "进入嗜血状态，攻击吸血"},
    "血之利刃": {"type": "projectile", "cooldown": 5, "damage": 55, "desc": "血液形成的利刃"},
    # 刺客途径技能
    "潜行": {"type": "buff", "cooldown": 12, "duration": 10, "desc": "进入潜行状态"},
    "致命一击": {"type": "melee", "cooldown": 8, "damage": 100, "desc": "从背后发动致命攻击"},
    "魅惑术": {"type": "control", "cooldown": 15, "duration": 8, "desc": "魅惑敌人使其听从命令"},
    # 耕种者途径技能
    "自然治愈": {"type": "heal", "cooldown": 15, "heal": 40, "desc": "自然之力治愈"},
    "藤蔓束缚": {"type": "control", "cooldown": 12, "duration": 5, "desc": "召唤藤蔓束缚敌人"},
    "丰收祝福": {"type": "buff", "cooldown": 25, "duration": 15, "desc": "获得丰收祝福增强"},
    # 药师途径技能
    "药剂投掷": {"type": "projectile", "cooldown": 4, "damage": 35, "desc": "投掷药剂造成伤害"},
    "变形术": {"type": "buff", "cooldown": 25, "duration": 15, "desc": "变形增强能力"},
    "召唤野兽": {"type": "summon", "cooldown": 20, "duration": 20, "desc": "召唤野兽助战"},
    # 律师途径技能
    "威压": {"type": "control", "cooldown": 15, "duration": 5, "desc": "释放威压使敌人恐惧"},
    "契约": {"type": "buff", "cooldown": 30, "duration": 0, "desc": "强制签订契约"},
    "腐化": {"type": "projectile", "cooldown": 10, "damage": 45, "desc": "腐化攻击"},
    # 仲裁人途径技能
    "神圣审判": {"type": "projectile", "cooldown": 10, "damage": 60, "desc": "神圣之力审判敌人"},
    "正义之锤": {"type": "melee", "cooldown": 6, "damage": 55, "desc": "以正义之名重击"},
    "庇护": {"type": "buff", "cooldown": 20, "duration": 8, "desc": "获得神圣庇护"},
    # 通识者途径技能
    "鉴定": {"type": "buff", "cooldown": 10, "duration": 15, "desc": "鉴定敌人弱点"},
    "工艺制作": {"type": "buff", "cooldown": 25, "duration": 0, "desc": "制作临时装备"},
    "炼金术": {"type": "projectile", "cooldown": 8, "damage": 50, "desc": "炼金术攻击"},
    # 窥秘人途径技能
    "巫术": {"type": "projectile", "cooldown": 6, "damage": 40, "desc": "释放巫术攻击"},
    "预言": {"type": "buff", "cooldown": 20, "duration": 10, "desc": "预言未来获得优势"},
    "卷轴释放": {"type": "projectile", "cooldown": 5, "damage": 45, "desc": "释放卷轴魔法"},
    # 罪犯途径技能
    "恐惧领域": {"type": "control", "cooldown": 20, "duration": 8, "desc": "创造恐惧区域"},
    "欲望操控": {"type": "control", "cooldown": 15, "duration": 6, "desc": "操控敌人欲望"},
    "深渊凝视": {"type": "projectile", "cooldown": 12, "damage": 70, "desc": "深渊的凝视"},
    # 囚犯途径技能
    "挣脱": {"type": "buff", "cooldown": 20, "duration": 0, "desc": "挣脱一切束缚"},
    "狂化": {"type": "buff", "cooldown": 25, "duration": 12, "desc": "进入狂化状态"},
    "怨念攻击": {"type": "projectile", "cooldown": 6, "damage": 45, "desc": "释放怨念攻击"},
    # 怪物途径技能
    "幸运加持": {"type": "buff", "cooldown": 18, "duration": 12, "desc": "增加暴击和闪避"},
    "灾祸诅咒": {"type": "control", "cooldown": 20, "duration": 8, "desc": "诅咒敌人降低其属性"},
    "命运逆转": {"type": "buff", "cooldown": 30, "duration": 0, "desc": "逆转即将受到的致命伤害"},
}

# 途径数据 - 22条途径（根据序列.xlsx）
PATHWAYS = {
    # ===== 诡秘之主组 =====
    "占卜家": {
        "name": "占卜家途径",
        "god": "愚者",
        "type": "magic",
        "group": "诡秘之主组",
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
    "学徒": {
        "name": "学徒途径",
        "god": "门",
        "type": "magic",
        "group": "诡秘之主组",
        "color": (138, 43, 226),  # 蓝紫色
        "desc": "空间与旅行之道，穿梭于星空之间",
        "sequences": {
            9: {"name": "学徒", "skills": ["戏法", "星象"], "hp": 95, "attack": 16, "defense": 4, "speed": 5},
            8: {"name": "戏法大师", "skills": ["戏法", "星象", "传送"], "hp": 145, "attack": 26, "defense": 7, "speed": 6},
            7: {"name": "占星人", "skills": ["戏法", "星象", "传送"], "hp": 195, "attack": 40, "defense": 10, "speed": 7},
            6: {"name": "记录官", "skills": ["戏法", "星象", "传送"], "hp": 270, "attack": 60, "defense": 15, "speed": 8},
            5: {"name": "旅行家", "skills": ["戏法", "星象", "传送"], "hp": 370, "attack": 86, "defense": 22, "speed": 9},
            4: {"name": "秘法师", "skills": ["戏法", "星象", "传送"], "hp": 490, "attack": 122, "defense": 32, "speed": 11},
            3: {"name": "漫游者", "skills": ["戏法", "星象", "传送"], "hp": 690, "attack": 182, "defense": 46, "speed": 13},
            2: {"name": "旅法师", "skills": ["戏法", "星象", "传送"], "hp": 990, "attack": 285, "defense": 72, "speed": 16},
            1: {"name": "星之匙", "skills": ["戏法", "星象", "传送"], "hp": 1470, "attack": 455, "defense": 110, "speed": 20},
            0: {"name": "门", "skills": ["戏法", "星象", "传送"], "hp": 2900, "attack": 810, "defense": 185, "speed": 28},
        }
    },
    "偷盗者": {
        "name": "偷盗者途径",
        "god": "错误",
        "type": "special",
        "group": "诡秘之主组",
        "color": (128, 0, 128),  # 紫色
        "desc": "欺诈与错误之道，在混乱中获取力量",
        "sequences": {
            9: {"name": "偷盗者", "skills": ["偷窃", "闪现"], "hp": 90, "attack": 18, "defense": 4, "speed": 7},
            8: {"name": "诈骗师", "skills": ["偷窃", "闪现", "解密"], "hp": 140, "attack": 28, "defense": 7, "speed": 8},
            7: {"name": "解密学者", "skills": ["偷窃", "闪现", "解密"], "hp": 190, "attack": 42, "defense": 10, "speed": 9},
            6: {"name": "盗火人", "skills": ["偷窃", "闪现", "解密"], "hp": 260, "attack": 62, "defense": 15, "speed": 10},
            5: {"name": "窃梦家", "skills": ["偷窃", "闪现", "解密"], "hp": 350, "attack": 88, "defense": 22, "speed": 11},
            4: {"name": "寄生者", "skills": ["偷窃", "闪现", "解密"], "hp": 480, "attack": 125, "defense": 32, "speed": 13},
            3: {"name": "欺诈导师", "skills": ["偷窃", "闪现", "解密"], "hp": 680, "attack": 185, "defense": 48, "speed": 15},
            2: {"name": "命运木马", "skills": ["偷窃", "闪现", "解密"], "hp": 980, "attack": 290, "defense": 75, "speed": 18},
            1: {"name": "时之虫", "skills": ["偷窃", "闪现", "解密"], "hp": 1450, "attack": 460, "defense": 115, "speed": 22},
            0: {"name": "错误", "skills": ["偷窃", "闪现", "解密"], "hp": 2800, "attack": 820, "defense": 190, "speed": 28},
        }
    },

    # ===== 上帝组 =====
    "观众": {
        "name": "观众途径",
        "god": "空想家",
        "type": "control",
        "group": "上帝组",
        "color": (75, 0, 130),  # 靛蓝色
        "desc": "心灵与操控之道，窥探他人思想",
        "sequences": {
            9: {"name": "观众", "skills": ["读心", "心灵冲击"], "hp": 95, "attack": 16, "defense": 5, "speed": 5},
            8: {"name": "读心者", "skills": ["读心", "心灵冲击", "催眠"], "hp": 145, "attack": 26, "defense": 8, "speed": 6},
            7: {"name": "心理医生", "skills": ["读心", "心灵冲击", "催眠", "梦境入侵"], "hp": 195, "attack": 40, "defense": 12, "speed": 7},
            6: {"name": "催眠师", "skills": ["读心", "心灵冲击", "催眠", "梦境入侵"], "hp": 270, "attack": 60, "defense": 18, "speed": 8},
            5: {"name": "梦境行者", "skills": ["读心", "心灵冲击", "催眠", "梦境入侵"], "hp": 370, "attack": 86, "defense": 25, "speed": 9},
            4: {"name": "操纵师", "skills": ["读心", "心灵冲击", "催眠", "梦境入侵"], "hp": 490, "attack": 122, "defense": 35, "speed": 10},
            3: {"name": "织梦人", "skills": ["读心", "心灵冲击", "催眠", "梦境入侵"], "hp": 690, "attack": 182, "defense": 50, "speed": 12},
            2: {"name": "洞察者", "skills": ["读心", "心灵冲击", "催眠", "梦境入侵"], "hp": 990, "attack": 285, "defense": 78, "speed": 15},
            1: {"name": "作家", "skills": ["读心", "心灵冲击", "催眠", "梦境入侵"], "hp": 1480, "attack": 455, "defense": 118, "speed": 18},
            0: {"name": "空想家", "skills": ["读心", "心灵冲击", "催眠", "梦境入侵"], "hp": 2900, "attack": 810, "defense": 195, "speed": 25},
        }
    },
    "秘祈人": {
        "name": "秘祈人途径",
        "god": "倒吊人",
        "type": "wisdom",
        "group": "上帝组",
        "color": (100, 60, 120),  # 深紫
        "desc": "秘密与祈祷之道，探寻隐藏的真理",
        "sequences": {
            9: {"name": "秘祈人", "skills": ["秘密感知", "祈祷"], "hp": 95, "attack": 15, "defense": 5, "speed": 5},
            8: {"name": "倾听者", "skills": ["秘密感知", "祈祷", "倾听"], "hp": 145, "attack": 25, "defense": 8, "speed": 6},
            7: {"name": "隐修士", "skills": ["秘密感知", "祈祷", "倾听"], "hp": 195, "attack": 39, "defense": 12, "speed": 7},
            6: {"name": "蔷薇主教", "skills": ["秘密感知", "祈祷", "倾听"], "hp": 270, "attack": 59, "defense": 18, "speed": 8},
            5: {"name": "牧羊人", "skills": ["秘密感知", "祈祷", "倾听"], "hp": 370, "attack": 85, "defense": 25, "speed": 9},
            4: {"name": "黑骑士", "skills": ["秘密感知", "祈祷", "倾听"], "hp": 490, "attack": 120, "defense": 35, "speed": 10},
            3: {"name": "三首圣堂", "skills": ["秘密感知", "祈祷", "倾听"], "hp": 690, "attack": 178, "defense": 50, "speed": 12},
            2: {"name": "秽语长老", "skills": ["秘密感知", "祈祷", "倾听"], "hp": 990, "attack": 280, "defense": 78, "speed": 15},
            1: {"name": "暗天使", "skills": ["秘密感知", "祈祷", "倾听"], "hp": 1470, "attack": 448, "defense": 118, "speed": 18},
            0: {"name": "倒吊人", "skills": ["秘密感知", "祈祷", "倾听"], "hp": 2900, "attack": 795, "defense": 195, "speed": 25},
        }
    },
    "歌颂者": {
        "name": "歌颂者途径",
        "god": "太阳",
        "type": "support",
        "group": "上帝组",
        "color": (255, 200, 50),  # 金黄色
        "desc": "光明与治愈之道，以信仰为力量",
        "sequences": {
            9: {"name": "歌颂者", "skills": ["神圣之光", "治愈祷言"], "hp": 110, "attack": 14, "defense": 7, "speed": 4},
            8: {"name": "祈光人", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 165, "attack": 24, "defense": 10, "speed": 5},
            7: {"name": "光之祭司", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 220, "attack": 38, "defense": 15, "speed": 6},
            6: {"name": "公证人", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 300, "attack": 58, "defense": 22, "speed": 7},
            5: {"name": "光之神仆", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 410, "attack": 84, "defense": 30, "speed": 8},
            4: {"name": "无暗者", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 540, "attack": 118, "defense": 40, "speed": 9},
            3: {"name": "猎魔者", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 750, "attack": 176, "defense": 58, "speed": 11},
            2: {"name": "逐光者", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 1070, "attack": 276, "defense": 88, "speed": 14},
            1: {"name": "纯白天使", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 1570, "attack": 442, "defense": 128, "speed": 17},
            0: {"name": "太阳", "skills": ["神圣之光", "治愈祷言", "惩戒"], "hp": 3150, "attack": 785, "defense": 215, "speed": 24},
        }
    },
    "水手": {
        "name": "水手途径",
        "god": "暴君",
        "type": "magic",
        "group": "上帝组",
        "color": (0, 105, 148),  # 深海蓝
        "desc": "风暴与海洋之道，驾驭自然之力",
        "sequences": {
            9: {"name": "水手", "skills": ["风暴召唤", "水流操控"], "hp": 100, "attack": 16, "defense": 5, "speed": 5},
            8: {"name": "暴怒之民", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 155, "attack": 26, "defense": 8, "speed": 6},
            7: {"name": "航海家", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 210, "attack": 40, "defense": 12, "speed": 7},
            6: {"name": "风眷者", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 290, "attack": 60, "defense": 18, "speed": 8},
            5: {"name": "海洋歌者", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 400, "attack": 86, "defense": 25, "speed": 9},
            4: {"name": "灾难主祭", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 530, "attack": 122, "defense": 35, "speed": 10},
            3: {"name": "海神", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 740, "attack": 182, "defense": 50, "speed": 12},
            2: {"name": "天灾", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 1050, "attack": 285, "defense": 78, "speed": 15},
            1: {"name": "雷神", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 1550, "attack": 455, "defense": 118, "speed": 18},
            0: {"name": "暴君", "skills": ["风暴召唤", "水流操控", "闪电链"], "hp": 3100, "attack": 810, "defense": 195, "speed": 25},
        }
    },
    "阅读者": {
        "name": "阅读者途径",
        "god": "白塔",
        "type": "wisdom",
        "group": "上帝组",
        "color": (70, 130, 180),  # 钢蓝色
        "desc": "知识与博学之道，以学识为武器",
        "sequences": {
            9: {"name": "阅读者", "skills": ["博学", "知识投射"], "hp": 100, "attack": 14, "defense": 6, "speed": 4},
            8: {"name": "格斗学者", "skills": ["博学", "知识投射", "考古"], "hp": 155, "attack": 24, "defense": 9, "speed": 5},
            7: {"name": "守知者", "skills": ["博学", "知识投射", "考古"], "hp": 210, "attack": 38, "defense": 14, "speed": 6},
            6: {"name": "博学者", "skills": ["博学", "知识投射", "考古"], "hp": 290, "attack": 58, "defense": 20, "speed": 7},
            5: {"name": "秘术导师", "skills": ["博学", "知识投射", "考古"], "hp": 400, "attack": 84, "defense": 28, "speed": 8},
            4: {"name": "奥秘学者", "skills": ["博学", "知识投射", "考古"], "hp": 530, "attack": 118, "defense": 38, "speed": 9},
            3: {"name": "知识皇帝", "skills": ["博学", "知识投射", "考古"], "hp": 740, "attack": 175, "defense": 55, "speed": 11},
            2: {"name": "洞悉者", "skills": ["博学", "知识投射", "考古"], "hp": 1050, "attack": 275, "defense": 85, "speed": 14},
            1: {"name": "全知者", "skills": ["博学", "知识投射", "考古"], "hp": 1550, "attack": 440, "defense": 125, "speed": 17},
            0: {"name": "白塔", "skills": ["博学", "知识投射", "考古"], "hp": 3100, "attack": 780, "defense": 210, "speed": 24},
        }
    },

    # ===== 永暗组 =====
    "不眠者": {
        "name": "不眠者途径",
        "god": "黑暗",
        "type": "special",
        "group": "永暗组",
        "color": (25, 25, 112),  # 午夜蓝
        "desc": "黑暗与隐匿之道，在永夜中潜行",
        "sequences": {
            9: {"name": "不眠者", "skills": ["暗影步", "噩梦释放"], "hp": 95, "attack": 17, "defense": 5, "speed": 6},
            8: {"name": "午夜诗人", "skills": ["暗影步", "噩梦释放", "黑暗笼罩"], "hp": 145, "attack": 27, "defense": 8, "speed": 7},
            7: {"name": "梦魇", "skills": ["暗影步", "噩梦释放", "黑暗笼罩"], "hp": 195, "attack": 42, "defense": 12, "speed": 8},
            6: {"name": "安魂师", "skills": ["暗影步", "噩梦释放", "黑暗笼罩"], "hp": 270, "attack": 62, "defense": 17, "speed": 9},
            5: {"name": "灵巫", "skills": ["暗影步", "噩梦释放", "黑暗笼罩"], "hp": 370, "attack": 88, "defense": 24, "speed": 10},
            4: {"name": "守夜人", "skills": ["暗影步", "噩梦释放", "黑暗笼罩"], "hp": 490, "attack": 124, "defense": 34, "speed": 12},
            3: {"name": "恐惧主教", "skills": ["暗影步", "噩梦释放", "黑暗笼罩"], "hp": 690, "attack": 184, "defense": 49, "speed": 14},
            2: {"name": "隐秘之仆", "skills": ["暗影步", "噩梦释放", "黑暗笼罩"], "hp": 990, "attack": 288, "defense": 77, "speed": 17},
            1: {"name": "厄难骑士", "skills": ["暗影步", "噩梦释放", "黑暗笼罩"], "hp": 1470, "attack": 458, "defense": 117, "speed": 21},
            0: {"name": "黑暗", "skills": ["暗影步", "噩梦释放", "黑暗笼罩"], "hp": 2850, "attack": 815, "defense": 192, "speed": 27},
        }
    },
    "收尸人": {
        "name": "收尸人途径",
        "god": "死神",
        "type": "magic",
        "group": "永暗组",
        "color": (47, 79, 79),  # 暗石板灰
        "desc": "死亡与灵魂之道，掌控生死轮回",
        "sequences": {
            9: {"name": "收尸人", "skills": ["亡灵召唤", "死亡凝视"], "hp": 105, "attack": 16, "defense": 6, "speed": 4},
            8: {"name": "掘墓人", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 160, "attack": 26, "defense": 9, "speed": 5},
            7: {"name": "通灵者", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 215, "attack": 40, "defense": 13, "speed": 6},
            6: {"name": "死灵导师", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 295, "attack": 60, "defense": 19, "speed": 7},
            5: {"name": "看门人", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 405, "attack": 86, "defense": 27, "speed": 8},
            4: {"name": "不死者", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 535, "attack": 120, "defense": 37, "speed": 9},
            3: {"name": "摆渡人", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 745, "attack": 178, "defense": 53, "speed": 11},
            2: {"name": "死亡执政官", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 1060, "attack": 278, "defense": 82, "speed": 14},
            1: {"name": "苍白皇帝", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 1560, "attack": 445, "defense": 122, "speed": 17},
            0: {"name": "死神", "skills": ["亡灵召唤", "死亡凝视", "灵魂收割"], "hp": 3050, "attack": 790, "defense": 205, "speed": 24},
        }
    },
    "战士": {
        "name": "战士途径",
        "god": "黄昏巨人",
        "type": "melee",
        "group": "永暗组",
        "color": (139, 69, 19),  # 鞍褐色
        "desc": "力量与战斗之道，以蛮力压制敌人",
        "sequences": {
            9: {"name": "战士", "skills": ["狂暴", "重击"], "hp": 130, "attack": 18, "defense": 8, "speed": 3},
            8: {"name": "格斗家", "skills": ["狂暴", "重击", "地震"], "hp": 195, "attack": 30, "defense": 12, "speed": 4},
            7: {"name": "武器大师", "skills": ["狂暴", "重击", "地震"], "hp": 260, "attack": 46, "defense": 18, "speed": 5},
            6: {"name": "黎明骑士", "skills": ["狂暴", "重击", "地震"], "hp": 350, "attack": 68, "defense": 26, "speed": 6},
            5: {"name": "守护者", "skills": ["狂暴", "重击", "地震"], "hp": 470, "attack": 96, "defense": 36, "speed": 7},
            4: {"name": "猎魔者", "skills": ["狂暴", "重击", "地震"], "hp": 620, "attack": 135, "defense": 48, "speed": 8},
            3: {"name": "银骑士", "skills": ["狂暴", "重击", "地震"], "hp": 860, "attack": 200, "defense": 68, "speed": 9},
            2: {"name": "荣耀者", "skills": ["狂暴", "重击", "地震"], "hp": 1220, "attack": 310, "defense": 100, "speed": 11},
            1: {"name": "神之手", "skills": ["狂暴", "重击", "地震"], "hp": 1800, "attack": 495, "defense": 145, "speed": 14},
            0: {"name": "黄昏巨人", "skills": ["狂暴", "重击", "地震"], "hp": 3500, "attack": 880, "defense": 240, "speed": 20},
        }
    },

    # ===== 灾祸组 =====
    "猎人": {
        "name": "猎人途径",
        "god": "红祭司",
        "type": "melee",
        "group": "灾祸组",
        "color": (220, 20, 60),  # 猩红色
        "desc": "猎杀与鲜血之道，以猎物之血为食",
        "sequences": {
            9: {"name": "猎人", "skills": ["猎杀标记", "血之利刃"], "hp": 110, "attack": 18, "defense": 6, "speed": 5},
            8: {"name": "挑衅者", "skills": ["猎杀标记", "血之利刃", "嗜血"], "hp": 165, "attack": 28, "defense": 9, "speed": 6},
            7: {"name": "纵火家", "skills": ["猎杀标记", "血之利刃", "嗜血"], "hp": 220, "attack": 44, "defense": 14, "speed": 7},
            6: {"name": "阴谋家", "skills": ["猎杀标记", "血之利刃", "嗜血"], "hp": 300, "attack": 66, "defense": 20, "speed": 8},
            5: {"name": "收割者", "skills": ["猎杀标记", "血之利刃", "嗜血"], "hp": 410, "attack": 94, "defense": 28, "speed": 9},
            4: {"name": "铁血骑士", "skills": ["猎杀标记", "血之利刃", "嗜血"], "hp": 540, "attack": 132, "defense": 38, "speed": 10},
            3: {"name": "战争主教", "skills": ["猎杀标记", "血之利刃", "嗜血"], "hp": 750, "attack": 196, "defense": 55, "speed": 12},
            2: {"name": "天气术士", "skills": ["猎杀标记", "血之利刃", "嗜血"], "hp": 1070, "attack": 306, "defense": 85, "speed": 15},
            1: {"name": "征服者", "skills": ["猎杀标记", "血之利刃", "嗜血"], "hp": 1570, "attack": 490, "defense": 125, "speed": 18},
            0: {"name": "红祭司", "skills": ["猎杀标记", "血之利刃", "嗜血"], "hp": 3150, "attack": 870, "defense": 210, "speed": 25},
        }
    },
    "刺客": {
        "name": "刺客途径",
        "god": "原初魔女",
        "type": "melee",
        "group": "灾祸组",
        "color": (128, 0, 64),  # 暗紫红
        "desc": "魅惑与诅咒之道，以情感为武器",
        "sequences": {
            9: {"name": "刺客", "skills": ["潜行", "致命一击"], "hp": 85, "attack": 20, "defense": 3, "speed": 7},
            8: {"name": "教唆者", "skills": ["潜行", "致命一击", "魅惑术"], "hp": 130, "attack": 32, "defense": 6, "speed": 8},
            7: {"name": "女巫", "skills": ["潜行", "致命一击", "魅惑术"], "hp": 175, "attack": 48, "defense": 9, "speed": 9},
            6: {"name": "欢愉魔女", "skills": ["潜行", "致命一击", "魅惑术"], "hp": 245, "attack": 70, "defense": 14, "speed": 10},
            5: {"name": "痛苦魔女", "skills": ["潜行", "致命一击", "魅惑术"], "hp": 335, "attack": 98, "defense": 20, "speed": 11},
            4: {"name": "绝望魔女", "skills": ["潜行", "致命一击", "魅惑术"], "hp": 450, "attack": 138, "defense": 29, "speed": 13},
            3: {"name": "不老魔女", "skills": ["潜行", "致命一击", "魅惑术"], "hp": 630, "attack": 204, "defense": 43, "speed": 15},
            2: {"name": "灾难魔女", "skills": ["潜行", "致命一击", "魅惑术"], "hp": 910, "attack": 318, "defense": 68, "speed": 18},
            1: {"name": "末日魔女", "skills": ["潜行", "致命一击", "魅惑术"], "hp": 1350, "attack": 508, "defense": 105, "speed": 22},
            0: {"name": "原初魔女", "skills": ["潜行", "致命一击", "魅惑术"], "hp": 2650, "attack": 900, "defense": 175, "speed": 30},
        }
    },

    # ===== 根源组 =====
    "耕种者": {
        "name": "耕种者途径",
        "god": "母亲",
        "type": "support",
        "group": "根源组",
        "color": (34, 139, 34),  # 森林绿
        "desc": "生命与大地之道，孕育万物的力量",
        "sequences": {
            9: {"name": "耕种者", "skills": ["自然治愈", "藤蔓束缚"], "hp": 105, "attack": 13, "defense": 6, "speed": 4},
            8: {"name": "医师", "skills": ["自然治愈", "藤蔓束缚", "丰收祝福"], "hp": 160, "attack": 22, "defense": 9, "speed": 5},
            7: {"name": "丰收祭司", "skills": ["自然治愈", "藤蔓束缚", "丰收祝福"], "hp": 215, "attack": 35, "defense": 14, "speed": 6},
            6: {"name": "生物学家", "skills": ["自然治愈", "藤蔓束缚", "丰收祝福"], "hp": 295, "attack": 53, "defense": 20, "speed": 7},
            5: {"name": "德鲁伊", "skills": ["自然治愈", "藤蔓束缚", "丰收祝福"], "hp": 405, "attack": 76, "defense": 28, "speed": 8},
            4: {"name": "古代炼金师", "skills": ["自然治愈", "藤蔓束缚", "丰收祝福"], "hp": 535, "attack": 107, "defense": 38, "speed": 9},
            3: {"name": "抬棺人", "skills": ["自然治愈", "藤蔓束缚", "丰收祝福"], "hp": 745, "attack": 160, "defense": 55, "speed": 11},
            2: {"name": "荒芜主母", "skills": ["自然治愈", "藤蔓束缚", "丰收祝福"], "hp": 1060, "attack": 250, "defense": 85, "speed": 14},
            1: {"name": "自然之母", "skills": ["自然治愈", "藤蔓束缚", "丰收祝福"], "hp": 1560, "attack": 400, "defense": 125, "speed": 17},
            0: {"name": "母亲", "skills": ["自然治愈", "藤蔓束缚", "丰收祝福"], "hp": 3200, "attack": 710, "defense": 215, "speed": 24},
        }
    },
    "药师": {
        "name": "药师途径",
        "god": "月亮",
        "type": "magic",
        "group": "根源组",
        "color": (200, 200, 230),  # 月白色
        "desc": "药剂与变形之道，借月之力量转化形态",
        "sequences": {
            9: {"name": "药师", "skills": ["药剂投掷", "召唤野兽"], "hp": 95, "attack": 16, "defense": 5, "speed": 5},
            8: {"name": "驯兽师", "skills": ["药剂投掷", "召唤野兽", "变形术"], "hp": 145, "attack": 26, "defense": 8, "speed": 6},
            7: {"name": "吸血鬼", "skills": ["药剂投掷", "召唤野兽", "变形术"], "hp": 195, "attack": 40, "defense": 12, "speed": 7},
            6: {"name": "魔药教授", "skills": ["药剂投掷", "召唤野兽", "变形术"], "hp": 270, "attack": 60, "defense": 18, "speed": 8},
            5: {"name": "深红学者", "skills": ["药剂投掷", "召唤野兽", "变形术"], "hp": 370, "attack": 86, "defense": 25, "speed": 9},
            4: {"name": "巫王", "skills": ["药剂投掷", "召唤野兽", "变形术"], "hp": 490, "attack": 122, "defense": 35, "speed": 11},
            3: {"name": "召唤大师", "skills": ["药剂投掷", "召唤野兽", "变形术"], "hp": 690, "attack": 182, "defense": 50, "speed": 13},
            2: {"name": "月亮木偶", "skills": ["药剂投掷", "召唤野兽", "变形术"], "hp": 990, "attack": 285, "defense": 78, "speed": 16},
            1: {"name": "美神", "skills": ["药剂投掷", "召唤野兽", "变形术"], "hp": 1470, "attack": 455, "defense": 118, "speed": 20},
            0: {"name": "月亮", "skills": ["药剂投掷", "召唤野兽", "变形术"], "hp": 2900, "attack": 810, "defense": 195, "speed": 27},
        }
    },

    # ===== 无序组 =====
    "律师": {
        "name": "律师途径",
        "god": "黑皇帝",
        "type": "control",
        "group": "无序组",
        "color": (30, 30, 30),  # 纯黑
        "desc": "权谋与统治之道，以黑暗手段掌控一切",
        "sequences": {
            9: {"name": "律师", "skills": ["威压", "契约"], "hp": 105, "attack": 14, "defense": 6, "speed": 5},
            8: {"name": "野蛮人", "skills": ["威压", "契约", "腐化"], "hp": 160, "attack": 24, "defense": 9, "speed": 6},
            7: {"name": "贿赂者", "skills": ["威压", "契约", "腐化"], "hp": 215, "attack": 38, "defense": 14, "speed": 7},
            6: {"name": "腐化男爵", "skills": ["威压", "契约", "腐化"], "hp": 295, "attack": 58, "defense": 20, "speed": 8},
            5: {"name": "混乱导师", "skills": ["威压", "契约", "腐化"], "hp": 405, "attack": 84, "defense": 28, "speed": 9},
            4: {"name": "堕落伯爵", "skills": ["威压", "契约", "腐化"], "hp": 535, "attack": 118, "defense": 38, "speed": 10},
            3: {"name": "狂乱法师", "skills": ["威压", "契约", "腐化"], "hp": 745, "attack": 176, "defense": 55, "speed": 12},
            2: {"name": "熵之公爵", "skills": ["威压", "契约", "腐化"], "hp": 1060, "attack": 276, "defense": 85, "speed": 15},
            1: {"name": "弑序亲王", "skills": ["威压", "契约", "腐化"], "hp": 1560, "attack": 442, "defense": 125, "speed": 18},
            0: {"name": "黑皇帝", "skills": ["威压", "契约", "腐化"], "hp": 3150, "attack": 785, "defense": 210, "speed": 25},
        }
    },
    "仲裁人": {
        "name": "仲裁人途径",
        "god": "审判者",
        "type": "melee",
        "group": "无序组",
        "color": (192, 192, 192),  # 银色
        "desc": "审判与正义之道，以神圣之力惩戒邪恶",
        "sequences": {
            9: {"name": "仲裁人", "skills": ["神圣审判", "正义之锤"], "hp": 115, "attack": 16, "defense": 8, "speed": 4},
            8: {"name": "治安官", "skills": ["神圣审判", "正义之锤", "庇护"], "hp": 175, "attack": 26, "defense": 12, "speed": 5},
            7: {"name": "审讯者", "skills": ["神圣审判", "正义之锤", "庇护"], "hp": 235, "attack": 40, "defense": 18, "speed": 6},
            6: {"name": "法官", "skills": ["神圣审判", "正义之锤", "庇护"], "hp": 320, "attack": 60, "defense": 26, "speed": 7},
            5: {"name": "惩戒骑士", "skills": ["神圣审判", "正义之锤", "庇护"], "hp": 435, "attack": 86, "defense": 36, "speed": 8},
            4: {"name": "律令法师", "skills": ["神圣审判", "正义之锤", "庇护"], "hp": 575, "attack": 120, "defense": 48, "speed": 9},
            3: {"name": "混乱猎手", "skills": ["神圣审判", "正义之锤", "庇护"], "hp": 800, "attack": 180, "defense": 68, "speed": 10},
            2: {"name": "平衡者", "skills": ["神圣审判", "正义之锤", "庇护"], "hp": 1150, "attack": 280, "defense": 100, "speed": 12},
            1: {"name": "秩序之手", "skills": ["神圣审判", "正义之锤", "庇护"], "hp": 1700, "attack": 450, "defense": 145, "speed": 15},
            0: {"name": "审判者", "skills": ["神圣审判", "正义之锤", "庇护"], "hp": 3400, "attack": 800, "defense": 240, "speed": 22},
        }
    },

    # ===== 知识妖鬼组 =====
    "通识者": {
        "name": "通识者途径",
        "god": "完美者",
        "type": "wisdom",
        "group": "知识妖鬼组",
        "color": (255, 215, 0),  # 金色
        "desc": "完美与极致之道，追求绝对的完美",
        "sequences": {
            9: {"name": "通识者", "skills": ["鉴定", "炼金术"], "hp": 100, "attack": 15, "defense": 6, "speed": 4},
            8: {"name": "考古学家", "skills": ["鉴定", "炼金术", "工艺制作"], "hp": 155, "attack": 25, "defense": 9, "speed": 5},
            7: {"name": "鉴定师", "skills": ["鉴定", "炼金术", "工艺制作"], "hp": 210, "attack": 39, "defense": 14, "speed": 6},
            6: {"name": "工匠", "skills": ["鉴定", "炼金术", "工艺制作"], "hp": 290, "attack": 59, "defense": 20, "speed": 7},
            5: {"name": "天文学家", "skills": ["鉴定", "炼金术", "工艺制作"], "hp": 400, "attack": 85, "defense": 28, "speed": 8},
            4: {"name": "炼金术士", "skills": ["鉴定", "炼金术", "工艺制作"], "hp": 530, "attack": 120, "defense": 38, "speed": 9},
            3: {"name": "奥秘学者", "skills": ["鉴定", "炼金术", "工艺制作"], "hp": 740, "attack": 178, "defense": 55, "speed": 11},
            2: {"name": "知识导师", "skills": ["鉴定", "炼金术", "工艺制作"], "hp": 1060, "attack": 280, "defense": 85, "speed": 14},
            1: {"name": "启蒙者", "skills": ["鉴定", "炼金术", "工艺制作"], "hp": 1560, "attack": 448, "defense": 125, "speed": 17},
            0: {"name": "完美者", "skills": ["鉴定", "炼金术", "工艺制作"], "hp": 3150, "attack": 795, "defense": 210, "speed": 24},
        }
    },
    "窥秘人": {
        "name": "窥秘人途径",
        "god": "隐者",
        "type": "magic",
        "group": "知识妖鬼组",
        "color": (139, 119, 101),  # 灰褐色
        "desc": "巫术与预言之道，窥探命运的奥秘",
        "sequences": {
            9: {"name": "窥秘人", "skills": ["巫术", "卷轴释放"], "hp": 95, "attack": 16, "defense": 5, "speed": 5},
            8: {"name": "格斗学者", "skills": ["巫术", "卷轴释放", "预言"], "hp": 145, "attack": 26, "defense": 8, "speed": 6},
            7: {"name": "巫师", "skills": ["巫术", "卷轴释放", "预言"], "hp": 195, "attack": 40, "defense": 12, "speed": 7},
            6: {"name": "卷轴教授", "skills": ["巫术", "卷轴释放", "预言"], "hp": 270, "attack": 60, "defense": 18, "speed": 8},
            5: {"name": "星象师", "skills": ["巫术", "卷轴释放", "预言"], "hp": 370, "attack": 86, "defense": 25, "speed": 9},
            4: {"name": "秘术导师", "skills": ["巫术", "卷轴释放", "预言"], "hp": 490, "attack": 122, "defense": 35, "speed": 10},
            3: {"name": "预言家", "skills": ["巫术", "卷轴释放", "预言"], "hp": 690, "attack": 182, "defense": 50, "speed": 12},
            2: {"name": "贤者", "skills": ["巫术", "卷轴释放", "预言"], "hp": 990, "attack": 285, "defense": 78, "speed": 15},
            1: {"name": "知识皇帝", "skills": ["巫术", "卷轴释放", "预言"], "hp": 1470, "attack": 455, "defense": 118, "speed": 18},
            0: {"name": "隐者", "skills": ["巫术", "卷轴释放", "预言"], "hp": 2900, "attack": 810, "defense": 195, "speed": 25},
        }
    },

    # ===== 恶魔之父组 =====
    "罪犯": {
        "name": "罪犯途径",
        "god": "深渊",
        "type": "special",
        "group": "恶魔之父组",
        "color": (20, 20, 60),  # 深蓝黑
        "desc": "深渊与毁灭之道，掌控黑暗力量",
        "sequences": {
            9: {"name": "罪犯", "skills": ["恐惧领域", "深渊凝视"], "hp": 100, "attack": 18, "defense": 4, "speed": 5},
            8: {"name": "冷血者", "skills": ["恐惧领域", "深渊凝视", "欲望操控"], "hp": 155, "attack": 29, "defense": 7, "speed": 6},
            7: {"name": "连环杀手", "skills": ["恐惧领域", "深渊凝视", "欲望操控"], "hp": 210, "attack": 44, "defense": 11, "speed": 7},
            6: {"name": "恶魔", "skills": ["恐惧领域", "深渊凝视", "欲望操控"], "hp": 290, "attack": 66, "defense": 16, "speed": 8},
            5: {"name": "欲望使徒", "skills": ["恐惧领域", "深渊凝视", "欲望操控"], "hp": 400, "attack": 94, "defense": 24, "speed": 9},
            4: {"name": "魔鬼大公", "skills": ["恐惧领域", "深渊凝视", "欲望操控"], "hp": 530, "attack": 132, "defense": 34, "speed": 10},
            3: {"name": "血腥大公", "skills": ["恐惧领域", "深渊凝视", "欲望操控"], "hp": 740, "attack": 196, "defense": 50, "speed": 12},
            2: {"name": "污秽君王", "skills": ["恐惧领域", "深渊凝视", "欲望操控"], "hp": 1060, "attack": 306, "defense": 78, "speed": 15},
            1: {"name": "深渊天使", "skills": ["恐惧领域", "深渊凝视", "欲望操控"], "hp": 1560, "attack": 490, "defense": 118, "speed": 18},
            0: {"name": "深渊", "skills": ["恐惧领域", "深渊凝视", "欲望操控"], "hp": 3150, "attack": 870, "defense": 200, "speed": 25},
        }
    },
    "囚犯": {
        "name": "囚犯途径",
        "god": "被缚者",
        "type": "melee",
        "group": "恶魔之父组",
        "color": (100, 80, 60),  # 锈棕色
        "desc": "束缚与挣脱之道，在枷锁中获得力量",
        "sequences": {
            9: {"name": "囚犯", "skills": ["挣脱", "怨念攻击"], "hp": 120, "attack": 16, "defense": 8, "speed": 4},
            8: {"name": "疯子", "skills": ["挣脱", "怨念攻击", "狂化"], "hp": 180, "attack": 26, "defense": 12, "speed": 5},
            7: {"name": "狼人", "skills": ["挣脱", "怨念攻击", "狂化"], "hp": 240, "attack": 40, "defense": 18, "speed": 6},
            6: {"name": "活尸", "skills": ["挣脱", "怨念攻击", "狂化"], "hp": 330, "attack": 60, "defense": 26, "speed": 7},
            5: {"name": "怨魂", "skills": ["挣脱", "怨念攻击", "狂化"], "hp": 450, "attack": 86, "defense": 36, "speed": 8},
            4: {"name": "木偶", "skills": ["挣脱", "怨念攻击", "狂化"], "hp": 600, "attack": 120, "defense": 48, "speed": 9},
            3: {"name": "沉默门徒", "skills": ["挣脱", "怨念攻击", "狂化"], "hp": 840, "attack": 178, "defense": 68, "speed": 10},
            2: {"name": "古代邪物", "skills": ["挣脱", "怨念攻击", "狂化"], "hp": 1200, "attack": 278, "defense": 100, "speed": 12},
            1: {"name": "神孽", "skills": ["挣脱", "怨念攻击", "狂化"], "hp": 1780, "attack": 445, "defense": 145, "speed": 15},
            0: {"name": "被缚者", "skills": ["挣脱", "怨念攻击", "狂化"], "hp": 3500, "attack": 790, "defense": 240, "speed": 22},
        }
    },

    # ===== 光之钥组 =====
    "怪物": {
        "name": "怪物途径",
        "god": "命运之轮",
        "type": "control",
        "group": "光之钥组",
        "color": (148, 0, 211),  # 紫罗兰
        "desc": "命运与因果之道，操控命运的齿轮",
        "sequences": {
            9: {"name": "怪物", "skills": ["幸运加持", "灾祸诅咒"], "hp": 95, "attack": 15, "defense": 5, "speed": 5},
            8: {"name": "机器", "skills": ["幸运加持", "灾祸诅咒", "命运逆转"], "hp": 145, "attack": 25, "defense": 8, "speed": 6},
            7: {"name": "幸运儿", "skills": ["幸运加持", "灾祸诅咒", "命运逆转"], "hp": 195, "attack": 39, "defense": 12, "speed": 7},
            6: {"name": "灾祸教士", "skills": ["幸运加持", "灾祸诅咒", "命运逆转"], "hp": 270, "attack": 59, "defense": 18, "speed": 8},
            5: {"name": "赢家", "skills": ["幸运加持", "灾祸诅咒", "命运逆转"], "hp": 370, "attack": 85, "defense": 25, "speed": 9},
            4: {"name": "厄运法师", "skills": ["幸运加持", "灾祸诅咒", "命运逆转"], "hp": 490, "attack": 120, "defense": 35, "speed": 10},
            3: {"name": "混乱行者", "skills": ["幸运加持", "灾祸诅咒", "命运逆转"], "hp": 690, "attack": 178, "defense": 50, "speed": 12},
            2: {"name": "先知", "skills": ["幸运加持", "灾祸诅咒", "命运逆转"], "hp": 990, "attack": 280, "defense": 78, "speed": 15},
            1: {"name": "水银之蛇", "skills": ["幸运加持", "灾祸诅咒", "命运逆转"], "hp": 1470, "attack": 448, "defense": 118, "speed": 18},
            0: {"name": "命运之轮", "skills": ["幸运加持", "灾祸诅咒", "命运逆转"], "hp": 2900, "attack": 795, "defense": 195, "speed": 25},
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


# 获取途径列表（按源质组分组）
def get_pathways_by_group():
    """获取按源质组分组的途径"""
    result = {}
    for pathway_id, data in PATHWAYS.items():
        group = data.get("group", "其他")
        if group not in result:
            result[group] = []
        result[group].append((pathway_id, data))
    return result
