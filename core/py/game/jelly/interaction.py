from py.game.building.entity import BuildingEntity
from py.game.jelly.variable import JellyStats


class JellyInteractionComponent:
    def __init__(self, stats: JellyStats):
        self.stats = stats

    def on_arrival(self):
        """ 當士兵抵達終點 (target_building) 時呼叫 """
        target: BuildingEntity = self.stats.target_building
        if not target: return

        # 判斷是敵方還是友方
        if target.stats.owner == self.stats.owner:
            self._reinforce(target)
        else:
            self._attack(target)

        # 任務完成，士兵消失
        self.stats.is_dead = True

    def _reinforce(self, building: BuildingEntity):
        """ 我方士兵碰觸我方建築 """
        # 公式：直接相加
        building.stats.army += self.stats.army

    def _attack(self, building: BuildingEntity):
        """ 敵方士兵碰觸敵方建築 """
        building_stats = building.stats
        jelly_stats = self.stats

        defender_power = building_stats.army * building_stats.defense
        attacker_power = jelly_stats.army * jelly_stats.attack
        result_power = defender_power - attacker_power

        if result_power > 0:
            # --- 防守成功 ---
            building_stats.army = round(result_power / building_stats.defense)

        else:
            # --- 防守失敗 ---
            building.set_owner(jelly_stats.owner)
            remaining_attack_power = result_power // jelly_stats.attack
            building_stats.army = abs(remaining_attack_power)
