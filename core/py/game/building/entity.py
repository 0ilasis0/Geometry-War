from enum import Enum

from py.game.building.logic.base import BuildingLogic
from py.game.building.logic.upgrade import UpgradeComponent
from py.game.building.logic.variable import LabConfig, LabSkillType
from py.game.building.variable import BaseStatsData, BuildingStats
from py.game.context import GameContext
from py.game.variable import GameType, GameTypeMap, GameVars
from py.resource.registry import ResourceRegistry
from py.ui_layout.scale.manager import IHasLayout
from py.ui_layout.variable import LayoutItem
from py.variable import GridPoint, Position


class BuildingEntity(IHasLayout):
    def __init__(
            self,
            stats: BuildingStats,
            grid_point: GridPoint,
            img_id: str,
            base_data: BaseStatsData
        ):
        self.ui = None
        self.stats = stats
        self.grid_point = grid_point
        self.img_id = img_id
        self._cached_img_id = None

        # 組件
        self.upgrade_comp = UpgradeComponent(self, base_data)
        self.logic_comp: BuildingLogic | None = None # 稍後由工廠注入

        # 狀態效果
        self.active_effects: dict[str, float] = {}

        self.setup()

    def setup(self):
        # 註冊見主擁有者
        GameContext.faction_mg.register(self)
        # 建立圖片快取
        self.refresh_img_id_cache()

    def update(self, dt: float):
        # 處理通用的兵量溢出衰減/處理狀態效果
        self._update_army_decay(dt)
        self._update_status_effects(dt)

        # 執行組件邏輯
        if self.logic_comp:
            self.logic_comp.update(dt)

    def update_layout(self, pos_z: int):
        screen_pos, target_size = GameContext.grid_cvt.get_block_rect(
            grid_pos = self.grid_point,
            grid_span = self.stats.grid_size
        )
        screen_pos.z = pos_z

        if self.layout_ui:
            self.ui.pos = screen_pos
            self.ui.size = target_size
        else:
            self.ui = LayoutItem(
                category = GameContext.page,
                img_id = self.get_self_img_id,
                size = target_size,
                pos = screen_pos,
            )

    def _update_army_decay(self, dt: float):
        stats = self.stats
        if self.has_effect(LabSkillType.ICE): return

        if stats.army > stats.max_army_capacity:
            stats.army -= GameVars.OVERFLOW_DECAY_RATE * dt
            if stats.army < stats.max_army_capacity:
                stats.army = stats.max_army_capacity

    def _update_status_effects(self, dt: float):
        expired_effects = []
        for effect, time in self.active_effects.items():
            self.active_effects[effect] -= dt

            if effect == LabSkillType.WEAK:
                self.stats.army -= LabConfig.WEAK_DAMAGE_PER_SEC * dt
                if self.stats.army < 0:
                    self.stats.army = 0

            # 將過時的效果加入 expired_effects 報廢
            if self.active_effects[effect] <= 0:
                expired_effects.append(effect)

        # 移除失效狀態
        for effect in expired_effects:
            del self.active_effects[effect]

    def add_effect(self, effect_name: Enum, duration: float = None):
        end_time = duration if duration is not None else float("inf")
        self.active_effects[effect_name] = end_time

    def has_effect(self, effect_name: Enum) -> bool:
        return effect_name in self.active_effects

    def set_owner(self, new_owner: GameTypeMap):
        """
        變更建築擁有者並重置狀態
        """
        # 如果擁有者沒變，就不執行
        old_owner = self.stats.owner
        if old_owner == new_owner: return

        # 變更註冊者
        GameContext.faction_mg.transfer_owner(self, old_owner, new_owner)
        # 變更擁有者
        self.stats.owner = new_owner
        # 更新快取
        self.refresh_img_id_cache()
        # 清空所有狀態效果
        self.active_effects.clear()

    def refresh_img_id_cache(self):
        """ 只有狀態改變時呼叫 """
        genre_str = GameTypeMap.get_value(GameType.Genre.ARCH)
        owner_str = GameTypeMap.get_value(self.stats.owner)
        arch_str = GameTypeMap.get_value(self.stats.arch)
        self._cached_img_id = ResourceRegistry.get_key(genre_str, owner_str, arch_str, self.stats.level)

        # 同步更新 UI 的 img_id
        if self.ui:
            self.ui.img_id = self._cached_img_id

    @property
    def center_pos(self) -> Position:
        """
        取得建築物的中心點
        """
        return GameContext.grid_cvt.get_block_center(self.grid_point, self.stats.grid_size)

    @property
    def get_self_img_id(self) -> str:
        return self._cached_img_id

    @property
    def layout_ui(self) -> LayoutItem:
        return self.ui
