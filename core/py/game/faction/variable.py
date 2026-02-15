from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol

from py.game.variable import GameType


class IHasArmy(Protocol):
    army: float
    owner: Any

class PowerEntity(Protocol):
    @property
    def stats(self) -> IHasArmy: ...


class FactionKey(str, Enum):
    IS_DEAD = "is_dead"
    ARMY = "army"
    ARCH = "arch"
    BUILDING = "building"
    RATE_OF_PRODUCTION = "rate_of_production"


@dataclass
class FactionStats:
    """ [數據快照] 用於計算過程中的暫存結構 """
    total_army: int = 0.0
    building_count: int = 0
    factory_count: int = 0
    production_rate: float = 0.0

@dataclass
class Faction:
    """ 代表一個陣營實體 """
    owner: GameType.Owner

    # --- 狀態標籤 ---
    is_defeated: bool = False
    is_active: bool = True

    # --- 戰略數據 (快取) ---
    total_army: int = 0.0
    building_count: int = 0
    factory_count: int = 0
    production_rate: float = 0.0

    def reset(self):
        """ 重置所有狀態 (新關卡開始時呼叫) """
        self.is_active = False
        self.is_defeated = False
        self.total_army = 0.0
        self.building_count = 0
        self.factory_count = 0

    def mark_defeated(self):
        """ 標記為死亡 """
        if not self.is_defeated:
            self.is_defeated = True
