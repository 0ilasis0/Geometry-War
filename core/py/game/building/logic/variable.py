from enum import Enum, IntEnum

from py.game.variable import GameType
from py.ui_layout.name.identifiers import LayoutName
from py.variable import Color


class LabSkillType(IntEnum):
    ICE = 0
    WEAK = 1
    DEMON = 2

class LabConfigKey(str, Enum):
    COST = "cost"
    LEVEL = "level"
    DURATION = "duration"
    CD = "cd"   # 冷卻時間
    COLOR = "color"

class LabSkillState(Enum):
    IDLE = 0     # 閒置 (可點擊按鈕開始製作)
    BREWING = 1  # 製作中 (讀條中)
    READY = 2    # 製作完成 (點擊實驗室可施放)

class LabConfig:
    # --- 全域設定 ---
    WEAK_DAMAGE_PER_SEC = 1.0

    # --- 技能配置表 (None表示無期限) ---
    SKILL = {
        LabSkillType.ICE: {
            LabConfigKey.COST: 20,
            LabConfigKey.LEVEL: 0,
            LabConfigKey.DURATION: None,
            LabConfigKey.CD: 10.0,
            LabConfigKey.COLOR: Color.SKY_BLUE.value
        },
        LabSkillType.WEAK: {
            LabConfigKey.COST: 30,
            LabConfigKey.LEVEL: 1,
            LabConfigKey.DURATION: 40.0,
            LabConfigKey.CD: 15.0,
            LabConfigKey.COLOR: Color.DEEP_GREEN.value
        },
        LabSkillType.DEMON: {
            LabConfigKey.COST: 50,
            LabConfigKey.LEVEL: 2,
            LabConfigKey.DURATION: 1.5,
            LabConfigKey.CD: 25.0,
            LabConfigKey.COLOR: Color.DEEP_RED.value
        }
    }



class CastleConfig(Enum):
    BUFFER_RANGE_RATIO = 1.15




class PrototypeConfigKey(str, Enum):
    COST = "cost"
    NAME = "name"

class PrototypeConfig:
    BECOME_MAP = {
        GameType.Arch.PRODUCTION: {
            PrototypeConfigKey.COST: 5,
            PrototypeConfigKey.NAME: LayoutName.GAME_BECOME.serial_list[0]
        },
        GameType.Arch.CASTLE: {
            PrototypeConfigKey.COST: 8,
            PrototypeConfigKey.NAME: LayoutName.GAME_BECOME.serial_list[1]
        },
        GameType.Arch.LAB: {
            PrototypeConfigKey.COST: 10,
            PrototypeConfigKey.NAME: LayoutName.GAME_BECOME.serial_list[2]
        },
    }

    @classmethod
    def get_name(cls, target_arch: GameType.Arch) -> str | None:
        """
        輸入目標建築類型，回傳對應的 UI 名稱
        如果找不到，回傳 None
        """
        config = cls.BECOME_MAP.get(target_arch)
        if config: return config.get(PrototypeConfigKey.NAME)
        return None

    @classmethod
    def get_cost(cls, target_arch: GameType.Arch) -> int | None:
        """
        輸入目標建築類型，回傳對應的 UI 名稱
        如果找不到，回傳 None
        """
        config = cls.BECOME_MAP.get(target_arch)
        if config: return config.get(PrototypeConfigKey.COST)
        return None
