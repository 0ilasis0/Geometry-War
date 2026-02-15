from copy import copy
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from py.debug import dbg
from py.game.ai.variable import AIStrategicState
from py.game.context import GameContext
from py.game.variable import GameType

if TYPE_CHECKING:
    from py.game.ai.command.manager import AICommander
    from py.game.building.entity import BuildingEntity

@dataclass
class GlobalSituation:
    my_total_army: float = 0
    my_production_rate: float = 0

    strongest_enemy_id: Optional[GameType.Owner] = None
    strongest_enemy_army: float = 0

    avg_enemy_army: float = 0
    avg_enemy_production: float = 0

    enemy_count: int = 0

class StrategyAnalyzer:
    def __init__(self, commander: "AICommander"):
        self.cmd = commander
        self.current_state = AIStrategicState.EARLY_EXPAND
        self.situation = GlobalSituation()

        # 備份一份原始設定，用於每一輪重置
        self.base_profile = copy(self.cmd.profile)

    def analyze(self):
        """ 分析全場局勢 """
        # 獲取我方數據 (直接讀 Faction 物件)
        my_faction = GameContext.faction_mg.get_faction(self.cmd.owner)
        if not my_faction: return # 防呆

        self.situation.my_total_army = my_faction.total_army
        self.situation.my_production_rate = my_faction.production_rate

        # 獲取敵方數據
        enemies = GameContext.faction_mg.get_alive_enemy_factions(exclude_owner=self.cmd.owner)

        total_enemy_army = 0.0
        total_enemy_prod = 0.0
        max_army = -1.0
        strongest_owner = None

        for e_faction in enemies:
            total_enemy_army += e_faction.total_army
            total_enemy_prod += e_faction.production_rate

            # 尋找最強者
            if e_faction.total_army > max_army:
                max_army = e_faction.total_army
                strongest_owner = e_faction.owner

        count = len(enemies)
        self.situation.enemy_count = count
        if count > 0:
            self.situation.strongest_enemy_id = strongest_owner
            self.situation.strongest_enemy_army = max_army
            self.situation.avg_enemy_army = total_enemy_army / count
            self.situation.avg_enemy_production = total_enemy_prod / count
        else:
            # 沒有敵人了
            self.situation.strongest_enemy_id = None
            self.situation.strongest_enemy_army = 0
            self.situation.avg_enemy_army = 0

        # 決定戰略狀態
        self._determine_state()

        # 應用策略權重
        self._apply_strategy()

    def _determine_state(self):
        my_army = self.situation.my_total_army
        top_enemy_army = self.situation.strongest_enemy_army

        # [階段 1] 開局期：兵都很像少的時候
        # 門檻可根據遊戲數值調整，例如 50
        if my_army < 100 and top_enemy_army < 100:
            self.current_state = AIStrategicState.EARLY_EXPAND
            return

        # [階段 2] 根據兵力比決定
        ratio = my_army / max(1.0, top_enemy_army)

        if ratio > 1.5:
            self.current_state = AIStrategicState.DOMINATING
        elif ratio < 0.4:
            self.current_state = AIStrategicState.SURVIVAL
        else:
            self.current_state = AIStrategicState.BALANCED

    def _apply_strategy(self):
        """ 根據狀態修改 cmd.profile 的參數 """
        self._reset_profile_defaults()

        # 取得引用
        p = self.cmd.profile
        base = self.base_profile
        state = self.current_state

        # 應用修正
        if state == AIStrategicState.EARLY_EXPAND:
            # [擴張期]
            p.weight_attack = base.weight_attack * 1.2
            p.bias_build_production += 0.5

            # 門檻降低
            p.swarm_trigger_ratio = max(0.2, base.swarm_trigger_ratio - 0.2)
            p.threshold_attack_neutral -= 1.0

            # 家裡少留點兵，全力擴張
            p.min_attack_reserve = max(1, int(base.min_attack_reserve * 0.5))

        elif state == AIStrategicState.DOMINATING:
            # [優勢期]
            p.weight_attack = base.weight_attack * 1.5
            p.weight_defense *= 0.5

            # 鼓勵升人口
            p.weight_upgrade_castle += 1.0
            p.swarm_trigger_ratio = max(0.3, base.swarm_trigger_ratio - 0.3)
            p.threshold_attack_base -= 2.0

            # 幾乎不留守兵力，全軍壓上
            p.min_attack_reserve = max(1, int(base.min_attack_reserve * 0.2))

        elif state == AIStrategicState.SURVIVAL:
            # [劣勢期]
            p.weight_attack *= 0.2
            p.weight_defense += 3.0
            p.weight_upgrade_production += 2.0
            p.weight_upgrade_castle = 0.0

            # 門檻極高
            p.swarm_trigger_ratio = 1.0
            p.threshold_attack_base += 10.0

            # 家裡必須留更多兵防守
            p.min_defense_reserve = int(base.min_defense_reserve * 1.5)
            p.min_attack_reserve = int(base.min_attack_reserve * 2.0)

        elif state == AIStrategicState.BALANCED:
            # [平衡期]
            p.weight_upgrade_castle += 0.2
            p.bias_build_production += 0.2
            p.swarm_trigger_ratio = max(0.5, base.swarm_trigger_ratio - 0.1)

    def _reset_profile_defaults(self):
        """ 將 Profile 數值重置為 '性格基底' """
        current = self.cmd.profile
        base = self.base_profile

        from dataclasses import fields
        for field in fields(base):
            value = getattr(base, field.name)
            setattr(current, field.name, value)

    def get_strategic_value_modifier(self, target_building: "BuildingEntity") -> float:
        """
        給予目標額外的戰略分數
        """
        bonus = 0.0
        stats = target_building.stats

        # --- 針對中立目標邏輯 (擴張期的關鍵) ---
        if stats.owner == GameType.Owner.NEUTRAL:
            if self.current_state == AIStrategicState.EARLY_EXPAND:
                bonus += 20.0  # 極度渴望中立地盤
            elif self.current_state == AIStrategicState.BALANCED:
                bonus += 5.0   # 加減吃
            elif self.current_state == AIStrategicState.SURVIVAL:
                bonus -= 10.0  # 別惹事

            return bonus

        # --- 針對最強者邏輯 ---
        strongest_id = self.situation.strongest_enemy_id
        if strongest_id and stats.owner == strongest_id:
            # 既然我最強，那誰最接近我，我就打誰，確保無人能追上
            if self.current_state == AIStrategicState.DOMINATING:
                bonus += 30.0  # 大幅增加權重，幾乎強制優先攻擊

            # 大家差不多，但我不希望最強者繼續坐大
            elif self.current_state == AIStrategicState.BALANCED:
                bonus += 20.0  # 給予足夠的誘因去騷擾最強者

            # 我快死了，絕對不要去碰最強的人
            elif self.current_state == AIStrategicState.SURVIVAL:
                bonus -= 50.0  # 極度排斥，除非對方空城

            # 除非最強者就在家門口，否則別理他
            elif self.current_state == AIStrategicState.EARLY_EXPAND:
                bonus -= 5.0   # 稍微降低興趣

        # --- 針對最弱者邏輯 ---
        # 如果不是最強者，且我是優勢或平衡，打弱者也是擴張的好方法
        elif stats.owner != GameType.Owner.NEUTRAL and stats.owner != GameType.Owner.PLAYER:
            if self.current_state == AIStrategicState.DOMINATING:
                bonus += 10.0 # 順手清理雜魚
            elif self.current_state == AIStrategicState.SURVIVAL:
                bonus += 15.0 # 劣勢時，只能透過吃掉更弱的對手來補血

        # --- 針對工廠邏輯 ---
        if stats.arch == GameType.Arch.PRODUCTION:
            my_prod = self.situation.my_production_rate
            avg_prod = self.situation.avg_enemy_production
            if my_prod < avg_prod:
                diff_ratio = avg_prod / max(0.1, my_prod)
                bonus += 3.0 * diff_ratio
            else:
                bonus += 2.0

        return bonus
