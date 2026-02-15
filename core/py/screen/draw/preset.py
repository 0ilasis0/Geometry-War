from enum import Enum

from py.hmi.config.variable import ConfigVar
from py.screen.draw.variable import DrawProfile, DrawShape
from py.ui_layout.name.identifiers import LayoutName
from py.ui_layout.scale.manager import location_config
from py.variable import Color


class DrawID(Enum):
    # MENU
    MENU_USER = DrawProfile(
        name = LayoutName.MENU_USER,
        color = Color.DEEP_RED.value,
        shape = DrawShape.RECT,
        hollow_factory = lambda: location_config.draw.hollow
    )

    # SINGLE_MENU
    SINGLE_MENU_USER = DrawProfile(
        name = LayoutName.SINGLE_MENU_USER,
        color = Color.HOT_PINK.value,
        shape = DrawShape.RECT,
        hollow_factory = lambda: location_config.draw.hollow
    )

    # GAME
    GAME_MENU_CIRCLE = DrawProfile(
        name = LayoutName.GAME_SELECT_CIRCLE,
        color = Color.CYAN.value,
        shape = DrawShape.CIRCLE,
        hollow_factory = lambda: location_config.draw.hollow
    )
    GAME_CASTLE_RANGE_CIRCLE = DrawProfile(
        name = LayoutName.GAME_CASTLE_RANGE_CIRCLE,
        color = Color.GREY.value,
        shape = DrawShape.CIRCLE,
        hollow_factory = lambda: location_config.draw.hollow
    )
    GAME_PROGRESS_BAR_COLOR = DrawProfile(
        name = LayoutName.GAME_PROGRESS_BAR_COLOR,
        color = None,
        shape = DrawShape.RECT,
    )
    GAME_PROGRESS_BAR = DrawProfile(
        name = LayoutName.GAME_PROGRESS_BAR,
        color = None,
        shape = DrawShape.RECT,
    )
    GAME_FACTION_BAR_COLOR = DrawProfile(
        name = LayoutName.GAME_FACTION_BAR_COLOR,
        color = None,
        shape = DrawShape.RECT,
    )


    # SYS_CONFIG
    SYS_SONG_USER = DrawProfile(
        name = LayoutName.SYS_SONG_USER,
        color = Color.DEEP_RED.value,
        shape = DrawShape.RECT,
        hollow_factory = lambda: location_config.draw.hollow,
    )
    SYS_SONG_BLOCK_CELL = DrawProfile(
        name = LayoutName.SYS_SONG_BLOCK,
        color = Color.DEEP_BLUE.value,
    )
    SYS_SONG_BLOCK_GRID = DrawProfile(
        name = LayoutName.SYS_SONG_BLOCK,
        color = Color.BLACK.value,
        width_block = ConfigVar.WIDTH_BLOCK,
        height_block = ConfigVar.HEIGHT_BLOCK,
        zoom_factory = lambda: location_config.sys_config.song_block_size.width // ConfigVar.WIDTH_BLOCK
    )



    ''' 需動態自行導入物件 '''
    # SINGLE_MENU
    SINGLE_MENU_RECT = DrawProfile(
        name = None,
        color = Color.BLACK.value,
        shape = DrawShape.RECT,
        hollow_factory = lambda: location_config.draw.hollow
    )
