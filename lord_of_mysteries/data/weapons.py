"""
武器数据定义
基于诡秘之主世界观的武器系统
"""

from data.items import (
    QUALITY_COMMON, QUALITY_UNCOMMON, QUALITY_RARE,
    QUALITY_EPIC, QUALITY_LEGENDARY, QUALITY_COLORS
)

# 武器类型
WEAPON_TYPE_SWORD = "sword"        # 剑
WEAPON_TYPE_DAGGER = "dagger"      # 匕首
WEAPON_TYPE_STAFF = "staff"        # 法杖
WEAPON_TYPE_BOW = "bow"            # 弓
WEAPON_TYPE_REVOLVER = "revolver"  # 左轮枪
WEAPON_TYPE_CANE = "cane"          # 手杖
WEAPON_TYPE_FIST = "fist"          # 拳套

# 武器类型中文名
WEAPON_TYPE_NAMES = {
    WEAPON_TYPE_SWORD: "剑",
    WEAPON_TYPE_DAGGER: "匕首",
    WEAPON_TYPE_STAFF: "法杖",
    WEAPON_TYPE_BOW: "弓",
    WEAPON_TYPE_REVOLVER: "左轮枪",
    WEAPON_TYPE_CANE: "手杖",
    WEAPON_TYPE_FIST: "拳套",
}

# 武器类型特性
WEAPON_TYPE_TRAITS = {
    WEAPON_TYPE_SWORD: {
        "attack_range": 70,
        "attack_speed": 3.0,   # 攻速提升
        "attack_width": 60,
        "is_ranged": False,
    },
    WEAPON_TYPE_DAGGER: {
        "attack_range": 45,
        "attack_speed": 5.0,   # 匕首攻速最快
        "attack_width": 40,
        "is_ranged": False,
    },
    WEAPON_TYPE_STAFF: {
        "attack_range": 200,
        "attack_speed": 2.5,   # 攻速提升
        "projectile_speed": 12,
        "is_ranged": True,
    },
    WEAPON_TYPE_BOW: {
        "attack_range": 300,
        "attack_speed": 2.8,   # 攻速提升
        "projectile_speed": 18,
        "is_ranged": True,
    },
    WEAPON_TYPE_REVOLVER: {
        "attack_range": 250,
        "attack_speed": 4.0,   # 左轮射速快
        "projectile_speed": 25,
        "is_ranged": True,
    },
    WEAPON_TYPE_CANE: {
        "attack_range": 60,
        "attack_speed": 3.5,   # 攻速提升
        "attack_width": 50,
        "is_ranged": False,
    },
    WEAPON_TYPE_FIST: {
        "attack_range": 40,
        "attack_speed": 6.0,   # 拳套最快
        "attack_width": 35,
        "is_ranged": False,
    },
}

# ==================== 武器定义 ====================
WEAPONS = {
    # ===== 普通武器 (序列9-8) =====
    "铁剑": {
        "name": "铁剑",
        "type": WEAPON_TYPE_SWORD,
        "quality": QUALITY_COMMON,
        "attack": 10,
        "desc": "普通的铁制长剑，锋利耐用",
        "drop_from": ["低级邪灵", "活尸"],
        "drop_rate": 0.08,
    },
    "短匕": {
        "name": "短匕",
        "type": WEAPON_TYPE_DAGGER,
        "quality": QUALITY_COMMON,
        "attack": 7,
        "crit_rate": 0.1,
        "desc": "轻便的短匕首，适合快速攻击",
        "drop_from": ["低级邪灵", "梦魇"],
        "drop_rate": 0.08,
    },
    "学徒法杖": {
        "name": "学徒法杖",
        "type": WEAPON_TYPE_STAFF,
        "quality": QUALITY_COMMON,
        "attack": 8,
        "spirit_bonus": 5,
        "desc": "初学者使用的木制法杖",
        "drop_from": ["梦魇", "低级邪灵"],
        "drop_rate": 0.06,
    },
    "猎弓": {
        "name": "猎弓",
        "type": WEAPON_TYPE_BOW,
        "quality": QUALITY_COMMON,
        "attack": 9,
        "desc": "猎人使用的普通弓",
        "drop_from": ["活尸", "疯狂信徒"],
        "drop_rate": 0.06,
    },
    "拳套": {
        "name": "拳套",
        "type": WEAPON_TYPE_FIST,
        "quality": QUALITY_COMMON,
        "attack": 6,
        "attack_speed_bonus": 0.2,
        "desc": "皮革制成的拳套",
        "drop_from": ["疯狂信徒", "活尸"],
        "drop_rate": 0.08,
    },

    # ===== 优质武器 (序列7-6) =====
    "银月剑": {
        "name": "银月剑",
        "type": WEAPON_TYPE_SWORD,
        "quality": QUALITY_UNCOMMON,
        "attack": 18,
        "special": "对邪灵额外伤害+20%",
        "spirit_damage_bonus": 0.2,
        "desc": "以银月力量祝福的长剑，对邪灵有特效",
        "drop_from": ["堕落非凡者", "暗影猎手"],
        "drop_rate": 0.05,
    },
    "暗杀者匕首": {
        "name": "暗杀者匕首",
        "type": WEAPON_TYPE_DAGGER,
        "quality": QUALITY_UNCOMMON,
        "attack": 12,
        "crit_rate": 0.2,
        "crit_damage": 0.5,
        "desc": "刺客专用的漆黑匕首，暴击伤害更高",
        "drop_from": ["暗影猎手"],
        "drop_rate": 0.04,
    },
    "灵能法杖": {
        "name": "灵能法杖",
        "type": WEAPON_TYPE_STAFF,
        "quality": QUALITY_UNCOMMON,
        "attack": 15,
        "spirit_bonus": 12,
        "special": "投射物可穿透1个敌人",
        "pierce": 1,
        "desc": "蕴含灵性力量的法杖",
        "drop_from": ["邪灵领主", "梦魇"],
        "drop_rate": 0.04,
    },
    "精灵弓": {
        "name": "精灵弓",
        "type": WEAPON_TYPE_BOW,
        "quality": QUALITY_UNCOMMON,
        "attack": 16,
        "attack_speed_bonus": 0.15,
        "desc": "轻巧的精灵制弓，射速更快",
        "drop_from": ["堕落非凡者", "邪灵领主"],
        "drop_rate": 0.04,
    },
    "绅士手杖": {
        "name": "绅士手杖",
        "type": WEAPON_TYPE_CANE,
        "quality": QUALITY_UNCOMMON,
        "attack": 14,
        "defense_bonus": 5,
        "desc": "看似普通的手杖，暗藏玄机",
        "drop_from": ["堕落非凡者"],
        "drop_rate": 0.04,
    },
    "左轮手枪": {
        "name": "左轮手枪",
        "type": WEAPON_TYPE_REVOLVER,
        "quality": QUALITY_UNCOMMON,
        "attack": 20,
        "special": "每6发需要装填",
        "magazine": 6,
        "desc": "六发装的左轮手枪",
        "drop_from": ["堕落非凡者", "暗影猎手"],
        "drop_rate": 0.03,
    },

    # ===== 稀有武器 (序列5-4) =====
    "审判之剑": {
        "name": "审判之剑",
        "type": WEAPON_TYPE_SWORD,
        "quality": QUALITY_RARE,
        "attack": 30,
        "special": "攻击有10%概率造成眩晕",
        "stun_chance": 0.1,
        "desc": "正义审判者的佩剑，敌人闻风丧胆",
        "drop_from": ["极光会主教"],
        "drop_rate": 0.1,
    },
    "黑夜匕首": {
        "name": "黑夜匕首",
        "type": WEAPON_TYPE_DAGGER,
        "quality": QUALITY_RARE,
        "attack": 22,
        "crit_rate": 0.25,
        "crit_damage": 0.8,
        "special": "背刺伤害+50%",
        "backstab_bonus": 0.5,
        "desc": "黑夜女神祝福的匕首，背刺威力惊人",
        "drop_from": ["极光会主教", "暗影猎手"],
        "drop_rate": 0.08,
    },
    "命运法杖": {
        "name": "命运法杖",
        "type": WEAPON_TYPE_STAFF,
        "quality": QUALITY_RARE,
        "attack": 25,
        "spirit_bonus": 20,
        "special": "投射物追踪敌人",
        "homing": True,
        "desc": "能感知命运走向的法杖，投射物自动追踪目标",
        "drop_from": ["愚者之影"],
        "drop_rate": 0.1,
    },
    "风暴长弓": {
        "name": "风暴长弓",
        "type": WEAPON_TYPE_BOW,
        "quality": QUALITY_RARE,
        "attack": 28,
        "special": "箭矢带有风暴效果",
        "aoe_radius": 40,
        "desc": "蕴含风暴之力的长弓，箭矢爆炸造成范围伤害",
        "drop_from": ["极光会主教"],
        "drop_rate": 0.08,
    },
    "死神左轮": {
        "name": "死神左轮",
        "type": WEAPON_TYPE_REVOLVER,
        "quality": QUALITY_RARE,
        "attack": 35,
        "special": "击杀敌人恢复生命",
        "lifesteal_on_kill": 10,
        "magazine": 6,
        "desc": "据说能收割灵魂的左轮枪",
        "drop_from": ["永暗巨兽"],
        "drop_rate": 0.1,
    },

    # ===== 史诗武器 (序列3-2) =====
    "愚者权杖": {
        "name": "愚者权杖",
        "type": WEAPON_TYPE_CANE,
        "quality": QUALITY_EPIC,
        "attack": 40,
        "spirit_bonus": 25,
        "special": "击中敌人有概率触发混乱效果",
        "confusion_chance": 0.15,
        "desc": "愚者途径的象征之物",
        "drop_from": ["愚者之影"],
        "drop_rate": 0.2,
    },
    "永暗之刃": {
        "name": "永暗之刃",
        "type": WEAPON_TYPE_SWORD,
        "quality": QUALITY_EPIC,
        "attack": 45,
        "special": "攻击附带黑暗侵蚀，持续伤害",
        "dot_damage": 5,
        "dot_duration": 3,
        "desc": "由永恒黑暗凝聚的大剑",
        "drop_from": ["永暗巨兽"],
        "drop_rate": 0.2,
    },
    "魔女之吻": {
        "name": "魔女之吻",
        "type": WEAPON_TYPE_DAGGER,
        "quality": QUALITY_EPIC,
        "attack": 35,
        "crit_rate": 0.3,
        "special": "暴击时施加诅咒，降低敌人防御",
        "curse_defense_reduce": 10,
        "desc": "原初魔女的祝福之物",
        "drop_from": ["原初魔女"],
        "drop_rate": 0.2,
    },
    "知识典籍": {
        "name": "知识典籍",
        "type": WEAPON_TYPE_STAFF,
        "quality": QUALITY_EPIC,
        "attack": 38,
        "spirit_bonus": 35,
        "special": "释放多道投射物",
        "multi_shot": 3,
        "desc": "记载禁忌知识的魔法书",
        "drop_from": ["知识妖鬼"],
        "drop_rate": 0.2,
    },

    # ===== 传说武器 (序列1-0) =====
    "黎明之剑": {
        "name": "黎明之剑",
        "type": WEAPON_TYPE_SWORD,
        "quality": QUALITY_LEGENDARY,
        "attack": 60,
        "special": "攻击带有圣光效果，对黑暗生物造成双倍伤害",
        "holy_damage": True,
        "desc": "传说中能驱散一切黑暗的神圣之剑",
        "drop_from": [],  # 特殊获取
        "drop_rate": 0,
    },
    "0-08号左轮": {
        "name": "0-08号左轮",
        "type": WEAPON_TYPE_REVOLVER,
        "quality": QUALITY_LEGENDARY,
        "attack": 55,
        "special": "射出的子弹必定命中，无视闪避",
        "true_strike": True,
        "magazine": 6,
        "desc": "隐秘组织的神秘武器，子弹似乎有自己的意志",
        "drop_from": [],  # 特殊获取
        "drop_rate": 0,
    },
}

# 起始武器（玩家默认装备）
STARTER_WEAPONS = {
    "melee": "铁剑",      # 默认近战武器
    "ranged": "猎弓",     # 默认远程武器
}


def get_weapon_data(weapon_name):
    """获取武器数据"""
    return WEAPONS.get(weapon_name, {}).copy()


def get_weapon_type_trait(weapon_type):
    """获取武器类型特性"""
    return WEAPON_TYPE_TRAITS.get(weapon_type, {}).copy()


def get_weapons_by_quality(quality):
    """根据品质获取武器列表"""
    return [name for name, data in WEAPONS.items() if data.get("quality") == quality]


def get_weapons_by_type(weapon_type):
    """根据类型获取武器列表"""
    return [name for name, data in WEAPONS.items() if data.get("type") == weapon_type]


def get_all_droppable_weapons():
    """获取所有可掉落的武器"""
    return [name for name, data in WEAPONS.items() if data.get("drop_rate", 0) > 0]
