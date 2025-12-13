"""
数据模块 - 途径数据、敌人数据、物品数据、任务数据
"""

from .pathways import PATHWAYS, SKILLS, PATHWAY_TYPES, get_pathways_by_type, get_pathway_names
from .enemies import ENEMY_TYPES, WAVE_CONFIG, get_enemy_data, get_wave_enemies
from .items import MATERIALS, POTION_RECIPES, CONSUMABLES, QUALITY_COLORS, get_material_info, get_potion_recipe
