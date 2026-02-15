from py.game.building.preset import Measurement
from py.game.obstacle.variable import LevelProfile, ObstacleSpawnData
from py.ui_layout.name.identifiers import LayoutName
from py.ui_layout.scale.manager import location_config
from py.variable import GridPoint, PageTable


def pos_to_grid(len, is_height: bool = True):
    if is_height:
        return len //  Measurement.cell_h
    else:
        return len //  Measurement.cell_w



# --- 關卡配置表 ---
LEVEL_CONFIG_MAP = {
    PageTable.SINGLE:{
        0: LevelProfile(obstacles = [
                ObstacleSpawnData(
                    LayoutName.OBSTACLE_BOARD,
                    GridPoint(
                        1,
                        Measurement.map_h - pos_to_grid(location_config.game.obstacle_board_size.height) * 0.9
                    )
                ),
        ]),

        1: LevelProfile(obstacles = [
                ObstacleSpawnData(
                    LayoutName.OBSTACLE_BOARD,
                    GridPoint(
                        1,
                        Measurement.map_h - pos_to_grid(location_config.game.obstacle_board_size.height) * 0.9
                    )
                ),
        ]),

        2: LevelProfile(obstacles = [
                ObstacleSpawnData(
                    LayoutName.OBSTACLE_BOARD,
                    GridPoint(
                        1,
                        Measurement.map_h - pos_to_grid(location_config.game.obstacle_board_size.height) * 0.9
                    )
                ),
        ]),

        3: LevelProfile(obstacles = [
                ObstacleSpawnData(
                    LayoutName.OBSTACLE_BOARD,
                    GridPoint(
                        1,
                        Measurement.map_h - pos_to_grid(location_config.game.obstacle_board_size.height) * 0.8
                    )
                ),
        ]),

        4: LevelProfile(obstacles = [
                ObstacleSpawnData(
                    LayoutName.OBSTACLE_PEN1.serial_list[0],
                    GridPoint(
                        Measurement.center_w,
                        Measurement.map_h - pos_to_grid(location_config.game.obstacle_pen1_size.height) * 0.95
                    )
                ),
                ObstacleSpawnData(
                    LayoutName.OBSTACLE_PEN1.serial_list[1],
                    GridPoint(
                        Measurement.center_w,
                        Measurement.map_h - pos_to_grid(location_config.game.obstacle_pen1_size.height) * 3 // 2
                    )
                ),
        ]),

        5: LevelProfile(obstacles = [
                ObstacleSpawnData(
                    LayoutName.OBSTACLE_COMPASS.serial_list[0],
                    GridPoint(
                        Measurement.map_w // 4 - pos_to_grid(location_config.game.obstacle_compass_size.width, False) // 2 + Measurement.b_w,
                        Measurement.map_h - pos_to_grid(location_config.game.obstacle_compass_size.height) - Measurement.b_h
                    )
                ),
                ObstacleSpawnData(
                    LayoutName.OBSTACLE_COMPASS.serial_list[1],
                    GridPoint(
                        Measurement.map_w * 3 // 4 - pos_to_grid(location_config.game.obstacle_compass_size.width, False) // 2,
                        Measurement.map_h - pos_to_grid(location_config.game.obstacle_compass_size.height) - Measurement.b_h
                    )
                ),
                ObstacleSpawnData(
                    LayoutName.OBSTACLE_ERASER,
                    GridPoint(
                        Measurement.map_w // 4 - pos_to_grid(location_config.game.obstacle_compass_size.width, False) // 2 + Measurement.b_w * 2 + pos_to_grid(location_config.game.obstacle_eraser_size.height),
                        Measurement.map_h - pos_to_grid(location_config.game.obstacle_compass_size.height) - Measurement.b_h - pos_to_grid(location_config.game.obstacle_eraser_size.height)
                    )
                ),
        ]),

        6: LevelProfile(obstacles = [
                ObstacleSpawnData(
                    LayoutName.OBSTACLE_RULER,
                    GridPoint(
                        Measurement.map_w * 6 // 21,
                        0
                    )
                ),
                ObstacleSpawnData(
                    LayoutName.OBSTACLE_RULER,
                    GridPoint(
                        Measurement.map_w * 15 // 21,
                        Measurement.map_h - pos_to_grid(location_config.game.obstacle_ruler_size.height)
                    )
                ),

        ]),

        7: LevelProfile(obstacles = [
                ObstacleSpawnData(
                    LayoutName.OBSTACLE_PEN_CROSS,
                    GridPoint(
                        Measurement.center_w - pos_to_grid(location_config.game.obstacle_pen_cross_size.width) // 2,
                        Measurement.center_h - pos_to_grid(location_config.game.obstacle_pen_cross_size.height) // 2
                    )
                ),
        ]),

        8: LevelProfile(obstacles = [
                ObstacleSpawnData(
                    LayoutName.OBSTACLE_PEN3,
                    GridPoint(
                        Measurement.map_w // 4 - pos_to_grid(location_config.game.obstacle_pen3_size.width) // 2 + Measurement.b_w,
                        Measurement.center_h - pos_to_grid(location_config.game.obstacle_pen3_size.height) // 2
                    )
                ),
                ObstacleSpawnData(
                    LayoutName.OBSTACLE_PEN3,
                    GridPoint(
                        Measurement.map_w * 3 // 4 - pos_to_grid(location_config.game.obstacle_pen3_size.width) // 2 - Measurement.b_w_mini,
                        Measurement.center_h - pos_to_grid(location_config.game.obstacle_pen3_size.height) // 2
                    )
                ),
        ]),

    }
}
