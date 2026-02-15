from py.game.context import GameContext
from py.game.jelly.interaction import JellyInteractionComponent
from py.game.jelly.move import JellyMoveComponent
from py.game.jelly.variable import JellyStats
from py.ui_layout.scale.manager import IHasLayout
from py.ui_layout.variable import LayoutItem, PosZLayer
from py.variable import GridPoint, Position


class JellyEntity(IHasLayout):
    def __init__(self, stats: JellyStats, img_id):
        self.stats = stats
        self.img_id = img_id

        # 組件
        self.move_comp = JellyMoveComponent(stats)
        self.interact_comp = JellyInteractionComponent(stats)

        # UI
        self.ui = LayoutItem(
            category = GameContext.page,
            img_id = img_id,
            pos = stats.pos, # 初始位置
            size = GameContext.grid_cvt.grid_to_size(self.stats.grid_size)
        )

        # 註冊新士兵擁有者
        GameContext.faction_mg.register(self)

    def update(self, dt: float):
        if self.stats.is_dead: return

        # 執行移動
        is_moving = self.move_comp.update(dt)

        # 同步 UI 位置
        self.ui.pos.x = self.stats.pos.x
        self.ui.pos.y = self.stats.pos.y
        self.ui.pos.z = PosZLayer.UI_ELEMENT_2

        # 抵達檢查
        if not is_moving:
            # 停止移動代表抵達建築
            self.interact_comp.on_arrival()

    def update_layout(self, pos_z: int):
        v_col, v_row = GameContext.grid_cvt.calc_virtual_grid(self.stats.pos)
        new_pos = GameContext.grid_cvt.grid_to_pos(GridPoint(v_col, v_row))
        new_pos.z = pos_z

        new_size = GameContext.grid_cvt.grid_to_size(self.stats.grid_size)

        if self.layout_ui:
            self.stats.pos = new_pos
            self.ui.pos = new_pos
            self.ui.size = new_size

    @property
    def layout_ui(self):
        return self.ui

    @property
    def center_pos(self) -> Position:
        """
        取得士兵的中心點
        """
        grid_point = GameContext.grid_cvt.pos_to_grid(self.stats.pos)

        return GameContext.grid_cvt.get_block_center(grid_point, self.stats.grid_size)
