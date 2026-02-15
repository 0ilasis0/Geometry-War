from dataclasses import dataclass
from enum import Enum
from typing import Any

from py.game.variable import EntitySpan, GameMaxVar, GameTypeMap
from py.variable import GridPoint, Size


class BuildingStatsKey(str, Enum):
    ARCH = 'arch'
    OWNER = 'owner'
    GRID = 'grid'

    LEVEL = 'level'
    MAX_LEVEL = 'max_level'

    ARMY = 'army'

@dataclass
class BuildingStats:
    # 基本
    arch: Any
    grid_point: GridPoint
    owner: GameTypeMap | None = None
    grid_size: Size = EntitySpan.BUILDING

    level: int = 0
    max_level: int = 0
    army: float = 0.0
    upgrade_cost_army: int | None = None
    max_army_capacity: int | None = None
    defense: float | None = 1.0
    is_dead: bool = False

    # production 特殊參數
    rate_of_production: float = 0.0

    # castle 特殊參數
    rate_of_fire: float | None = None
    effective_grid_range: float | None = None
    bullet_speed_grid: float = 0
    bullet_damage: float = 0.0

    # jelly(army) 參數
    jelly_attack: float = 0.0
    jelly_speed_grid: int = 0
    jelly_speed: float = 0.0

    @property
    def visual_sprite_index(self) -> int:
        """
        根據兵量百分比，回傳 0~4 的索引
        """
        ratio = self.army / self.max_army_capacity
        idx = int(ratio * (GameMaxVar.VISUAL_STATE_COUNT - 1))
        return max(0, min(GameMaxVar.VISUAL_STATE_COUNT - 1, idx))


@dataclass
class BaseStatsData:
    """
    [建築體質設定檔]
    定義該類型建築的基礎數值與成長規則
    """
    # --- 基礎數值 (Level 0 的狀態) ---
    base_army_cap: int          # 基礎兵量上限 (例如 10, 20, 30)
    base_defense: float = 1.0   # 基礎防禦力
    base_bullet_damage: float = 0.0 # 子彈傷害
    base_rate_of_fire: float = 0.0  # 子彈發射速度週期

    # --- 成長規則開關 ---
    # 費用係數: 預設是 base_army // 2，若有特殊需求可調整
    cost_factor: float = 0.5

    # castle 特殊參數開啟設定
    castle_enable: bool = False
    defence_rate_growth: float = 0.0
    rate_of_fire_growth: float = 0.0
    bullet_damage_rate_groth: float = 0.0

    # 生產速率成長幅度
    prod_rate_base: float = 0.0     # 基礎生產率 (若為0代表不生產)
    prod_rate_growth: float = 0.0   # 每級增加多少生產率

    # --- 士兵能力成長參數 (預設為 0，代表不成長) ---
    jelly_enable: bool = False
    jelly_speed_grid_growth: int = 0.0       # 速度成長 (網格/秒)
    jelly_attack_growth: float = 0.0      # 攻擊成長
