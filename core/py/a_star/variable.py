from dataclasses import dataclass

from py.variable import GridPoint


@dataclass(frozen = True)
class PositionSamePath:
    map_name: str
    start: GridPoint
    end: GridPoint
