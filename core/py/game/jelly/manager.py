from py.debug import dbg
from py.font.manager import font_mg
from py.font.preset import TextID
from py.game.building.entity import BuildingEntity
from py.game.context import GameContext
from py.game.jelly.entity import JellyEntity
from py.game.jelly.factory import JellyFactory
from py.screen.image.manager.core import img_mg
from py.ui_layout.scale.manager import location_config
from py.ui_layout.variable import PosZLayer
from py.variable import GridPoint


class ArmyManager:
    def __init__(self):
        # 存放所有活著的士兵實體
        self.jellies: list[JellyEntity] = []
        # 用於存放目前存在士兵的網格
        self.spatial_map: dict[tuple[int, int], list[JellyEntity]] = {}

    def spawn_jelly(self, source_building: BuildingEntity, target_building, path: list[GridPoint], army_count: int):
        """ [外部入口] 生成並註冊新士兵 """
        new_jelly = JellyFactory.spawn_from_building(
            source_building = source_building,
            path = path,
            target_building = target_building,
            army_count = army_count,
        )

        if new_jelly:
            self.add_jelly(new_jelly)
        else:
            dbg.war("Failed to spawn jelly from factory.")

    def add_jelly(self, jelly: JellyEntity):
        """ 將士兵加入管理列表 """
        if jelly not in self.jellies:
            self.jellies.append(jelly)

    def remove_jelly(self, jelly: JellyEntity):
        """ 移除單一士兵 """
        if jelly in self.jellies:
            GameContext.faction_mg.unregister(jelly)
            self.jellies.remove(jelly)

    def clear_all(self):
        """ 清空所有士兵 """
        self.jellies.clear()
        self.spatial_map.clear()

    def load_level(self):
        """ 載入關卡 """
        self.clear_all()

    # =========================================================================
    # [Render & Update] 渲染與更新
    # =========================================================================

    def update(self, dt: float):
        """ [核心迴圈] 更新所有士兵狀態 """
        dead_jellies = []
        self.spatial_map.clear()

        for jelly in self.jellies:
            # 執行士兵自己的更新邏輯 (移動、互動)
            jelly.update(dt)

            # 檢查是否死亡 (或任務完成)
            if jelly.stats.is_dead:
                dead_jellies.append(jelly)
                continue

            # 將活著的士兵註冊到空間表
            g_pos = GameContext.grid_cvt.pos_to_grid(jelly.stats.pos)
            key = (g_pos.col, g_pos.row)

            if key not in self.spatial_map:
                self.spatial_map[key] = []

            self.spatial_map[key].append(jelly)

        # 統一清理屍體
        for dead in dead_jellies:
            self.remove_jelly(dead)

    def render(self):
        """ [集中渲染控制] 遍歷所有士兵並繪製 """
        for jelly in self.jellies:
            img_mg.draw_image_dynamic(
                image_id = jelly.layout_ui.img_id,
                pos = jelly.layout_ui.pos,
                size = jelly.layout_ui.size,
            )
            font_mg.draw_text(
                TextID.GAME_JELLY_WORD,
                int(jelly.stats.army),
                offset_pos = location_config.game.jelly_word_offset,
                override_pos = jelly.layout_ui.pos
            )

    def reload_setup(self):
        for jelly in self.jellies:
            jelly.update_layout(PosZLayer.UI_ELEMENT_2)

    def get_jellies_in_grid(self, col: int, row: int) -> list[JellyEntity]:
        """ 取得特定格子內的所有士兵 """
        return self.spatial_map.get((col, row), [])
