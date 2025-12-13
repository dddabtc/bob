"""
背包系统
"""

from data.items import MATERIALS, CONSUMABLES, QUALITY_COLORS, get_material_info


class Inventory:
    """玩家背包"""

    def __init__(self, max_slots=50):
        self.max_slots = max_slots
        self.materials = {}  # 材料: {名称: 数量}
        self.consumables = {}  # 消耗品: {名称: 数量}
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
            "gold": self.gold,
        }

    def from_dict(self, data):
        """从字典恢复（用于读档）"""
        self.materials = data.get("materials", {})
        self.consumables = data.get("consumables", {})
        self.gold = data.get("gold", 0)
