from enum import Enum

from py.font.variable import TextProfile
from py.path.manager import JsonFileID, PathConfig
from py.ui_layout.name.identifiers import LayoutName
from py.variable import Color, PageTable


class TextID(Enum):
    ''' 靜態物件使用 '''
    # SYS_CONFIG
    SYS_SONG_NAME = TextProfile(
        name        = LayoutName.SYS_SONG_NAME,
        content     = "{}",
        color       = Color.BLACK.value,
    )
    SYS_WINDOW_SCALE = TextProfile(
        name        = LayoutName.SYS_WINDOW_SCALE,
        content     = "{}",
        color       = Color.BLACK.value,
    )

    # Game
    GAME_OVER = TextProfile(
        name        = LayoutName.GAME_OVER,
        content     = "Game Over",
        color       = Color.BLACK.value,
        font        = PathConfig.font_eng2
    )
    GAME_TEACH = TextProfile(
        name        = LayoutName.GAME_TEACH,
        content     = "{}",
        color       = Color.BLACK.value,
        font        = PathConfig.font_base
    )

    GAME_BUILDING_ARMY = TextProfile(
        name        = LayoutName.GAME_BUILDING_ARMY,
        content     = "{}",
        color       = Color.BLACK.value,
        font        = PathConfig.font_eng1
    )
    GAME_STATUS_WORD = TextProfile(
        name        = LayoutName.GAME_STATUS_WORD,
        content     = "{}",
        color       = Color.BLACK.value,
        font        = PathConfig.font_eng2
    )
    GAME_JELLY_WORD = TextProfile(
        name        = LayoutName.GAME_JELLY_WORD,
        content     = "{}",
        color       = Color.BLACK.value,
        font        = PathConfig.font_eng1
    )
    GAME_UPGRADE_USER_PRICE = TextProfile(
        name        = LayoutName.GAME_UPGRADE_USER_PRICE,
        content     = "{}",
        color       = Color.BLACK.value,
        font        = PathConfig.font_eng2
    )
    GAME_ABILITY_PRICE = TextProfile(
        name        = LayoutName.GAME_ABILITY_PRICE,
        content     = "{}",
        color       = Color.BLACK.value,
        font        = PathConfig.font_eng2
    )
    GAME_BECOME_PRICE = TextProfile(
        name        = LayoutName.GAME_BECOME_PRICE,
        content     = "{}",
        color       = Color.BLACK.value,
        font        = PathConfig.font_eng2
    )
    GAME_FACTION_BAR_ARMY = TextProfile(
        name        = LayoutName.GAME_FACTION_BAR_ARMY,
        content     = "{}",
        color       = None,
        font        = PathConfig.font_eng2
    )


    ''' 需動態自行導入物件 '''
    # SINGLE_MENU
    SINGLE_MENU_LEVEL_STYLE = TextProfile(
        name    = None,
        content = "{}",
        color   = Color.BLACK.value,
    )


    ''' JSON提取區 '''
    # MENU
    MENU_MAIN = TextProfile(
        name        = LayoutName.MENU_MAIN,
        content     = "{}",
        color       = Color.BLACK.value,
    )

    # SYS_CONFIG
    SYS_SONG_MAIN = TextProfile(
        name        = LayoutName.SYS_SONG_MAIN,
        content     = "{}",
        color       = Color.BLACK.value,
    )

    # HELP
    HELP_DYNAMIC_TITLE = TextProfile(
        name    = LayoutName.HELP_OPTION_TITLE,
        content = "{}",
        color   = Color.BLACK.value,
    )
    HELP_DYNAMIC_DESC = TextProfile(
        name    = LayoutName.HELP_OPTION_DESC,
        content = "{}",
        color   = Color.BLACK.value,
    )


# 改這邊的路徑，必須同步JSON裡面的dict路徑喔
class TextJson:
    """
    建立 TextID 到 JSON 路徑的直接映射
    Key: TextID
    Value: (JSON_Key_Layer1, JSON_Key_Layer2...)
    """
    mapping = {
        # MENU
        TextID.MENU_MAIN: (JsonFileID.DISPLAY, PageTable.MENU.value, "title"),

        TextID.GAME_TEACH: [
            (JsonFileID.DISPLAY, PageTable.SINGLE.value, "level_0"),
            (JsonFileID.DISPLAY, PageTable.SINGLE.value, "level_1"),
            (JsonFileID.DISPLAY, PageTable.SINGLE.value, "level_2"),
            (JsonFileID.DISPLAY, PageTable.SINGLE.value, "level_3"),
        ],

        TextID.SYS_SONG_MAIN: (JsonFileID.DISPLAY, PageTable.SYS_CONFIG.value, "title"),

        TextID.HELP_DYNAMIC_TITLE: [
            (JsonFileID.DISPLAY, PageTable.HELP.value, "0", "title"),
            (JsonFileID.DISPLAY, PageTable.HELP.value, "1", "title"),
            (JsonFileID.DISPLAY, PageTable.HELP.value, "2", "title")
        ],
        TextID.HELP_DYNAMIC_DESC: [
            (JsonFileID.DISPLAY, PageTable.HELP.value, "0", "description"),
            (JsonFileID.DISPLAY, PageTable.HELP.value, "1", "description"),
            (JsonFileID.DISPLAY, PageTable.HELP.value, "2", "description")
        ],
    }
