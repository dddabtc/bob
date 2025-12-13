"""
魔药炮制系统
"""

from data.items import POTION_RECIPES, get_potion_recipe, can_craft_potion
from data.pathways import PATHWAYS


class PotionSystem:
    """魔药炮制系统"""

    def __init__(self):
        pass

    def get_available_potion(self, player, inventory):
        """获取当前可炮制的魔药（下一序列）"""
        pathway_name = player.pathway_name
        next_sequence = player.sequence - 1  # 晋升到更高序列

        if next_sequence < 7:
            return None, "序列6及以上需要完成最终任务"

        recipe = get_potion_recipe(pathway_name, next_sequence)
        if not recipe:
            return None, "没有对应的魔药配方"

        return recipe, None

    def check_can_craft(self, player, inventory):
        """检查是否可以炮制当前序列的魔药"""
        pathway_name = player.pathway_name
        next_sequence = player.sequence - 1

        if next_sequence < 7:
            return False, "序列6及以上需要完成最终任务", None

        recipe = get_potion_recipe(pathway_name, next_sequence)
        if not recipe:
            return False, "没有对应的魔药配方", None

        # 检查材料
        can_make, msg = can_craft_potion(inventory.materials, pathway_name, next_sequence)
        return can_make, msg, recipe

    def get_recipe_status(self, player, inventory):
        """获取配方状态，显示材料是否足够"""
        pathway_name = player.pathway_name
        next_sequence = player.sequence - 1

        if next_sequence < 7:
            return {
                "available": False,
                "reason": "序列6及以上需要完成最终任务",
                "recipe": None,
                "materials_status": [],
            }

        recipe = get_potion_recipe(pathway_name, next_sequence)
        if not recipe:
            return {
                "available": False,
                "reason": "没有对应的魔药配方",
                "recipe": None,
                "materials_status": [],
            }

        # 检查每种材料
        materials_status = []
        all_enough = True
        for material, required in recipe["materials"].items():
            have = inventory.get_material_count(material)
            enough = have >= required
            if not enough:
                all_enough = False
            materials_status.append({
                "name": material,
                "required": required,
                "have": have,
                "enough": enough,
            })

        return {
            "available": all_enough,
            "reason": "可以炮制" if all_enough else "材料不足",
            "recipe": recipe,
            "materials_status": materials_status,
        }

    def craft_potion(self, player, inventory):
        """炮制魔药并晋升"""
        pathway_name = player.pathway_name
        next_sequence = player.sequence - 1

        # 检查是否可以炮制
        can_make, msg, recipe = self.check_can_craft(player, inventory)
        if not can_make:
            return False, msg

        # 消耗材料
        success, consume_msg = inventory.consume_materials(recipe["materials"])
        if not success:
            return False, consume_msg

        # 执行晋升
        success, advance_msg = self.advance_sequence(player)
        if not success:
            return False, advance_msg

        return True, f"成功炮制{recipe['name']}！{advance_msg}"

    def advance_sequence(self, player):
        """晋升序列"""
        pathway_name = player.pathway_name
        current_sequence = player.sequence
        next_sequence = current_sequence - 1

        if next_sequence < 7:
            return False, "序列6及以上需要完成最终任务"

        # 获取途径数据
        pathway = PATHWAYS.get(pathway_name)
        if not pathway:
            return False, "途径数据错误"

        # 获取新序列数据
        new_seq_data = pathway["sequences"].get(next_sequence)
        if not new_seq_data:
            return False, "序列数据错误"

        # 更新玩家属性
        player.sequence = next_sequence
        player.name = new_seq_data["name"]
        player.max_hp = new_seq_data["hp"]
        player.hp = player.max_hp  # 晋升时恢复满血
        player.attack = new_seq_data["attack"]
        player.defense = new_seq_data["defense"]
        player.speed = new_seq_data["speed"]

        # 更新技能
        player.skill_names = new_seq_data["skills"]
        player._init_skills()

        return True, f"晋升为序列{next_sequence} {player.name}！"

    def get_all_recipes_for_pathway(self, pathway_name):
        """获取指定途径的所有魔药配方"""
        return POTION_RECIPES.get(pathway_name, {})

    def get_pathway_progress(self, player):
        """获取途径进度信息"""
        pathway_name = player.pathway_name
        current_seq = player.sequence

        # 可晋升范围是序列9到序列7
        total_craftable = 3  # 序列9, 8, 7
        crafted = 9 - current_seq  # 已经晋升的次数

        return {
            "pathway": pathway_name,
            "current_sequence": current_seq,
            "current_name": player.name,
            "progress": crafted,
            "max_progress": total_craftable,
            "can_advance": current_seq > 7,
            "next_sequence": current_seq - 1 if current_seq > 7 else None,
        }
