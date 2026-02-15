import sys
from dataclasses import dataclass
from pathlib import Path

from py.path.variable import JsonFileID, MixPath


def resource_path(*paths):
    """
    取得外部資源路徑：
    - 打包成 exe 時：使用 exe 同目錄
    - 開發模式：使用專案根目錄
    """
    if getattr(sys, "frozen", False):
        # exe 打包後使用的路徑
        base_path = Path(sys.executable).resolve().parent
    else:
        # 開發環境使用的路徑
        base_path = Path(__file__).resolve().parent.parent.parent.parent

    return base_path.joinpath(*paths)

@dataclass(frozen = True)
class PathBase:
    background = resource_path("background")
    img        = resource_path("img")
    sprite     = resource_path("img", "sprite")
    pattern    = resource_path("img", "pattern")
    vfx        = resource_path("img", "vfx")
    vfx_lab    = resource_path("img", "vfx", "lab")
    obstacle   = resource_path("img", "obstacle")
    icon       = resource_path("images.ico")
    json       = resource_path("data")
    song       = resource_path("song")
    font       = resource_path("font")
    core       = resource_path("core")



@dataclass(frozen = True)
class PathConfig:
    bg_menu         = PathBase.background / "bg_menu.png"
    bg_single       = PathBase.background / "bg_single1.png"
    bg_single_menu  = PathBase.background / "bg_single_menu.png"
    bg_sys          = PathBase.background / "bg_sys.png"
    img_clock   = PathBase.img / "clock.jpg"
    img_panel   = [
        PathBase.img / "panel1.png",
        PathBase.img / "panel2.png",
        PathBase.img / "panel3.png"
    ]
    img_lace        = PathBase.img / "lace.png"
    img_ranking     = PathBase.img / "ranking.png"
    img_frame       = PathBase.img / "frame.png"
    img_O           = PathBase.img / "O.png"
    img_square      = PathBase.img / "square.png"
    img_board       = PathBase.img / "board.png"

    progress_bar    = PathBase.img / "progress_bar.png"
    faction_bar     = PathBase.img / "faction_bar.png"
    vfx_lab_impact  = [
        PathBase.vfx_lab / "impact" / "ice.png",
        PathBase.vfx_lab / "impact" / "weak.png",
        PathBase.vfx_lab / "impact" / "demon.png"
    ]
    vfx_lab_ready   = [
        PathBase.vfx_lab / "ready" / "ice.png",
        PathBase.vfx_lab / "ready" / "weak.png",
        PathBase.vfx_lab / "ready" / "demon.png"
    ]

    pattern_status_bar          = PathBase.pattern / "status_bar.png"
    pattern_upgrade             = PathBase.pattern / "upgrade.png"
    pattern_upgrade_user        = PathBase.pattern / "upgrade_user.png"
    pattern_ability_ice         = PathBase.pattern / "ice.png"
    pattern_ability_weak        = PathBase.pattern / "weak.png"
    pattern_ability_demon       = PathBase.pattern / "demon.png"
    pattern_become_production   = PathBase.pattern / "production.png"
    pattern_become_castle       = PathBase.pattern / "castle.png"
    pattern_become_lab          = PathBase.pattern / "lab.png"

    obstacle_board              = PathBase.obstacle / "board.png"
    obstacle_pen1               = PathBase.obstacle / "pen1.png"
    obstacle_pen3               = PathBase.obstacle / "pen3.png"
    obstacle_pen_cross          = PathBase.obstacle / "pen_cross.png"
    obstacle_compass            = PathBase.obstacle / "compass.png"
    obstacle_eraser             = PathBase.obstacle / "eraser.png"
    obstacle_ruler              = PathBase.obstacle / "ruler.png"


    sprite_bt_board = PathBase.sprite / "black_tower_billboard.png"

    font_base       = PathBase.font / 'NotoSansTC-VariableFont_wght.ttf'
    font_eng1       = PathBase.font / 'PressStart2P-Regular.ttf'
    font_eng2       = PathBase.font / 'Audiowide-Regular.ttf'

    json_save       = (PathBase.json / JsonFileID.SAVE).with_suffix(".json")
    json_display    = (PathBase.json / JsonFileID.DISPLAY).with_suffix(".json")
    a_star          = MixPath(
        (PathBase.core / "c_src" / "a_star" / "main.c", PathBase.core / "c_src" / "a_star" / "base.c"),
        PathBase.core / "dll" / "a_star.dll"
    )
