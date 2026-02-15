from enum import Enum, IntEnum, auto


class AIActionKey(str, Enum):
    OWNER = "owner"
    TYPE = "type"
    TARGET = "target"
    SOURCE = "source"
    ARCH = "arch"
    SCORE = "score"
    SKILL = "skill"
    OVER_TIME = "over_time"

class AIActionType(Enum):
    BUILD = auto()      # 地基變身
    UPGRADE = auto()    # 建築升級
    ATTACK = auto()     # 派兵攻擊/佔領
    DEFEND = auto()     # 派兵支援
    TRANSFER = auto()   # 運輸支援
    LAB_SKILL = auto()  # 施放技能


class AIStrategicState(Enum):
    EARLY_EXPAND = auto()   # [開局] 搶中立建築、搶工廠
    BALANCED = auto()       # [均勢] 穩紮穩打
    DOMINATING = auto()     # [優勢] 積極進攻、碾壓 (滾雪球)
    SURVIVAL = auto()       # [劣勢] 龜縮防守、只升級工廠、屯兵



class AIVar(IntEnum):
    PATH_STEP_STRIDE = 5
