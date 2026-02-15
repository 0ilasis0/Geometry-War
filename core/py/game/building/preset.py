from enum import IntEnum

from py.debug import dbg
from py.game.building.variable import BuildingStats, BuildingStatsKey
from py.game.variable import GameType, GameTypeMap
from py.screen.variable import ScreenConfig
from py.ui_layout.scale.manager import location_config
from py.variable import GridPoint


class Measurement(IntEnum):
    cell_w = location_config.map_grid.cell_w
    cell_h = location_config.map_grid.cell_h
    map_w = ScreenConfig.width // cell_w
    map_h = ScreenConfig.height // cell_h

    b_w = BuildingStats.grid_size.width
    b_h = BuildingStats.grid_size.height
    b_w_mini = BuildingStats.grid_size.width // 2
    b_h_mini = BuildingStats.grid_size.height // 2
    b_w_plus = BuildingStats.grid_size.width * 1.5
    b_h_plus = BuildingStats.grid_size.height * 1.5

    center_w = map_w // 2
    center_h = map_h // 2
    center_w_b = (map_w - b_w) // 2
    center_h_b = (map_h - b_h) // 2



GAME_OBJ_CONFIG = {
    0: {
        GameTypeMap.get_value(GameType.Genre.ARCH): [
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w * 2 // 3,
                    Measurement.center_h_b - Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PLAYER,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w * 2 // 3,
                    Measurement.center_h_b + Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PLAYER,
                BuildingStatsKey.ARMY: 30,
                BuildingStatsKey.LEVEL: 3
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w,
                    Measurement.center_h_b
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w * 4 // 3,
                    Measurement.center_h_b
                ),
                BuildingStatsKey.OWNER: GameType.Owner.RED,
                BuildingStatsKey.ARMY: 20,
                BuildingStatsKey.LEVEL: 2
            },
        ],
    },

    1: {
        GameTypeMap.get_value(GameType.Genre.ARCH): [
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w * 3 // 9,
                    Measurement.center_h_b
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PLAYER,
                BuildingStatsKey.ARMY: 50,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w * 2 // 9,
                    Measurement.center_h_b
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PLAYER,
                BuildingStatsKey.ARMY: 30,
                BuildingStatsKey.LEVEL: 3
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w * 6 // 9,
                    Measurement.center_h_b
                ),
                BuildingStatsKey.OWNER: GameType.Owner.RED,
                BuildingStatsKey.ARMY: 20,
                BuildingStatsKey.LEVEL: 4
            },
        ],
    },

    2: {
        GameTypeMap.get_value(GameType.Genre.ARCH): [
            {
                BuildingStatsKey.ARCH: GameType.Arch.LAB,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w * 2 // 9,
                    Measurement.center_h_b + Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PLAYER,
                BuildingStatsKey.ARMY: 20,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.LAB,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w * 2 // 9,
                    Measurement.center_h_b - Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PLAYER,
                BuildingStatsKey.ARMY: 30,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.LAB,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w * 1 // 9,
                    Measurement.center_h_b
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PLAYER,
                BuildingStatsKey.ARMY: 50,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w_b,
                    Measurement.center_h_b + Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 100,
                BuildingStatsKey.LEVEL: 4
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w_b,
                    Measurement.center_h_b - Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 100,
                BuildingStatsKey.LEVEL: 4
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w * 7 // 9,
                    Measurement.center_h_b - Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.YELLOW,
                BuildingStatsKey.ARMY: 40,
                BuildingStatsKey.LEVEL: 4
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w * 7 // 9,
                    Measurement.center_h_b + Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.YELLOW,
                BuildingStatsKey.ARMY: 40,
                BuildingStatsKey.LEVEL: 4
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w * 8 // 9,
                    Measurement.center_h_b
                ),
                BuildingStatsKey.OWNER: GameType.Owner.YELLOW,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
        ],
    },

    3: {
        GameTypeMap.get_value(GameType.Genre.ARCH): [
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w_b - Measurement.b_w_plus * 3,
                    Measurement.center_h_b
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PLAYER,
                BuildingStatsKey.ARMY: 50,
                BuildingStatsKey.LEVEL: 4
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w_b - Measurement.b_w_plus * 2,
                    Measurement.center_h_b
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w_b - Measurement.b_w_plus * 2,
                    Measurement.center_h_b - Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w_b - Measurement.b_w_plus * 2,
                    Measurement.center_h_b + Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 0
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w,
                    Measurement.center_h_b + Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 25,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w,
                    Measurement.center_h_b
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 100,
                BuildingStatsKey.LEVEL: 4
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w,
                    Measurement.center_h_b - Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 25,
                BuildingStatsKey.LEVEL: 2
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w_b + Measurement.b_w_plus * 4,
                    Measurement.center_h_b
                ),
                BuildingStatsKey.OWNER: GameType.Owner.RED,
                BuildingStatsKey.ARMY: 30,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w_b + Measurement.b_w_plus * 3,
                    Measurement.center_h_b
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w_b + Measurement.b_w_plus * 3,
                    Measurement.center_h_b - Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w_b + Measurement.b_w_plus * 3,
                    Measurement.center_h_b + Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 0
            },
        ],
    },

    4: {
        GameTypeMap.get_value(GameType.Genre.ARCH): [
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w,
                    Measurement.map_h - Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PLAYER,
                BuildingStatsKey.ARMY: 25,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w * 3,
                    Measurement.map_h - Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w,
                    Measurement.map_h - Measurement.b_h_plus - Measurement.b_h * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w * 3,
                    Measurement.map_h - Measurement.b_h_plus - Measurement.b_h * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w * 5,
                    Measurement.map_h - Measurement.b_h_plus - Measurement.b_h * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 20,
                BuildingStatsKey.LEVEL: 1
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w,
                    Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.YELLOW,
                BuildingStatsKey.ARMY: 40,
                BuildingStatsKey.LEVEL: 4
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w - Measurement.b_w * 2,
                    Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.YELLOW,
                BuildingStatsKey.ARMY: 20,
                BuildingStatsKey.LEVEL: 3
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w + Measurement.b_w * 2,
                    Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.YELLOW,
                BuildingStatsKey.ARMY: 20,
                BuildingStatsKey.LEVEL: 3
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w - Measurement.b_w_plus * 3,
                    Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w + Measurement.b_w_plus * 3,
                    Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 0
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w,
                    Measurement.map_h - Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.RED,
                BuildingStatsKey.ARMY: 40,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w * 3,
                    Measurement.map_h - Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w,
                    Measurement.map_h - Measurement.b_h_plus - Measurement.b_h * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w * 3,
                    Measurement.map_h - Measurement.b_h_plus - Measurement.b_h * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w * 5,
                    Measurement.map_h - Measurement.b_h_plus - Measurement.b_h * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 20,
                BuildingStatsKey.LEVEL: 1
            },
        ],
    },

    5: {
        GameTypeMap.get_value(GameType.Genre.ARCH): [
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w + 2,
                    Measurement.map_h - Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PLAYER,
                BuildingStatsKey.ARMY: 30,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w + Measurement.b_w * 2 + 2,
                    Measurement.map_h - Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w - Measurement.b_w * 2 + 2,
                    Measurement.map_h - Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w + Measurement.b_w + 2,
                    Measurement.map_h - Measurement.b_h * 3
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 20,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w - Measurement.b_w + 2,
                    Measurement.map_h - Measurement.b_h * 3
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 20,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w - Measurement.b_w* 2 - Measurement.b_w_plus + 2,
                    Measurement.map_h - Measurement.b_h * 4
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 30,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w + Measurement.b_w * 2 + Measurement.b_w_plus + 2,
                    Measurement.map_h - Measurement.b_h * 4
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 30,
                BuildingStatsKey.LEVEL: 2
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.LAB,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus - 1,
                    Measurement.b_h_mini
                ),
                BuildingStatsKey.OWNER: GameType.Owner.RED,
                BuildingStatsKey.ARMY: 90,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 2 - 1,
                    Measurement.b_h_mini
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 15,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus - 1,
                    Measurement.b_h_mini + Measurement.b_h * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus - 1,
                    Measurement.b_h_mini + Measurement.b_h * 4
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus - 1,
                    Measurement.b_h_mini + Measurement.b_h * 4 + Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w * 2 - Measurement.b_w_plus * 2,
                    Measurement.b_h_mini
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 25,
                BuildingStatsKey.LEVEL: 4
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.LAB,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w,
                    Measurement.b_h_mini
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PURPLE,
                BuildingStatsKey.ARMY: 90,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w - Measurement.b_w_plus,
                    Measurement.b_h_mini
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w,
                    Measurement.b_h_mini + Measurement.b_h * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w,
                    Measurement.b_h_mini + Measurement.b_h * 4
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w,
                    Measurement.b_h_mini + Measurement.b_h * 4 + Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },

        ],
    },

    6: {
         GameTypeMap.get_value(GameType.Genre.ARCH): [
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w,
                    Measurement.b_h_mini
                ),
                BuildingStatsKey.OWNER: GameType.Owner.GREEN,
                BuildingStatsKey.ARMY: 50,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w + Measurement.b_w_plus,
                    Measurement.b_h_mini + Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w,
                    Measurement.b_h_mini + Measurement.b_h + Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 20,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w + Measurement.b_w_plus,
                    Measurement.b_h_mini + Measurement.b_h + Measurement.b_h_plus * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w,
                    Measurement.b_h_mini + Measurement.b_h * 2 + Measurement.b_h_plus * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PLAYER,
                BuildingStatsKey.ARMY: 30,
                BuildingStatsKey.LEVEL: 0
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w,
                    Measurement.center_h - 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.YELLOW,
                BuildingStatsKey.ARMY: 50,
                BuildingStatsKey.LEVEL: 4
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w + Measurement.b_w_plus,
                    Measurement.center_h - Measurement.b_h_plus - 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w + Measurement.b_w_plus,
                    Measurement.center_h + Measurement.b_h_plus - 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w - Measurement.b_w_plus,
                    Measurement.center_h + Measurement.b_h_plus - 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w - Measurement.b_w_plus,
                    Measurement.center_h - Measurement.b_h_plus - 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w,
                    Measurement.center_h - Measurement.b_h_plus - Measurement.b_h - 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w,
                    Measurement.center_h + Measurement.b_h_plus + Measurement.b_h - 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w,
                    Measurement.b_h_mini
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PURPLE,
                BuildingStatsKey.ARMY: 50,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - (Measurement.b_w + Measurement.b_w_plus),
                    Measurement.b_h_mini + Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w,
                    Measurement.b_h_mini + Measurement.b_h + Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 20,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - (Measurement.b_w + Measurement.b_w_plus),
                    Measurement.b_h_mini + Measurement.b_h + Measurement.b_h_plus * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w,
                    Measurement.b_h_mini + Measurement.b_h * 2 + Measurement.b_h_plus * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.RED,
                BuildingStatsKey.ARMY: 50,
                BuildingStatsKey.LEVEL: 0
            },
         ]
    },

    7: {
        GameTypeMap.get_value(GameType.Genre.ARCH): [
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_mini,
                    Measurement.b_h_mini
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PLAYER,
                BuildingStatsKey.ARMY: 20,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_mini + Measurement.b_w_plus * 3,
                    Measurement.b_h_mini
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_mini + Measurement.b_w_plus * 3 // 2,
                    Measurement.b_h_mini + Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.GREEN,
                BuildingStatsKey.ARMY: 35,
                BuildingStatsKey.LEVEL: 3
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_mini,
                    Measurement.b_h_mini + Measurement.b_h * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_mini + Measurement.b_w_plus * 3,
                    Measurement.b_h * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w_mini * 2,
                    Measurement.b_h_mini
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 20,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w_mini * 2 - Measurement.b_w_plus * 3,
                    Measurement.b_h_mini
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w_mini * 2 - Measurement.b_w_plus * 3 // 2,
                    Measurement.b_h_mini + Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.YELLOW,
                BuildingStatsKey.ARMY: 35,
                BuildingStatsKey.LEVEL: 3
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w_mini * 2,
                    Measurement.b_h_mini + Measurement.b_h * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w_mini * 2 - Measurement.b_w_plus * 3,
                    Measurement.b_h * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w_mini * 2,
                    Measurement.center_h + Measurement.b_h_mini
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w_mini * 2 - Measurement.b_w_plus * 3,
                    Measurement.center_h + Measurement.b_h_mini + Measurement.b_h * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w_mini * 2 - Measurement.b_w_plus * 3 // 2,
                    Measurement.center_h + Measurement.b_h_mini + Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PURPLE,
                BuildingStatsKey.ARMY: 35,
                BuildingStatsKey.LEVEL: 3
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w_mini * 2,
                    Measurement.center_h + Measurement.b_h_mini + Measurement.b_h * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 20,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w_mini * 2 - Measurement.b_w_plus * 3,
                    Measurement.center_h + Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_mini,
                    Measurement.center_h + Measurement.b_h_mini
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_mini + Measurement.b_w_plus * 3,
                    Measurement.center_h + Measurement.b_h_mini + Measurement.b_h * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_mini + Measurement.b_w_plus * 3 // 2,
                    Measurement.center_h + Measurement.b_h_mini + Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.RED,
                BuildingStatsKey.ARMY: 35,
                BuildingStatsKey.LEVEL: 3
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_mini,
                    Measurement.center_h + Measurement.b_h_mini + Measurement.b_h * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 20,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_mini + Measurement.b_w_plus * 3,
                    Measurement.center_h + Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },

        ]
    },

    8: {
        GameTypeMap.get_value(GameType.Genre.ARCH): [
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w,
                    0
                ),
                BuildingStatsKey.OWNER: GameType.Owner.RED,
                BuildingStatsKey.ARMY: 50,
                BuildingStatsKey.LEVEL: 4
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w + Measurement.b_w_plus,
                    Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.RED,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w + Measurement.b_w_plus * 2,
                    0
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w,
                    Measurement.center_h - Measurement.b_h_mini
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 25,
                BuildingStatsKey.LEVEL: 4
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w,
                    0
                ),
                BuildingStatsKey.OWNER: GameType.Owner.GREEN,
                BuildingStatsKey.ARMY: 50,
                BuildingStatsKey.LEVEL: 4
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w - Measurement.b_w_plus,
                    Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.GREEN,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w - Measurement.b_w_plus * 2,
                    0
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w,
                    Measurement.map_h - Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.YELLOW,
                BuildingStatsKey.ARMY: 50,
                BuildingStatsKey.LEVEL: 4
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w + Measurement.b_w_plus,
                    Measurement.map_h - Measurement.b_h - Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.YELLOW,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w + Measurement.b_w_plus * 2,
                    Measurement.map_h - Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w,
                    Measurement.center_h - Measurement.b_h_mini
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 25,
                BuildingStatsKey.LEVEL: 4
            },


            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w,
                    Measurement.map_h - Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PURPLE,
                BuildingStatsKey.ARMY: 50,
                BuildingStatsKey.LEVEL: 4
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w - Measurement.b_w_plus,
                    Measurement.map_h - Measurement.b_h - Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PURPLE,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.map_w - Measurement.b_w - Measurement.b_w_plus * 2,
                    Measurement.map_h - Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.LAB,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w,
                    Measurement.center_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PLAYER,
                BuildingStatsKey.ARMY: 100,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w + Measurement.b_w + 1,
                    Measurement.center_h + Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w - Measurement.b_w - 1,
                    Measurement.center_h - Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 10,
                BuildingStatsKey.LEVEL: 1
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w,
                    Measurement.center_h + Measurement.b_h_plus + Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.center_w,
                    Measurement.center_h - Measurement.b_h_plus - Measurement.b_h
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
        ]
    },

    9: {
        GameTypeMap.get_value(GameType.Genre.ARCH): [
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus + Measurement.b_w_plus,
                    0
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PURPLE,
                BuildingStatsKey.ARMY: 30,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 2 + Measurement.b_w_plus,
                    0
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 3 + Measurement.b_w_plus,
                    0
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 4 + Measurement.b_w_plus,
                    0
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 5 + Measurement.b_w_plus,
                    0
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 6 + Measurement.b_w_plus,
                    0
                ),
                BuildingStatsKey.OWNER: GameType.Owner.GREEN,
                BuildingStatsKey.ARMY: 30,
                BuildingStatsKey.LEVEL: 3
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus + Measurement.b_w_plus,
                    Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 2 + Measurement.b_w_plus,
                    Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 60,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 3 + Measurement.b_w_plus,
                    Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 4 + Measurement.b_w_plus,
                    Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 5 + Measurement.b_w_plus,
                    Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 60,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 6 + Measurement.b_w_plus,
                    Measurement.b_h_plus
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus + Measurement.b_w_plus,
                    Measurement.b_h_plus * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 2 + Measurement.b_w_plus,
                    Measurement.b_h_plus * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 3 + Measurement.b_w_plus,
                    Measurement.b_h_plus * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.PLAYER,
                BuildingStatsKey.ARMY: 20,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 4 + Measurement.b_w_plus,
                    Measurement.b_h_plus * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 5 + Measurement.b_w_plus,
                    Measurement.b_h_plus * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 6 + Measurement.b_w_plus,
                    Measurement.b_h_plus * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus + Measurement.b_w_plus,
                    Measurement.b_h_plus * 3
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 2 + Measurement.b_w_plus,
                    Measurement.b_h_plus * 3
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 60,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 3 + Measurement.b_w_plus,
                    Measurement.b_h_plus * 3
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 4 + Measurement.b_w_plus,
                    Measurement.b_h_plus * 3
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.CASTLE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 5 + Measurement.b_w_plus,
                    Measurement.b_h_plus * 3
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 60,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 6 + Measurement.b_w_plus,
                    Measurement.b_h_plus * 3
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus + Measurement.b_w_plus,
                    Measurement.b_h_plus * 4
                ),
                BuildingStatsKey.OWNER: GameType.Owner.YELLOW,
                BuildingStatsKey.ARMY: 30,
                BuildingStatsKey.LEVEL: 3
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 2 + Measurement.b_w_plus,
                    Measurement.b_h_plus * 4
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 3 + Measurement.b_w_plus,
                    Measurement.b_h_plus * 4
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 4 + Measurement.b_w_plus,
                    Measurement.b_h_plus * 4
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PROTOTYPE,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 5 + Measurement.b_w_plus,
                    Measurement.b_h_plus * 4
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 0
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.PRODUCTION,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 6 + Measurement.b_w_plus,
                    Measurement.b_h_plus * 4
                ),
                BuildingStatsKey.OWNER: GameType.Owner.RED,
                BuildingStatsKey.ARMY: 30,
                BuildingStatsKey.LEVEL: 3
            },

            {
                BuildingStatsKey.ARCH: GameType.Arch.LAB,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus,
                    Measurement.b_h_plus * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 2
            },
            {
                BuildingStatsKey.ARCH: GameType.Arch.LAB,
                BuildingStatsKey.GRID: GridPoint(
                    Measurement.b_w_plus * 7 + Measurement.b_w_plus,
                    Measurement.b_h_plus * 2
                ),
                BuildingStatsKey.OWNER: GameType.Owner.NEUTRAL,
                BuildingStatsKey.ARMY: 5,
                BuildingStatsKey.LEVEL: 2
            },

        ]
    },

}

