"""
22条途径完整数据
根据原著序列链条表
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
    # ===== 愚者途径技能 =====
    "灵视": {"type": "buff", "cooldown": 10, "duration": 5, "desc": "开启灵视，看穿敌人弱点，增加20%暴击率"},
    "占卜": {"type": "buff", "cooldown": 15, "duration": 3, "desc": "预知危险，短暂无敌"},
    "纸牌投掷": {"type": "projectile", "cooldown": 2, "damage": 25, "desc": "投掷锋利纸牌，远程攻击"},
    "火焰跳跃": {"type": "dash", "cooldown": 8, "damage": 40, "desc": "化为火焰瞬移，对路径敌人造成伤害"},
    "空气炮": {"type": "projectile", "cooldown": 5, "damage": 60, "desc": "压缩空气形成炮弹"},
    "易容": {"type": "buff", "cooldown": 30, "duration": 10, "desc": "改变外貌，敌人不会主动攻击"},

    # ===== 门途径技能 =====
    "闪现": {"type": "dash", "cooldown": 5, "desc": "短距离瞬移"},
    "隐藏": {"type": "buff", "cooldown": 12, "duration": 5, "desc": "隐入阴影，进入隐身状态"},
    "短距传送": {"type": "dash", "cooldown": 3, "desc": "传送到视野内任意位置"},
    "窃取": {"type": "special", "cooldown": 20, "desc": "窃取敌人的一个增益效果"},
    "空间切割": {"type": "projectile", "cooldown": 8, "damage": 80, "desc": "撕裂空间，造成高额伤害"},

    # ===== 错误途径技能 =====
    "诅咒": {"type": "debuff", "cooldown": 10, "duration": 5, "desc": "诅咒敌人，降低20%攻击力"},
    "混乱领域": {"type": "aoe", "cooldown": 15, "damage": 30, "desc": "释放混乱能量，范围伤害"},
    "变异": {"type": "buff", "cooldown": 25, "duration": 8, "desc": "身体变异，增加50%攻击力和移速"},
    "疫病": {"type": "dot", "cooldown": 12, "damage": 15, "duration": 6, "desc": "释放疫病，持续造成伤害"},

    # ===== 隐秘途径技能 =====
    "读心": {"type": "special", "cooldown": 8, "desc": "读取敌人意图，预判下次攻击"},
    "心灵冲击": {"type": "projectile", "cooldown": 6, "damage": 35, "desc": "精神攻击，无视防御"},
    "催眠": {"type": "control", "cooldown": 15, "duration": 3, "desc": "催眠敌人，使其无法行动"},
    "梦境": {"type": "special", "cooldown": 20, "desc": "将敌人拉入梦境，降低其攻击命中"},
    "精神操控": {"type": "control", "cooldown": 25, "duration": 5, "desc": "操控敌人攻击其同伴"},

    # ===== 命运途径技能 =====
    "幸运一击": {"type": "buff", "cooldown": 8, "duration": 3, "desc": "下次攻击必定暴击"},
    "厄运转移": {"type": "special", "cooldown": 15, "desc": "将受到的伤害转移给敌人"},
    "概率操控": {"type": "buff", "cooldown": 20, "duration": 5, "desc": "50%几率闪避所有攻击"},
    "灾难降临": {"type": "aoe", "cooldown": 25, "damage": 100, "desc": "召唤灾难打击敌人"},

    # ===== 太阳途径技能 =====
    "圣光": {"type": "projectile", "cooldown": 4, "damage": 30, "desc": "发射圣光球"},
    "治疗": {"type": "heal", "cooldown": 10, "heal": 50, "desc": "恢复生命值"},
    "光明祝福": {"type": "buff", "cooldown": 15, "duration": 8, "desc": "增加全属性10%"},
    "净化": {"type": "special", "cooldown": 12, "desc": "净化所有负面状态"},
    "阳光之怒": {"type": "aoe", "cooldown": 20, "damage": 80, "desc": "召唤阳光轰炸区域"},

    # ===== 暴风途径技能 =====
    "风刃": {"type": "projectile", "cooldown": 3, "damage": 25, "desc": "发射风刃"},
    "海浪冲击": {"type": "aoe", "cooldown": 10, "damage": 45, "desc": "召唤海浪冲击敌人"},
    "风暴护盾": {"type": "buff", "cooldown": 15, "duration": 6, "desc": "风暴环绕，反弹30%伤害"},
    "闪电链": {"type": "projectile", "cooldown": 8, "damage": 55, "desc": "闪电在敌人间弹跳"},
    "暴风领域": {"type": "aoe", "cooldown": 25, "damage": 70, "desc": "召唤暴风，持续范围伤害"},

    # ===== 审判/战争途径技能 =====
    "重击": {"type": "melee", "cooldown": 3, "damage": 40, "desc": "蓄力重击"},
    "战吼": {"type": "buff", "cooldown": 12, "duration": 6, "desc": "战吼提升攻击力30%"},
    "铁壁": {"type": "buff", "cooldown": 15, "duration": 5, "desc": "防御姿态，减少50%伤害"},
    "冲锋": {"type": "dash", "cooldown": 8, "damage": 35, "desc": "冲向敌人并造成伤害"},
    "处决": {"type": "melee", "cooldown": 20, "damage": 120, "desc": "对低血量敌人造成巨额伤害"},

    # ===== 黑夜途径技能 =====
    "暗影潜行": {"type": "buff", "cooldown": 10, "duration": 5, "desc": "融入黑暗，隐身"},
    "黑暗侵蚀": {"type": "dot", "cooldown": 8, "damage": 20, "duration": 5, "desc": "黑暗侵蚀敌人"},
    "恐惧": {"type": "control", "cooldown": 12, "duration": 3, "desc": "使敌人陷入恐惧，无法行动"},
    "暗影刺杀": {"type": "melee", "cooldown": 15, "damage": 90, "desc": "从阴影中突袭，高额伤害"},

    # ===== 死亡途径技能 =====
    "召唤亡灵": {"type": "summon", "cooldown": 15, "duration": 20, "desc": "召唤骷髅战士"},
    "灵魂抽取": {"type": "projectile", "cooldown": 10, "damage": 40, "heal": 20, "desc": "抽取敌人灵魂，恢复生命"},
    "死亡之触": {"type": "melee", "cooldown": 8, "damage": 50, "desc": "触碰带来死亡"},
    "亡灵大军": {"type": "summon", "cooldown": 30, "duration": 15, "desc": "召唤亡灵大军"},

    # ===== 智慧/律师途径技能 =====
    "知识之光": {"type": "buff", "cooldown": 10, "duration": 8, "desc": "增加暴击伤害30%"},
    "弱点分析": {"type": "debuff", "cooldown": 8, "duration": 5, "desc": "分析敌人弱点，降低其防御"},
    "言灵": {"type": "special", "cooldown": 20, "desc": "言出法随，效果随机"},
    "契约束缚": {"type": "control", "cooldown": 15, "duration": 4, "desc": "用契约束缚敌人"},

    # ===== 猎人途径技能 =====
    "追踪": {"type": "buff", "cooldown": 5, "duration": 10, "desc": "标记敌人，增加对其伤害"},
    "致命射击": {"type": "projectile", "cooldown": 6, "damage": 50, "desc": "精准射击"},
    "血怒": {"type": "buff", "cooldown": 15, "duration": 8, "desc": "进入狂暴，攻击力+50%，攻速+30%"},
    "鲜血汲取": {"type": "melee", "cooldown": 10, "damage": 35, "heal": 25, "desc": "攻击并吸取生命"},

    # ===== 刺客途径技能 =====
    "潜行": {"type": "buff", "cooldown": 8, "duration": 5, "desc": "进入潜行状态"},
    "背刺": {"type": "melee", "cooldown": 5, "damage": 70, "desc": "从背后攻击造成高额伤害"},
    "毒刃": {"type": "buff", "cooldown": 12, "duration": 10, "desc": "武器附毒，攻击造成持续伤害"},
    "影分身": {"type": "special", "cooldown": 20, "duration": 8, "desc": "创造分身分散敌人注意"},

    # ===== 预言家途径技能 =====
    "预言": {"type": "buff", "cooldown": 15, "duration": 5, "desc": "预知未来，闪避率+50%"},
    "祸连": {"type": "debuff", "cooldown": 10, "duration": 6, "desc": "将厄运连接到敌人身上"},
    "通灵": {"type": "summon", "cooldown": 20, "duration": 15, "desc": "召唤灵体助战"},
    "命运揭示": {"type": "special", "cooldown": 25, "desc": "揭示敌人命运，造成大量伤害"},

    # ===== 炼药途径技能 =====
    "投掷药剂": {"type": "projectile", "cooldown": 4, "damage": 30, "desc": "投掷爆炸药剂"},
    "治疗药剂": {"type": "heal", "cooldown": 12, "heal": 60, "desc": "使用治疗药剂"},
    "变形": {"type": "buff", "cooldown": 20, "duration": 10, "desc": "变形增强战斗能力"},
    "毒雾": {"type": "aoe", "cooldown": 15, "damage": 25, "duration": 5, "desc": "释放毒雾"},

    # ===== 驭兽途径技能 =====
    "召唤野兽": {"type": "summon", "cooldown": 15, "duration": 20, "desc": "召唤野兽助战"},
    "自然治愈": {"type": "heal", "cooldown": 10, "heal": 40, "desc": "自然之力恢复生命"},
    "野性变身": {"type": "buff", "cooldown": 25, "duration": 12, "desc": "变身为野兽形态"},
    "精灵召唤": {"type": "summon", "cooldown": 20, "duration": 15, "desc": "召唤精灵"},

    # ===== 执剑途径技能 =====
    "剑气": {"type": "projectile", "cooldown": 4, "damage": 35, "desc": "发射剑气"},
    "旋风斩": {"type": "aoe", "cooldown": 8, "damage": 45, "desc": "旋转攻击周围敌人"},
    "剑舞": {"type": "buff", "cooldown": 15, "duration": 6, "desc": "进入剑舞状态，攻速+50%"},
    "圣剑审判": {"type": "melee", "cooldown": 20, "damage": 100, "desc": "召唤圣剑之力"},

    # ===== 机械途径技能 =====
    "枪械射击": {"type": "projectile", "cooldown": 2, "damage": 20, "desc": "快速射击"},
    "手雷": {"type": "aoe", "cooldown": 10, "damage": 60, "desc": "投掷手雷"},
    "机械傀儡": {"type": "summon", "cooldown": 18, "duration": 20, "desc": "部署机械傀儡"},
    "爆破": {"type": "aoe", "cooldown": 25, "damage": 120, "desc": "大范围爆破"},

    # ===== 旁观者途径技能 =====
    "洞察": {"type": "buff", "cooldown": 8, "duration": 6, "desc": "洞察敌人，增加命中率"},
    "精神干扰": {"type": "debuff", "cooldown": 10, "duration": 4, "desc": "干扰敌人精神，降低命中"},
    "操纵": {"type": "control", "cooldown": 20, "duration": 5, "desc": "操纵敌人行动"},
    "主宰意志": {"type": "aoe", "cooldown": 25, "damage": 70, "desc": "以意志压制敌人"},

    # ===== 黑皇帝途径技能 =====
    "威压": {"type": "debuff", "cooldown": 8, "duration": 5, "desc": "释放威压，降低敌人攻击"},
    "征服": {"type": "buff", "cooldown": 15, "duration": 8, "desc": "征服意志，增加全属性"},
    "暴君之力": {"type": "melee", "cooldown": 10, "damage": 60, "desc": "暴君的一击"},
    "帝国军团": {"type": "summon", "cooldown": 30, "duration": 15, "desc": "召唤帝国士兵"},
}

# 22条途径完整数据 - 根据原著序列链条表
PATHWAYS = {
    # ===== 1. 愚者/世界途径 =====
    "愚者": {
        "name": "愚者途径",
        "god": "愚者",
        "type": "magic",
        "color": (218, 165, 32),
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

    # ===== 2. 魔术师/门途径 =====
    "门": {
        "name": "门途径",
        "god": "门",
        "type": "special",
        "color": (75, 0, 130),
        "desc": "空间与盗窃之道，穿梭于世界的缝隙",
        "sequences": {
            9: {"name": "学徒", "skills": ["闪现"], "hp": 80, "attack": 18, "defense": 4, "speed": 7},
            8: {"name": "戏法大师", "skills": ["闪现", "隐藏"], "hp": 120, "attack": 28, "defense": 6, "speed": 8},
            7: {"name": "占星官", "skills": ["闪现", "隐藏", "短距传送"], "hp": 170, "attack": 42, "defense": 10, "speed": 9},
            6: {"name": "旅行家", "skills": ["闪现", "隐藏", "短距传送", "窃取"], "hp": 240, "attack": 62, "defense": 15, "speed": 10},
            5: {"name": "秘法师", "skills": ["闪现", "隐藏", "短距传送", "窃取", "空间切割"], "hp": 330, "attack": 88, "defense": 22, "speed": 12},
            4: {"name": "漫游者", "skills": ["闪现", "隐藏", "短距传送", "窃取", "空间切割"], "hp": 450, "attack": 125, "defense": 32, "speed": 14},
            3: {"name": "旅法师", "skills": ["闪现", "隐藏", "短距传送", "窃取", "空间切割"], "hp": 650, "attack": 190, "defense": 48, "speed": 16},
            2: {"name": "星之使", "skills": ["闪现", "隐藏", "短距传送", "窃取", "空间切割"], "hp": 950, "attack": 300, "defense": 75, "speed": 19},
            1: {"name": "空间行者", "skills": ["闪现", "隐藏", "短距传送", "窃取", "空间切割"], "hp": 1400, "attack": 480, "defense": 115, "speed": 22},
            0: {"name": "门", "skills": ["闪现", "隐藏", "短距传送", "窃取", "空间切割"], "hp": 2800, "attack": 850, "defense": 190, "speed": 30},
        }
    },

    # ===== 3. 偷盗者/错误途径 =====
    "错误": {
        "name": "错误途径",
        "god": "错误",
        "type": "special",
        "color": (139, 69, 19),
        "desc": "混乱与变异之道，拥抱错误的力量",
        "sequences": {
            9: {"name": "偷盗者", "skills": ["诅咒"], "hp": 90, "attack": 16, "defense": 6, "speed": 5},
            8: {"name": "诈骗师", "skills": ["诅咒", "混乱领域"], "hp": 135, "attack": 26, "defense": 9, "speed": 5},
            7: {"name": "密室学者", "skills": ["诅咒", "混乱领域", "变异"], "hp": 190, "attack": 40, "defense": 14, "speed": 6},
            6: {"name": "盗火人", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 270, "attack": 60, "defense": 20, "speed": 6},
            5: {"name": "筑梦家", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 370, "attack": 85, "defense": 28, "speed": 7},
            4: {"name": "寄生者", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 500, "attack": 120, "defense": 40, "speed": 7},
            3: {"name": "欺骗导师", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 720, "attack": 180, "defense": 58, "speed": 8},
            2: {"name": "命运木马", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 1050, "attack": 280, "defense": 90, "speed": 9},
            1: {"name": "时之虫", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 1550, "attack": 450, "defense": 135, "speed": 10},
            0: {"name": "错误", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 3100, "attack": 800, "defense": 220, "speed": 12},
        }
    },

    # ===== 4. 正义/隐秘途径 =====
    "隐秘": {
        "name": "隐秘途径",
        "god": "隐秘侍者",
        "type": "control",
        "color": (128, 0, 128),
        "desc": "精神与控制之道，操纵他人的心灵",
        "sequences": {
            9: {"name": "观众", "skills": ["读心", "心灵冲击"], "hp": 85, "attack": 17, "defense": 4, "speed": 5},
            8: {"name": "读心者", "skills": ["读心", "心灵冲击", "催眠"], "hp": 125, "attack": 27, "defense": 7, "speed": 5},
            7: {"name": "心理医生", "skills": ["读心", "心灵冲击", "催眠", "梦境"], "hp": 175, "attack": 42, "defense": 10, "speed": 6},
            6: {"name": "催眠师", "skills": ["读心", "心灵冲击", "催眠", "梦境", "精神操控"], "hp": 250, "attack": 62, "defense": 15, "speed": 7},
            5: {"name": "梦境行者", "skills": ["读心", "心灵冲击", "催眠", "梦境", "精神操控"], "hp": 350, "attack": 88, "defense": 22, "speed": 8},
            4: {"name": "操控师", "skills": ["读心", "心灵冲击", "催眠", "梦境", "精神操控"], "hp": 480, "attack": 125, "defense": 32, "speed": 9},
            3: {"name": "扭梦人", "skills": ["读心", "心灵冲击", "催眠", "梦境", "精神操控"], "hp": 700, "attack": 190, "defense": 48, "speed": 10},
            2: {"name": "洞察者", "skills": ["读心", "心灵冲击", "催眠", "梦境", "精神操控"], "hp": 1000, "attack": 300, "defense": 75, "speed": 12},
            1: {"name": "作家", "skills": ["读心", "心灵冲击", "催眠", "梦境", "精神操控"], "hp": 1480, "attack": 480, "defense": 115, "speed": 14},
            0: {"name": "隐秘侍者", "skills": ["读心", "心灵冲击", "催眠", "梦境", "精神操控"], "hp": 2950, "attack": 850, "defense": 190, "speed": 18},
        }
    },

    # ===== 5. 倒吊人/暴风途径 =====
    "暴风": {
        "name": "暴风途径",
        "god": "风暴之主",
        "type": "support",
        "color": (0, 191, 255),
        "desc": "风暴与航海之道，掌控自然之力",
        "sequences": {
            9: {"name": "水手", "skills": ["风刃"], "hp": 100, "attack": 15, "defense": 5, "speed": 6},
            8: {"name": "暴怒之民", "skills": ["风刃", "海浪冲击"], "hp": 150, "attack": 25, "defense": 8, "speed": 7},
            7: {"name": "航海家", "skills": ["风刃", "海浪冲击", "风暴护盾"], "hp": 210, "attack": 40, "defense": 12, "speed": 8},
            6: {"name": "风管家", "skills": ["风刃", "海浪冲击", "风暴护盾", "闪电链"], "hp": 295, "attack": 60, "defense": 18, "speed": 10},
            5: {"name": "海洋主教", "skills": ["风刃", "海浪冲击", "风暴护盾", "闪电链", "暴风领域"], "hp": 405, "attack": 85, "defense": 26, "speed": 12},
            4: {"name": "灾难主教", "skills": ["风刃", "海浪冲击", "风暴护盾", "闪电链", "暴风领域"], "hp": 550, "attack": 120, "defense": 38, "speed": 14},
            3: {"name": "海王", "skills": ["风刃", "海浪冲击", "风暴护盾", "闪电链", "暴风领域"], "hp": 790, "attack": 180, "defense": 55, "speed": 17},
            2: {"name": "天灾", "skills": ["风刃", "海浪冲击", "风暴护盾", "闪电链", "暴风领域"], "hp": 1150, "attack": 280, "defense": 85, "speed": 20},
            1: {"name": "风暴天使", "skills": ["风刃", "海浪冲击", "风暴护盾", "闪电链", "暴风领域"], "hp": 1700, "attack": 450, "defense": 130, "speed": 24},
            0: {"name": "风暴之主", "skills": ["风刃", "海浪冲击", "风暴护盾", "闪电链", "暴风领域"], "hp": 3400, "attack": 800, "defense": 210, "speed": 30},
        }
    },

    # ===== 6. 太阳途径 =====
    "太阳": {
        "name": "太阳途径",
        "god": "永恒烈阳",
        "type": "magic",
        "color": (255, 200, 0),
        "desc": "光明与治愈之道，驱散一切黑暗",
        "sequences": {
            9: {"name": "歌颂者", "skills": ["圣光", "治疗"], "hp": 110, "attack": 14, "defense": 6, "speed": 4},
            8: {"name": "折光者", "skills": ["圣光", "治疗", "光明祝福"], "hp": 165, "attack": 24, "defense": 10, "speed": 5},
            7: {"name": "太阳神官", "skills": ["圣光", "治疗", "光明祝福", "净化"], "hp": 230, "attack": 38, "defense": 15, "speed": 5},
            6: {"name": "公证人", "skills": ["圣光", "治疗", "光明祝福", "净化", "阳光之怒"], "hp": 320, "attack": 58, "defense": 22, "speed": 6},
            5: {"name": "光之学司", "skills": ["圣光", "治疗", "光明祝福", "净化", "阳光之怒"], "hp": 440, "attack": 82, "defense": 32, "speed": 6},
            4: {"name": "无暇者", "skills": ["圣光", "治疗", "光明祝福", "净化", "阳光之怒"], "hp": 600, "attack": 118, "defense": 45, "speed": 7},
            3: {"name": "正义导师", "skills": ["圣光", "治疗", "光明祝福", "净化", "阳光之怒"], "hp": 860, "attack": 178, "defense": 65, "speed": 8},
            2: {"name": "逐日者", "skills": ["圣光", "治疗", "光明祝福", "净化", "阳光之怒"], "hp": 1250, "attack": 278, "defense": 100, "speed": 10},
            1: {"name": "纯白天使", "skills": ["圣光", "治疗", "光明祝福", "净化", "阳光之怒"], "hp": 1850, "attack": 448, "defense": 150, "speed": 12},
            0: {"name": "太阳", "skills": ["圣光", "治疗", "光明祝福", "净化", "阳光之怒"], "hp": 3700, "attack": 800, "defense": 250, "speed": 15},
        }
    },

    # ===== 7. 阅读者/智慧途径 =====
    "智慧": {
        "name": "智慧途径",
        "god": "智慧之神",
        "type": "wisdom",
        "color": (70, 130, 180),
        "desc": "知识与鉴定之道，探索世界的真理",
        "sequences": {
            9: {"name": "阅读者", "skills": ["知识之光", "弱点分析"], "hp": 85, "attack": 14, "defense": 4, "speed": 5},
            8: {"name": "推理学员", "skills": ["知识之光", "弱点分析"], "hp": 127, "attack": 24, "defense": 7, "speed": 5},
            7: {"name": "守知者", "skills": ["知识之光", "弱点分析"], "hp": 178, "attack": 38, "defense": 10, "speed": 6},
            6: {"name": "博学者", "skills": ["知识之光", "弱点分析"], "hp": 255, "attack": 58, "defense": 15, "speed": 6},
            5: {"name": "秘术导师", "skills": ["知识之光", "弱点分析"], "hp": 350, "attack": 82, "defense": 22, "speed": 7},
            4: {"name": "预言家", "skills": ["知识之光", "弱点分析"], "hp": 480, "attack": 118, "defense": 32, "speed": 8},
            3: {"name": "洞悉者", "skills": ["知识之光", "弱点分析"], "hp": 690, "attack": 178, "defense": 48, "speed": 9},
            2: {"name": "智天使", "skills": ["知识之光", "弱点分析"], "hp": 1000, "attack": 278, "defense": 75, "speed": 10},
            1: {"name": "全知之眼", "skills": ["知识之光", "弱点分析"], "hp": 1480, "attack": 448, "defense": 115, "speed": 12},
            0: {"name": "智慧之神", "skills": ["知识之光", "弱点分析"], "hp": 2960, "attack": 800, "defense": 190, "speed": 15},
        }
    },

    # ===== 8. 秘祈人/黑夜途径 =====
    "黑夜": {
        "name": "黑夜途径",
        "god": "永夜女神",
        "type": "magic",
        "color": (25, 25, 112),
        "desc": "黑暗与隐匿之道，夜幕下的猎手",
        "sequences": {
            9: {"name": "倾听者", "skills": ["暗影潜行", "黑暗侵蚀"], "hp": 90, "attack": 16, "defense": 5, "speed": 6},
            8: {"name": "隐修士", "skills": ["暗影潜行", "黑暗侵蚀", "恐惧"], "hp": 135, "attack": 26, "defense": 8, "speed": 7},
            7: {"name": "蔷薇主教", "skills": ["暗影潜行", "黑暗侵蚀", "恐惧", "暗影刺杀"], "hp": 190, "attack": 42, "defense": 12, "speed": 8},
            6: {"name": "牧羊人", "skills": ["暗影潜行", "黑暗侵蚀", "恐惧", "暗影刺杀"], "hp": 270, "attack": 62, "defense": 18, "speed": 10},
            5: {"name": "黑骑士", "skills": ["暗影潜行", "黑暗侵蚀", "恐惧", "暗影刺杀"], "hp": 370, "attack": 88, "defense": 26, "speed": 12},
            4: {"name": "三首圣堂", "skills": ["暗影潜行", "黑暗侵蚀", "恐惧", "暗影刺杀"], "hp": 500, "attack": 125, "defense": 38, "speed": 14},
            3: {"name": "移语长老", "skills": ["暗影潜行", "黑暗侵蚀", "恐惧", "暗影刺杀"], "hp": 720, "attack": 190, "defense": 55, "speed": 17},
            2: {"name": "暗天使", "skills": ["暗影潜行", "黑暗侵蚀", "恐惧", "暗影刺杀"], "hp": 1050, "attack": 295, "defense": 85, "speed": 20},
            1: {"name": "苍白皇帝", "skills": ["暗影潜行", "黑暗侵蚀", "恐惧", "暗影刺杀"], "hp": 1550, "attack": 475, "defense": 130, "speed": 24},
            0: {"name": "黑暗", "skills": ["暗影潜行", "黑暗侵蚀", "恐惧", "暗影刺杀"], "hp": 3100, "attack": 850, "defense": 210, "speed": 30},
        }
    },

    # ===== 9. 收尸人/死亡途径 =====
    "死亡": {
        "name": "死亡途径",
        "god": "死神",
        "type": "magic",
        "color": (47, 79, 79),
        "desc": "死灵与亡魂之道，掌控生死轮回",
        "sequences": {
            9: {"name": "掘墓人", "skills": ["召唤亡灵", "灵魂抽取"], "hp": 95, "attack": 17, "defense": 5, "speed": 4},
            8: {"name": "通灵者", "skills": ["召唤亡灵", "灵魂抽取", "死亡之触"], "hp": 142, "attack": 28, "defense": 8, "speed": 4},
            7: {"name": "死灵导师", "skills": ["召唤亡灵", "灵魂抽取", "死亡之触", "亡灵大军"], "hp": 200, "attack": 44, "defense": 12, "speed": 5},
            6: {"name": "看门人", "skills": ["召唤亡灵", "灵魂抽取", "死亡之触", "亡灵大军"], "hp": 285, "attack": 66, "defense": 18, "speed": 5},
            5: {"name": "不死者", "skills": ["召唤亡灵", "灵魂抽取", "死亡之触", "亡灵大军"], "hp": 390, "attack": 94, "defense": 26, "speed": 6},
            4: {"name": "摆渡人", "skills": ["召唤亡灵", "灵魂抽取", "死亡之触", "亡灵大军"], "hp": 530, "attack": 133, "defense": 38, "speed": 6},
            3: {"name": "死亡执政官", "skills": ["召唤亡灵", "灵魂抽取", "死亡之触", "亡灵大军"], "hp": 760, "attack": 200, "defense": 55, "speed": 7},
            2: {"name": "厄运祭司", "skills": ["召唤亡灵", "灵魂抽取", "死亡之触", "亡灵大军"], "hp": 1100, "attack": 310, "defense": 85, "speed": 8},
            1: {"name": "死亡天使", "skills": ["召唤亡灵", "灵魂抽取", "死亡之触", "亡灵大军"], "hp": 1620, "attack": 500, "defense": 130, "speed": 10},
            0: {"name": "死神", "skills": ["召唤亡灵", "灵魂抽取", "死亡之触", "亡灵大军"], "hp": 3250, "attack": 890, "defense": 210, "speed": 12},
        }
    },

    # ===== 10. 星星/命运途径 =====
    "命运": {
        "name": "命运途径",
        "god": "命运",
        "type": "control",
        "color": (255, 215, 0),
        "desc": "概率与运气之道，玩弄命运于股掌",
        "sequences": {
            9: {"name": "不眠者", "skills": ["幸运一击"], "hp": 90, "attack": 14, "defense": 5, "speed": 6},
            8: {"name": "午夜诗人", "skills": ["幸运一击", "厄运转移"], "hp": 135, "attack": 24, "defense": 8, "speed": 7},
            7: {"name": "梦魇", "skills": ["幸运一击", "厄运转移", "概率操控"], "hp": 190, "attack": 38, "defense": 12, "speed": 8},
            6: {"name": "安魂师", "skills": ["幸运一击", "厄运转移", "概率操控", "灾难降临"], "hp": 270, "attack": 58, "defense": 18, "speed": 9},
            5: {"name": "守门人", "skills": ["幸运一击", "厄运转移", "概率操控", "灾难降临"], "hp": 370, "attack": 82, "defense": 26, "speed": 10},
            4: {"name": "恶愿主教", "skills": ["幸运一击", "厄运转移", "概率操控", "灾难降临"], "hp": 500, "attack": 118, "defense": 38, "speed": 11},
            3: {"name": "隐秘主教", "skills": ["幸运一击", "厄运转移", "概率操控", "灾难降临"], "hp": 720, "attack": 178, "defense": 55, "speed": 13},
            2: {"name": "厄运者", "skills": ["幸运一击", "厄运转移", "概率操控", "灾难降临"], "hp": 1050, "attack": 278, "defense": 85, "speed": 15},
            1: {"name": "黑暗天使", "skills": ["幸运一击", "厄运转移", "概率操控", "灾难降临"], "hp": 1550, "attack": 448, "defense": 130, "speed": 18},
            0: {"name": "黑夜", "skills": ["幸运一击", "厄运转移", "概率操控", "灾难降临"], "hp": 3100, "attack": 800, "defense": 210, "speed": 22},
        }
    },

    # ===== 11. 战士途径 =====
    "战争": {
        "name": "战争途径",
        "god": "战神",
        "type": "melee",
        "color": (178, 34, 34),
        "desc": "纯粹的武力之道，战场上的王者",
        "sequences": {
            9: {"name": "战士", "skills": ["重击", "冲锋"], "hp": 130, "attack": 20, "defense": 7, "speed": 5},
            8: {"name": "格斗家", "skills": ["重击", "冲锋", "战吼"], "hp": 195, "attack": 32, "defense": 12, "speed": 5},
            7: {"name": "武器大师", "skills": ["重击", "冲锋", "战吼", "铁壁"], "hp": 280, "attack": 50, "defense": 18, "speed": 6},
            6: {"name": "黎明骑士", "skills": ["重击", "冲锋", "战吼", "铁壁", "处决"], "hp": 400, "attack": 75, "defense": 28, "speed": 6},
            5: {"name": "守护者", "skills": ["重击", "冲锋", "战吼", "铁壁", "处决"], "hp": 550, "attack": 106, "defense": 40, "speed": 7},
            4: {"name": "猎魔者", "skills": ["重击", "冲锋", "战吼", "铁壁", "处决"], "hp": 750, "attack": 150, "defense": 55, "speed": 7},
            3: {"name": "银骑士", "skills": ["重击", "冲锋", "战吼", "铁壁", "处决"], "hp": 1080, "attack": 225, "defense": 80, "speed": 8},
            2: {"name": "荣耀者", "skills": ["重击", "冲锋", "战吼", "铁壁", "处决"], "hp": 1560, "attack": 350, "defense": 125, "speed": 9},
            1: {"name": "神明之子", "skills": ["重击", "冲锋", "战吼", "铁壁", "处决"], "hp": 2300, "attack": 560, "defense": 190, "speed": 11},
            0: {"name": "战神", "skills": ["重击", "冲锋", "战吼", "铁壁", "处决"], "hp": 4600, "attack": 1000, "defense": 320, "speed": 14},
        }
    },

    # ===== 12. 刺客/魔女途径 =====
    "刺客": {
        "name": "刺客途径",
        "god": "隐者",
        "type": "special",
        "color": (0, 0, 0),
        "desc": "暗杀与隐匿之道，黑暗中的死神",
        "sequences": {
            9: {"name": "刺客", "skills": ["潜行", "背刺"], "hp": 80, "attack": 22, "defense": 3, "speed": 8},
            8: {"name": "教唆者", "skills": ["潜行", "背刺", "毒刃"], "hp": 120, "attack": 35, "defense": 5, "speed": 9},
            7: {"name": "女巫", "skills": ["潜行", "背刺", "毒刃", "影分身"], "hp": 168, "attack": 55, "defense": 8, "speed": 10},
            6: {"name": "欢愉魔女", "skills": ["潜行", "背刺", "毒刃", "影分身"], "hp": 240, "attack": 82, "defense": 12, "speed": 12},
            5: {"name": "绝望魔女", "skills": ["潜行", "背刺", "毒刃", "影分身"], "hp": 330, "attack": 116, "defense": 18, "speed": 14},
            4: {"name": "不老魔女", "skills": ["潜行", "背刺", "毒刃", "影分身"], "hp": 450, "attack": 165, "defense": 26, "speed": 16},
            3: {"name": "灾难魔女", "skills": ["潜行", "背刺", "毒刃", "影分身"], "hp": 650, "attack": 248, "defense": 38, "speed": 19},
            2: {"name": "末日", "skills": ["潜行", "背刺", "毒刃", "影分身"], "hp": 940, "attack": 385, "defense": 60, "speed": 22},
            1: {"name": "黑巫王", "skills": ["潜行", "背刺", "毒刃", "影分身"], "hp": 1400, "attack": 620, "defense": 92, "speed": 26},
            0: {"name": "魔女", "skills": ["潜行", "背刺", "毒刃", "影分身"], "hp": 2800, "attack": 1100, "defense": 150, "speed": 35},
        }
    },

    # ===== 13. 猎人途径 =====
    "猎人": {
        "name": "猎人途径",
        "god": "红祭司",
        "type": "melee",
        "color": (139, 0, 0),
        "desc": "猎杀与鲜血之道，嗜血的狩猎者",
        "sequences": {
            9: {"name": "猎人", "skills": ["追踪", "致命射击"], "hp": 105, "attack": 19, "defense": 5, "speed": 6},
            8: {"name": "挑衅家", "skills": ["追踪", "致命射击", "血怒"], "hp": 157, "attack": 31, "defense": 8, "speed": 7},
            7: {"name": "阴谋家", "skills": ["追踪", "致命射击", "血怒", "鲜血汲取"], "hp": 220, "attack": 48, "defense": 12, "speed": 8},
            6: {"name": "收割者", "skills": ["追踪", "致命射击", "血怒", "鲜血汲取"], "hp": 310, "attack": 72, "defense": 18, "speed": 9},
            5: {"name": "铁血骑士", "skills": ["追踪", "致命射击", "血怒", "鲜血汲取"], "hp": 425, "attack": 102, "defense": 26, "speed": 10},
            4: {"name": "战争主教", "skills": ["追踪", "致命射击", "血怒", "鲜血汲取"], "hp": 580, "attack": 145, "defense": 38, "speed": 12},
            3: {"name": "征服", "skills": ["追踪", "致命射击", "血怒", "鲜血汲取"], "hp": 830, "attack": 218, "defense": 55, "speed": 14},
            2: {"name": "天气术士", "skills": ["追踪", "致命射击", "血怒", "鲜血汲取"], "hp": 1200, "attack": 340, "defense": 85, "speed": 16},
            1: {"name": "血之始祖", "skills": ["追踪", "致命射击", "血怒", "鲜血汲取"], "hp": 1780, "attack": 545, "defense": 130, "speed": 19},
            0: {"name": "红祭司", "skills": ["追踪", "致命射击", "血怒", "鲜血汲取"], "hp": 3560, "attack": 970, "defense": 210, "speed": 24},
        }
    },

    # ===== 14. 隐者途径 =====
    "隐者": {
        "name": "隐者途径",
        "god": "隐者",
        "type": "special",
        "color": (100, 100, 100),
        "desc": "窥探与隐匿之道，知识的守护者",
        "sequences": {
            9: {"name": "窥秘人", "skills": ["洞察", "精神干扰"], "hp": 85, "attack": 14, "defense": 4, "speed": 5},
            8: {"name": "格斗学者", "skills": ["洞察", "精神干扰"], "hp": 127, "attack": 24, "defense": 7, "speed": 5},
            7: {"name": "王牌", "skills": ["洞察", "精神干扰", "操纵"], "hp": 178, "attack": 38, "defense": 10, "speed": 6},
            6: {"name": "卷轴教授", "skills": ["洞察", "精神干扰", "操纵", "主宰意志"], "hp": 255, "attack": 58, "defense": 15, "speed": 7},
            5: {"name": "神秘学家", "skills": ["洞察", "精神干扰", "操纵", "主宰意志"], "hp": 350, "attack": 82, "defense": 22, "speed": 8},
            4: {"name": "星象师", "skills": ["洞察", "精神干扰", "操纵", "主宰意志"], "hp": 480, "attack": 118, "defense": 32, "speed": 9},
            3: {"name": "预言大师", "skills": ["洞察", "精神干扰", "操纵", "主宰意志"], "hp": 690, "attack": 178, "defense": 48, "speed": 10},
            2: {"name": "搜寻者", "skills": ["洞察", "精神干扰", "操纵", "主宰意志"], "hp": 1000, "attack": 278, "defense": 75, "speed": 12},
            1: {"name": "知识皇帝", "skills": ["洞察", "精神干扰", "操纵", "主宰意志"], "hp": 1480, "attack": 448, "defense": 115, "speed": 14},
            0: {"name": "隐者", "skills": ["洞察", "精神干扰", "操纵", "主宰意志"], "hp": 2960, "attack": 800, "defense": 190, "speed": 18},
        }
    },

    # ===== 15. 通道学者/考古学家途径 =====
    "考古": {
        "name": "考古途径",
        "god": "知识与智慧之神",
        "type": "wisdom",
        "color": (150, 120, 90),
        "desc": "历史与考古之道，发掘远古的秘密",
        "sequences": {
            9: {"name": "通道学者", "skills": ["知识之光", "弱点分析"], "hp": 88, "attack": 14, "defense": 5, "speed": 5},
            8: {"name": "考古学家", "skills": ["知识之光", "弱点分析"], "hp": 132, "attack": 24, "defense": 8, "speed": 5},
            7: {"name": "鉴定师", "skills": ["知识之光", "弱点分析"], "hp": 185, "attack": 38, "defense": 12, "speed": 6},
            6: {"name": "机械专家", "skills": ["知识之光", "弱点分析"], "hp": 264, "attack": 58, "defense": 18, "speed": 7},
            5: {"name": "天文学家", "skills": ["知识之光", "弱点分析"], "hp": 362, "attack": 82, "defense": 26, "speed": 8},
            4: {"name": "炼金术士", "skills": ["知识之光", "弱点分析"], "hp": 495, "attack": 118, "defense": 38, "speed": 9},
            3: {"name": "神秘学家", "skills": ["知识之光", "弱点分析"], "hp": 710, "attack": 178, "defense": 55, "speed": 10},
            2: {"name": "知识导师", "skills": ["知识之光", "弱点分析"], "hp": 1030, "attack": 278, "defense": 85, "speed": 12},
            1: {"name": "启蒙者", "skills": ["知识之光", "弱点分析"], "hp": 1520, "attack": 448, "defense": 130, "speed": 14},
            0: {"name": "完美者", "skills": ["知识之光", "弱点分析"], "hp": 3050, "attack": 800, "defense": 210, "speed": 18},
        }
    },

    # ===== 16. 怪物/畸变途径 =====
    "畸变": {
        "name": "畸变途径",
        "god": "命运/水银之蛇",
        "type": "special",
        "color": (100, 50, 100),
        "desc": "变异与怪物之道，突破人类的极限",
        "sequences": {
            9: {"name": "怪物", "skills": ["变异", "疫病"], "hp": 100, "attack": 16, "defense": 6, "speed": 5},
            8: {"name": "机器", "skills": ["变异", "疫病"], "hp": 150, "attack": 26, "defense": 10, "speed": 5},
            7: {"name": "幸运者", "skills": ["变异", "疫病"], "hp": 210, "attack": 42, "defense": 15, "speed": 6},
            6: {"name": "厄运教士", "skills": ["变异", "疫病"], "hp": 300, "attack": 62, "defense": 22, "speed": 6},
            5: {"name": "赢家", "skills": ["变异", "疫病"], "hp": 410, "attack": 88, "defense": 30, "speed": 7},
            4: {"name": "厄运法师", "skills": ["变异", "疫病"], "hp": 560, "attack": 125, "defense": 42, "speed": 8},
            3: {"name": "混乱行者", "skills": ["变异", "疫病"], "hp": 800, "attack": 188, "defense": 60, "speed": 9},
            2: {"name": "不知", "skills": ["变异", "疫病"], "hp": 1160, "attack": 295, "defense": 92, "speed": 10},
            1: {"name": "巨蛇", "skills": ["变异", "疫病"], "hp": 1720, "attack": 475, "defense": 140, "speed": 12},
            0: {"name": "命运之轮", "skills": ["变异", "疫病"], "hp": 3440, "attack": 850, "defense": 230, "speed": 15},
        }
    },

    # ===== 17. 囚犯/罪犯途径 =====
    "罪犯": {
        "name": "罪犯途径",
        "god": "野兽主/骸骨王座",
        "type": "special",
        "color": (80, 60, 50),
        "desc": "囚禁与束缚之道，挣脱命运的枷锁",
        "sequences": {
            9: {"name": "囚犯", "skills": ["诅咒", "混乱领域"], "hp": 95, "attack": 15, "defense": 5, "speed": 5},
            8: {"name": "疯子", "skills": ["诅咒", "混乱领域"], "hp": 142, "attack": 25, "defense": 8, "speed": 5},
            7: {"name": "狼人", "skills": ["诅咒", "混乱领域", "变异"], "hp": 200, "attack": 40, "defense": 12, "speed": 6},
            6: {"name": "活尸", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 285, "attack": 60, "defense": 18, "speed": 6},
            5: {"name": "怨魂", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 390, "attack": 85, "defense": 26, "speed": 7},
            4: {"name": "木偶", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 530, "attack": 120, "defense": 38, "speed": 7},
            3: {"name": "沉默门徒", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 760, "attack": 180, "defense": 55, "speed": 8},
            2: {"name": "古代巫物", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 1100, "attack": 280, "defense": 85, "speed": 9},
            1: {"name": "神躯", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 1620, "attack": 450, "defense": 130, "speed": 10},
            0: {"name": "黑暗之父", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 3250, "attack": 800, "defense": 210, "speed": 12},
        }
    },

    # ===== 18. 罪犯/折翼天使途径 =====
    "堕落": {
        "name": "堕落途径",
        "god": "深渊",
        "type": "special",
        "color": (60, 40, 80),
        "desc": "堕落与腐化之道，黑暗中的诱惑者",
        "sequences": {
            9: {"name": "罪犯", "skills": ["诅咒", "混乱领域"], "hp": 90, "attack": 16, "defense": 5, "speed": 5},
            8: {"name": "折翼天使", "skills": ["诅咒", "混乱领域"], "hp": 135, "attack": 26, "defense": 8, "speed": 5},
            7: {"name": "连环杀手", "skills": ["诅咒", "混乱领域", "变异"], "hp": 190, "attack": 42, "defense": 12, "speed": 6},
            6: {"name": "恶魔", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 270, "attack": 62, "defense": 18, "speed": 7},
            5: {"name": "欲望使徒", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 370, "attack": 88, "defense": 26, "speed": 8},
            4: {"name": "欲望魔女", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 500, "attack": 125, "defense": 38, "speed": 9},
            3: {"name": "啃噬者", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 720, "attack": 190, "defense": 55, "speed": 10},
            2: {"name": "鲜血大公", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 1050, "attack": 295, "defense": 85, "speed": 12},
            1: {"name": "污秽君王", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 1550, "attack": 475, "defense": 130, "speed": 14},
            0: {"name": "深渊", "skills": ["诅咒", "混乱领域", "变异", "疫病"], "hp": 3100, "attack": 850, "defense": 210, "speed": 18},
        }
    },

    # ===== 19. 审判/仲裁者途径 =====
    "审判": {
        "name": "审判途径",
        "god": "战神",
        "type": "melee",
        "color": (192, 192, 192),
        "desc": "正义与铁血之道，执行神圣审判",
        "sequences": {
            9: {"name": "休", "skills": ["重击", "战吼"], "hp": 120, "attack": 18, "defense": 8, "speed": 4},
            8: {"name": "仲裁人", "skills": ["重击", "战吼", "铁壁"], "hp": 180, "attack": 30, "defense": 14, "speed": 4},
            7: {"name": "治安官", "skills": ["重击", "战吼", "铁壁", "冲锋"], "hp": 260, "attack": 48, "defense": 22, "speed": 5},
            6: {"name": "审讯者", "skills": ["重击", "战吼", "铁壁", "冲锋", "处决"], "hp": 370, "attack": 72, "defense": 32, "speed": 5},
            5: {"name": "法官", "skills": ["重击", "战吼", "铁壁", "冲锋", "处决"], "hp": 510, "attack": 102, "defense": 45, "speed": 6},
            4: {"name": "迅疾骑士", "skills": ["重击", "战吼", "铁壁", "冲锋", "处决"], "hp": 700, "attack": 145, "defense": 62, "speed": 6},
            3: {"name": "令命法师", "skills": ["重击", "战吼", "铁壁", "冲锋", "处决"], "hp": 1000, "attack": 220, "defense": 90, "speed": 7},
            2: {"name": "混乱猎手", "skills": ["重击", "战吼", "铁壁", "冲锋", "处决"], "hp": 1450, "attack": 340, "defense": 140, "speed": 8},
            1: {"name": "平衡者", "skills": ["重击", "战吼", "铁壁", "冲锋", "处决"], "hp": 2150, "attack": 550, "defense": 210, "speed": 10},
            0: {"name": "审判者", "skills": ["重击", "战吼", "铁壁", "冲锋", "处决"], "hp": 4300, "attack": 980, "defense": 350, "speed": 12},
        }
    },

    # ===== 20. 律师途径 =====
    "律师": {
        "name": "律师途径",
        "god": "智慧之神",
        "type": "wisdom",
        "color": (105, 105, 105),
        "desc": "言语与契约之道，用语言编织世界",
        "sequences": {
            9: {"name": "律师", "skills": ["言灵", "契约束缚"], "hp": 88, "attack": 15, "defense": 4, "speed": 5},
            8: {"name": "野蛮人", "skills": ["言灵", "契约束缚"], "hp": 132, "attack": 25, "defense": 7, "speed": 5},
            7: {"name": "赌骰者", "skills": ["言灵", "契约束缚"], "hp": 185, "attack": 40, "defense": 10, "speed": 6},
            6: {"name": "腐化男爵", "skills": ["言灵", "契约束缚"], "hp": 264, "attack": 60, "defense": 15, "speed": 6},
            5: {"name": "混乱导师", "skills": ["言灵", "契约束缚"], "hp": 362, "attack": 85, "defense": 22, "speed": 7},
            4: {"name": "堕落伯爵", "skills": ["言灵", "契约束缚"], "hp": 495, "attack": 120, "defense": 32, "speed": 8},
            3: {"name": "疯乱法师", "skills": ["言灵", "契约束缚"], "hp": 710, "attack": 180, "defense": 48, "speed": 9},
            2: {"name": "搞之公爵", "skills": ["言灵", "契约束缚"], "hp": 1030, "attack": 280, "defense": 75, "speed": 10},
            1: {"name": "试序帝王", "skills": ["言灵", "契约束缚"], "hp": 1520, "attack": 450, "defense": 115, "speed": 12},
            0: {"name": "黑皇帝", "skills": ["言灵", "契约束缚"], "hp": 3050, "attack": 800, "defense": 190, "speed": 15},
        }
    },

    # ===== 21. 耕种者/驭兽途径 =====
    "驭兽": {
        "name": "驭兽途径",
        "god": "神母/大地母神",
        "type": "support",
        "color": (34, 139, 34),
        "desc": "召唤与变形之道，万兽之友",
        "sequences": {
            9: {"name": "耕种者", "skills": ["召唤野兽", "自然治愈"], "hp": 100, "attack": 13, "defense": 5, "speed": 5},
            8: {"name": "治疗师", "skills": ["召唤野兽", "自然治愈"], "hp": 150, "attack": 22, "defense": 8, "speed": 5},
            7: {"name": "丰收导引", "skills": ["召唤野兽", "自然治愈", "野性变身"], "hp": 210, "attack": 35, "defense": 12, "speed": 6},
            6: {"name": "生物学家", "skills": ["召唤野兽", "自然治愈", "野性变身", "精灵召唤"], "hp": 300, "attack": 54, "defense": 18, "speed": 7},
            5: {"name": "德鲁伊", "skills": ["召唤野兽", "自然治愈", "野性变身", "精灵召唤"], "hp": 410, "attack": 76, "defense": 26, "speed": 8},
            4: {"name": "古曲|古代炼金师", "skills": ["召唤野兽", "自然治愈", "野性变身", "精灵召唤"], "hp": 560, "attack": 110, "defense": 38, "speed": 9},
            3: {"name": "主宰", "skills": ["召唤野兽", "自然治愈", "野性变身", "精灵召唤"], "hp": 800, "attack": 166, "defense": 55, "speed": 10},
            2: {"name": "白噢大师", "skills": ["召唤野兽", "自然治愈", "野性变身", "精灵召唤"], "hp": 1160, "attack": 258, "defense": 85, "speed": 12},
            1: {"name": "创生", "skills": ["召唤野兽", "自然治愈", "野性变身", "精灵召唤"], "hp": 1710, "attack": 418, "defense": 130, "speed": 14},
            0: {"name": "美神", "skills": ["召唤野兽", "自然治愈", "野性变身", "精灵召唤"], "hp": 3420, "attack": 750, "defense": 210, "speed": 18},
        }
    },

    # ===== 22. 月亮/药师途径 =====
    "药师": {
        "name": "药师途径",
        "god": "月亮",
        "type": "support",
        "color": (200, 200, 220),
        "desc": "药剂与变形之道，生命的炼金术士",
        "sequences": {
            9: {"name": "药师", "skills": ["投掷药剂", "治疗药剂"], "hp": 95, "attack": 14, "defense": 5, "speed": 5},
            8: {"name": "驯兽师", "skills": ["投掷药剂", "治疗药剂", "毒雾"], "hp": 142, "attack": 24, "defense": 8, "speed": 5},
            7: {"name": "吸血鬼", "skills": ["投掷药剂", "治疗药剂", "毒雾", "变形"], "hp": 200, "attack": 38, "defense": 12, "speed": 6},
            6: {"name": "毒药教授", "skills": ["投掷药剂", "治疗药剂", "毒雾", "变形"], "hp": 285, "attack": 58, "defense": 18, "speed": 7},
            5: {"name": "深红|血族男爵", "skills": ["投掷药剂", "治疗药剂", "毒雾", "变形"], "hp": 390, "attack": 82, "defense": 26, "speed": 8},
            4: {"name": "主", "skills": ["投掷药剂", "治疗药剂", "毒雾", "变形"], "hp": 530, "attack": 118, "defense": 38, "speed": 9},
            3: {"name": "血族伯爵", "skills": ["投掷药剂", "治疗药剂", "毒雾", "变形"], "hp": 760, "attack": 178, "defense": 55, "speed": 10},
            2: {"name": "血族男爵", "skills": ["投掷药剂", "治疗药剂", "毒雾", "变形"], "hp": 1100, "attack": 278, "defense": 85, "speed": 12},
            1: {"name": "吸血鬼帝组", "skills": ["投掷药剂", "治疗药剂", "毒雾", "变形"], "hp": 1620, "attack": 448, "defense": 130, "speed": 14},
            0: {"name": "月亮", "skills": ["投掷药剂", "治疗药剂", "毒雾", "变形"], "hp": 3250, "attack": 800, "defense": 210, "speed": 18},
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
