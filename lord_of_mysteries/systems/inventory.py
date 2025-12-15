"""
背包系统
"""

from data.items import MATERIALS, CONSUMABLES, QUALITY_COLORS, get_material_info
from data.weapons import WEAPONS, get_weapon_data


class Inventory:
    """玩家背包"""

    def __init__(self, max_slots=50):
        self.max_slots = max_slots
        self.materials = {}  # 材料: {名称: 数量}
        self.consumables = {}  # 消耗品: {名称: 数量}
        self.weapons = []  # 武器列表（存储武器名称）
        self.max_weapons = 20  # 最多持有武器数
        self.gold = 0  # 金币

    def add_material(self, name, count=1):
        """添加材料"""
        if name not in MATERIALS:
            return False, f"未知材料: {name}"

        current = self.materials.get(name, 0)
        self.materials[name] = current + count
        return True, f"获得 {name} x{count}"

    def remove_material(self, name, count=1):
        """移除材料"""
        current = self.materials.get(name, 0)
        if current < count:
            return False, f"材料不足: {name}"

        self.materials[name] = current - count
        if self.materials[name] <= 0:
            del self.materials[name]
        return True, f"消耗 {name} x{count}"

    def add_consumable(self, name, count=1):
        """添加消耗品"""
        if name not in CONSUMABLES:
            return False, f"未知消耗品: {name}"

        current = self.consumables.get(name, 0)
        self.consumables[name] = current + count
        return True, f"获得 {name} x{count}"

    def remove_consumable(self, name, count=1):
        """移除消耗品"""
        current = self.consumables.get(name, 0)
        if current < count:
            return False, f"消耗品不足: {name}"

        self.consumables[name] = current - count
        if self.consumables[name] <= 0:
            del self.consumables[name]
        return True, f"消耗 {name} x{count}"

    def use_consumable(self, name, player):
        """使用消耗品"""
        if name not in self.consumables or self.consumables[name] <= 0:
            return False, "没有该消耗品"

        item_data = CONSUMABLES.get(name)
        if not item_data:
            return False, "未知消耗品"

        effect = item_data.get("effect", {})

        # 应用效果
        if "heal" in effect:
            heal_amount = effect["heal"]
            player.hp = min(player.hp + heal_amount, player.max_hp)
            self.remove_consumable(name)
            return True, f"恢复了 {heal_amount} 点生命值"

        return False, "无效的消耗品效果"

    def add_gold(self, amount):
        """添加金币"""
        self.gold += amount
        return True, f"获得 {amount} 金币"

    def remove_gold(self, amount):
        """移除金币"""
        if self.gold < amount:
            return False, "金币不足"
        self.gold -= amount
        return True, f"消耗 {amount} 金币"

    def get_material_count(self, name):
        """获取材料数量"""
        return self.materials.get(name, 0)

    def get_consumable_count(self, name):
        """获取消耗品数量"""
        return self.consumables.get(name, 0)

    def get_total_items(self):
        """获取物品总数"""
        return len(self.materials) + len(self.consumables)

    def get_all_materials(self):
        """获取所有材料列表（带详情）"""
        result = []
        for name, count in self.materials.items():
            info = get_material_info(name)
            if info:
                result.append({
                    "name": name,
                    "count": count,
                    "quality": info["quality"],
                    "type": info["type"],
                    "desc": info["desc"],
                })
        # 按品质排序
        quality_order = {"legendary": 0, "epic": 1, "rare": 2, "uncommon": 3, "common": 4}
        result.sort(key=lambda x: quality_order.get(x["quality"], 5))
        return result

    def get_all_consumables(self):
        """获取所有消耗品列表（带详情）"""
        result = []
        for name, count in self.consumables.items():
            info = CONSUMABLES.get(name, {})
            result.append({
                "name": name,
                "count": count,
                "quality": info.get("quality", "common"),
                "desc": info.get("desc", ""),
            })
        return result

    def has_materials(self, materials_dict):
        """检查是否拥有指定材料"""
        for name, count in materials_dict.items():
            if self.get_material_count(name) < count:
                return False
        return True

    def consume_materials(self, materials_dict):
        """消耗指定材料"""
        # 先检查是否足够
        if not self.has_materials(materials_dict):
            return False, "材料不足"

        # 执行消耗
        for name, count in materials_dict.items():
            self.remove_material(name, count)

        return True, "材料已消耗"

    def to_dict(self):
        """序列化为字典（用于存档）"""
        return {
            "materials": dict(self.materials),
            "consumables": dict(self.consumables),
            "weapons": list(self.weapons),
            "gold": self.gold,
        }

    def from_dict(self, data):
        """从字典恢复（用于读档）"""
        self.materials = data.get("materials", {})
        self.consumables = data.get("consumables", {})
        self.weapons = data.get("weapons", [])
        self.gold = data.get("gold", 0)

    # ==================== 武器管理 ====================

    def add_weapon(self, weapon_name):
        """添加武器到背包"""
        if weapon_name not in WEAPONS:
            return False, f"未知武器: {weapon_name}"

        if len(self.weapons) >= self.max_weapons:
            return False, "武器栏已满"

        self.weapons.append(weapon_name)
        return True, f"获得武器: {weapon_name}"

    def remove_weapon(self, weapon_name):
        """从背包移除武器"""
        if weapon_name in self.weapons:
            self.weapons.remove(weapon_name)
            return True, f"移除武器: {weapon_name}"
        return False, "没有该武器"

    def has_weapon(self, weapon_name):
        """检查是否拥有武器"""
        return weapon_name in self.weapons

    def get_all_weapons(self):
        """获取所有武器列表（带详情）"""
        result = []
        for weapon_name in self.weapons:
            weapon_data = get_weapon_data(weapon_name)
            if weapon_data:
                result.append({
                    "name": weapon_name,
                    "type": weapon_data.get("type"),
                    "quality": weapon_data.get("quality", "common"),
                    "attack": weapon_data.get("attack", 0),
                    "special": weapon_data.get("special", ""),
                    "desc": weapon_data.get("desc", ""),
                })
        # 按品质排序
        quality_order = {"legendary": 0, "epic": 1, "rare": 2, "uncommon": 3, "common": 4}
        result.sort(key=lambda x: quality_order.get(x["quality"], 5))
        return result

    def get_weapons_count(self):
        """获取武器数量"""
        return len(self.weapons)
