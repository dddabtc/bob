"""
任务系统
"""

from data.quests import (
    ALL_QUESTS, MAIN_QUESTS, SIDE_QUESTS, DAILY_QUESTS,
    QUEST_STATUS_LOCKED, QUEST_STATUS_AVAILABLE, QUEST_STATUS_ACTIVE,
    QUEST_STATUS_COMPLETE, QUEST_STATUS_FINISHED,
    OBJECTIVE_KILL, OBJECTIVE_COLLECT, OBJECTIVE_REACH_WAVE,
    OBJECTIVE_CRAFT, OBJECTIVE_TALK, OBJECTIVE_ADVANCE,
    get_quest_data, get_initial_quests
)


class QuestSystem:
    """任务系统"""

    def __init__(self):
        # 任务状态: {quest_id: status}
        self.quest_status = {}
        # 任务进度: {quest_id: {objective_index: current_count}}
        self.quest_progress = {}
        # 已完成的任务
        self.completed_quests = set()
        # 当前激活的任务
        self.active_quests = []
        # 待播放的对话
        self.pending_dialogue = None
        # 初始化
        self._init_quests()

    def _init_quests(self):
        """初始化任务状态"""
        # 设置所有任务初始状态
        for quest_id, quest in ALL_QUESTS.items():
            prereqs = quest.get("prerequisites", [])
            if not prereqs:
                # 没有前置任务，直接可用
                self.quest_status[quest_id] = QUEST_STATUS_AVAILABLE
            else:
                self.quest_status[quest_id] = QUEST_STATUS_LOCKED

    def get_quest_status(self, quest_id):
        """获取任务状态"""
        return self.quest_status.get(quest_id, QUEST_STATUS_LOCKED)

    def get_available_quests(self, player_sequence):
        """获取可接取的任务列表"""
        available = []
        for quest_id, status in self.quest_status.items():
            if status == QUEST_STATUS_AVAILABLE:
                quest = get_quest_data(quest_id)
                if quest and quest.get("required_sequence", 9) >= player_sequence:
                    available.append(quest_id)
        return available

    def get_active_quests(self):
        """获取进行中的任务"""
        return self.active_quests

    def accept_quest(self, quest_id):
        """接受任务"""
        if self.quest_status.get(quest_id) != QUEST_STATUS_AVAILABLE:
            return False, "任务不可接取"

        quest = get_quest_data(quest_id)
        if not quest:
            return False, "任务不存在"

        # 设置任务状态
        self.quest_status[quest_id] = QUEST_STATUS_ACTIVE
        self.active_quests.append(quest_id)

        # 初始化进度
        self.quest_progress[quest_id] = {}
        for i, obj in enumerate(quest.get("objectives", [])):
            self.quest_progress[quest_id][i] = 0

        # 设置开始对话
        if "dialogue_start" in quest:
            self.pending_dialogue = {
                "quest_id": quest_id,
                "type": "start",
                "dialogues": quest["dialogue_start"],
            }

        return True, f"接受任务: {quest['name']}"

    def update_objective(self, objective_type, target, count=1):
        """更新任务目标进度"""
        updated_quests = []

        for quest_id in self.active_quests:
            quest = get_quest_data(quest_id)
            if not quest:
                continue

            progress = self.quest_progress.get(quest_id, {})

            for i, obj in enumerate(quest.get("objectives", [])):
                if obj["type"] != objective_type:
                    continue

                # 检查目标匹配
                obj_target = obj.get("target", "any")
                if obj_target != "any" and obj_target != target:
                    continue

                # 更新进度
                current = progress.get(i, 0)
                required = obj.get("count", 1)

                if current < required:
                    progress[i] = min(current + count, required)
                    self.quest_progress[quest_id] = progress
                    updated_quests.append((quest_id, obj["desc"], progress[i], required))

            # 检查任务是否完成
            if self._check_quest_complete(quest_id):
                self.quest_status[quest_id] = QUEST_STATUS_COMPLETE

        return updated_quests

    def _check_quest_complete(self, quest_id):
        """检查任务是否完成所有目标"""
        quest = get_quest_data(quest_id)
        if not quest:
            return False

        progress = self.quest_progress.get(quest_id, {})

        for i, obj in enumerate(quest.get("objectives", [])):
            required = obj.get("count", 1)
            current = progress.get(i, 0)
            if current < required:
                return False

        return True

    def complete_quest(self, quest_id, inventory):
        """完成任务并领取奖励"""
        if self.quest_status.get(quest_id) != QUEST_STATUS_COMPLETE:
            return False, "任务未完成", None

        quest = get_quest_data(quest_id)
        if not quest:
            return False, "任务不存在", None

        # 标记完成
        self.quest_status[quest_id] = QUEST_STATUS_FINISHED
        self.completed_quests.add(quest_id)
        if quest_id in self.active_quests:
            self.active_quests.remove(quest_id)

        # 发放奖励
        rewards = quest.get("rewards", {})
        reward_text = []

        # 经验奖励
        exp = rewards.get("exp", 0)
        if exp > 0:
            reward_text.append(f"经验 +{exp}")

        # 材料奖励
        materials = rewards.get("materials", {})
        for mat_name, mat_count in materials.items():
            inventory.add_material(mat_name, mat_count)
            reward_text.append(f"{mat_name} x{mat_count}")

        # 解锁后续任务
        unlock_quests = quest.get("unlock_quests", [])
        for unlock_id in unlock_quests:
            if self.quest_status.get(unlock_id) == QUEST_STATUS_LOCKED:
                self.quest_status[unlock_id] = QUEST_STATUS_AVAILABLE

        # 设置结束对话
        if "dialogue_end" in quest:
            self.pending_dialogue = {
                "quest_id": quest_id,
                "type": "end",
                "dialogues": quest["dialogue_end"],
            }

        return True, f"完成任务: {quest['name']}", {
            "exp": exp,
            "materials": materials,
            "reward_text": ", ".join(reward_text),
        }

    def get_quest_progress(self, quest_id):
        """获取任务进度详情"""
        quest = get_quest_data(quest_id)
        if not quest:
            return None

        progress = self.quest_progress.get(quest_id, {})
        result = []

        for i, obj in enumerate(quest.get("objectives", [])):
            current = progress.get(i, 0)
            required = obj.get("count", 1)
            result.append({
                "desc": obj.get("desc", "未知目标"),
                "current": current,
                "required": required,
                "complete": current >= required,
            })

        return result

    def on_enemy_killed(self, enemy_name):
        """敌人被击杀时调用"""
        return self.update_objective(OBJECTIVE_KILL, enemy_name)

    def on_item_collected(self, item_name, count=1):
        """物品被收集时调用"""
        return self.update_objective(OBJECTIVE_COLLECT, item_name, count)

    def on_wave_reached(self, wave_number):
        """达到波次时调用"""
        return self.update_objective(OBJECTIVE_REACH_WAVE, wave_number)

    def on_sequence_advanced(self, new_sequence):
        """晋升序列时调用"""
        return self.update_objective(OBJECTIVE_ADVANCE, new_sequence)

    def get_pending_dialogue(self):
        """获取待播放的对话"""
        dialogue = self.pending_dialogue
        self.pending_dialogue = None
        return dialogue

    def has_pending_dialogue(self):
        """是否有待播放的对话"""
        return self.pending_dialogue is not None

    def get_main_quest_progress(self):
        """获取主线任务进度"""
        completed = 0
        total = len(MAIN_QUESTS)
        current = None

        for quest_id in MAIN_QUESTS:
            status = self.quest_status.get(quest_id)
            if status == QUEST_STATUS_FINISHED:
                completed += 1
            elif status in [QUEST_STATUS_ACTIVE, QUEST_STATUS_COMPLETE]:
                current = quest_id

        return {
            "completed": completed,
            "total": total,
            "current": current,
            "progress_percent": (completed / total * 100) if total > 0 else 0,
        }

    def to_dict(self):
        """序列化为字典（用于存档）"""
        return {
            "quest_status": dict(self.quest_status),
            "quest_progress": {k: dict(v) for k, v in self.quest_progress.items()},
            "completed_quests": list(self.completed_quests),
            "active_quests": list(self.active_quests),
        }

    def from_dict(self, data):
        """从字典恢复（用于读档）"""
        self.quest_status = data.get("quest_status", {})
        self.quest_progress = {k: dict(v) for k, v in data.get("quest_progress", {}).items()}
        self.completed_quests = set(data.get("completed_quests", []))
        self.active_quests = data.get("active_quests", [])
