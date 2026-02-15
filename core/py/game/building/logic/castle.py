from typing import TYPE_CHECKING

from py.game.building.logic.base import BuildingLogic
from py.game.building.logic.variable import CastleConfig, LabSkillType
from py.game.context import GameContext
from py.ui_layout.variable import PosZLayer

if TYPE_CHECKING:
    from py.game.jelly.entity import JellyEntity

class CastleLogic(BuildingLogic):
    def __init__(self, building):
        super().__init__(building)
        self.cooldown_timer = 0.0
        self.current_target: "JellyEntity" = None

        # 預算攻擊範圍平方
        radius_grid = self.building.stats.effective_grid_range / 2.0
        radius_px = GameContext.grid_cvt.col_to_px(radius_grid)
        self.attack_range_sq = radius_px**2 * CastleConfig.BUFFER_RANGE_RATIO.value
        self.attack_range_grid_sq = radius_grid**2

        # 攻擊中心點
        grid_point = self.building.stats.grid_point
        grid_size = self.building.stats.grid_size
        self.center_pos = GameContext.grid_cvt.get_block_center(grid_point, grid_size, PosZLayer.UI_ELEMENT)

    def update(self, dt: float):
        if self.building.has_effect(LabSkillType.ICE): return
        # 處理冷卻
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt

        # 驗證目標
        if self.current_target:
            if not self._is_target_valid(self.current_target):
                self.current_target = None

        # 尋找目標
        if self.current_target is None:
            self.current_target = self._find_best_target_optimized()

        if self.current_target and self.cooldown_timer <= 0:
            self._shoot()

    def _shoot(self):
        """ 發射子彈 """
        if not self.current_target: return

        GameContext.bullet_mg.spawn_bullet(
            building = self.building,
            target = self.current_target,
            owner_logic = self,
        )

        self.cooldown_timer = self.building.stats.rate_of_fire

    def _is_target_valid(self, target: "JellyEntity"):
        """ 檢查目標是否還能打 (活著 + 距離內) """
        if target.stats.is_dead: return False

        dist_sq = (target.stats.pos.x - self.center_pos.x)**2 + (target.stats.pos.y - self.center_pos.y)**2

        return dist_sq <= self.attack_range_sq

    def _find_best_target_optimized(self):
        """ 遍歷敵人列表，找出最近的一個 """
        enemies = GameContext.army_mg.jellies

        best_target = None
        min_dist_sq = self.attack_range_sq

        my_pos = self.center_pos
        my_owner = self.building.stats.owner

        for jelly in enemies:
            if jelly.stats.owner == my_owner: continue
            if jelly.stats.is_dead: continue

            # 距離快篩 (先算 X 軸，太遠直接跳過)
            dx = jelly.stats.pos.x - my_pos.x
            if dx**2 > min_dist_sq: continue

            dy = jelly.stats.pos.y - my_pos.y
            dist_sq = dx**2 + dy**2

            # 更新最近目標
            if dist_sq <= min_dist_sq:
                min_dist_sq = dist_sq
                best_target = jelly

        return best_target
