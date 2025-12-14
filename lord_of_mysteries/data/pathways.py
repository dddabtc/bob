"""
途径数据 - 简化版本
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
    "灵视": {"type": "buff", "cooldown": 10, "duration": 5, "desc": "开启灵视，看穿敌人弱点，增加20%暴击率"},
    "占卜": {"type": "buff", "cooldown": 15, "duration": 3, "desc": "预知危险，短暂无敌"},
    "纸牌投掷": {"type": "projectile", "cooldown": 2, "damage": 25, "desc": "投掷锋利纸牌，远程攻击"},
    "火焰跳跃": {"type": "dash", "cooldown": 8, "damage": 40, "desc": "化为火焰瞬移，对路径敌人造成伤害"},
    "空气炮": {"type": "projectile", "cooldown": 5, "damage": 60, "desc": "压缩空气形成炮弹"},
    "易容": {"type": "buff", "cooldown": 30, "duration": 10, "desc": "改变外貌，敌人不会主动攻击"},
}

# 途径数据 - 只有占卜家
PATHWAYS = {
    "占卜家": {
        "name": "占卜家途径",
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
