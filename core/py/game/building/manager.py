from typing import TYPE_CHECKING, List

from py.debug import dbg
from py.font.manager import font_mg
from py.font.preset import TextID
from py.game.building.entity import BuildingEntity
from py.game.building.factory import BUILDING_REGISTRY
from py.game.building.logic.variable import (LabConfig, LabConfigKey,
                                             LabSkillState)
from py.game.building.preset import GAME_OBJ_CONFIG
from py.game.building.variable import BuildingStatsKey
from py.game.context import GameContext
from py.game.variable import GameType, GameTypeMap
from py.screen.draw.manager import draw_mg
from py.screen.draw.preset import DrawID
from py.screen.image.manager.core import img_mg
from py.ui_layout.main import layout_mg
from py.ui_layout.name.identifiers import LayoutName
from py.ui_layout.name.registry import LayoutNameRegistry
from py.ui_layout.scale.manager import location_config
from py.ui_layout.variable import PosZLayer
from py.variable import GridPoint, Position, Size

if TYPE_CHECKING:
    from py.game.building.logic.lab import LabLogic


class BuildingManager:
    def __init__(self):
        self.building_map: dict[GridPoint, BuildingEntity] = {}

    # =========================================================================
    # [Level Management] 關卡載入與清空
    # =========================================================================

    def load_level(self):
        """ 載入關卡：讀取設定檔 -> 查找工廠 -> 生成物件 -> 計算 UI """
        self._clear_level()

        if GameContext.level not in GAME_OBJ_CONFIG:
            dbg.error(f'Level {GameContext.level} not in GAME_OBJ_CONFIG')
            return

        level_data = GAME_OBJ_CONFIG[GameContext.level]
        # 注意：這裡使用 get_value 確保 key 是字串 (例如 "arch")
        arch_list = level_data.get(GameTypeMap.get_value(GameType.Genre.ARCH), [])

        # 遍歷建築清單
        for index, data_value in enumerate(arch_list):
            self._create_entity_from_data(data_value, index)

        dbg.log(f"Level {GameContext.level} loaded. Total buildings: {len(self.building_map)}")

    def _clear_level(self):
        """ 清空當前關卡所有建築 """
        for building in self.building_map.values():
            if building.layout_ui:
                # 從命名系統註銷
                LayoutNameRegistry.unregister(building.layout_ui.name)
                # 從 LayoutManager 移除 (停止渲染與事件判定)
                layout_mg.remove_item(building.layout_ui)

        # 清空管理器自己的字典
        self.building_map.clear()

    def _create_entity_from_data(self, data: dict, index: int):
        """ 根據資料生成單一建築並註冊 UI """
        genre = data.get(BuildingStatsKey.ARCH)

        # 從 Factory 的註冊表中查找對應的生成函式
        make_func = BUILDING_REGISTRY.get(genre)

        if not make_func:
            dbg.error(f"[BuildingManager] No factory registered for type: {genre}")
            return

        # 執行生成函式
        entity: BuildingEntity = make_func(
            owner       = data.get(BuildingStatsKey.OWNER),
            grid_pos    = data.get(BuildingStatsKey.GRID),
            army        = data.get(BuildingStatsKey.ARMY, 0),
            level       = data.get(BuildingStatsKey.LEVEL, 0)
        )

        # 立即初始化 Layout 位置
        entity.update_layout(PosZLayer.UI_ELEMENT.value)

        if entity.layout_ui:
            # 確保生成 ID 使用字串而非數字 (3 -> "production")
            genre_str = GameTypeMap.get_value(GameType.Genre.ARCH)
            arch_str = GameTypeMap.get_value(genre)

            unique_name = f"{GameContext.page.value}_{GameContext.level}_{genre_str}_{arch_str}_{index}".upper()

            entity.layout_ui.update(
                category = GameContext.page,
                name = unique_name,
            )

            # 註冊到 LayoutNameRegistry
            LayoutNameRegistry.register(name = unique_name, group_key = GameContext.page)
            # 註冊到 LayoutManager
            layout_mg.add_item(entity.layout_ui)

        self.add_building(entity)

    # =========================================================================
    # [Object Management] 物件增刪
    # =========================================================================

    def add_building(self, entity: BuildingEntity):
        """ 將建築加入管理 Map """
        size = entity.stats.grid_size

        if not GameContext.world_map.is_area_free(entity.grid_point, entity.stats.grid_size):
            dbg.war(f"[BuildingManager] Add failed. Point:{entity.grid_point}, Size:{size} occupied.")
            return False

        if entity.grid_point in self.building_map:
            dbg.war(f"[BuildingManager] Overwriting building at {entity.grid_point}")
            return False

        # 向 WorldMap 註冊佔用
        GameContext.world_map.register_object(entity, entity.grid_point, size)

        # 加入管理器字典
        self.building_map[entity.grid_point] = entity
        return True

    def remove_building(self, entity: BuildingEntity):
        """ 移除單一建築 """
        if entity.grid_point not in self.building_map: return

        # 移除建築註冊
        GameContext.faction_mg.unregister(entity)

        # 移除 UI
        if entity.layout_ui:
            LayoutNameRegistry.unregister(entity.layout_ui.name)
            layout_mg.remove_item(entity.layout_ui)

        # 解除地圖佔用
        GameContext.world_map.unregister_object(entity.grid_point, entity.stats.grid_size)

        # 從管理器移除
        del self.building_map[entity.grid_point]

    # =========================================================================
    # [Query] 查詢介面
    # =========================================================================

    def get_all_buildings(self) -> List[BuildingEntity]:
        """ 取得當前所有建築列表 (供 AI 遍歷使用) """
        return list(self.building_map.values())

    def get_building(self, grid_pos: GridPoint) -> BuildingEntity | None:
        """ 透過座標快速取得建築 """
        obj = GameContext.world_map.get_object_at(grid_pos)
        if isinstance(obj, BuildingEntity):
            return obj
        return None

    def get_building_from_pixel(self, mouse_pos: tuple[int, int]) -> BuildingEntity | None:
        """ [純查詢] 根據螢幕像素座標取得建築 """
        pos = Position(mouse_pos[0], mouse_pos[1], 0)
        grid_pt = GameContext.grid_cvt.pos_to_grid(pos)
        return self.get_building(grid_pt)

    # =========================================================================
    # [Render & Update] 渲染與更新
    # =========================================================================

    def update(self, dt: float):
        for building in self.building_map.values():
            building.update(dt)

    def render(self):
        """ [集中渲染控制] 遍歷所有建築並繪製圖像與文字 """
        for building in self.building_map.values():
            ui_item = building.layout_ui
            if not ui_item:
                continue

            # 畫建築物圖
            target_id = building.get_self_img_id
            sprite_idx = building.stats.visual_sprite_index

            img_mg.draw_image_dynamic(
                image_id = target_id,
                pos = ui_item.pos,
                size = ui_item.size,
                sprite_index = sprite_idx
            )

            # 畫兵量文字
            army_count = int(building.stats.army)
            army_upgrade = building.stats.upgrade_cost_army
            owner = building.stats.owner
            font_mg.draw_text(
                TextID.GAME_BUILDING_ARMY,
                army_count,
                offset_pos = location_config.game.building_army_font_offset,
                override_pos = Position(
                    ui_item.pos.x,
                    ui_item.pos.y,
                    PosZLayer.TEXT
                )
            )

            # 畫建築物特效
            for effect_type in building.active_effects:
                img_mg.draw_image_dynamic(
                    image_id = LayoutName.GAME_VFX_LAB_IMPACT,
                    pos = ui_item.pos,
                    sprite_index = effect_type.value
                )

            # 畫玩家特殊顯示
            if owner == GameType.Owner.PLAYER:
                if army_count > army_upgrade and building.stats.level < building.stats.max_level:
                    img_mg.draw_image_dynamic(
                        image_id = LayoutName.GAME_UPGRADE,
                        pos = ui_item.pos,
                        offset_pos = location_config.game.upgrade_offset,
                    )

            # 繪製 castle 範圍
            if building.stats.arch == GameType.Arch.CASTLE:
                draw_mg.add_form(
                    draw_id = DrawID.GAME_CASTLE_RANGE_CIRCLE,
                    override_pos = ui_item.pos,
                    offset_pos = location_config.game.castle_range_circle_offset,
                )
                layout_mg.update_item_pos(
                    page = GameContext.page,
                    name = LayoutName.GAME_CASTLE_RANGE_CIRCLE,
                    pos = ui_item.pos,
                    offset_pos = location_config.game.castle_range_circle_offset
                )

            # 繪製 lab 特效
            if building.stats.arch == GameType.Arch.LAB:
                logic: "LabLogic" = building.logic_comp
                skill = logic.active_skill

                if logic.current_state == LabSkillState.BREWING:
                    max_cd = logic.get_max_cd(skill)
                    remaining_cd = logic.get_remaining_cd(skill)

                    progress_bar_width = location_config.game.progress_bar_draw_size.width
                    progress_bar_height = location_config.game.progress_bar_draw_size.height
                    progress_rate = (1 - remaining_cd / max_cd) * progress_bar_width

                    color = LabConfig.SKILL[skill].get(LabConfigKey.COLOR)

                    draw_mg.add_form(
                        draw_id = DrawID.GAME_PROGRESS_BAR,
                        override_pos = ui_item.pos,
                        offset_pos = location_config.game.progress_bar_draw_offset,
                        override_size = Size(progress_rate, progress_bar_height),
                        override_color = color
                    )
                    img_mg.draw_image_dynamic(
                        image_id = LayoutName.GAME_PROGRESS_BAR,
                        pos = ui_item.pos,
                        offset_pos = location_config.game.progress_bar_offset
                    )

                elif logic.current_state == LabSkillState.READY:
                    img_mg.draw_image_dynamic(
                        image_id = LayoutName.GAME_VFX_LAB_READY,
                        pos = ui_item.pos,
                        sprite_index = skill.value
                    )

    def reload_setup(self):
        # 更新建築 Layout
        for b in self.building_map.values():
            b.update_layout(PosZLayer.UI_ELEMENT.value)
