from py.debug import dbg
from py.game.building.logic.base import BuildingLogic
from py.game.building.logic.variable import LabSkillType, PrototypeConfig
from py.game.variable import GameType


class PrototypeLogic(BuildingLogic):
    def update(self, dt: float):
        stats = self.building.stats

        # 中立建築不生產士兵
        if stats.owner == GameType.Owner.NEUTRAL: return
        # 如果被虛弱，就停止生產
        if self.building.has_effect(LabSkillType.WEAK): return
        # 檢查是否達到兵量上限
        if stats.army >= stats.max_army_capacity: return
        else:
            stats.army += stats.rate_of_production * dt
            if stats.army >= stats.max_army_capacity:
                stats.army = stats.max_army_capacity

    def transform_to(self, target_arch: GameType.Arch):
        """
        呼叫工廠將自己變身
        """
        cost = PrototypeConfig.get_cost(target_arch)
        if cost is None:
            dbg.error(f">> Error: No cost defined for {target_arch}")
            return

        if self.building.stats.army < cost: return

        self.building.stats.army -= cost

        from py.game.building.factory import BuildingFactory
        BuildingFactory.transform_entity(self.building, target_arch)
