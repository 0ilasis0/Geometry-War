from typing import TYPE_CHECKING

from py.game.building.logic.variable import (LabSkillState, LabSkillType,
                                             PrototypeConfig)
from py.game.slection import selection_mg
from py.game.variable import GameType
from py.input.mouse.inter_sta_mg import inter_sta_mg
from py.input.mouse.interaction_tool import (get_target_building,
                                             handle_lab_skill_click,
                                             perform_transform)
from py.input.mouse.register import MouseRegistry
from py.input.mouse.variable import IHoverHandler
from py.ui_layout.name.identifiers import LayoutName

if TYPE_CHECKING:
    from py.game.building.entity import BuildingEntity
    from py.game.building.logic.lab import LabLogic

# --- UI 行為註冊 ---

@MouseRegistry.register_ui(LayoutName.MENU_BT_BOARD)
def text_bt():
    print(">> 黑塔轉轉轉 ")


@MouseRegistry.register_ui(LayoutName.GAME_UPGRADE_USER)
def on_click_building_upgrade():
    target = get_target_building()
    if target:
        target.upgrade_comp.perform_upgrade()


@MouseRegistry.register_ui(PrototypeConfig.get_name(GameType.Arch.PRODUCTION))
def on_click_become_production():
    perform_transform(GameType.Arch.PRODUCTION)

@MouseRegistry.register_ui(PrototypeConfig.get_name(GameType.Arch.CASTLE))
def on_click_become_castle():
    perform_transform(GameType.Arch.CASTLE)

@MouseRegistry.register_ui(PrototypeConfig.get_name(GameType.Arch.LAB))
def on_click_become_lab():
    perform_transform(GameType.Arch.LAB)


@MouseRegistry.register_ui(LayoutName.GAME_ABILITY.serial_list[0])
def on_click_skill_ice():
    handle_lab_skill_click(LabSkillType.ICE)

@MouseRegistry.register_ui(LayoutName.GAME_ABILITY.serial_list[1])
def on_click_skill_weak():
    handle_lab_skill_click(LabSkillType.WEAK)

@MouseRegistry.register_ui(LayoutName.GAME_ABILITY.serial_list[2])
def on_click_skill_demon():
    handle_lab_skill_click(LabSkillType.DEMON)



# --- 遊戲物件行為註冊 ---

@MouseRegistry.register_building(None)
def default_building_click(building):
    ''' 註冊通用的 building 行為 '''
    inter_sta_mg.handle_map_click(None)

@MouseRegistry.register_building(GameType.Arch.PROTOTYPE)
def handle_production_click(building):
    inter_sta_mg.handle_map_click(building)

@MouseRegistry.register_building(GameType.Arch.PRODUCTION)
def handle_production_click(building):
    inter_sta_mg.handle_map_click(building)

@MouseRegistry.register_building(GameType.Arch.CASTLE)
def handle_castle_click(building):
    inter_sta_mg.handle_map_click(building)

@MouseRegistry.register_building(GameType.Arch.LAB)
def handle_lab_click(building: "BuildingEntity"):
    logic: LabLogic = building.logic_comp
    target_skill = logic.active_skill

    if logic.current_state == LabSkillState.READY and target_skill is not None:
        # 進入瞄準模式
        selection_mg.select(building)

        def execute_skill(target_entity):
            if target_entity:
                return logic.cast_skill(target_skill, target_entity)
            return False

        inter_sta_mg.enter_targeting_mode(execute_skill)

    else:
        inter_sta_mg.handle_map_click(building)



# --- 定義 Hover 行為 ---

@MouseRegistry.register_building_hover(None)
class DefaultHoverStrategy(IHoverHandler):
    ''' 註冊通用的 Hover 行為 '''
    def on_enter(self, building):
        pass

    def on_exit(self, building):
        pass

@MouseRegistry.register_building_hover(GameType.Arch.CASTLE)
class CastleHoverStrategy(IHoverHandler):
    def on_enter(self, building):
        pass

    def on_exit(self, building):
        pass
