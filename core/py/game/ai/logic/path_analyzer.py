from typing import TYPE_CHECKING, List

from py.game.ai.variable import AIVar
from py.variable import GridPoint

if TYPE_CHECKING:
    from py.game.building.entity import BuildingEntity
    from py.game.building.variable import BuildingStats



class PathAnalyzer:
    @staticmethod
    def calculate_danger_cost(
        path: List["GridPoint"],
        enemy_buildings: List["BuildingEntity"],
        source_building: "BuildingEntity"
    ) -> float:
        """
        計算走這條路徑預計會損失多少兵力 (考慮移動速度與射速)
        """
        if not path: return 0.0

        # 計算路徑的 AABB 包圍盒
        all_cols = [p.col for p in path]
        all_rows = [p.row for p in path]
        p_min_c, p_max_c = min(all_cols), max(all_cols)
        p_min_r, p_max_r = min(all_rows), max(all_rows)

        # 設定最大射程緩衝
        buffer = 12

        # 只處理那些「有可能」打到這條路的敵人
        active_threats = []
        for b in enemy_buildings:
            s = b.stats
            # 必須有攻擊力且有射速
            if not s.rate_of_fire or not s.effective_grid_range or s.bullet_damage <= 0: continue

            # AABB 碰撞檢查：如果敵人的位置在路徑包圍盒外圍 (考慮射程buffer)，直接排除
            e_col, e_row = b.grid_point.col, b.grid_point.row

            # 判斷是否在包圍盒+緩衝區內
            if not (p_min_c - buffer <= e_col <= p_max_c + buffer and
                    p_min_r - buffer <= e_row <= p_max_r + buffer):
                continue

            # 預算 DPS 與 射程平方，避免在內層迴圈重複計算
            # 防除以零：max(s.rate_of_fire, 0.1)
            active_threats.append({
                "col": e_col,
                "row": e_row,
                "range_sq": s.effective_grid_range ** 2,
                "dps": s.bullet_damage / max(s.rate_of_fire, 0.1)
            })

        # 如果附近很安全，直接回傳
        if not active_threats: return 0.0

        # 執行取樣計算
        move_speed = source_building.stats.jelly_speed_grid
        if move_speed <= 0: return float('inf')

        total_damage = 0.0
        stride = AIVar.PATH_STEP_STRIDE

        for i in range(0, len(path), stride):
            point = path[i]

            # 這裡簡單化處理，固定步長代表的時間
            exposure_time = stride / move_speed

            for enemy in active_threats:
                # 使用預算好的數據，只做最簡單的加減乘
                dist_sq = (point.col - enemy["col"])**2 + (point.row - enemy["row"])**2

                if dist_sq <= enemy["range_sq"]:
                    total_damage += enemy["dps"] * exposure_time

        return total_damage * 1.2

    @staticmethod
    def estimate_danger_linear(
            start: "GridPoint", end: "GridPoint",
            unit_speed: float,
            enemy_buildings: List["BuildingEntity"],
            steps: int = AIVar.PATH_STEP_STRIDE
        ) -> float:
        """
        [輕量級路徑評估]
        假設部隊走直線，計算路上經過多少敵方塔的射程，預估會損失多少兵力。
        效能消耗：低 (只做幾次距離運算)
        # steps:採樣點越多越準，但越慢
        """
        buffer = 12
        min_col = min(start.col, end.col) - buffer
        max_col = max(start.col, end.col) + buffer
        min_row = min(start.row, end.row) - buffer
        max_row = max(start.row, end.row) + buffer

        potential_threats = []
        for enemy in enemy_buildings:
            stats: "BuildingStats" = enemy.stats
            if not stats.rate_of_fire: continue
            if (min_col <= stats.grid_point.col <= max_col) and (min_row <= stats.grid_point.row <= max_row):
                potential_threats.append((stats, stats.effective_grid_range**2))

        # 如果路徑附近根本沒敵人，直接回傳
        if not potential_threats: return 0.0

        # 計算總時間與步長
        total_dist = start.dist_to(end)
        total_time = total_dist / unit_speed

        steps = max(1, steps)
        dx = (end.col - start.col) / steps
        dy = (end.row - start.row) / steps

        # 計算每個採樣點代表的時間片段
        time_per_step = total_time / steps
        total_damage = 0.0

        for i in range(1, steps + 1):
            curr_col = start.col + dx * i
            curr_row = start.row + dy * i

            # 檢查所有敵人
            for stats, range_sq in potential_threats:
                dist_sq = (curr_col - stats.grid_point.col)**2 + (curr_row - stats.grid_point.row)**2

                # 如果在射程內 -> 計算傷害
                if dist_sq <= range_sq:
                    dps = stats.bullet_damage / stats.rate_of_fire
                    damage = dps * time_per_step
                    total_damage += damage

        return (total_damage * 1.2) # 不要太樂觀所以多乘1.2
