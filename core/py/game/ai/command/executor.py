from typing import TYPE_CHECKING, Any, Dict

from py.debug import dbg
from py.game.ai.variable import AIActionKey, AIActionType
from py.game.building.logic.variable import (LabConfig, LabConfigKey,
                                             PrototypeConfig)
from py.game.jelly.action import execute_dispatch_army
from py.game.variable import GameType

if TYPE_CHECKING:
    from py.game.building.entity import BuildingEntity
    from py.game.building.logic.lab import LabLogic
    from py.game.building.logic.prototype import PrototypeLogic
    from py.game.building.logic.upgrade import UpgradeComponent

class AIExecutor:
    @staticmethod
    def execute(action: dict):
        """ 執行單一 AI 指令 """
        if not AIExecutor._is_valid(action):
            return

        action_type = action[AIActionKey.TYPE]
        target: "BuildingEntity" = action[AIActionKey.TARGET]

        # 建設 (Build)
        if action_type == AIActionType.BUILD:
            # 確保目標是原型地基
            if target.stats.arch != GameType.Arch.PROTOTYPE: return

            target_logic: "PrototypeLogic" = getattr(target, "logic_comp", None)
            if target_logic:
                arch = action[AIActionKey.ARCH]
                target_logic.transform_to(arch)

        # 升級 (Upgrade)
        elif action_type == AIActionType.UPGRADE:
            target_upgrade: "UpgradeComponent" = getattr(target, "upgrade_comp", None)
            if target_upgrade:
                target_upgrade.perform_upgrade()

        # 派兵 (Attack / Defend / Transfer)
        elif action_type in (AIActionType.ATTACK, AIActionType.DEFEND, AIActionType.TRANSFER):
            source: "BuildingEntity" = action[AIActionKey.SOURCE]
            execute_dispatch_army(source, target)

        # 實驗室技能 (Lab Skill)
        elif action_type == AIActionType.LAB_SKILL:
            source: "BuildingEntity" = action[AIActionKey.SOURCE]
            skill_type = action[AIActionKey.SKILL]
            logic: "LabLogic" = getattr(source, "logic_comp", None)

            if not logic: return

            if source == target:
                # 目標是自己 -> 開始製作
                logic.start_production(skill_type)
            else:
                # 目標是別人 -> 丟出去
                logic.cast_skill(skill_type, target)

    @staticmethod
    def _is_valid(action: Dict[str, Any]) -> bool:
        """ 驗證指令是否過期或無效 """
        action_type = action[AIActionKey.TYPE]
        target: "BuildingEntity" = action.get(AIActionKey.TARGET)

        if not target or getattr(target.stats, "is_dead", False): return False

        # 確保目標的所有權沒變 (例如想救援隊友，結果隊友剛被佔領變成敵人)
        expected_owner = action.get(AIActionKey.OWNER)
        if expected_owner is not None and target.stats.owner != expected_owner:
            return False

        # --- 分類檢查 ---

        if action_type == AIActionType.BUILD:
            if target.stats.arch != GameType.Arch.PROTOTYPE: return False
            arch = action[AIActionKey.ARCH]
            cost = PrototypeConfig.get_cost(arch)
            # 檢查錢夠不夠
            if target.stats.army < cost: return False
            return True

        elif action_type == AIActionType.UPGRADE:
            if target.stats.level >= target.stats.max_level: return False
            # 檢查錢夠不夠
            if target.stats.army < target.stats.upgrade_cost_army: return False
            return True

        elif action_type in (AIActionType.ATTACK, AIActionType.DEFEND, AIActionType.TRANSFER):
            source: "BuildingEntity" = action.get(AIActionKey.SOURCE)
            if not source or getattr(source.stats, "is_dead", False): return False
            if source.stats.army < 1: return False

            # 確保來源還是自己的 (可能剛被偷家)
            if source.stats.owner != target.stats.owner and action_type == AIActionType.TRANSFER:
                return False

            return True

        elif action_type == AIActionType.LAB_SKILL:
            source: "BuildingEntity" = action.get(AIActionKey.SOURCE)
            skill_type = action.get(AIActionKey.SKILL)

            if not source or getattr(source.stats, "is_dead", False): return False
            if source.stats.arch != GameType.Arch.LAB: return False

            logic: "LabLogic" = getattr(source, "logic_comp", None)
            if not logic: return False

            # 製作藥水
            if source == target:
                # 必須是閒置狀態 (手裡沒藥，也沒在做藥)
                if not logic.can_cast(): return False
                # 檢查費用
                config = LabConfig.SKILL.get(skill_type)
                if not config or source.stats.army < config[LabConfigKey.COST]: return False

            # 施放藥水
            else:
                # 手裡必須有藥，且藥的種類正確
                ready_skill = logic.get_ready_skill()
                if not ready_skill or ready_skill != skill_type: return False

                # 攻擊型法術不能對友軍施放
                if source.stats.owner == target.stats.owner: return False

            return True

        return False
