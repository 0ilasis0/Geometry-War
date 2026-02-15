from py.a_star.manage import a_star_mg
from py.font.manager import font_mg
from py.font.preset import TextID
from py.game.ai.manager import AIManager
from py.game.building.logic.variable import (LabConfig, LabConfigKey,
                                             LabSkillType, PrototypeConfig,
                                             PrototypeConfigKey)
from py.game.building.manager import BuildingManager
from py.game.building.preset import GAME_OBJ_CONFIG
from py.game.bullet.manager import BulletManager
from py.game.context import GameContext
from py.game.faction.manager import FactionManager
from py.game.jelly.manager import ArmyManager
from py.game.map.grid_converter import GridConverter
from py.game.map.world_map import GameWorldMap
from py.game.obstacle.manager import ObstacleManager
from py.game.slection import selection_mg
from py.game.variable import FACTION_COLORS, GameType
from py.page.navigation import base_nav
from py.screen.draw.manager import draw_mg
from py.screen.draw.preset import DrawID
from py.screen.image.manager.core import img_mg
from py.screen.variable import ScreenConfig
from py.ui_layout.main import layout_mg
from py.ui_layout.name.identifiers import LayoutName
from py.ui_layout.scale.manager import location_config
from py.ui_layout.scale.preset.base import ScaleMapGrid
from py.variable import Align, Color, PageTable, Position, Size


class GameManager:
    def __init__(self):
        self.current_page: PageTable = PageTable.SINGLE
        self.current_level: int = None

        # 由 GameManager 統一持有
        self.grid_cvt = GridConverter(
            start_x = location_config.map_grid.start_x,
            start_y = location_config.map_grid.start_y,
            cell_width = location_config.map_grid.cell_w,
            cell_height = location_config.map_grid.cell_h
        )

        cols = ScreenConfig.width // ScaleMapGrid.cell_w
        rows = ScreenConfig.height // ScaleMapGrid.cell_h
        self.world_map = GameWorldMap(cols, rows)

        self.faction_mg = FactionManager()
        self.building_mg = BuildingManager()
        self.obstacle_mg = ObstacleManager(self.world_map)
        self.army_mg = ArmyManager()
        self.bullet_mg = BulletManager()
        self.ai_mg = AIManager()

        # 計時器
        self.tick_timer = 0.0

        self._context_reload()

    def load_level(self, level_id: int):
        """ 統籌載入流程 """
        self.current_level = level_id
        # 讀取關卡資料
        level_data = GAME_OBJ_CONFIG.get(level_id, {})

        # 清理環境
        self.world_map.clear()
        selection_mg.deselect()
        a_star_mg.clear_cache()
        self.faction_mg.setup_level(level_data)

        self._context_reload()

        self.ai_mg.setup_level()
        self.bullet_mg.clear_all()
        self.army_mg.load_level()
        self.obstacle_mg.load_level(level_id)
        self.building_mg.load_level()

    def update(self, dt):
        self.ai_mg.update(dt)
        self.building_mg.update(dt)
        self.army_mg.update(dt)
        self.bullet_mg.update(dt)

        self.tick_timer += dt
        if self.tick_timer > 0.3:
            # 更新玩家選取建築是否為己方
            selection_mg.update(dt)
            # 更新當前陣營的所有士兵數量數據
            self.faction_mg.update_strategic_stats()
            self.tick_timer = 0.0

        # 檢查勝負
        self._check_game_result()

    def _check_game_result(self):
        # 檢查玩家是否戰敗
        if not self.faction_mg.is_player_alive():
            font_mg.draw_text(TextID.GAME_OVER)
            return

        # 檢查敵人是否戰敗
        enemies = self.faction_mg.get_alive_enemy_factions()
        if not enemies:
            base_nav.single_menu_mg.unlock_level(self.current_level + 1)
            base_nav.back_to_prev(self.current_page)
            return

    def render(self):
        """ 統籌渲染 """
        # 畫建築 (地板/牆壁)
        self.obstacle_mg.render()
        self.building_mg.render()
        self.army_mg.render()
        self.bullet_mg.render()
        self._render_selection_effect()
        self._render_faction_bar()
        self._render_teach()

    def _render_selection_effect(self):
        """ 負責選取渲染 (支援單選詳情與多選簡潔模式) """
        # 改為獲取所有被選取的實體列表
        targets = selection_mg.selected_entities
        if not targets: return

        # 判斷是否為多選模式 (拖曳中)
        is_multi_mode = selection_mg.is_multi_select

        for target in targets:
            item_pos = target.layout_ui.pos
            building_stats = target.stats

            # =========================================================
            # [始終顯示] 玩家選取圓圈
            # =========================================================
            draw_mg.add_form(
                draw_id = DrawID.GAME_MENU_CIRCLE,
                override_pos = item_pos,
                offset_pos = location_config.game.building_select_circle_offset
            )

            # =========================================================
            # [過濾器] 如果是多選/拖曳模式，到這裡就停止，不渲染詳細菜單
            # =========================================================
            if is_multi_mode: continue

            # =========================================================
            # [單選專用] 詳細 UI (狀態欄、升級按鈕、變身按鈕)
            # =========================================================

            # --- 狀態欄 ---
            img_mg.draw_image_dynamic(
                image_id = LayoutName.GAME_STATUS_BAR,
                pos = item_pos,
                offset_pos = location_config.game.status_bar_offset
            )

            # 狀態欄文字
            content = [
                building_stats.max_army_capacity, building_stats.rate_of_production,
                building_stats.jelly_speed, building_stats.defense
            ]
            for index, text in enumerate(content):
                font_mg.draw_text(
                    TextID.GAME_STATUS_WORD,
                    text,
                    offset_pos = location_config.game.status_word_offset[index],
                    override_pos = item_pos
                )

            # --- 升級符號/價格文字 ---
            if building_stats.level < building_stats.max_level:
                upgrade_pos = layout_mg.get_item_pos(GameContext.page, LayoutName.GAME_UPGRADE_USER)
                layout_mg.update_item_pos(
                    page = self.current_page,
                    name = LayoutName.GAME_UPGRADE_USER,
                    pos = Position(item_pos.x, item_pos.y, upgrade_pos.z),
                    offset_pos = location_config.game.upgrade_user_offset
                )
                img_mg.draw_image_dynamic(
                    image_id = LayoutName.GAME_UPGRADE_USER,
                    pos = Position(item_pos.x, item_pos.y, upgrade_pos.z),
                    offset_pos = location_config.game.upgrade_user_offset
                )
                font_mg.draw_text(
                    TextID.GAME_UPGRADE_USER_PRICE,
                    building_stats.upgrade_cost_army,
                    override_pos = item_pos,
                    offset_pos = location_config.game.upgrade_user_price_offset
                )

            # --- 原形建築變身符號/價格文字 ---
            if building_stats.arch == GameType.Arch.PROTOTYPE:
                become_pos = layout_mg.get_item_pos(GameContext.page, LayoutName.GAME_BECOME.serial_list[0])
                for index, (target_arch, data) in enumerate(PrototypeConfig.BECOME_MAP.items()):
                    if target_arch == GameType.Arch.PROTOTYPE: continue
                    ui_name = data[PrototypeConfigKey.NAME]
                    cost = data[PrototypeConfigKey.COST]
                    layout_mg.update_item_pos(
                        page = self.current_page,
                        name = ui_name,
                        pos = Position(item_pos.x, item_pos.y, become_pos.z),
                        offset_pos = location_config.game.become_offset[index]
                    )
                    img_mg.draw_image_dynamic(
                        image_id = ui_name,
                        pos = Position(item_pos.x, item_pos.y, become_pos.z),
                        offset_pos = location_config.game.become_offset[index]
                    )
                    font_mg.draw_text(
                        TextID.GAME_ABILITY_PRICE,
                        cost,
                        override_pos = item_pos,
                        offset_pos = location_config.game.become_price_offset[index]
                    )

            # --- 實驗室技能符號/價格文字 ---
            if building_stats.arch == GameType.Arch.LAB:
                lab_ability_pos = layout_mg.get_item_pos(GameContext.page, LayoutName.GAME_ABILITY.serial_list[0])
                level = building_stats.level + 1
                for index in range(level):
                    layout_mg.update_item_pos(
                        page = self.current_page,
                        name = LayoutName.GAME_ABILITY.serial_list[index],
                        pos = Position(item_pos.x, item_pos.y, lab_ability_pos.z),
                        offset_pos = location_config.game.ability_lab_offset[index]
                    )
                    img_mg.draw_image_dynamic(
                        image_id = LayoutName.GAME_ABILITY.serial_list[index],
                        pos = Position(item_pos.x, item_pos.y, lab_ability_pos.z),
                        offset_pos = location_config.game.ability_lab_offset[index]
                    )

                    skill_type = LabSkillType(index)
                    config = LabConfig.SKILL.get(skill_type)
                    cost = config[LabConfigKey.COST]
                    font_mg.draw_text(
                        TextID.GAME_ABILITY_PRICE,
                        cost,
                        override_pos = item_pos,
                        offset_pos = location_config.game.ability_price_offset[index]
                    )

    def _render_teach(self):
        ''' 繪製關卡教學文字 '''
        if self.current_level > 3: return

        font_mg.draw_json_text(
            text_id = TextID.GAME_TEACH,
            index = self.current_level,
            align = Align.TOP_LEFT
        )

    def _render_faction_bar(self):
        """
        計算場上所有非中立陣營的兵力總和，依比例繪製長條圖
        """
        # 獲取數據 (格式:List[Tuple[Owner, Power]])
        power_data = []
        total_power = 0.0

        for owner, faction in self.faction_mg.factions.items():
            if not faction.is_active: continue
            if owner == GameType.Owner.NEUTRAL: continue

            army = faction.total_army
            if army > 0:
                power_data.append((owner, army))
                total_power += army

        power_data.sort(key=lambda x: x[0].value)

        target_item = layout_mg.get_item(GameContext.page, LayoutName.GAME_FACTION_BAR)
        base_offset = location_config.game.faction_bar_draw_offset
        base_pos = target_item.pos
        total_width = target_item.size.width * 0.95
        bar_height = target_item.size.height * 0.5

        current_x_offset = 0.0 # 累加的 X 偏移量
        for owner, army in power_data:
            ratio = army / total_power
            segment_width = total_width * ratio
            color = FACTION_COLORS.get(owner, Color.GREY.value)

            # 繪製陣營矩形
            draw_mg.add_form(
                draw_id = DrawID.GAME_FACTION_BAR_COLOR,
                override_pos = base_pos,
                offset_pos = Position(base_offset.x + current_x_offset, base_offset.y, 0),
                override_size = Size(segment_width, bar_height),
                override_color = color
            )
            # 繪製陣營目前數量
            pos_x = base_offset.x + current_x_offset + segment_width // 2
            pos_y = base_offset.y * 0.55
            font_mg.draw_text(
                TextID.GAME_FACTION_BAR_ARMY,
                int(army),
                override_pos = base_pos,
                offset_pos = Position(pos_x, pos_y, 0),
                override_color = color
            )

            # 更新下一個區塊的起點
            current_x_offset += segment_width

    def reload_setup(self):
        """ 視窗縮放時的統一更新 """
        self.grid_cvt.update_params(
            location_config.map_grid.start_x,
            location_config.map_grid.start_y,
            location_config.map_grid.cell_w,
            location_config.map_grid.cell_h
        )

        self.building_mg.reload_setup()
        self.army_mg.reload_setup()

    def _context_reload(self):
        GameContext.reset()
        GameContext.page = self.current_page
        GameContext.level = self.current_level
        GameContext.world_map = self.world_map
        GameContext.grid_cvt = self.grid_cvt
        GameContext.faction_mg = self.faction_mg
        GameContext.building_mg = self.building_mg
        GameContext.army_mg = self.army_mg
        GameContext.bullet_mg = self.bullet_mg

    def switch_page(self, page):
        self.current_page = page
        GameContext.page = self.current_page

game_mg = GameManager()
