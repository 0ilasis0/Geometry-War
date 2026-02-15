import math
from typing import TYPE_CHECKING

from py.a_star.main import main_a_star
from py.debug import dbg
from py.game.context import GameContext

if TYPE_CHECKING:
    from py.game.building.entity import BuildingEntity


def execute_dispatch_army(source: "BuildingEntity", target: "BuildingEntity"):
    """ 執行出兵邏輯：計算路徑 -> 生成士兵 """
    if source == target: return False
    if source.stats.army < 1: return False

    # 找出 Source 的門口 (離 Target 最近的空地)
    start_node = GameContext.world_map.get_access_point(
        building_grid = source.stats.grid_point,
        size = source.stats.grid_size,
        target_grid = target.stats.grid_point
    )

    # 找出 Target 的門口 (離 Source 最近的空地)
    end_node = GameContext.world_map.get_access_point(
        building_grid = target.stats.grid_point,
        size = target.stats.grid_size,
        target_grid = source.stats.grid_point
    )

    if not start_node or not end_node:
        dbg.war(f">> 無法出兵：建築物被完全包圍，無路可走")
        return False

    path = main_a_star(
        grid_data = GameContext.world_map,
        start_pos = start_node, # 用門口當起點
        end_pos = end_node,     # 用門口當終點
        map_tag = GameContext.map_tag()
    )

    if not path:
        dbg.war(">> 無法抵達目標")
        return False

    # 這裡派出一半的兵力
    send_amount = math.ceil(source.stats.army / 2)
    source.stats.army -= send_amount # 扣除建築兵量

    GameContext.army_mg.spawn_jelly(
        source_building = source,
        target_building = target,
        path = path,
        army_count = send_amount,
    )

    return True
