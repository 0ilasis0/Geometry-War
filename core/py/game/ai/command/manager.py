from typing import TYPE_CHECKING, List

from py.debug import dbg
from py.game.ai.command.brain import AIBrain
from py.game.ai.command.executor import AIExecutor
from py.game.ai.command.strategy import StrategyAnalyzer
from py.game.ai.profile.base import AIProfile
from py.game.ai.tool import RandomTool
from py.game.context import GameContext
from py.game.variable import GameType, GameTypeMap

if TYPE_CHECKING:
    from py.game.building.entity import BuildingEntity


class AICommander:
    def __init__(self, owner: "GameTypeMap", profile: AIProfile = None):
        # 如果傳入的是 Faction 物件，自動提取裡面的 owner Enum
        self.owner = owner
        self.profile = profile if profile else AIProfile()

        # 組件
        self.brain = AIBrain(self)
        self.executor = AIExecutor()
        self.strategy = StrategyAnalyzer(self)

        # 數據緩存 (Perception Cache)
        self.my_buildings: List["BuildingEntity"] = []
        self.enemy_buildings: List["BuildingEntity"] = []
        self.neutral_targets : List["BuildingEntity"]= []
        self.my_prototypes: List["BuildingEntity"] = []

        # 佇列與計時器
        self._command_queue = []
        self._think_timer = 0.0      # 思考冷卻
        self._action_timer = 0.0     # 動作執行冷卻 (模擬 APM)
        self._strategy_timer = 0.0   # 戰略分析冷卻

    def update(self, dt: float):
        # 戰略思考 (低頻率)
        self._strategy_timer -= dt
        if self._strategy_timer <= 0:
            self._strategy_timer += RandomTool.calc_fluctuation(
                self.profile.strategy_interval,
                self.profile.random_time_rate
            )
            self._perceive_world()
            self.strategy.analyze()

        # 戰術思考 (中頻率)
        self._think_timer -= dt
        if self._think_timer <= 0:
            self._think_timer += RandomTool.calc_fluctuation(
                self.profile.think_interval,
                self.profile.random_time_rate
            )
            self._perceive_world()

            # 委託大腦思考
            batch_actions = self.brain.think(dt)

            if batch_actions:
                self._command_queue.extend(batch_actions)
                # 避免佇列積壓過多過期指令
                max_queue = int(self.profile.max_batch_actions * 2.5)
                while len(self._command_queue) > max_queue:
                    self._command_queue.pop(0)

        # 執行動作 (高頻率)
        actions_executed = 0
        self._action_timer -= dt
        while self._action_timer <= 0 and self._command_queue:
            # 即使時間未到，但這幀做太多事了，留到下一幀
            if actions_executed >= self.profile.max_actions_per_frame:
                self._action_timer = 0
                break

            self._action_timer += RandomTool.calc_fluctuation(
                self.profile.action_interval,
                self.profile.random_time_rate
            )

            action = self._command_queue.pop(0)
            self.executor.execute(action)
            actions_executed += 1

    def _perceive_world(self):
        """ 更新戰場感知數據 """
        all_buildings = GameContext.building_mg.get_all_buildings()

        self.my_buildings.clear()
        self.enemy_buildings.clear()
        self.neutral_targets.clear()
        self.my_prototypes.clear()

        for b in all_buildings:
            if b.stats.is_dead: continue

            if b.stats.owner == self.owner:
                if b.stats.arch == GameType.Arch.PROTOTYPE:
                    self.my_prototypes.append(b)
                else:
                    self.my_buildings.append(b)
            elif b.stats.owner == GameType.Owner.NEUTRAL:
                self.neutral_targets.append(b)
            else:
                self.enemy_buildings.append(b)

    def calculate_threat_score(self, building: "BuildingEntity", radius_grid = 20) -> int:
        score = 0.0
        for enemy in self.enemy_buildings:
            dx = abs(building.grid_point.col - enemy.grid_point.col)
            dy = abs(building.grid_point.row - enemy.grid_point.row)
            dist_sq = dx**2 + dy**2
            radius_sq = radius_grid*2
            if dist_sq <= radius_sq:
                threat = 1.0
                threat += (enemy.stats.army * 0.1) * enemy.stats.jelly_attack
                threat += enemy.stats.level * 0.5
                score += threat
        return score

    def calculate_defence_power(self,  building: "BuildingEntity"):
        return (building.stats.army * 0.1) * building.stats.defense + 1.0

    def calculate_safety_margin(self, building: "BuildingEntity") -> float:
        """
        計算安全餘裕 (Safety Margin)
        > 0 : 安全 (數值越大越有餘力)
        < 0 : 危險 (數值越小越快死)
        """
        threat = self.calculate_threat_score(building)
        defense = self.calculate_defence_power(building)

        # 餘裕 = 防禦力 - 威脅值
        return defense - threat

    def get_strategic_value(self, building: "BuildingEntity") -> float:
        base_value = 1.0
        stats = building.stats

        if stats.arch == GameType.Arch.CASTLE:
            base_value *= self.profile.val_attack_castle
        elif stats.arch == GameType.Arch.PRODUCTION:
            base_value *= self.profile.val_attack_production
        elif stats.arch == GameType.Arch.LAB:
            base_value *= self.profile.val_attack_lab

        base_value += (stats.level - 1) * 0.5
        strategic_bonus = self.strategy.get_strategic_value_modifier(building)
        return base_value + strategic_bonus

    def get_nearest_enemy_dist(self, building: "BuildingEntity") -> float:
        """ 找出離該建築最近的敵人距離 (Grid Unit) """
        min_dist_sq = float('inf')

        for enemy in self.enemy_buildings:
            d_sq = building.grid_point.dist_sq_to(enemy.grid_point)
            if d_sq < min_dist_sq:
                min_dist_sq = d_sq

        return min_dist_sq ** 0.5 if min_dist_sq != float('inf') else float('inf')

    def get_unit_stats(self, building: "BuildingEntity") -> tuple[float, float]:
        """
        取得該建築生產兵種的 [攻擊力, 移動速度(格/秒)]
        回傳: (attack, speed)
        """
        speed_grid = building.stats.jelly_speed_grid
        attack = building.stats.jelly_attack

        return max(attack, 1.0), max(speed_grid, 0.1)

    def _clear_all(self):
        self.my_buildings.clear()
        self.enemy_buildings.clear()
        self.neutral_targets.clear()
        self.my_prototypes.clear()
