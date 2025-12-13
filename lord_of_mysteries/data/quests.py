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
            "materials": {"星辰草": 1},
        },
        "repeatable": True,
        "required_sequence": 9,
    },
}

# 合并所有任务
ALL_QUESTS = {}
ALL_QUESTS.update(MAIN_QUESTS)
ALL_QUESTS.update(SIDE_QUESTS)
ALL_QUESTS.update(DAILY_QUESTS)


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


def get_initial_quests():
    """获取初始可用任务"""
    initial = []
    for quest_id, quest in ALL_QUESTS.items():
        if "prerequisites" not in quest or not quest["prerequisites"]:
            if quest["type"] == QUEST_TYPE_MAIN:
                initial.append(quest_id)
    return initial
