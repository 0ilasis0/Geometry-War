import heapq
from typing import TYPE_CHECKING, List, Optional, Tuple

from py.a_star.main import main_a_star
from py.game.context import GameContext

if TYPE_CHECKING:
    from py.game.building.entity import BuildingEntity
    from py.variable import GridPoint

class TargetSelector:
    """
    負責處理高階的索敵邏輯
    包含：兩階段篩選 (直線距離快篩 -> A* 路徑精算)
    """

    @staticmethod
    def find_best_target(
        source: "BuildingEntity",
        targets: List["BuildingEntity"],
        top_k: int = 3
    ) -> Tuple[Optional["BuildingEntity"], float, Optional[List["GridPoint"]]]:
        """
        :param source: 發起攻擊的建築
        :param targets: 候選目標列表
        :param top_k: 初選要保留前幾名 (建議 3~5)
        :return: (最佳目標, 真實路徑長度(grid), 真實路徑(grid))
        """
        if not targets: return None, 0.0, None

        # 初選 (歐幾里得距離平方)
        candidates = []
        src_center = source.center_pos

        for i, target in enumerate(targets):
            tgt_center = target.center_pos

            dx = src_center.x - tgt_center.x
            dy = src_center.y - tgt_center.y
            dist_sq = dx*dx + dy*dy

            # 存入 (距離, index, target)，index 用於避免 target 比較出錯
            heapq.heappush(candidates, (dist_sq, i, target))

        # 取出前 K 名
        top_candidates = heapq.nsmallest(top_k, candidates)

        # 決選 (A* 真實尋路)
        world_map = GameContext.world_map
        min_path_len = float('inf')
        best_target = None
        best_path = None

        for _, _, target in top_candidates:
            # 取得建築物邊緣的「出入口」，避免起點終點在牆壁內
            start_node = world_map.get_access_point(
                source.stats.grid_point, source.stats.grid_size, target.stats.grid_point
            )
            end_node = world_map.get_access_point(
                target.stats.grid_point, target.stats.grid_size, source.stats.grid_point
            )

            if not start_node or not end_node: continue

            path = main_a_star(world_map, start_node, end_node, GameContext.map_tag())

            if path:
                real_dist = len(path)
                if real_dist < min_path_len:
                    min_path_len = real_dist
                    best_target = target
                    best_path = path

        # 如果 A* 全滅 (都被圍死)，回退到直線距離最近的
        if best_target is None and top_candidates:
            best_target = top_candidates[0][2]
            best_path = None
            # 這裡回傳 inf 代表無法到達，但在 AICommander 中會被過濾掉
            min_path_len = float('inf')

        return best_target, min_path_len, best_path