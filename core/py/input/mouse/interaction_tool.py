from typing import TYPE_CHECKING

from py.game.building.logic.variable import LabSkillState, LabSkillType
from py.game.slection import selection_mg
from py.game.variable import GameType

if TYPE_CHECKING:
    from py.game.building.entity import BuildingEntity
    from py.game.building.logic.lab import LabLogic
    from py.game.building.logic.prototype import PrototypeLogic

def get_target_building():
    target: "BuildingEntity" | None = selection_mg.selected_entity
    if not target: return None
    return target


def perform_transform(target_arch: GameType.Arch):
    target = get_target_building()

    if target and target.stats.arch == GameType.Arch.PROTOTYPE:
        logic: PrototypeLogic = target.logic_comp
        logic.transform_to(target_arch)
        selection_mg.deselect()


def handle_lab_skill_click(skill_type: LabSkillType):
    """
    通用的實驗室技能點擊處理邏輯
    """
    target = get_target_building()
    if not target: return

    logic: "LabLogic" = target.logic_comp

    # 檢查是否忙碌
    if not can_brew(logic): return

    # 嘗試開始製作
    if logic.start_production(skill_type):
        # 成功後關閉介面
        selection_mg.deselect()

def can_brew(logic: "LabLogic") -> bool:
    if logic.current_state != LabSkillState.IDLE:
        return False
    return True
