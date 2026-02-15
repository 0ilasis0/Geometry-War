from py.game.building.logic.base import BuildingLogic
from py.game.building.logic.variable import LabSkillType
from py.game.variable import GameType


class ProductionLogic(BuildingLogic):
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
                
