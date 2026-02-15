import math

from py.game.context import GameContext
from py.game.jelly.variable import JellyStats


class JellyMoveComponent:
    def __init__(self, stats: JellyStats):
        self.stats: JellyStats = stats

        # 當前前往的路徑點索引 (從 1 起點，因為 0 是終點)
        self.current_path_index = 1

    def update(self, dt: float) -> bool:
        """
        更新移動
        回傳: True 表示還在移動, False 表示已抵達終點
        """
        # 如果沒有路徑或已經走完
        if not self.stats.path or self.current_path_index >= len(self.stats.path): return False

        # 取得當前目標格子的 "像素中心點"
        target_grid = self.stats.path[self.current_path_index]
        target_pixel = GameContext.grid_cvt.get_pixel_center(target_grid)
        dx = target_pixel.x - self.stats.pos.x
        dy = target_pixel.y - self.stats.pos.y
        dist = math.sqrt(dx**2 + dy**2)

        # 本幀移動距離
        move_step = self.stats.move_speed * dt

        if dist <= move_step:
            # --- 抵達當前節點 ---
            # 直接瞬移到目標點 (修正誤差)
            self.stats.pos.x = float(target_pixel.x)
            self.stats.pos.y = float(target_pixel.y)

            # 推進到下一個路徑點
            self.current_path_index += 1

            # 檢查是否完全抵達終點
            if self.current_path_index >= len(self.stats.path): return False

        else:
            # --- 移動中 ---
            ratio = move_step / dist
            self.stats.pos.x += dx * ratio
            self.stats.pos.y += dy * ratio

        return True
