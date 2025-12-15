"""
任务数据定义 - 剧情任务系统
"""

# 任务类型
QUEST_TYPE_MAIN = "main"      # 主线任务
QUEST_TYPE_SIDE = "side"      # 支线任务
QUEST_TYPE_DAILY = "daily"    # 日常任务

# 任务状态
QUEST_STATUS_LOCKED = "locked"        # 未解锁
QUEST_STATUS_AVAILABLE = "available"  # 可接取
QUEST_STATUS_ACTIVE = "active"        # 进行中
QUEST_STATUS_COMPLETE = "complete"    # 已完成（待提交）
QUEST_STATUS_FINISHED = "finished"    # 已完成（已提交）

# 目标类型
OBJECTIVE_KILL = "kill"           # 击杀敌人
OBJECTIVE_COLLECT = "collect"     # 收集物品
OBJECTIVE_REACH_WAVE = "wave"     # 达到波次
OBJECTIVE_CRAFT = "craft"         # 炮制魔药
OBJECTIVE_TALK = "talk"           # 对话
OBJECTIVE_ADVANCE = "advance"     # 晋升序列
OBJECTIVE_BOSS = "boss"           # 击杀Boss
OBJECTIVE_SURVIVE = "survive"     # 限时生存
OBJECTIVE_NO_DAMAGE = "no_damage" # 无伤挑战
OBJECTIVE_COMBO = "combo"         # 连击数
OBJECTIVE_EQUIP = "equip"         # 装备武器
OBJECTIVE_GOLD = "gold"           # 获得金币

# 任务难度
QUEST_DIFFICULTY_EASY = "easy"
QUEST_DIFFICULTY_NORMAL = "normal"
QUEST_DIFFICULTY_HARD = "hard"
QUEST_DIFFICULTY_NIGHTMARE = "nightmare"

DIFFICULTY_NAMES = {
    "easy": "简单",
    "normal": "普通",
    "hard": "困难",
    "nightmare": "噩梦"
}

# ==================== 主线任务 ====================
MAIN_QUESTS = {
    # === 第一章：初入非凡 ===
    "main_001": {
        "name": "初入非凡之路",
        "chapter": 1,
        "type": QUEST_TYPE_MAIN,
        "desc": "你感受到了体内涌动的非凡力量，是时候开始你的非凡之旅了。",
        "objectives": [
            {"type": OBJECTIVE_KILL, "target": "低级邪灵", "count": 3, "desc": "击杀低级邪灵"},
        ],
        "rewards": {
            "exp": 50,
            "materials": {"蒸馏水": 2, "黑曜石粉": 1},
        },
        "dialogue_start": [
            {"speaker": "旁白", "text": "贝克兰德的夜晚总是充满危险..."},
            {"speaker": "旁白", "text": "你感受到一股邪异的气息从黑暗中涌来。"},
            {"speaker": "???", "text": "新晋的非凡者吗？让我看看你有多少本事！"},
        ],
        "dialogue_end": [
            {"speaker": "旁白", "text": "你成功击退了邪灵的袭击。"},
            {"speaker": "旁白", "text": "这只是开始，更大的危险还在等待着你..."},
        ],
        "unlock_quests": ["main_002"],
        "required_sequence": 9,
    },

    "main_002": {
        "name": "收集魔药材料",
        "chapter": 1,
        "type": QUEST_TYPE_MAIN,
        "desc": "要变得更强，你需要炮制魔药晋升序列。先收集必要的材料吧。",
        "objectives": [
            {"type": OBJECTIVE_COLLECT, "target": "夜香花", "count": 2, "desc": "收集夜香花"},
            {"type": OBJECTIVE_COLLECT, "target": "冷杉精华", "count": 1, "desc": "收集冷杉精华"},
        ],
        "rewards": {
            "exp": 80,
            "materials": {"蒸馏水": 3},
        },
        "dialogue_start": [
            {"speaker": "神秘商人", "text": "年轻的非凡者，我看得出你渴望力量。"},
            {"speaker": "神秘商人", "text": "想要晋升序列，你需要炮制魔药。"},
            {"speaker": "神秘商人", "text": "去收集一些材料吧，击杀怪物可以获得它们。"},
        ],
        "dialogue_end": [
            {"speaker": "神秘商人", "text": "很好，你收集到了所需的材料。"},
            {"speaker": "神秘商人", "text": "按下'I'打开背包，在炮制界面可以合成魔药。"},
        ],
        "prerequisites": ["main_001"],
        "unlock_quests": ["main_003"],
        "required_sequence": 9,
    },

    "main_003": {
        "name": "首次晋升",
        "chapter": 1,
        "type": QUEST_TYPE_MAIN,
        "desc": "你已经收集了足够的材料，是时候炮制魔药并晋升了！",
        "objectives": [
            {"type": OBJECTIVE_ADVANCE, "target": 8, "count": 1, "desc": "晋升至序列8"},
        ],
        "rewards": {
            "exp": 150,
            "materials": {"银月草汁": 2, "魔鬼蛆": 1},
        },
        "dialogue_start": [
            {"speaker": "旁白", "text": "你感受到体内的灵性已经足够支撑晋升了。"},
            {"speaker": "旁白", "text": "打开背包，在炮制界面合成魔药并服用。"},
        ],
        "dialogue_end": [
            {"speaker": "旁白", "text": "一股强大的力量涌入你的身体！"},
            {"speaker": "旁白", "text": "你成功晋升了！新的能力已经觉醒。"},
            {"speaker": "旁白", "text": "但这只是开始，更强大的敌人也将出现..."},
        ],
        "prerequisites": ["main_002"],
        "unlock_quests": ["main_004"],
        "required_sequence": 9,
    },

    # === 第二章：暗流涌动 ===
    "main_004": {
        "name": "极光会的阴谋",
        "chapter": 2,
        "type": QUEST_TYPE_MAIN,
        "desc": "你发现了极光会的踪迹，他们似乎在策划什么阴谋...",
        "objectives": [
            {"type": OBJECTIVE_KILL, "target": "堕落非凡者", "count": 5, "desc": "击杀堕落非凡者"},
            {"type": OBJECTIVE_REACH_WAVE, "target": 5, "count": 1, "desc": "生存至第5波"},
        ],
        "rewards": {
            "exp": 200,
            "materials": {"梦境尘埃": 2, "九叶莲": 1},
        },
        "dialogue_start": [
            {"speaker": "线人", "text": "极光会最近活动频繁，他们在召集堕落的非凡者。"},
            {"speaker": "线人", "text": "小心，他们比普通邪灵危险得多。"},
            {"speaker": "旁白", "text": "你决定深入调查这个神秘组织..."},
        ],
        "dialogue_end": [
            {"speaker": "旁白", "text": "你成功挫败了极光会的一次行动。"},
            {"speaker": "神秘声音", "text": "有趣的小老鼠...我们会再见面的。"},
        ],
        "prerequisites": ["main_003"],
        "unlock_quests": ["main_005"],
        "required_sequence": 8,
    },

    "main_005": {
        "name": "序列8的门槛",
        "chapter": 2,
        "type": QUEST_TYPE_MAIN,
        "desc": "为了对抗极光会，你需要变得更强。收集稀有材料准备晋升。",
        "objectives": [
            {"type": OBJECTIVE_COLLECT, "target": "梦境尘埃", "count": 2, "desc": "收集梦境尘埃"},
            {"type": OBJECTIVE_COLLECT, "target": "九叶莲", "count": 1, "desc": "收集九叶莲"},
            {"type": OBJECTIVE_KILL, "target": "梦魇", "count": 10, "desc": "击杀梦魇"},
        ],
        "rewards": {
            "exp": 250,
            "materials": {"灵银粉": 2},
        },
        "dialogue_start": [
            {"speaker": "旁白", "text": "要对抗极光会，你现在的力量还不够。"},
            {"speaker": "旁白", "text": "梦魇是梦境力量的具现，击杀它们可以获得稀有材料。"},
        ],
        "dialogue_end": [
            {"speaker": "旁白", "text": "你感受到自己距离更高的境界只有一步之遥。"},
        ],
        "prerequisites": ["main_004"],
        "unlock_quests": ["main_006"],
        "required_sequence": 8,
    },

    "main_006": {
        "name": "再次晋升",
        "chapter": 2,
        "type": QUEST_TYPE_MAIN,
        "desc": "材料已经齐全，是时候突破序列8的门槛了！",
        "objectives": [
            {"type": OBJECTIVE_ADVANCE, "target": 7, "count": 1, "desc": "晋升至序列7"},
        ],
        "rewards": {
            "exp": 300,
            "materials": {"深红月晶": 1, "太阳圣水": 1},
        },
        "dialogue_start": [
            {"speaker": "旁白", "text": "你已经准备好了，开始炮制魔药吧。"},
        ],
        "dialogue_end": [
            {"speaker": "旁白", "text": "强大的力量在你体内觉醒！"},
            {"speaker": "旁白", "text": "你已经成为了真正的非凡者。"},
            {"speaker": "旁白", "text": "现在，是时候直面极光会的首领了..."},
        ],
        "prerequisites": ["main_005"],
        "unlock_quests": ["main_007"],
        "required_sequence": 8,
    },

    # === 第三章：终极对决 ===
    "main_007": {
        "name": "极光会主教",
        "chapter": 3,
        "type": QUEST_TYPE_MAIN,
        "desc": "极光会主教现身了！这是一场决定命运的战斗！",
        "objectives": [
            {"type": OBJECTIVE_KILL, "target": "极光会主教", "count": 1, "desc": "击败极光会主教"},
        ],
        "rewards": {
            "exp": 500,
            "materials": {"腐化之心": 1, "极光碎片": 1},
        },
        "dialogue_start": [
            {"speaker": "极光会主教", "text": "没想到你真的追到这里来了..."},
            {"speaker": "极光会主教", "text": "既然如此，就让我亲自送你上路吧！"},
            {"speaker": "旁白", "text": "一场生死之战即将展开！"},
        ],
        "dialogue_end": [
            {"speaker": "旁白", "text": "极光会主教倒下了！"},
            {"speaker": "极光会主教", "text": "不...不可能...这只是开始..."},
            {"speaker": "旁白", "text": "你取得了重大的胜利，但隐约感觉到更大的阴谋还在酝酿中..."},
            {"speaker": "旁白", "text": "【第一部分完】"},
            {"speaker": "旁白", "text": "感谢游玩！更多内容敬请期待..."},
        ],
        "prerequisites": ["main_006"],
        "unlock_quests": [],
        "required_sequence": 7,
        "is_final": True,
    },
}

# ==================== 支线任务 ====================
SIDE_QUESTS = {
    "side_001": {
        "name": "清理邪灵",
        "type": QUEST_TYPE_SIDE,
        "desc": "贝克兰德的街头邪灵横行，帮助清理它们吧。",
        "objectives": [
            {"type": OBJECTIVE_KILL, "target": "低级邪灵", "count": 10, "desc": "击杀低级邪灵"},
        ],
        "rewards": {
            "exp": 100,
            "materials": {"夜香花": 2, "星辰草": 1},
        },
        "dialogue_start": [
            {"speaker": "市民", "text": "求求你，帮帮我们！"},
            {"speaker": "市民", "text": "最近街上出现了很多邪灵，我们都不敢出门了。"},
        ],
        "dialogue_end": [
            {"speaker": "市民", "text": "太感谢你了！愿女神保佑你！"},
        ],
        "repeatable": False,
        "required_sequence": 9,
    },

    "side_002": {
        "name": "活尸横行",
        "type": QUEST_TYPE_SIDE,
        "desc": "墓地附近出现了大量活尸，需要有人去处理。",
        "objectives": [
            {"type": OBJECTIVE_KILL, "target": "活尸", "count": 15, "desc": "击杀活尸"},
        ],
        "rewards": {
            "exp": 120,
            "materials": {"黑曜石粉": 3, "魔鬼蛆": 1},
        },
        "dialogue_start": [
            {"speaker": "守墓人", "text": "墓地里的死者不再安息了..."},
            {"speaker": "守墓人", "text": "他们爬出坟墓，四处游荡。请帮帮忙！"},
        ],
        "dialogue_end": [
            {"speaker": "守墓人", "text": "死者终于可以安息了，谢谢你。"},
        ],
        "repeatable": False,
        "required_sequence": 9,
    },

    "side_003": {
        "name": "梦魇猎手",
        "type": QUEST_TYPE_SIDE,
        "desc": "有人被困在噩梦中无法醒来，消灭梦魇来拯救他们。",
        "objectives": [
            {"type": OBJECTIVE_KILL, "target": "梦魇", "count": 8, "desc": "击杀梦魇"},
            {"type": OBJECTIVE_COLLECT, "target": "梦境尘埃", "count": 3, "desc": "收集梦境尘埃"},
        ],
        "rewards": {
            "exp": 180,
            "materials": {"紫月花": 2, "梦境尘埃": 1},
        },
        "dialogue_start": [
            {"speaker": "医生", "text": "我的病人陷入了无法醒来的噩梦..."},
            {"speaker": "医生", "text": "只有消灭梦魇，他们才能获救。"},
        ],
        "dialogue_end": [
            {"speaker": "医生", "text": "他们醒了！你真是救命恩人！"},
        ],
        "prerequisites": ["main_003"],
        "repeatable": False,
        "required_sequence": 8,
    },

    "side_004": {
        "name": "生存挑战",
        "type": QUEST_TYPE_SIDE,
        "desc": "证明你的实力，在无尽的敌人面前生存下来！",
        "objectives": [
            {"type": OBJECTIVE_REACH_WAVE, "target": 10, "count": 1, "desc": "生存至第10波"},
        ],
        "rewards": {
            "exp": 300,
            "materials": {"深红月晶": 1, "风暴精华": 1},
        },
        "dialogue_start": [
            {"speaker": "竞技场主持人", "text": "欢迎来到生存挑战！"},
            {"speaker": "竞技场主持人", "text": "看看你能坚持多久！"},
        ],
        "dialogue_end": [
            {"speaker": "竞技场主持人", "text": "难以置信！你竟然做到了！"},
            {"speaker": "竞技场主持人", "text": "这是你应得的奖励！"},
        ],
        "prerequisites": ["main_004"],
        "repeatable": False,
        "required_sequence": 8,
    },

    # ===== Boss挑战任务 =====
    "side_005": {
        "name": "愚者之影",
        "type": QUEST_TYPE_SIDE,
        "desc": "传闻有一个神秘的存在在暗中观察着一切，他自称为愚者之影...",
        "difficulty": QUEST_DIFFICULTY_HARD,
        "objectives": [
            {"type": OBJECTIVE_BOSS, "target": "愚者之影", "count": 1, "desc": "击败愚者之影"},
        ],
        "rewards": {
            "exp": 500,
            "gold": 300,
            "materials": {"命运之线": 1, "灵银粉": 2},
            "weapon": "命运小丑匕首",
        },
        "dialogue_start": [
            {"speaker": "神秘声音", "text": "欢迎来到这场欺诈的盛宴..."},
            {"speaker": "愚者之影", "text": "我是愚者之影，命运的观察者。"},
            {"speaker": "愚者之影", "text": "让我看看你能否改变自己的命运！"},
        ],
        "dialogue_end": [
            {"speaker": "愚者之影", "text": "有趣...你确实有些实力。"},
            {"speaker": "愚者之影", "text": "命运的轮盘已经开始转动..."},
        ],
        "prerequisites": ["main_007"],
        "repeatable": True,
        "required_sequence": 7,
    },

    "side_006": {
        "name": "永暗巨兽",
        "type": QUEST_TYPE_SIDE,
        "desc": "从永暗深渊中爬出的恐怖存在，它吞噬一切光明...",
        "difficulty": QUEST_DIFFICULTY_HARD,
        "objectives": [
            {"type": OBJECTIVE_BOSS, "target": "永暗巨兽", "count": 1, "desc": "击败永暗巨兽"},
        ],
        "rewards": {
            "exp": 550,
            "gold": 350,
            "materials": {"永暗精华": 1, "深红月晶": 2},
            "weapon": "深渊之刃",
        },
        "dialogue_start": [
            {"speaker": "旁白", "text": "黑暗开始蔓延，所有的光芒都在消失..."},
            {"speaker": "永暗巨兽", "text": "■■■■■...（无法理解的低语）"},
        ],
        "dialogue_end": [
            {"speaker": "旁白", "text": "光明重新降临，永暗巨兽暂时退却了。"},
        ],
        "prerequisites": ["side_005"],
        "repeatable": True,
        "required_sequence": 7,
    },

    "side_007": {
        "name": "原初魔女",
        "type": QUEST_TYPE_SIDE,
        "desc": "诅咒与灾祸的化身，原初魔女降临于此世界...",
        "difficulty": QUEST_DIFFICULTY_NIGHTMARE,
        "objectives": [
            {"type": OBJECTIVE_BOSS, "target": "原初魔女", "count": 1, "desc": "击败原初魔女"},
        ],
        "rewards": {
            "exp": 600,
            "gold": 400,
            "materials": {"诅咒之心": 1, "腐化之心": 2},
            "weapon": "灾祸权杖",
        },
        "dialogue_start": [
            {"speaker": "原初魔女", "text": "愚蠢的生灵，竟敢觊觎我的力量？"},
            {"speaker": "原初魔女", "text": "让我用诅咒将你的灵魂撕碎！"},
        ],
        "dialogue_end": [
            {"speaker": "原初魔女", "text": "不...不可能...我是原初的..."},
            {"speaker": "旁白", "text": "魔女消散了，但诅咒的余韵仍在空气中飘荡。"},
        ],
        "prerequisites": ["side_006"],
        "repeatable": True,
        "required_sequence": 6,
    },

    "side_008": {
        "name": "知识妖鬼",
        "type": QUEST_TYPE_SIDE,
        "desc": "掌握无尽知识的可怕存在，它的目光能让人陷入疯狂...",
        "difficulty": QUEST_DIFFICULTY_NIGHTMARE,
        "objectives": [
            {"type": OBJECTIVE_BOSS, "target": "知识妖鬼", "count": 1, "desc": "击败知识妖鬼"},
        ],
        "rewards": {
            "exp": 650,
            "gold": 450,
            "materials": {"疯狂卷轴": 1, "太阳圣水": 2},
            "weapon": "卷轴法杖",
        },
        "dialogue_start": [
            {"speaker": "知识妖鬼", "text": "我看到了你的过去、现在和未来..."},
            {"speaker": "知识妖鬼", "text": "所有的知识都将属于我！"},
        ],
        "dialogue_end": [
            {"speaker": "旁白", "text": "无尽的知识随着妖鬼的消散而散落..."},
            {"speaker": "旁白", "text": "你感到头脑前所未有的清明。"},
        ],
        "prerequisites": ["side_007"],
        "repeatable": True,
        "required_sequence": 6,
    },

    # ===== 连环任务线 - 武器大师 =====
    "side_009": {
        "name": "武器入门",
        "type": QUEST_TYPE_SIDE,
        "desc": "想要成为真正的战士，首先需要一把趁手的武器。",
        "difficulty": QUEST_DIFFICULTY_EASY,
        "objectives": [
            {"type": OBJECTIVE_EQUIP, "target": "any", "count": 1, "desc": "装备一把武器"},
        ],
        "rewards": {
            "exp": 50,
            "gold": 50,
        },
        "dialogue_start": [
            {"speaker": "武器商人", "text": "年轻人，我看你还没有装备武器？"},
            {"speaker": "武器商人", "text": "击杀敌人可以获得武器，按Shift+W打开武器背包。"},
        ],
        "dialogue_end": [
            {"speaker": "武器商人", "text": "不错的选择！武器是战士的灵魂！"},
        ],
        "repeatable": False,
        "required_sequence": 9,
    },

    "side_010": {
        "name": "武器收藏家",
        "type": QUEST_TYPE_SIDE,
        "desc": "真正的收藏家会收集各种品质的武器。",
        "difficulty": QUEST_DIFFICULTY_NORMAL,
        "objectives": [
            {"type": OBJECTIVE_COLLECT, "target": "weapon_rare", "count": 3, "desc": "获得3把稀有武器"},
        ],
        "rewards": {
            "exp": 200,
            "gold": 200,
            "materials": {"灵银粉": 2},
        },
        "dialogue_start": [
            {"speaker": "收藏家", "text": "我听说你开始收集武器了？"},
            {"speaker": "收藏家", "text": "帮我找到一些稀有武器，我会给你丰厚的报酬。"},
        ],
        "dialogue_end": [
            {"speaker": "收藏家", "text": "这些武器真是太美了！收下这些奖励吧。"},
        ],
        "prerequisites": ["side_009"],
        "repeatable": False,
        "required_sequence": 8,
    },

    "side_011": {
        "name": "传说猎人",
        "type": QUEST_TYPE_SIDE,
        "desc": "只有真正的强者才能获得传说级武器。",
        "difficulty": QUEST_DIFFICULTY_HARD,
        "objectives": [
            {"type": OBJECTIVE_COLLECT, "target": "weapon_legendary", "count": 1, "desc": "获得1把传说武器"},
        ],
        "rewards": {
            "exp": 400,
            "gold": 500,
            "materials": {"深红月晶": 2, "太阳圣水": 1},
        },
        "dialogue_start": [
            {"speaker": "传说猎人", "text": "传说级的武器...那是每个战士的梦想。"},
            {"speaker": "传说猎人", "text": "只有击败最强大的敌人，才有可能获得它们。"},
        ],
        "dialogue_end": [
            {"speaker": "传说猎人", "text": "你做到了！你已经是真正的传说猎人了！"},
        ],
        "prerequisites": ["side_010"],
        "repeatable": False,
        "required_sequence": 7,
    },

    # ===== 挑战任务 =====
    "side_012": {
        "name": "无伤挑战",
        "type": QUEST_TYPE_SIDE,
        "desc": "在不受伤的情况下击败20个敌人，证明你的实力！",
        "difficulty": QUEST_DIFFICULTY_HARD,
        "objectives": [
            {"type": OBJECTIVE_NO_DAMAGE, "target": 20, "count": 1, "desc": "无伤击杀20个敌人"},
        ],
        "rewards": {
            "exp": 300,
            "gold": 300,
            "materials": {"风暴精华": 2},
        },
        "dialogue_start": [
            {"speaker": "挑战者", "text": "真正的高手，一根汗毛都不会被敌人碰到！"},
        ],
        "dialogue_end": [
            {"speaker": "挑战者", "text": "不可思议！你是我见过最敏捷的战士！"},
        ],
        "prerequisites": ["main_003"],
        "repeatable": True,
        "required_sequence": 8,
    },

    "side_013": {
        "name": "连击大师",
        "type": QUEST_TYPE_SIDE,
        "desc": "在一次战斗中达成50连击！",
        "difficulty": QUEST_DIFFICULTY_NORMAL,
        "objectives": [
            {"type": OBJECTIVE_COMBO, "target": 50, "count": 1, "desc": "达成50连击"},
        ],
        "rewards": {
            "exp": 200,
            "gold": 150,
            "materials": {"星辰草": 3},
        },
        "dialogue_start": [
            {"speaker": "格斗教练", "text": "连击是战斗的艺术！"},
            {"speaker": "格斗教练", "text": "在不被打断的情况下连续攻击敌人吧！"},
        ],
        "dialogue_end": [
            {"speaker": "格斗教练", "text": "完美的连击！你已经掌握了战斗的节奏！"},
        ],
        "prerequisites": ["main_002"],
        "repeatable": True,
        "required_sequence": 9,
    },

    "side_014": {
        "name": "生存专家",
        "type": QUEST_TYPE_SIDE,
        "desc": "挑战自我极限，生存至第20波！",
        "difficulty": QUEST_DIFFICULTY_NIGHTMARE,
        "objectives": [
            {"type": OBJECTIVE_REACH_WAVE, "target": 20, "count": 1, "desc": "生存至第20波"},
        ],
        "rewards": {
            "exp": 800,
            "gold": 600,
            "materials": {"深红月晶": 3, "腐化之心": 1},
        },
        "dialogue_start": [
            {"speaker": "竞技场主持人", "text": "第20波...你确定你准备好了吗？"},
            {"speaker": "竞技场主持人", "text": "那里有超乎想象的恐怖存在！"},
        ],
        "dialogue_end": [
            {"speaker": "竞技场主持人", "text": "传奇！你创造了新的记录！"},
        ],
        "prerequisites": ["side_004"],
        "repeatable": True,
        "required_sequence": 7,
    },

    # ===== 故事支线 - 神秘商人 =====
    "side_015": {
        "name": "神秘商人的请求",
        "type": QUEST_TYPE_SIDE,
        "desc": "神秘商人需要一些特殊的材料来进行秘密交易...",
        "difficulty": QUEST_DIFFICULTY_NORMAL,
        "objectives": [
            {"type": OBJECTIVE_COLLECT, "target": "夜香花", "count": 5, "desc": "收集夜香花"},
            {"type": OBJECTIVE_COLLECT, "target": "黑曜石粉", "count": 3, "desc": "收集黑曜石粉"},
        ],
        "rewards": {
            "exp": 150,
            "gold": 100,
            "materials": {"梦境尘埃": 2},
        },
        "dialogue_start": [
            {"speaker": "神秘商人", "text": "我需要一些...特殊的材料。"},
            {"speaker": "神秘商人", "text": "别问太多，帮我收集就是了。"},
        ],
        "dialogue_end": [
            {"speaker": "神秘商人", "text": "很好...我会记住你的帮助的。"},
        ],
        "unlock_quests": ["side_016"],
        "repeatable": False,
        "required_sequence": 9,
    },

    "side_016": {
        "name": "商人的秘密",
        "type": QUEST_TYPE_SIDE,
        "desc": "神秘商人似乎藏着什么秘密，帮他收集更多材料或许能发现些什么...",
        "difficulty": QUEST_DIFFICULTY_NORMAL,
        "objectives": [
            {"type": OBJECTIVE_COLLECT, "target": "梦境尘埃", "count": 3, "desc": "收集梦境尘埃"},
            {"type": OBJECTIVE_COLLECT, "target": "九叶莲", "count": 2, "desc": "收集九叶莲"},
        ],
        "rewards": {
            "exp": 250,
            "gold": 200,
            "materials": {"灵银粉": 3},
        },
        "dialogue_start": [
            {"speaker": "神秘商人", "text": "你的效率让我印象深刻。"},
            {"speaker": "神秘商人", "text": "我需要更多材料，报酬会更丰厚。"},
        ],
        "dialogue_end": [
            {"speaker": "神秘商人", "text": "或许...我可以告诉你一个秘密。"},
            {"speaker": "神秘商人", "text": "这个世界比你想象的要复杂得多..."},
        ],
        "prerequisites": ["side_015"],
        "unlock_quests": ["side_017"],
        "repeatable": False,
        "required_sequence": 8,
    },

    "side_017": {
        "name": "塔罗会的邀请",
        "type": QUEST_TYPE_SIDE,
        "desc": "神秘商人透露他是塔罗会的成员，并邀请你加入一场特殊的聚会...",
        "difficulty": QUEST_DIFFICULTY_HARD,
        "objectives": [
            {"type": OBJECTIVE_KILL, "target": "堕落非凡者", "count": 10, "desc": "击杀堕落非凡者"},
            {"type": OBJECTIVE_REACH_WAVE, "target": 15, "count": 1, "desc": "证明实力(生存至第15波)"},
        ],
        "rewards": {
            "exp": 500,
            "gold": 400,
            "materials": {"命运之线": 1, "太阳圣水": 2},
        },
        "dialogue_start": [
            {"speaker": "神秘商人", "text": "我是塔罗会的成员之一。"},
            {"speaker": "神秘商人", "text": "我们是一群追求真相的非凡者。"},
            {"speaker": "神秘商人", "text": "如果你想加入，首先需要证明你的实力。"},
        ],
        "dialogue_end": [
            {"speaker": "神秘商人", "text": "欢迎加入塔罗会，愚者先生会很高兴见到你。"},
            {"speaker": "旁白", "text": "你感到自己触碰到了这个世界更深层的秘密..."},
        ],
        "prerequisites": ["side_016"],
        "repeatable": False,
        "required_sequence": 7,
    },
}

# ==================== 日常任务 ====================
DAILY_QUESTS = {
    "daily_001": {
        "name": "日常巡逻",
        "type": QUEST_TYPE_DAILY,
        "desc": "每天清理一些敌人，保持战斗状态。",
        "objectives": [
            {"type": OBJECTIVE_KILL, "target": "any", "count": 20, "desc": "击杀任意敌人"},
        ],
        "rewards": {
            "exp": 50,
            "gold": 30,
            "materials": {"蒸馏水": 2},
        },
        "repeatable": True,
        "required_sequence": 9,
    },

    "daily_002": {
        "name": "材料收集",
        "type": QUEST_TYPE_DAILY,
        "desc": "收集一些基础材料。",
        "objectives": [
            {"type": OBJECTIVE_COLLECT, "target": "any", "count": 5, "desc": "收集任意材料"},
        ],
        "rewards": {
            "exp": 30,
            "gold": 20,
            "materials": {"星辰草": 1},
        },
        "repeatable": True,
        "required_sequence": 9,
    },

    "daily_003": {
        "name": "波次挑战",
        "type": QUEST_TYPE_DAILY,
        "desc": "每天挑战波次生存，保持战斗技巧。",
        "objectives": [
            {"type": OBJECTIVE_REACH_WAVE, "target": 5, "count": 1, "desc": "生存至第5波"},
        ],
        "rewards": {
            "exp": 80,
            "gold": 50,
            "materials": {"夜香花": 2},
        },
        "repeatable": True,
        "required_sequence": 9,
    },

    "daily_004": {
        "name": "邪灵猎人",
        "type": QUEST_TYPE_DAILY,
        "desc": "清除贝克兰德的邪灵威胁。",
        "objectives": [
            {"type": OBJECTIVE_KILL, "target": "低级邪灵", "count": 15, "desc": "击杀低级邪灵"},
        ],
        "rewards": {
            "exp": 60,
            "gold": 40,
            "materials": {"黑曜石粉": 2},
        },
        "repeatable": True,
        "required_sequence": 9,
    },

    "daily_005": {
        "name": "活尸清理",
        "type": QUEST_TYPE_DAILY,
        "desc": "墓地的活尸需要定期清理。",
        "objectives": [
            {"type": OBJECTIVE_KILL, "target": "活尸", "count": 10, "desc": "击杀活尸"},
        ],
        "rewards": {
            "exp": 60,
            "gold": 40,
            "materials": {"冷杉精华": 1},
        },
        "repeatable": True,
        "required_sequence": 9,
    },

    "daily_006": {
        "name": "梦魇驱逐",
        "type": QUEST_TYPE_DAILY,
        "desc": "驱逐入侵现实的梦魇。",
        "objectives": [
            {"type": OBJECTIVE_KILL, "target": "梦魇", "count": 8, "desc": "击杀梦魇"},
        ],
        "rewards": {
            "exp": 100,
            "gold": 60,
            "materials": {"梦境尘埃": 1},
        },
        "prerequisites": ["main_003"],
        "repeatable": True,
        "required_sequence": 8,
    },

    "daily_007": {
        "name": "高级巡逻",
        "type": QUEST_TYPE_DAILY,
        "desc": "在更危险的区域巡逻，击杀更强大的敌人。",
        "objectives": [
            {"type": OBJECTIVE_KILL, "target": "堕落非凡者", "count": 5, "desc": "击杀堕落非凡者"},
        ],
        "rewards": {
            "exp": 150,
            "gold": 80,
            "materials": {"灵银粉": 1},
        },
        "prerequisites": ["main_004"],
        "repeatable": True,
        "required_sequence": 8,
    },

    "daily_008": {
        "name": "金币猎人",
        "type": QUEST_TYPE_DAILY,
        "desc": "通过战斗积累财富。",
        "objectives": [
            {"type": OBJECTIVE_GOLD, "target": "any", "count": 100, "desc": "获得100金币"},
        ],
        "rewards": {
            "exp": 80,
            "gold": 50,  # 额外金币奖励
        },
        "repeatable": True,
        "required_sequence": 9,
    },

    "daily_009": {
        "name": "连击练习",
        "type": QUEST_TYPE_DAILY,
        "desc": "通过练习连击来提升战斗技巧。",
        "objectives": [
            {"type": OBJECTIVE_COMBO, "target": 20, "count": 1, "desc": "达成20连击"},
        ],
        "rewards": {
            "exp": 70,
            "gold": 40,
            "materials": {"星辰草": 2},
        },
        "repeatable": True,
        "required_sequence": 9,
    },

    "daily_010": {
        "name": "稀有材料收集",
        "type": QUEST_TYPE_DAILY,
        "desc": "收集稀有的魔药材料。",
        "objectives": [
            {"type": OBJECTIVE_COLLECT, "target": "rare_material", "count": 2, "desc": "收集稀有材料"},
        ],
        "rewards": {
            "exp": 120,
            "gold": 80,
            "materials": {"九叶莲": 1},
        },
        "prerequisites": ["main_004"],
        "repeatable": True,
        "required_sequence": 8,
    },
}

# ==================== 周常任务 ====================
WEEKLY_QUESTS = {
    "weekly_001": {
        "name": "周末大扫除",
        "type": QUEST_TYPE_DAILY,  # 使用daily类型但有weekly标记
        "is_weekly": True,
        "desc": "每周清理大量敌人，维护贝克兰德的安全。",
        "objectives": [
            {"type": OBJECTIVE_KILL, "target": "any", "count": 100, "desc": "击杀100个敌人"},
        ],
        "rewards": {
            "exp": 300,
            "gold": 200,
            "materials": {"梦境尘埃": 3, "灵银粉": 2},
        },
        "repeatable": True,
        "required_sequence": 9,
    },

    "weekly_002": {
        "name": "波次精英",
        "type": QUEST_TYPE_DAILY,
        "is_weekly": True,
        "desc": "每周挑战高波次生存。",
        "objectives": [
            {"type": OBJECTIVE_REACH_WAVE, "target": 15, "count": 1, "desc": "生存至第15波"},
        ],
        "rewards": {
            "exp": 500,
            "gold": 300,
            "materials": {"深红月晶": 2, "风暴精华": 1},
        },
        "prerequisites": ["main_004"],
        "repeatable": True,
        "required_sequence": 8,
    },

    "weekly_003": {
        "name": "材料囤积",
        "type": QUEST_TYPE_DAILY,
        "is_weekly": True,
        "desc": "每周收集足够的材料储备。",
        "objectives": [
            {"type": OBJECTIVE_COLLECT, "target": "any", "count": 30, "desc": "收集30个材料"},
        ],
        "rewards": {
            "exp": 250,
            "gold": 150,
            "materials": {"太阳圣水": 1, "九叶莲": 2},
        },
        "repeatable": True,
        "required_sequence": 9,
    },

    "weekly_004": {
        "name": "Boss挑战",
        "type": QUEST_TYPE_DAILY,
        "is_weekly": True,
        "desc": "每周挑战一次Boss战斗。",
        "objectives": [
            {"type": OBJECTIVE_BOSS, "target": "any", "count": 1, "desc": "击败任意Boss"},
        ],
        "rewards": {
            "exp": 400,
            "gold": 250,
            "materials": {"腐化之心": 1},
        },
        "prerequisites": ["main_007"],
        "repeatable": True,
        "required_sequence": 7,
    },
}

# 合并所有任务
ALL_QUESTS = {}
ALL_QUESTS.update(MAIN_QUESTS)
ALL_QUESTS.update(SIDE_QUESTS)
ALL_QUESTS.update(DAILY_QUESTS)
ALL_QUESTS.update(WEEKLY_QUESTS)


def get_quest_data(quest_id):
    """获取任务数据"""
    return ALL_QUESTS.get(quest_id)


def get_main_quests():
    """获取所有主线任务"""
    return MAIN_QUESTS


def get_side_quests():
    """获取所有支线任务"""
    return SIDE_QUESTS


def get_daily_quests():
    """获取所有日常任务"""
    return DAILY_QUESTS


def get_weekly_quests():
    """获取所有周常任务"""
    return WEEKLY_QUESTS


def get_initial_quests():
    """获取初始可用任务"""
    initial = []
    for quest_id, quest in ALL_QUESTS.items():
        if "prerequisites" not in quest or not quest["prerequisites"]:
            if quest["type"] == QUEST_TYPE_MAIN:
                initial.append(quest_id)
    return initial
