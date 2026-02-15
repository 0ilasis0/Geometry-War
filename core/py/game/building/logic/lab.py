from typing import TYPE_CHECKING, Callable

from py.debug import dbg
from py.game.building.logic.base import BuildingLogic
from py.game.building.logic.variable import (LabConfig, LabConfigKey,
                                             LabSkillState, LabSkillType)
from py.game.slection import selection_mg
from py.game.variable import GameType
from py.input.mouse.inter_sta_mg import inter_sta_mg

if TYPE_CHECKING:
    from py.game.building.entity import BuildingEntity

class LabLogic(BuildingLogic):
    def __init__(self, building: "BuildingEntity"):
        super().__init__(building)

        self._skill_dispatch: dict[LabSkillType, Callable] = {
            LabSkillType.ICE: self._apply_ice,
            LabSkillType.WEAK: self._apply_weak,
            LabSkillType.DEMON: self._apply_demon,
        }

        self.current_state: LabSkillState = LabSkillState.IDLE
        self.active_skill: LabSkillType | None = None  # 目前正在做(或做完)的是哪一個
        self.production_timer: float = 0.0                # 倒數計時器

    def update(self, dt: float):
        if self.current_state == LabSkillState.BREWING:
            if self.production_timer > 0:
                self.production_timer -= dt
            else:
                # --- 製作完成 ---
                self.current_state = LabSkillState.READY
                self.production_timer = 0.0
                # 如果玩家正選著這棟建築，直接進入瞄準
                if self.building.stats.owner == GameType.Owner.PLAYER:
                    if selection_mg.selected_entity == self.building:
                        self._enter_auto_targeting()

    def start_production(self, skill_type: LabSkillType) -> bool:
        """ [階段一] 開始製藥 (扣款、開始 CD) """
        # 檢查狀態 (只有 IDLE 才能製作)
        if self.current_state != LabSkillState.IDLE: return False

        config = LabConfig.SKILL.get(skill_type)
        if not config: return False

        cost = config[LabConfigKey.COST]
        if self.building.stats.army < cost: return False

        # 執行製作 (扣款、設 Timer)
        self.building.stats.army -= cost
        self.current_state = LabSkillState.BREWING
        self.active_skill = skill_type

        # 讀取 CD 時間作為製作時間
        cd_time = config.get(LabConfigKey.CD)
        self.production_timer = cd_time

        return True

    def cast_skill(self, skill_type: LabSkillType, target: "BuildingEntity") -> bool:
        """ [階段二] 施放技能 (只有 READY 才能施放) """
        # 檢查狀態
        if self.current_state != LabSkillState.READY: return False

        # 檢查施放的是不是手上拿的那個藥
        if self.active_skill != skill_type: return False

        # 檢查是不是自己人
        if self.building.stats.owner == target.stats.owner: return

        # 真正產生效果
        apply_func = self._skill_dispatch.get(skill_type)
        if apply_func:
            apply_func(target)
            self.current_state = LabSkillState.IDLE
            self.active_skill = None
            return True
        else:
            dbg.error(f'{skill_type} apply_func is not exisit')

        return False

    def get_ready_skill(self) -> LabSkillType | None:
        """ 取得目前佔用實驗室的技能 (不論是 BREWING 還是 READY) """
        return self.active_skill

    def get_remaining_cd(self, skill_type: LabSkillType) -> float:
        """ 回傳某技能還剩幾秒 CD (0 代表可用) """
        if self.current_state == LabSkillState.BREWING and self.active_skill == skill_type:
            return max(0.0, self.production_timer)
        return 0.0

    def get_max_cd(self, skill_type: LabSkillType) -> float:
        """ 回傳某技能的總 CD 時間 (用來畫進度條) """
        config = LabConfig.SKILL.get(skill_type)
        if config:
            return config.get(LabConfigKey.CD, 1.0) # 避免除以 0
        return 1.0

    # --- 技能效果實作 ---

    def _apply_ice(self, target: "BuildingEntity"):
        """ ICE: 將敵人建築變成中立 (且溢出與建築效果消失) """
        target.set_owner(GameType.Owner.NEUTRAL)
        target.add_effect(LabSkillType.ICE)

    def _apply_weak(self, target: "BuildingEntity"):
        """ WEAK: 虛弱狀態 40秒 (-1/s, 停產) """
        skill_data = LabConfig.SKILL[LabSkillType.WEAK]
        duration = skill_data.get(LabConfigKey.DURATION, 0.0)

        if duration > 0:
            target.add_effect(LabSkillType.WEAK, duration = duration)
        else:
            dbg.war("Weak skill casted but no duration defined in config!")

    def _apply_demon(self, target: "BuildingEntity"):
        """ DEMON: 將敵人建築變為我方 """
        skill_data = LabConfig.SKILL[LabSkillType.DEMON]
        duration = skill_data.get(LabConfigKey.DURATION, 0.0)

        if duration > 0:
            target.set_owner(self.building.stats.owner)
            target.add_effect(LabSkillType.DEMON, duration = duration)
        else:
            dbg.war("Weak skill casted but no duration defined in config!")

    # --- 內部邏輯 ---

    def _enter_auto_targeting(self):
        """ 進入瞄準模式 """
        current_skill = self.active_skill

        def execute_skill(target_entity):
            if target_entity:
                return self.cast_skill(current_skill, target_entity)
            return False

        inter_sta_mg.enter_targeting_mode(execute_skill)

    # --- AI邏輯 ---

    def can_cast(self) -> bool:
        return self.current_state == LabSkillState.IDLE

    def get_ready_skill(self) -> LabSkillType | None:
        ''' 讓 AI 查詢目前準備好的技能 '''
        if self.current_state == LabSkillState.READY:
            return self.active_skill
        return None
