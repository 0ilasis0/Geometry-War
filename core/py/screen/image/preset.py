from py.path.manager import PathConfig
from py.resource.loader import ResourceAutoLoader
from py.screen.image.variable import ImageProfile
from py.ui_layout.name.identifiers import LayoutName
from py.ui_layout.scale.preset.menu import ScaleMenuVar


def P(path, **kwargs):
    return ImageProfile(path = path, **kwargs)

IMAGE_RESOURCE_MAP = {
    # --- 背景類 ---
    LayoutName.MENU_BG:          P(PathConfig.bg_menu),
    LayoutName.SINGLE_BG:        P(PathConfig.bg_single),
    LayoutName.SINGLE_MENU_BG:   P(PathConfig.bg_single_menu),
    LayoutName.SYS_CONFIG_BG:    P(PathConfig.bg_sys),
    LayoutName.HELP_BG:          P(PathConfig.bg_sys),

    # --- UI 類 ---
    LayoutName.MENU_BT_BOARD:    P(
        PathConfig.sprite_bt_board,
        is_sprite_sheet = True,
        frame_count = ScaleMenuVar.BT_BOARD_WH_QUANTITY * ScaleMenuVar.BT_BOARD_WH_QUANTITY - 1,
        frame_row = ScaleMenuVar.BT_BOARD_WH_QUANTITY,
        frame_col = ScaleMenuVar.BT_BOARD_WH_QUANTITY
    ),

    LayoutName.GAME_STATUS_BAR:  P(PathConfig.pattern_status_bar, is_static = False),
    LayoutName.GAME_UPGRADE:     P(PathConfig.pattern_upgrade, is_static = False),
    LayoutName.GAME_UPGRADE_USER:P(PathConfig.pattern_upgrade_user, is_static = False),
    LayoutName.GAME_PROGRESS_BAR:P(PathConfig.progress_bar, is_static = False),
    LayoutName.GAME_FACTION_BAR :P(PathConfig.faction_bar),
    LayoutName.GAME_VFX_LAB_IMPACT:         P(PathConfig.vfx_lab_impact, is_static = False),
    LayoutName.GAME_VFX_LAB_READY:          P(PathConfig.vfx_lab_ready, is_static = False),
    LayoutName.GAME_ABILITY.serial_list[0]: P(PathConfig.pattern_ability_ice, is_static = False),
    LayoutName.GAME_ABILITY.serial_list[1]: P(PathConfig.pattern_ability_weak, is_static = False),
    LayoutName.GAME_ABILITY.serial_list[2]: P(PathConfig.pattern_ability_demon, is_static = False),
    LayoutName.GAME_BECOME.serial_list[0]:  P(PathConfig.pattern_become_production, is_static = False),
    LayoutName.GAME_BECOME.serial_list[1]:  P(PathConfig.pattern_become_castle, is_static = False),
    LayoutName.GAME_BECOME.serial_list[2]:  P(PathConfig.pattern_become_lab, is_static = False),

    LayoutName.OBSTACLE_BOARD:                  P(PathConfig.obstacle_board, is_static = False),
    LayoutName.OBSTACLE_PEN1.serial_list[0]:    P(PathConfig.obstacle_pen1, is_static = False),
    LayoutName.OBSTACLE_PEN1.serial_list[1]:    P(PathConfig.obstacle_pen1, is_static = False, angle = 90),
    LayoutName.OBSTACLE_PEN3:                   P(PathConfig.obstacle_pen3, is_static = False),
    LayoutName.OBSTACLE_PEN_CROSS:              P(PathConfig.obstacle_pen_cross, is_static = False),
    LayoutName.OBSTACLE_COMPASS.serial_list[0]: P(PathConfig.obstacle_compass, is_static = False),
    LayoutName.OBSTACLE_COMPASS.serial_list[1]: P(PathConfig.obstacle_compass, is_static = False, flip_x = True),
    LayoutName.OBSTACLE_ERASER:                 P(PathConfig.obstacle_eraser, is_static = False),
    LayoutName.OBSTACLE_RULER:                  P(PathConfig.obstacle_ruler, is_static = False),

    # LayoutName.HELP_LACE:        P(PathConfig.img_lace),
    LayoutName.HELP_PANEL:       P(PathConfig.img_panel),
}


# 執行自動加載(將 IMAGE_RESOURCE_MAP 傳進去，Loader 會直接修改這個字典)
loader = ResourceAutoLoader(IMAGE_RESOURCE_MAP)
loader.load_all()
