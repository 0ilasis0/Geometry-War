from dataclasses import dataclass

from py.game.building.variable import BuildingStats
from py.game.variable import EntitySpan
from py.screen.variable import ScreenConfig
from py.ui_layout.scale.preset.base import ScaleFont, ScaleMapGrid
from py.variable import PosField, Position, PosListField, Size


@dataclass
class ScaleGame:
    _build_w = ScaleMapGrid.cell_w * BuildingStats.grid_size.width
    _build_h = ScaleMapGrid.cell_h * BuildingStats.grid_size.height

    building_army_font_size: Size = Size(ScaleMapGrid.x2cell_w, ScaleMapGrid.x2cell_h)
    building_army_font_offset: Position = PosField(
        (_build_w - building_army_font_size.width) // 2 * 1.15,
        (_build_h - building_army_font_size.height) // 2 * 1.4
    )
    building_select_circle_size: Size = Size(_build_w * 1.2, _build_h * 1.2)
    building_select_circle_offset: Position = PosField(_build_w * (-1) // 8, _build_h * (-1) // 10)

    _castle_range_w = ScaleMapGrid.cell_w * EntitySpan.CASTLE_RANGE.width
    _castle_range_h = ScaleMapGrid.cell_h * EntitySpan.CASTLE_RANGE.height
    castle_range_circle_size: Size = Size(_castle_range_w, _castle_range_h)
    castle_range_circle_offset: Position = PosField(
        (_castle_range_w - _build_w)  // 2 * (-1),
        (_castle_range_h - _build_h) // 2 * (-1),
    )

    upgrade_size: Size = Size(_build_w // 5, _build_h // 5)
    upgrade_offset: Position = PosField(_build_w // 1.4, _build_h // 1.4)
    upgrade_user_size: Size = Size(_build_w // 4, _build_h // 4)

    _upgrade_user_offset_w = _build_w // 5 * (-1)
    _upgrade_user_offset_h = _build_h // 2
    upgrade_user_offset: Position = PosField(_upgrade_user_offset_w, _upgrade_user_offset_h)
    upgrade_user_price_size: Size = Size(_build_w // 8, _build_h // 8)
    upgrade_user_price_offset: Position = PosField(
        _upgrade_user_offset_w + upgrade_user_size.width // 2,
        _upgrade_user_offset_h + upgrade_user_size.height * 1.2
    )
    status_bar_size: Size = Size(_build_w, _build_h // 3)
    status_bar_offset: Position = PosField(0, _build_h * 1.1)

    _status_word_width_r = _build_w // 4
    _status_word_width_l = _build_w * 3 // 4
    _status_word_height1 = _build_h * 1.2
    _status_word_height2 = _build_h * 1.3
    status_word_size: Size = Size(_build_w // 8, _build_h // 8)
    status_word_offset: list = PosListField(
        (_status_word_width_r, _status_word_height1 // 1.03),
        (_status_word_width_l, _status_word_height1 // 1.03),
        (_status_word_width_r, _status_word_height2 * 1.02),
        (_status_word_width_l, _status_word_height2 * 1.02)
    )

    _jelly_w = EntitySpan.JELLY.width * ScaleMapGrid.cell_w
    _jelly_h = EntitySpan.JELLY.height * ScaleMapGrid.cell_h
    jelly_word_size: Size = Size(_jelly_w // 3, _jelly_h // 3)
    jelly_word_offset: Position = PosField(
        (_jelly_w - jelly_word_size.width) // 2 * 1.45,
        (_jelly_h - jelly_word_size.height) // 2 * 1.4
    )

    bullet_size: Size = Size(_jelly_w // 3, _jelly_h // 3)
    faction_bar_army_size: Size = Size(ScaleFont.mini, ScaleFont.mini)
    faction_bar_size: Size = Size(1800 // 3, 180 / 5)
    faction_bar_gap_y: int = ScreenConfig.DESIGN_HEIGHT - faction_bar_size.height * 3
    faction_bar_draw_offset: Position = PosField(15, 15)
    progress_bar_size: Size = Size(_build_w, _build_h // 6)
    progress_bar_offset: Position = PosField(0, progress_bar_size.height * (-1))
    progress_bar_draw_size: Size = Size(_build_w * 0.9, _build_h // 6 * 0.75)
    progress_bar_draw_offset: Position = PosField(3, progress_bar_size.height * (-1) + 3)
    vfx_lab_impact_size: Size = Size(_build_w, _build_h)
    vfx_lab_ready_size: Size = vfx_lab_impact_size

    _lab_coords = (
        (_build_w // 1.3, _build_h // 60),
        (_build_w // 1.1, _build_h * 3 // 8),
        (_build_w // 1.2, _build_h * 23 // 30),
    )
    ability_lab_size: Size = upgrade_user_size
    ability_lab_offset: list = PosListField(*_lab_coords)
    become_size: Size = ability_lab_size
    become_offset: list = PosListField(*_lab_coords)

    _ability_price_offset_w = ability_lab_size.width * 1.4
    _ability_price_offset_h = (ability_lab_size.height) // 2
    _price_coords = (
        (_build_w // 1.3 + _ability_price_offset_w, _build_h // 60 + _ability_price_offset_h),
        (_build_w // 1.1 + _ability_price_offset_w, _build_h * 3 // 8 + _ability_price_offset_h),
        (_build_w // 1.2 + _ability_price_offset_w, _build_h * 23 // 30 + _ability_price_offset_h),
    )
    ability_price_size: Size = upgrade_user_price_size
    ability_price_offset: list = PosListField(*_price_coords)
    become_price_size: Size = ability_price_size
    become_price_offset: list = PosListField(*_price_coords)


    obstacle_board_size: Size = Size(440, 306)
    obstacle_pen1_size: Size = Size(120, 600 + 100)
    obstacle_pen3_size: Size = Size(210, 600)
    obstacle_pen_cross_size: Size = Size(800, 800)
    obstacle_compass_size: Size = Size(550, 650)
    obstacle_eraser_size: Size = Size(450, 200)
    obstacle_ruler_size: Size = Size(180, 900)
