from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from py.game.context import GameContext
from py.game.variable import EntitySpan, GameType

if TYPE_CHECKING:
    from py.game.building.entity import BuildingEntity
    from py.variable import GridPoint, Position, Size

# 定義 建築 -> 兵種 的對應關係
ARCH_TO_JOB_MAP = {
    GameType.Arch.PROTOTYPE:  GameType.Job.MILITIA,
    GameType.Arch.CASTLE:     GameType.Job.SHIELDBEARED,
    GameType.Arch.PRODUCTION: GameType.Job.WARRIOR,
    GameType.Arch.LAB:        GameType.Job.MAGICIAN,
}

@dataclass
class JellyBaseData:
    """ [士兵體質設定檔] 定義職業的基礎能力 """
    attack: int = 1
    move_speed_grid: int = 0        # 移動速度 (網格/秒)

@dataclass
class JellyStats:
    """ [士兵實體數據] 會隨遊戲進行而變動 """
    job: GameType.Job       # 職業 (WARRIOR, RANGER...)
    owner: GameType.Owner   # 陣營 (PLAYER, RED...)

    pos: "Position"
    grid_size: "Size" = EntitySpan.JELLY
    path: list["GridPoint"] = field(default_factory = list)

    # 戰鬥數值
    army: float = 0.0
    attack: float = 0.0
    move_speed: float = 0.0

    # 狀態標記
    is_dead: bool = False
    target_building: any = None  # 當前攻擊/移動的目標

@dataclass
class SpawnContext:
    """
    生成情境：將原本散落在各處的參數封裝起來。
    就像是一個「訂單」，包含了工廠生產所需的所有資訊。
    """
    source: "BuildingEntity"       # 來源建築
    target: any                  # 目標建築
    path: list["GridPoint"]        # 移動路徑
    amount: int                  # 生產數量

    @property
    def owner(self):
        return self.source.stats.owner

    @property
    def start_pos(self) -> "Position":
        grid_point = self.source.grid_point
        grid_size = self.source.stats.grid_size
        pos_z = self.source.layout_ui.pos.z
        return GameContext.grid_cvt.get_block_center(grid_point, grid_size, pos_z)

JELLY_BASE_CONFIG = {
    GameType.Job.MILITIA:      JellyBaseData(attack = 0.5, move_speed_grid = 4),
    GameType.Job.SHIELDBEARED: JellyBaseData(attack = 1.0, move_speed_grid = 3),
    GameType.Job.WARRIOR:      JellyBaseData(attack = 1.0, move_speed_grid = 6),
    GameType.Job.MAGICIAN:     JellyBaseData(attack = 1.0, move_speed_grid = 8),
}
