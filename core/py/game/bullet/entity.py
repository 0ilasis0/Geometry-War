import math
from typing import TYPE_CHECKING

from py.game.bullet.variable import BulletStats, BulletVar
from py.game.context import GameContext
from py.game.variable import GameType, GameTypeMap
from py.resource.registry import ResourceRegistry
from py.ui_layout.scale.manager import location_config
from py.ui_layout.variable import LayoutItem, PosZLayer
from py.variable import Position

if TYPE_CHECKING:
    from py.game.building.entity import BuildingEntity
    from py.game.building.logic.castle import CastleLogic
    from py.game.jelly.entity import JellyEntity


class BulletEntity:
    def __init__(self, building: "BuildingEntity", target: "JellyEntity", owner_logic: "CastleLogic"):
        """
        :param start_pos: 發射起始點
        :param target: 追蹤的目標 (Jelly)
        :param stats: 數值 (傷害, 速度)
        :param owner_logic: 發射這顆子彈的 CastleLogic (用於回報命中)
        """
        self.target = target
        self.owner_logic = owner_logic
        self.current_owner = building.stats.owner

        bullet_speed_px = GameContext.grid_cvt.col_to_px(building.stats.bullet_speed_grid)
        self.stats = BulletStats(building.stats.bullet_damage, bullet_speed_px)

        self.is_active = True

        start_pos = building.center_pos
        self.pos = Position(start_pos.x, start_pos.y, PosZLayer.PROJECTILE)
        self.ui = LayoutItem(
            category = GameContext.page,
            img_id = self._get_self_img_id(building.stats.owner),
            pos = self.pos,
            size = location_config.game.bullet_size
        )

    def update(self, dt: float):
        if not self.is_active: return

        # 檢查城堡狀態是否改變
        if not self._check_owner_status(): return

        # 如果目標死了，子彈要消失
        if self.target.stats.is_dead:
            self._on_miss()
            return

        # 計算向量
        dx = self.target.center_pos.x - self.pos.x
        dy = self.target.center_pos.y - self.pos.y
        dist_sq = dx**2 + dy**2

        # 命中判定
        current_hit_radius = GameContext.grid_cvt.col_to_px(BulletVar.HIT_RADIUS_GRID.value)**2
        if dist_sq < current_hit_radius:
            self._on_hit()
            return

        dist = math.sqrt(dist_sq)
        move_dist = self.stats.speed * dt

        # 正規化向量 * 移動距離
        self.pos.x += (dx / dist) * move_dist
        self.pos.y += (dy / dist) * move_dist

        # 同步 UI
        self.ui.pos.x = self.pos.x
        self.ui.pos.y = self.pos.y

    def _on_hit(self):
        """ 命中處理 """
        self.is_active = False

        self.target.stats.army -= self.stats.damage
        if self.target.stats.army <= 0:
            self.target.stats.is_dead = True
            self.target.stats.army = 0

    def _on_miss(self):
        """ 目標丟失處理 """
        self.is_active = False

    def _check_owner_status(self) -> bool:
        """
        檢查發射這顆子彈的城堡是否易主
        Returns: True (狀態正常，繼續飛行), False (子彈應失效)
        """
        real_time_owner = self.owner_logic.building.stats.owner

        if real_time_owner != self.current_owner:
            self.current_owner = real_time_owner

            # 更新子彈圖片
            self.ui.img_id = self._get_self_img_id(self.current_owner)

            # 檢查當前鎖定的目標是否變成了「友軍」
            if self.target.stats.owner == self.current_owner:
                self.is_active = False
                return False

        return True

    def _get_self_img_id(self, owner) -> str:
        """
        自動根據當前數值，組合出對應的圖片 ID
        """
        genre_str = GameTypeMap.get_value(GameType.Genre.BULLET)
        owner_str = GameTypeMap.get_value(owner)

        # 這裡的參數必須跟你在註冊時傳給 PathUtility.generate_id 的順序一模一樣
        return ResourceRegistry.get_key(genre_str, owner_str)

    @property
    def layout_ui(self):
        return self.ui
