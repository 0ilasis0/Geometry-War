from dataclasses import dataclass
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from py.ui_layout.name.identifiers import LayoutName
    from py.ui_layout.variable import LayoutItem
    from py.variable import GridPoint

@dataclass
class ObstacleEntity:
    layout_item: "LayoutItem"
    grid_origin: "GridPoint" # 紀錄生成時的網格原點
    occupied_cells: List["GridPoint"]

@dataclass
class ObstacleSpawnData:
    """ 定義單個障礙物的生成資訊 """
    layout_name: "LayoutName"  # 對應 LayoutItem (長相/大小)
    grid_pos: "GridPoint"      # 在地圖上的位置 (網格座標)

@dataclass
class LevelProfile:
    """ 定義整個關卡的配置 """
    obstacles: List[ObstacleSpawnData]
