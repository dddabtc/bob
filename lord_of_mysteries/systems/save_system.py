"""
存档系统
管理游戏存档、读档和继续功能
"""

import os
import json
import time
from datetime import datetime


class SaveSystem:
    """存档系统"""

    def __init__(self, save_dir="saves"):
        self.save_dir = save_dir
        self.max_saves = 5  # 最大存档数
        self.auto_save_slot = "auto"  # 自动存档槽位
        self._ensure_save_dir()

    def _ensure_save_dir(self):
        """确保存档目录存在"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def _get_save_path(self, slot):
        """获取存档文件路径"""
        return os.path.join(self.save_dir, f"save_{slot}.json")

    def save_game(self, slot, game_data, screenshot=None):
        """
        保存游戏
        game_data: 包含所有需要保存的数据的字典
        """
        save_path = self._get_save_path(slot)

        save_data = {
            "version": "1.0",
            "timestamp": time.time(),
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": game_data,
        }

        try:
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            return True, "存档成功"
        except Exception as e:
            return False, f"存档失败: {str(e)}"

    def load_game(self, slot):
        """
        读取存档
        返回: (成功?, 数据或错误信息)
        """
        save_path = self._get_save_path(slot)

        if not os.path.exists(save_path):
            return False, "存档不存在"

        try:
            with open(save_path, "r", encoding="utf-8") as f:
                save_data = json.load(f)
            return True, save_data
        except json.JSONDecodeError:
            return False, "存档文件损坏"
        except Exception as e:
            return False, f"读档失败: {str(e)}"

    def delete_save(self, slot):
        """删除存档"""
        save_path = self._get_save_path(slot)

        if not os.path.exists(save_path):
            return False, "存档不存在"

        try:
            os.remove(save_path)
            return True, "存档已删除"
        except Exception as e:
            return False, f"删除失败: {str(e)}"

    def get_save_info(self, slot):
        """
        获取存档信息（不加载完整数据）
        """
        save_path = self._get_save_path(slot)

        if not os.path.exists(save_path):
            return None

        try:
            with open(save_path, "r", encoding="utf-8") as f:
                save_data = json.load(f)

            data = save_data.get("data", {})
            player_data = data.get("player", {})
            quest_data = data.get("quest", {})

            return {
                "slot": slot,
                "datetime": save_data.get("datetime", "未知"),
                "timestamp": save_data.get("timestamp", 0),
                "player_name": player_data.get("name", "未知"),
                "pathway": player_data.get("pathway", "未知"),
                "sequence": player_data.get("sequence", 9),
                "level": player_data.get("level", 1),
                "wave": data.get("wave", 1),
                "playtime": data.get("playtime", 0),
                "quest_progress": len(quest_data.get("completed_quests", [])),
            }
        except:
            return None

    def get_all_saves(self):
        """获取所有存档信息"""
        saves = []

        # 检查所有可能的存档槽位
        for slot in range(1, self.max_saves + 1):
            info = self.get_save_info(slot)
            if info:
                saves.append(info)
            else:
                saves.append({
                    "slot": slot,
                    "empty": True,
                })

        # 检查自动存档
        auto_info = self.get_save_info(self.auto_save_slot)
        if auto_info:
            auto_info["is_auto"] = True
            saves.insert(0, auto_info)
        else:
            saves.insert(0, {
                "slot": self.auto_save_slot,
                "empty": True,
                "is_auto": True,
            })

        return saves

    def has_any_save(self):
        """检查是否有任何存档"""
        for slot in range(1, self.max_saves + 1):
            if os.path.exists(self._get_save_path(slot)):
                return True
        if os.path.exists(self._get_save_path(self.auto_save_slot)):
            return True
        return False

    def get_latest_save(self):
        """获取最新的存档"""
        latest = None
        latest_time = 0

        for slot in range(1, self.max_saves + 1):
            info = self.get_save_info(slot)
            if info and info.get("timestamp", 0) > latest_time:
                latest_time = info["timestamp"]
                latest = info

        # 检查自动存档
        auto_info = self.get_save_info(self.auto_save_slot)
        if auto_info and auto_info.get("timestamp", 0) > latest_time:
            latest = auto_info

        return latest

    def auto_save(self, game_data):
        """自动存档"""
        return self.save_game(self.auto_save_slot, game_data)


def collect_game_data(game):
    """
    从游戏实例收集需要保存的数据
    """
    data = {}

    # 玩家数据
    if game.player:
        player = game.player
        data["player"] = {
            "name": getattr(player, "name", "未知"),
            "pathway": getattr(player, "pathway_id", "未知"),
            "sequence": getattr(player, "sequence", 9),
            "level": getattr(player, "level", 1),
            "exp": getattr(player, "exp", 0),
            "hp": player.hp,
            "max_hp": player.max_hp,
            "attack": player.attack,
            "defense": player.defense,
            "x": player.x,
            "y": player.y,
            "equipped_weapon": player.get_equipped_weapon() if hasattr(player, "get_equipped_weapon") else None,
            "skills": player.skills if hasattr(player, "skills") else {},
        }

    # 背包数据
    if hasattr(game, "inventory") and game.inventory:
        data["inventory"] = game.inventory.to_dict()

    # 任务数据
    if hasattr(game, "quest_system") and game.quest_system:
        data["quest"] = game.quest_system.to_dict()

    # 游戏状态
    data["wave"] = getattr(game, "wave", 1)
    data["score"] = getattr(game, "score", 0)
    data["playtime"] = getattr(game, "playtime", 0)
    data["kills"] = getattr(game, "total_kills", 0)

    # 统计数据
    data["stats"] = {
        "total_kills": getattr(game, "total_kills", 0),
        "max_wave": getattr(game, "max_wave_reached", 1),
        "max_combo": getattr(game, "max_combo", 0),
        "bosses_killed": getattr(game, "bosses_killed", 0),
        "deaths": getattr(game, "deaths", 0),
    }

    return data


def apply_save_data(game, save_data):
    """
    将存档数据应用到游戏实例
    """
    data = save_data.get("data", {})

    # 恢复玩家数据
    player_data = data.get("player", {})
    if game.player and player_data:
        player = game.player
        player.pathway_id = player_data.get("pathway", player.pathway_id)
        player.sequence = player_data.get("sequence", 9)
        player.level = player_data.get("level", 1)
        player.exp = player_data.get("exp", 0)
        player.hp = player_data.get("hp", player.max_hp)
        player.max_hp = player_data.get("max_hp", player.max_hp)
        player.attack = player_data.get("attack", player.attack)
        player.defense = player_data.get("defense", player.defense)

        # 恢复位置
        player.x = player_data.get("x", player.x)
        player.y = player_data.get("y", player.y)

        # 恢复装备武器
        equipped_weapon = player_data.get("equipped_weapon")
        if equipped_weapon and hasattr(player, "equip_weapon"):
            player.equip_weapon(equipped_weapon)

        # 恢复技能
        if "skills" in player_data and hasattr(player, "skills"):
            player.skills = player_data["skills"]

    # 恢复背包数据
    inventory_data = data.get("inventory")
    if hasattr(game, "inventory") and game.inventory and inventory_data:
        game.inventory.from_dict(inventory_data)

    # 恢复任务数据
    quest_data = data.get("quest")
    if hasattr(game, "quest_system") and game.quest_system and quest_data:
        game.quest_system.from_dict(quest_data)

    # 恢复游戏状态
    game.wave = data.get("wave", 1)
    game.score = data.get("score", 0)
    game.playtime = data.get("playtime", 0)
    game.total_kills = data.get("kills", 0)

    # 恢复统计数据
    stats = data.get("stats", {})
    game.total_kills = stats.get("total_kills", game.total_kills)
    game.max_wave_reached = stats.get("max_wave", 1)
    game.max_combo = stats.get("max_combo", 0)
    game.bosses_killed = stats.get("bosses_killed", 0)
    game.deaths = stats.get("deaths", 0)

    return True
