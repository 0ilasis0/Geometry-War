from py.debug import dbg
from py.font.preset import TextID, TextJson
from py.hmi.single_menu.variable import SingleMenuVar
from py.json.manager import json_mg
from py.screen.draw.preset import DrawID
from py.screen.variable import ScreenConfig
from py.ui_layout.manager import LayoutManager
from py.ui_layout.name.identifiers import LayoutName
from py.ui_layout.scale.manager import location_config
from py.ui_layout.variable import LayoutItem, PosZLayer
from py.variable import Align, PageTable, Position, Size


# 建立虛擬 Pos Size 的物件
class LayoutCollection:
    def __init__(self, lay_mg: LayoutManager) -> None:
        self.lay_mg = lay_mg
        self.reload_setup()

    def reload_setup(self):
        self.lay_mg.clear_items()
        self.lay_mg.update_screen_size(ScreenConfig.width, ScreenConfig.height)
        self._setup_menu(PageTable.MENU)
        self._setup_single_menu(PageTable.SINGLE_MENU)
        self._setup_single(PageTable.SINGLE)
        self._setup_sys_config(PageTable.SYS_CONFIG)
        self._setup_help(PageTable.HELP)

    def check_integrity(self):
        """
        遍歷所有的 DrawID 和 TextID，確保它們參照的 LayoutItem 和 JSON 資料真的存在。
        """
        dbg.log("=== 開始 Layout 完整性檢查 (全域掃描模式) ===")
        error_count = 0

        # --- 檢查 DrawID (Layout 參照) ---
        # 建立「已知 Layout 名稱」的白名單
        all_existing_names = set()
        for page_data in self.lay_mg.items.values():
            for name in page_data.keys():
                all_existing_names.add(name)

        for member in DrawID:
            profile = member.value
            if profile.name is None:
                continue

            if profile.name not in all_existing_names:
                dbg.error(f"[DrawID Integrity] {member.name} 指向的 layout_name='{profile.name}' 在任何頁面都找不到！")
                error_count += 1

        # --- 檢查 TextID (JSON 資料參照) ---
        for member in TextID:
            # 取得映射設定
            path_or_list = TextJson.mapping.get(member)

            # 純動態文字或無 Mapping，跳過
            if not path_or_list: continue

            # 統一轉成 List 處理 (為了同時支援「單一路徑 Tuple」與「多重路徑 List」)
            paths_to_check = []
            if isinstance(path_or_list, list):
                paths_to_check = path_or_list
            else:
                paths_to_check = [path_or_list]

            # 檢查列表中的每一條路徑
            for path_tuple in paths_to_check:

                # 格式防呆: 確保 tuple 至少包含 (FileID, Key...)
                if not path_tuple or len(path_tuple) < 1:
                    dbg.war(f"[TextID Config Error] {member.name} 的路徑格式錯誤: {path_tuple}")
                    error_count += 1
                    continue

                file_id = path_tuple[0]  # 第一個元素是 JsonID (例如 JsonID.DISPLAY)
                keys = path_tuple[1:]    # 剩下的是 Keys (例如 "page", "title")

                # 呼叫新版 get_data 進行驗證
                data = json_mg.get_data(file_id, *keys, silent=True)

                if data is None:
                    file_id_str = file_id.name if hasattr(file_id, 'name') else str(file_id)

                    dbg.war(f"[TextID JSON Error] {member.name} 找不到資料 -> File:{file_id_str}, Path:{keys}")
                    error_count += 1

        if error_count == 0:
            dbg.log("=== Layout & JSON 完整性檢查通過！ ===")
        else:
            dbg.war(f"=== 檢查完成，共發現 {error_count} 個錯誤 ===")

    @staticmethod
    def _create_item(category, name, size, pos = None):
        return LayoutItem(
            category = category,
            name = name,
            size = size,
            pos = pos or Position(0, 0, 0),
        )

    def _batch_add_to_collection(self, page, layout_enum: LayoutName, size, pos_z, collection_key: str):
        """
        批次添加項目並存入 self[collection_key] 中
        """
        # 這行程式碼等同於: self.變數名稱 = []
        setattr(self, collection_key, [])

        target_list: list = getattr(self, collection_key)

        for name in layout_enum.serial_list:
            temp_item = self.lay_mg.add_item(
                item = self._create_item(
                    category = page,
                    name = name,
                    size = size
                ),
                z = pos_z
            )
            target_list.append(temp_item)

    def _setup_menu(self, page: PageTable):
        # page
        self.menu_bg = self.lay_mg.add_item(
            self._create_item(
                page,
                LayoutName.MENU_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0, PosZLayer.BACKGROUND.value),
            ),
        )
        self.menu_main = self.lay_mg.add_center(
            item = self._create_item(
                page,
                LayoutName.MENU_MAIN,
                location_config.menu.main_size
            ),
            pos_z = PosZLayer.MAIN.value,
        )
        self.menu_user = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.MENU_USER,
                location_config.menu.user_size
            ),
            target = self.menu_main,
            pos_z = PosZLayer.TOP_OVERLAY.value,
            align = Align.TOP_CENTER,
            gap_y = location_config.menu.gap_y
        )
        self.menu_bt_board = self.lay_mg.add_left_of(
            item = self._create_item(
                page,
                LayoutName.MENU_BT_BOARD,
                location_config.menu.bt_board_size
            ),
            target = self.menu_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.menu.gap_x,
            align = Align.BOTTOM_LEFT
        )

    def _setup_single_menu(self, page: PageTable):
        self.single_menu_bg = self.lay_mg.add_item(
            self._create_item(
                page,
                LayoutName.SINGLE_MENU_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0, PosZLayer.BACKGROUND.value),
            ),
        )
        self.single_menu_main = self.lay_mg.add_center(
            item = self._create_item(
                page,
                LayoutName.SINGLE_MENU_MAIN,
                location_config.single_menu.main_size
            ),
            pos_z = PosZLayer.MAIN.value,
        )
        self.single_menu_user = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.SINGLE_MENU_USER,
                location_config.single_menu.block_size
            ),
            target = self.single_menu_main,
            pos_z = PosZLayer.TOP_OVERLAY.value,
            align = Align.TOP_LEFT,
        )

        self.single_menu_rects = []
        self.single_menu_levels = []
        for r in range(SingleMenuVar.HEIGHT_BLOCK):
            for c in range(SingleMenuVar.WIDTH_BLOCK):
                index = r * SingleMenuVar.WIDTH_BLOCK + c

                rect_item = self.lay_mg.add_inner(
                    item = self._create_item(
                        page,
                        LayoutName.SINGLE_MENU_RECT.serial_list[index],
                        location_config.single_menu.block_size
                    ),
                    target = self.single_menu_main,
                    pos_z = PosZLayer.UI_ELEMENT.value,
                    align = Align.TOP_LEFT,
                    gap_x = c * location_config.single_menu.gap,
                    gap_y = r * location_config.single_menu.gap
                )
                self.single_menu_rects.append(rect_item)

                text_item = self.lay_mg.add_center(
                    item = self._create_item(
                        page,
                        LayoutName.SINGLE_MENU_LEVEL.serial_list[index],
                        location_config.single_menu.number_size
                    ),
                    pos_z = PosZLayer.TEXT.value,
                    target = rect_item,
                )
                self.single_menu_levels.append(text_item)

    def _setup_single(self, page: PageTable):
        self.single_bg = self.lay_mg.add_item(
            item = self._create_item(
                page,
                LayoutName.SINGLE_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0, PosZLayer.BACKGROUND.value),
            ),
        )
        self.game_over = self.lay_mg.add_center(
            item = self._create_item(
                page,
                LayoutName.GAME_OVER,
                Size(ScreenConfig.width // 4, ScreenConfig.height // 4)
            ),
            pos_z = PosZLayer.GAME_NOTIFY
        )
        self.game_teach = self.lay_mg.add_item(
            item = self._create_item(
                page,
                LayoutName.GAME_TEACH,
                Size(
                    location_config.game.obstacle_board_size.width * 3 // 4,
                    location_config.game.obstacle_board_size.height * 3 // 4
                ),
                Position(
                    ScreenConfig.width // 50,
                    ScreenConfig.height - location_config.game.obstacle_board_size.height,
                    PosZLayer.TEXT.value
                )
            ),
        )

        self.game_building_army = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_BUILDING_ARMY,
                size = location_config.game.building_army_font_size
            ),
            z = PosZLayer.TEXT.value
        )
        self.game_select_circle = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_SELECT_CIRCLE,
                size = location_config.game.building_select_circle_size
            ),
            z = PosZLayer.UI_ELEMENT.value
        )
        self.game_castle_range_circle = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_CASTLE_RANGE_CIRCLE,
                size = location_config.game.castle_range_circle_size
            ),
            z = PosZLayer.CASTLE_RANGE.value
        )
        self.game_status_bar = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_STATUS_BAR,
                size = location_config.game.status_bar_size
            ),
            z = PosZLayer.UI_ELEMENT_1.value
        )
        self.game_upgrade = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_UPGRADE,
                size = location_config.game.upgrade_size
            ),
            z = PosZLayer.UI_ELEMENT_1.value
        )
        self.game_upgrade_user = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_UPGRADE_USER,
                size = location_config.game.upgrade_user_size
            ),
            z = PosZLayer.TOP_OVERLAY.value
        )
        self.game_upgrade_user_price = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_UPGRADE_USER_PRICE,
                size = location_config.game.upgrade_user_price_size
            ),
            z = PosZLayer.UI_ELEMENT_2.value
        )

        self.game_ability_ice = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_ABILITY.serial_list[0],
                size = location_config.game.ability_lab_size
            ),
            z = PosZLayer.TOP_OVERLAY.value
        )
        self.game_ability_weak = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_ABILITY.serial_list[1],
                size = location_config.game.ability_lab_size
            ),
            z = PosZLayer.TOP_OVERLAY.value
        )
        self.game_ability_demon = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_ABILITY.serial_list[2],
                size = location_config.game.ability_lab_size
            ),
            z = PosZLayer.TOP_OVERLAY.value
        )
        self.game_ability_price = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_ABILITY_PRICE,
                size = location_config.game.ability_price_size
            ),
            z = PosZLayer.UI_ELEMENT_2.value
        )
        self.game_status_word = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_STATUS_WORD,
                size = location_config.game.status_word_size
            ),
            z = PosZLayer.UI_ELEMENT_2.value
        )
        self.game_jelly_word = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_JELLY_WORD,
                size = location_config.game.jelly_word_size
            ),
            z = PosZLayer.TEXT.value
        )
        self.game_progress_bar = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_PROGRESS_BAR,
                size = location_config.game.progress_bar_size
            ),
            z = PosZLayer.UI_ELEMENT_1.value,
        )
        self.game_faction_bar_color = self.lay_mg.add_center(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_FACTION_BAR_COLOR,
                size = location_config.game.faction_bar_size
            ),
            pos_z = PosZLayer.FACTION_BAR_COLOR.value,
            gap_y = location_config.game.faction_bar_gap_y,
        )
        self.game_faction_bar = self.lay_mg.add_center(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_FACTION_BAR,
                size = location_config.game.faction_bar_size
            ),
            pos_z = PosZLayer.FACTION_BAR.value,
            gap_y = location_config.game.faction_bar_gap_y,
        )
        self.game_faction_bar_army = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_FACTION_BAR_ARMY,
                size = location_config.game.faction_bar_army_size
            ),
            z = PosZLayer.FACTION_BAR_ARMY.value,
        )
        self.game_vfx_lab_ready = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_VFX_LAB_READY,
                size = location_config.game.vfx_lab_ready_size
            ),
            z = PosZLayer.UI_ELEMENT_1.value
        )
        self.game_vfx_lab_impact = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_VFX_LAB_IMPACT,
                size = location_config.game.vfx_lab_impact_size
            ),
            z = PosZLayer.UI_ELEMENT_1.value
        )
        self.game_become_production = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_BECOME.serial_list[0],
                size = location_config.game.become_size
            ),
            z = PosZLayer.TOP_OVERLAY.value
        )
        self.game_become_castle = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_BECOME.serial_list[1],
                size = location_config.game.become_size
            ),
            z = PosZLayer.TOP_OVERLAY.value
        )
        self.game_become_lab = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_BECOME.serial_list[2],
                size = location_config.game.become_size
            ),
            z = PosZLayer.TOP_OVERLAY.value
        )
        self.game_become_price = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.GAME_BECOME_PRICE,
                size = location_config.game.become_price_size
            ),
            z = PosZLayer.UI_ELEMENT_2.value
        )

        self._batch_add_to_collection(
            page = page,
            layout_enum = LayoutName.OBSTACLE_PEN1,
            size = location_config.game.obstacle_pen1_size,
            pos_z = PosZLayer.UI_ELEMENT.value,
            collection_key = "game_obstacle_pen1"
        )
        self._batch_add_to_collection(
            page = page,
            layout_enum = LayoutName.OBSTACLE_COMPASS,
            size = location_config.game.obstacle_compass_size,
            pos_z = PosZLayer.UI_ELEMENT.value,
            collection_key = "game_obstacle_compass"
        )
        self.game_obstacle_board = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.OBSTACLE_BOARD,
                size = location_config.game.obstacle_board_size
            ),
            z = PosZLayer.UI_ELEMENT.value
        )
        self.game_obstacle_pen3 = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.OBSTACLE_PEN3,
                size = location_config.game.obstacle_pen3_size
            ),
            z = PosZLayer.UI_ELEMENT.value
        )
        self.game_obstacle_pen_cross = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.OBSTACLE_PEN_CROSS,
                size = location_config.game.obstacle_pen_cross_size
            ),
            z = PosZLayer.UI_ELEMENT.value
        )
        self.game_obstacle_eraser = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.OBSTACLE_ERASER,
                size = location_config.game.obstacle_eraser_size
            ),
            z = PosZLayer.UI_ELEMENT.value
        )
        self.game_obstacle_ruler = self.lay_mg.add_item(
            item = self._create_item(
                category = page,
                name = LayoutName.OBSTACLE_RULER,
                size = location_config.game.obstacle_ruler_size
            ),
            z = PosZLayer.UI_ELEMENT.value
        )

    def _setup_sys_config(self, page: PageTable):
        self.song_bg = self.lay_mg.add_item(
            self._create_item(
                page,
                LayoutName.SYS_CONFIG_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0, PosZLayer.BACKGROUND.value),
            ),
        )
        self.song_main = self.lay_mg.add_center(
            item = self._create_item(
                page,
                LayoutName.SYS_SONG_MAIN,
                location_config.sys_config.main_size,
            ),
            pos_z = PosZLayer.MAIN.value,
            gap_x = location_config.sys_config.main_gap_x
        )
        self.song_name = self.lay_mg.add_right_of(
            item = self._create_item(
                page,
                LayoutName.SYS_SONG_NAME,
                location_config.sys_config.song_name_size
            ),
            target = self.song_main,
            pos_z = PosZLayer.TEXT.value,
            gap_x = location_config.sys_config.gap_x,
            align = Align.TOP_LEFT
        )
        self.song_block = self.lay_mg.add_below(
            item = self._create_item(
                page,
                LayoutName.SYS_SONG_BLOCK,
                location_config.sys_config.song_block_size
            ),
            target = self.song_name,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap = location_config.sys_config.block_gap_y,
            align = Align.CENTER_LEFT
        )
        self.window_scale_size = self.lay_mg.add_below(
            item = self._create_item(
                page,
                LayoutName.SYS_WINDOW_SCALE,
                location_config.sys_config.window_scale_size
            ),
            target = self.song_block,
            pos_z = PosZLayer.TEXT.value,
            gap = location_config.sys_config.window_scale_gap_y,
            align = Align.CENTER
        )
        self.sys_config_user = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.SYS_SONG_USER,
                location_config.sys_config.user_size,
            ),
            target = self.song_main,
            pos_z = PosZLayer.TOP_OVERLAY.value,
            align = Align.TOP_LEFT,
            gap_x = location_config.sys_config.user_gap_x * (-1),
            gap_y = location_config.sys_config.user_gap_y,
        )

    def _setup_help(self, page: PageTable):
        self.help_bg = self.lay_mg.add_item(
            item = self._create_item(
                page,
                LayoutName.HELP_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0, PosZLayer.BACKGROUND.value),
            ),
        )
        self.help_panel = self.lay_mg.add_center(
            item = self._create_item(
                page,
                LayoutName.HELP_PANEL,
                location_config.help.panel_size
            ),
            pos_z = PosZLayer.MAIN.value,
            gap_y = location_config.help.panel_gap_y * (-1)
        )
        self.help_lace = self.lay_mg.add_center(
            item = self._create_item(
                page,
                LayoutName.HELP_LACE,
                location_config.help.lace_size
            ),
            pos_z = PosZLayer.DECORATION.value,
            gap_y = location_config.help.lace_gap_y
        )
        self.help_option_title = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.HELP_OPTION_TITLE,
                location_config.help.option_title_size,
            ),
            target = self.help_panel,
            pos_z = PosZLayer.TEXT.value,
            align = Align.TOP_LEFT,
            gap_x = location_config.help.title_gap_x,
            gap_y = location_config.help.title_gap_y
        )

        self.help_option_desc_sl = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.HELP_OPTION_DESC,
                location_config.help.option_desc_size,
            ),
            target = self.help_lace,
            pos_z = PosZLayer.TEXT.value,
            align = Align.TOP_LEFT,
            gap_x = location_config.help.desc_gap_x,
            gap_y = location_config.help.desc_gap_y
        )

layout_mg = LayoutManager(ScreenConfig.width, ScreenConfig.height)

layout_collection = LayoutCollection(layout_mg)
