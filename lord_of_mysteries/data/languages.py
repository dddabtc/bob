"""
多语言文本数据
"""

# 支持的语言
SUPPORTED_LANGUAGES = ["zh_CN", "en_US"]

# 默认语言
DEFAULT_LANGUAGE = "zh_CN"

# 语言显示名称
LANGUAGE_NAMES = {
    "zh_CN": "简体中文",
    "en_US": "English"
}

# 所有文本翻译
TRANSLATIONS = {
    # ========== 主菜单 ==========
    "menu_title": {
        "zh_CN": "诡秘之主",
        "en_US": "Lord of Mysteries"
    },
    "menu_subtitle": {
        "zh_CN": "Lord of Mysteries",
        "en_US": "A Dark Fantasy RPG"
    },
    "menu_new_game": {
        "zh_CN": "新游戏",
        "en_US": "New Game"
    },
    "menu_continue": {
        "zh_CN": "继续游戏",
        "en_US": "Continue"
    },
    "menu_load_game": {
        "zh_CN": "读取存档",
        "en_US": "Load Game"
    },
    "menu_settings": {
        "zh_CN": "设置",
        "en_US": "Settings"
    },
    "menu_quit": {
        "zh_CN": "退出游戏",
        "en_US": "Quit"
    },

    # ========== 暂停菜单 ==========
    "pause_title": {
        "zh_CN": "游戏暂停",
        "en_US": "Game Paused"
    },
    "pause_resume": {
        "zh_CN": "继续游戏",
        "en_US": "Resume"
    },
    "pause_save": {
        "zh_CN": "保存游戏",
        "en_US": "Save Game"
    },
    "pause_load": {
        "zh_CN": "读取存档",
        "en_US": "Load Game"
    },
    "pause_settings": {
        "zh_CN": "设置",
        "en_US": "Settings"
    },
    "pause_main_menu": {
        "zh_CN": "返回主菜单",
        "en_US": "Main Menu"
    },
    "pause_quit": {
        "zh_CN": "退出游戏",
        "en_US": "Quit"
    },

    # ========== 设置界面 ==========
    "settings_title": {
        "zh_CN": "设置",
        "en_US": "Settings"
    },
    "settings_language": {
        "zh_CN": "语言",
        "en_US": "Language"
    },
    "settings_sound": {
        "zh_CN": "音效",
        "en_US": "Sound"
    },
    "settings_music": {
        "zh_CN": "音乐",
        "en_US": "Music"
    },
    "settings_fullscreen": {
        "zh_CN": "全屏",
        "en_US": "Fullscreen"
    },
    "settings_back": {
        "zh_CN": "返回",
        "en_US": "Back"
    },
    "settings_apply": {
        "zh_CN": "应用",
        "en_US": "Apply"
    },
    "settings_on": {
        "zh_CN": "开",
        "en_US": "ON"
    },
    "settings_off": {
        "zh_CN": "关",
        "en_US": "OFF"
    },

    # ========== 途径选择 ==========
    "pathway_select_title": {
        "zh_CN": "选择你的途径",
        "en_US": "Choose Your Pathway"
    },
    "pathway_select_back": {
        "zh_CN": "返回",
        "en_US": "Back"
    },
    "pathway_select_confirm": {
        "zh_CN": "确认选择",
        "en_US": "Confirm"
    },
    "pathway_filter_all": {
        "zh_CN": "全部",
        "en_US": "All"
    },
    "pathway_filter_melee": {
        "zh_CN": "近战",
        "en_US": "Melee"
    },
    "pathway_filter_magic": {
        "zh_CN": "魔法",
        "en_US": "Magic"
    },
    "pathway_filter_control": {
        "zh_CN": "控制",
        "en_US": "Control"
    },
    "pathway_filter_special": {
        "zh_CN": "特殊",
        "en_US": "Special"
    },
    "pathway_filter_support": {
        "zh_CN": "支援",
        "en_US": "Support"
    },
    "pathway_filter_wisdom": {
        "zh_CN": "智慧",
        "en_US": "Wisdom"
    },
    "pathway_god": {
        "zh_CN": "对应神灵",
        "en_US": "Deity"
    },
    "pathway_sequence": {
        "zh_CN": "序列",
        "en_US": "Sequence"
    },
    "pathway_start": {
        "zh_CN": "开始游戏",
        "en_US": "Start Game"
    },

    # ========== 游戏内HUD ==========
    "hud_hp": {
        "zh_CN": "生命",
        "en_US": "HP"
    },
    "hud_wave": {
        "zh_CN": "波次",
        "en_US": "Wave"
    },
    "hud_enemies": {
        "zh_CN": "敌人",
        "en_US": "Enemies"
    },
    "hud_kills": {
        "zh_CN": "击杀",
        "en_US": "Kills"
    },
    "hud_exp": {
        "zh_CN": "经验",
        "en_US": "EXP"
    },
    "hud_next_sequence": {
        "zh_CN": "下一序列",
        "en_US": "Next Seq"
    },
    "hud_next_wave": {
        "zh_CN": "下一波",
        "en_US": "Next Wave"
    },

    # ========== 背包界面 ==========
    "inventory_title": {
        "zh_CN": "背包",
        "en_US": "Inventory"
    },
    "inventory_materials": {
        "zh_CN": "材料",
        "en_US": "Materials"
    },
    "inventory_consumables": {
        "zh_CN": "消耗品",
        "en_US": "Consumables"
    },
    "inventory_potions": {
        "zh_CN": "魔药炮制",
        "en_US": "Potion Craft"
    },
    "inventory_craft": {
        "zh_CN": "炮制",
        "en_US": "Craft"
    },
    "inventory_use": {
        "zh_CN": "使用",
        "en_US": "Use"
    },
    "inventory_close": {
        "zh_CN": "关闭",
        "en_US": "Close"
    },
    "inventory_gold": {
        "zh_CN": "金币",
        "en_US": "Gold"
    },

    # ========== 武器界面 ==========
    "weapon_title": {
        "zh_CN": "武器",
        "en_US": "Weapons"
    },
    "weapon_equip": {
        "zh_CN": "装备",
        "en_US": "Equip"
    },
    "weapon_unequip": {
        "zh_CN": "卸下",
        "en_US": "Unequip"
    },
    "weapon_attack": {
        "zh_CN": "攻击力",
        "en_US": "Attack"
    },
    "weapon_crit_rate": {
        "zh_CN": "暴击率",
        "en_US": "Crit Rate"
    },
    "weapon_crit_damage": {
        "zh_CN": "暴击伤害",
        "en_US": "Crit Dmg"
    },
    "weapon_range": {
        "zh_CN": "范围",
        "en_US": "Range"
    },
    "weapon_speed": {
        "zh_CN": "攻速",
        "en_US": "Speed"
    },

    # ========== 任务界面 ==========
    "quest_title": {
        "zh_CN": "任务",
        "en_US": "Quests"
    },
    "quest_main": {
        "zh_CN": "主线任务",
        "en_US": "Main Quests"
    },
    "quest_side": {
        "zh_CN": "支线任务",
        "en_US": "Side Quests"
    },
    "quest_daily": {
        "zh_CN": "每日任务",
        "en_US": "Daily"
    },
    "quest_weekly": {
        "zh_CN": "每周任务",
        "en_US": "Weekly"
    },
    "quest_accept": {
        "zh_CN": "接受任务",
        "en_US": "Accept"
    },
    "quest_complete": {
        "zh_CN": "完成任务",
        "en_US": "Complete"
    },
    "quest_rewards": {
        "zh_CN": "奖励",
        "en_US": "Rewards"
    },
    "quest_progress": {
        "zh_CN": "进度",
        "en_US": "Progress"
    },

    # ========== 存档界面 ==========
    "save_title": {
        "zh_CN": "保存游戏",
        "en_US": "Save Game"
    },
    "load_title": {
        "zh_CN": "读取存档",
        "en_US": "Load Game"
    },
    "save_slot": {
        "zh_CN": "存档位",
        "en_US": "Slot"
    },
    "save_empty": {
        "zh_CN": "空",
        "en_US": "Empty"
    },
    "save_auto": {
        "zh_CN": "自动存档",
        "en_US": "Auto Save"
    },
    "save_confirm": {
        "zh_CN": "保存",
        "en_US": "Save"
    },
    "save_delete": {
        "zh_CN": "删除",
        "en_US": "Delete"
    },
    "save_success": {
        "zh_CN": "保存成功！",
        "en_US": "Game Saved!"
    },
    "load_success": {
        "zh_CN": "读档成功！",
        "en_US": "Game Loaded!"
    },
    "save_overwrite": {
        "zh_CN": "覆盖存档？",
        "en_US": "Overwrite?"
    },

    # ========== 游戏结束 ==========
    "game_over_title": {
        "zh_CN": "游戏结束",
        "en_US": "Game Over"
    },
    "game_over_wave": {
        "zh_CN": "到达波次",
        "en_US": "Wave Reached"
    },
    "game_over_kills": {
        "zh_CN": "击杀敌人",
        "en_US": "Enemies Killed"
    },
    "game_over_exp": {
        "zh_CN": "获得经验",
        "en_US": "EXP Earned"
    },
    "game_over_restart": {
        "zh_CN": "按 SPACE 重新开始",
        "en_US": "Press SPACE to Restart"
    },
    "game_over_menu": {
        "zh_CN": "按 ESC 返回主菜单",
        "en_US": "Press ESC for Main Menu"
    },

    # ========== 战斗提示 ==========
    "combat_wave_start": {
        "zh_CN": "波次",
        "en_US": "Wave"
    },
    "combat_wave_complete": {
        "zh_CN": "波次完成！",
        "en_US": "Wave Complete!"
    },
    "combat_boss_incoming": {
        "zh_CN": "! BOSS战 !",
        "en_US": "! BOSS FIGHT !"
    },
    "combat_boss_defeated": {
        "zh_CN": "击败",
        "en_US": "Defeated"
    },
    "combat_crit": {
        "zh_CN": "暴击!",
        "en_US": "CRIT!"
    },
    "combat_evade": {
        "zh_CN": "闪避!",
        "en_US": "EVADE!"
    },
    "combat_invincible": {
        "zh_CN": "无敌!",
        "en_US": "IMMUNE!"
    },
    "combat_reflect": {
        "zh_CN": "反弹!",
        "en_US": "REFLECT!"
    },
    "combat_stun": {
        "zh_CN": "眩晕!",
        "en_US": "STUN!"
    },

    # ========== 物品拾取 ==========
    "pickup_weapon": {
        "zh_CN": "获得武器",
        "en_US": "Got Weapon"
    },
    "pickup_material": {
        "zh_CN": "获得",
        "en_US": "Got"
    },
    "pickup_health_full": {
        "zh_CN": "生命已满",
        "en_US": "HP Full"
    },
    "pickup_health_potion_small": {
        "zh_CN": "小血瓶",
        "en_US": "Small Potion"
    },
    "pickup_health_potion_medium": {
        "zh_CN": "中血瓶",
        "en_US": "Medium Potion"
    },
    "pickup_health_potion_large": {
        "zh_CN": "大血瓶",
        "en_US": "Large Potion"
    },

    # ========== 魔药炮制 ==========
    "potion_craft_success": {
        "zh_CN": "晋升成功！",
        "en_US": "Advancement Success!"
    },
    "potion_craft_fail": {
        "zh_CN": "炮制失败",
        "en_US": "Craft Failed"
    },
    "potion_digesting": {
        "zh_CN": "正在消化魔药...",
        "en_US": "Digesting potion..."
    },
    "potion_materials_lack": {
        "zh_CN": "材料不足",
        "en_US": "Not enough materials"
    },

    # ========== 品质名称 ==========
    "quality_common": {
        "zh_CN": "普通",
        "en_US": "Common"
    },
    "quality_uncommon": {
        "zh_CN": "优秀",
        "en_US": "Uncommon"
    },
    "quality_rare": {
        "zh_CN": "稀有",
        "en_US": "Rare"
    },
    "quality_epic": {
        "zh_CN": "史诗",
        "en_US": "Epic"
    },
    "quality_legendary": {
        "zh_CN": "传说",
        "en_US": "Legendary"
    },

    # ========== 欢迎消息 ==========
    "welcome_message": {
        "zh_CN": "欢迎，{name}！",
        "en_US": "Welcome, {name}!"
    },

    # ========== 任务通知 ==========
    "quest_accepted": {
        "zh_CN": "接受任务: {name}",
        "en_US": "Quest Accepted: {name}"
    },
    "quest_objective_complete": {
        "zh_CN": "目标完成: {objective}",
        "en_US": "Objective Complete: {objective}"
    },
    "quest_reward": {
        "zh_CN": "奖励: {reward}",
        "en_US": "Reward: {reward}"
    },

    # ========== 控制提示 ==========
    "controls_move": {
        "zh_CN": "WASD/方向键: 移动",
        "en_US": "WASD/Arrows: Move"
    },
    "controls_attack": {
        "zh_CN": "J/鼠标左键: 攻击",
        "en_US": "J/Left Click: Attack"
    },
    "controls_dodge": {
        "zh_CN": "K/鼠标右键: 闪避",
        "en_US": "K/Right Click: Dodge"
    },
    "controls_skills": {
        "zh_CN": "1-4: 技能",
        "en_US": "1-4: Skills"
    },
    "controls_inventory": {
        "zh_CN": "I: 背包",
        "en_US": "I: Inventory"
    },
    "controls_quests": {
        "zh_CN": "Q: 任务",
        "en_US": "Q: Quests"
    },
    "controls_weapons": {
        "zh_CN": "E: 武器",
        "en_US": "E: Weapons"
    },
    "controls_pause": {
        "zh_CN": "ESC: 暂停",
        "en_US": "ESC: Pause"
    },
}
