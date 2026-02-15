from dataclasses import dataclass
from enum import Enum


@dataclass
class BulletStats:
    damage: float
    speed: float

class BulletVar(Enum):
    # 判定命中 「碰撞半徑」
    HIT_RADIUS_GRID = 0.4
    # 子彈真實移動速度
    MOVE_SPEED_GRID = 35
