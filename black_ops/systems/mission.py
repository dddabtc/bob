"""
Black Ops - 关卡任务系统
"""

import math

# 导入关卡数据
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.missions import MISSIONS, MISSION_REWARDS


class Objective:
    """任务目标"""

    def __init__(self, data):
        self.id = data['id']
        self.type = data['type']
        self.description = data['description']
        self.required = data.get('required', True)
        self.completed = False

        # 根据类型设置目标数据
        self.target = data.get('target')
        self.item = data.get('item')
        self.count = data.get('count', 1)
        self.current_count = 0

    def check(self, **kwargs):
        """检查目标是否完成"""
        if self.completed:
            return False

        if self.type == 'reach':
            player_pos = kwargs.get('player_pos')
            if player_pos:
                dx = player_pos[0] - self.target[0]
                dy = player_pos[1] - self.target[1]
                if dx * dx + dy * dy < 4:  # 距离小于2
                    self.completed = True
                    return True

        elif self.type == 'collect':
            collected_item = kwargs.get('item')
            if collected_item == self.item:
                self.current_count += 1
                if self.current_count >= self.count:
                    self.completed = True
                    return True

        elif self.type == 'kill':
            killed_type = kwargs.get('enemy_type')
            if killed_type == self.target:
                self.completed = True
                return True

        elif self.type == 'kill_all':
            alive_count = kwargs.get('alive_count', 1)
            if alive_count == 0:
                self.completed = True
                return True

        elif self.type == 'interact':
            interacted = kwargs.get('interact_target')
            if interacted == self.target:
                self.completed = True
                return True

        return False


class MissionSystem:
    """关卡任务系统"""

    def __init__(self):
        self.current_mission_id = None
        self.current_mission = None
        self.objectives = []
        self.completed_missions = set()
        self.dialogue_queue = []
        self.current_dialogue = None

    def load_mission(self, mission_id):
        """加载关卡"""
        if mission_id not in MISSIONS:
            print(f"Mission not found: {mission_id}")
            return None

        self.current_mission_id = mission_id
        self.current_mission = MISSIONS[mission_id].copy()

        # 创建目标对象
        self.objectives = []
        for obj_data in self.current_mission['objectives']:
            self.objectives.append(Objective(obj_data))

        # 加载开场对话
        dialogue = self.current_mission.get('dialogue', {})
        if 'start' in dialogue:
            self.dialogue_queue = list(dialogue['start'])

        return self.current_mission

    def get_mission_info(self, mission_id=None):
        """获取关卡信息"""
        mid = mission_id or self.current_mission_id
        return MISSIONS.get(mid)

    def check_objectives(self, **kwargs):
        """检查任务目标"""
        completed_objectives = []

        for obj in self.objectives:
            if obj.check(**kwargs):
                completed_objectives.append(obj)

                # 触发对话
                dialogue = self.current_mission.get('dialogue', {})
                if obj.id in dialogue:
                    self.dialogue_queue.extend(dialogue[obj.id])

        return completed_objectives

    def is_mission_complete(self):
        """检查关卡是否完成"""
        for obj in self.objectives:
            if obj.required and not obj.completed:
                return False
        return True

    def get_current_objective(self):
        """获取当前目标"""
        for obj in self.objectives:
            if not obj.completed and obj.required:
                return obj
        return None

    def get_all_objectives(self):
        """获取所有目标"""
        return self.objectives

    def complete_mission(self):
        """完成当前关卡"""
        if self.current_mission_id:
            self.completed_missions.add(self.current_mission_id)

        # 获取奖励
        rewards = MISSION_REWARDS.get(self.current_mission_id, {})
        return rewards

    def get_next_mission(self):
        """获取下一关卡"""
        if self.current_mission:
            return self.current_mission.get('next_mission')
        return None

    def has_next_dialogue(self):
        """是否有下一条对话"""
        return len(self.dialogue_queue) > 0

    def get_next_dialogue(self):
        """获取下一条对话"""
        if self.dialogue_queue:
            return self.dialogue_queue.pop(0)
        return None

    def get_player_start(self):
        """获取玩家起始位置"""
        if self.current_mission:
            return self.current_mission.get('player_start', (2, 2))
        return (2, 2)

    def get_player_angle(self):
        """获取玩家起始角度"""
        if self.current_mission:
            return self.current_mission.get('player_angle', 0)
        return 0

    def get_loadout(self):
        """获取关卡装备配置"""
        if self.current_mission:
            return self.current_mission.get('loadout', {})
        return {}

    def get_available_missions(self):
        """获取可用的关卡列表"""
        available = []
        for mid, mdata in MISSIONS.items():
            available.append({
                'id': mid,
                'name': mdata['name'],
                'subtitle': mdata.get('subtitle', ''),
                'completed': mid in self.completed_missions,
            })
        return available


class GameItem:
    """游戏物品 (地图上的可拾取物)"""

    def __init__(self, x, y, item_type, **kwargs):
        self.x = x
        self.y = y
        self.type = item_type
        self.picked_up = False

        # 根据类型设置属性
        self.id = kwargs.get('id')
        self.amount = kwargs.get('amount', 0)
        self.ammo_type = kwargs.get('ammo_type')
        self.weapon_id = kwargs.get('weapon_id')

        # 动画
        self.bob_offset = 0
        self.bob_timer = 0

        # 生成精灵
        self.color = self._get_color()

    def _get_color(self):
        """根据类型获取颜色"""
        colors = {
            'health': (200, 50, 50),
            'armor': (50, 100, 200),
            'ammo': (200, 180, 50),
            'weapon': (150, 100, 200),
            'intel': (50, 200, 100),
            'key': (200, 200, 50),
        }
        return colors.get(self.type, (150, 150, 150))

    def update(self, dt):
        """更新物品状态"""
        self.bob_timer += dt * 3
        self.bob_offset = math.sin(self.bob_timer) * 0.1

    def check_pickup(self, player_x, player_y, pickup_radius=0.8):
        """检查是否被拾取"""
        if self.picked_up:
            return False

        dx = player_x - self.x
        dy = player_y - self.y
        if dx * dx + dy * dy < pickup_radius * pickup_radius:
            self.picked_up = True
            return True

        return False

    def get_sprite_surface(self, width, height):
        """获取物品精灵"""
        import pygame

        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # 根据类型绘制
        if self.type == 'health':
            # 红色十字
            cx, cy = width // 2, height // 2
            size = min(width, height) // 3
            pygame.draw.rect(surface, self.color, (cx - size // 4, cy - size, size // 2, size * 2))
            pygame.draw.rect(surface, self.color, (cx - size, cy - size // 4, size * 2, size // 2))

        elif self.type == 'armor':
            # 蓝色盾牌
            points = [
                (width // 2, height // 5),
                (width * 4 // 5, height // 3),
                (width * 4 // 5, height * 2 // 3),
                (width // 2, height * 4 // 5),
                (width // 5, height * 2 // 3),
                (width // 5, height // 3),
            ]
            pygame.draw.polygon(surface, self.color, points)

        elif self.type == 'ammo':
            # 黄色弹药箱
            pygame.draw.rect(surface, self.color, (width // 4, height // 3, width // 2, height // 2))
            pygame.draw.rect(surface, (150, 130, 30), (width // 4, height // 3, width // 2, height // 2), 2)

        elif self.type == 'weapon':
            # 紫色武器
            pygame.draw.rect(surface, self.color, (width // 6, height // 2 - 5, width * 2 // 3, 10))
            pygame.draw.rect(surface, (100, 70, 150), (width // 4, height // 2 - 8, width // 5, 16))

        elif self.type == 'intel':
            # 绿色文件
            pygame.draw.rect(surface, (250, 250, 240), (width // 4, height // 4, width // 2, height // 2))
            pygame.draw.rect(surface, self.color, (width // 4, height // 4, width // 2, height // 2), 2)
            # 文字线条
            for i in range(3):
                y = height // 4 + 8 + i * 8
                pygame.draw.line(surface, (100, 100, 100), (width // 4 + 5, y), (width * 3 // 4 - 5, y), 1)

        else:
            # 默认圆形
            pygame.draw.circle(surface, self.color, (width // 2, height // 2), min(width, height) // 3)

        return surface


class ItemManager:
    """物品管理器"""

    def __init__(self):
        self.items = []

    def spawn_item(self, x, y, item_type, **kwargs):
        """生成物品"""
        item = GameItem(x, y, item_type, **kwargs)
        self.items.append(item)
        return item

    def spawn_from_mission(self, mission_data):
        """从关卡数据生成物品"""
        self.items.clear()
        for item_data in mission_data.get('items', []):
            self.spawn_item(
                item_data['x'],
                item_data['y'],
                item_data['type'],
                **{k: v for k, v in item_data.items() if k not in ['x', 'y', 'type']}
            )

    def spawn_drop(self, x, y, drop_data):
        """生成敌人掉落物"""
        self.spawn_item(
            x, y,
            drop_data['type'],
            amount=drop_data.get('amount', 0),
            ammo_type=drop_data.get('ammo_type'),
        )

    def update(self, dt, player_x, player_y):
        """更新所有物品"""
        pickups = []

        for item in self.items:
            if item.picked_up:
                continue

            item.update(dt)

            if item.check_pickup(player_x, player_y):
                pickups.append(item)

        return pickups

    def get_active_items(self):
        """获取未拾取的物品"""
        return [item for item in self.items if not item.picked_up]

    def clear(self):
        """清空所有物品"""
        self.items.clear()
