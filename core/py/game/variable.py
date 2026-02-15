from enum import Enum, IntEnum, auto

from py.path.variable import (GamePathArch, GamePathGenre, GamePathJob,
                              GamePathOwner)
from py.variable import Color, Size


class GameVars(IntEnum):
    OVERFLOW_DECAY_RATE: float = 1.0

class GridParamsType(str, Enum):
    ORIGIN_X = 'origin_x'
    ORIGIN_Y = 'origin_y'
    CELL_W = 'cell_w'
    CELL_H = 'cell_h'

class EntitySpan:
    BUILDING = Size(10, 10)
    JELLY = Size(4, 4)
    CASTLE_RANGE = Size(35, 35)

class GameMaxVar(IntEnum):
    JELLY_CELL_CAP = 999

    # 0 為 1 等
    LEVEL_PROTOTYPE = 0
    LEVEL_CASTLE = 4
    LEVEL_LAB = 2
    LEVEL_PRODUCTION = 4

    LAB_ABILITY = 3

    VISUAL_STATE_COUNT = 5


class GameType:
    class Genre(Enum):
        ARCH = auto()
        JELLY = auto()
        BULLET = auto()

    class Owner(Enum):
        PLAYER = auto()
        RED = auto()
        YELLOW = auto()
        GREEN = auto()
        PURPLE = auto()
        NEUTRAL = auto()

    class Arch(Enum):
        PROTOTYPE = auto()
        CASTLE = auto()
        LAB = auto()
        PRODUCTION = auto()

    class Job(Enum):
        MILITIA = auto()
        WARRIOR = auto()
        SHIELDBEARED = auto()
        MAGICIAN = auto()


class GameTypeMap:
    genre = {
        GameType.Genre.ARCH: GamePathGenre.ARCH,
        GameType.Genre.JELLY: GamePathGenre.JELLY,
        GameType.Genre.BULLET: GamePathGenre.BULLET
    }

    owner = {
        GameType.Owner.PLAYER: GamePathOwner.PLAYER,
        GameType.Owner.RED: GamePathOwner.RED,
        GameType.Owner.YELLOW: GamePathOwner.YELLOW,
        GameType.Owner.GREEN: GamePathOwner.GREEN,
        GameType.Owner.PURPLE: GamePathOwner.PURPLE,
        GameType.Owner.NEUTRAL: GamePathOwner.NEUTRAL
    }

    arch = {
        GameType.Arch.PROTOTYPE: GamePathArch.PROTOTYPE,
        GameType.Arch.CASTLE: GamePathArch.CASTLE,
        GameType.Arch.LAB: GamePathArch.LAB,
        GameType.Arch.PRODUCTION: GamePathArch.PRODUCTION
    }

    job = {
        GameType.Job.WARRIOR: GamePathJob.WARRIOR,
        GameType.Job.SHIELDBEARED: GamePathJob.SHIELDBEARED,
        GameType.Job.MAGICIAN: GamePathJob.MAGICIAN,
    }

    _ALL_MAP = {**genre, **owner, **arch, **job}

    @classmethod
    def get_value(cls, key: GameType):
        data = cls._ALL_MAP.get(key)
        if data:
            return data.value
        else:
            return None


FACTION_COLORS = {
    GameType.Owner.PLAYER: Color.FACTION_BLUE.value,
    GameType.Owner.RED:    Color.FACTION_RED.value,
    GameType.Owner.YELLOW: Color.FACTION_YELLOW.value,
    GameType.Owner.GREEN: Color.FACTION_GREEN.value,
    GameType.Owner.PURPLE: Color.FACTION_PURPLE.value,
}
