from py.base import central_mg, global_timer
from py.debug import dbg
from py.font.manager import font_mg
from py.font.preset import TextID
from py.font.variable import TextContent
from py.game.context import GameContext
from py.game.manager import game_mg
from py.hmi.config.variable import ConfigVar
from py.json.preset import SaveID
from py.page.base import BootMode, page_mg
from py.page.navigation import BasePageNavigation, base_nav
from py.page.variable import HelpConfig
from py.screen.draw.manager import draw_mg
from py.screen.draw.preset import DrawID
from py.screen.image.manager.core import img_mg
from py.ui_layout.main import layout_mg
from py.ui_layout.name.identifiers import LayoutName
from py.ui_layout.scale.manager import location_config
from py.ui_layout.scale.preset.menu import ScaleMenuVar
from py.ui_layout.scale.preset.sys_config import ScaleSysConfigVar
from py.variable import Align, PageTable, Position, Size


def main_page():
    page_function = page_mg.keymaps[page_mg.current_page]

    # 決定是否載入當前boot
    if page_mg.current_boot == page_mg.current_page:
        page_mg.load_page_boot(page_mg.current_boot)
        page_mg.switch_boot(None)

    # 執行當前頁面主循環
    if page_function is not None:
        page_function()
    else:
        dbg.error(f"no load {page_mg.current_page}")



class PageNavigation:
    def __init__(self, base_nav) -> None:
        self.base_nav: BasePageNavigation = base_nav

    def MENU(self):
        font_mg.draw_json_text(TextID.MENU_MAIN)

        # 畫玩家選擇方塊
        rect_pos: Position = layout_mg.get_item_pos(PageTable.MENU, LayoutName.MENU_USER)
        main_size: Size = layout_mg.get_item_size(PageTable.MENU, LayoutName.MENU_MAIN)
        main_one_height = main_size.height // ScaleMenuVar.MAIN_QUANTITY

        draw_mg.add_form(
            draw_id = DrawID.MENU_USER,
            override_pos = Position(
                rect_pos.x,
                rect_pos.y + main_one_height * self.base_nav.menu_mg.hook_y,
                rect_pos.z
            )
        )

        # 黑塔轉圈圈gif
        amount = ScaleMenuVar.BT_BOARD_WH_QUANTITY * ScaleMenuVar.BT_BOARD_WH_QUANTITY - 1
        time = global_timer.sprite_time_change(amount, amount)
        img_mg.switch_image_idx(LayoutName.MENU_BT_BOARD, time)

    def SINGLE_MENU(self):
        # 畫基本關卡方塊
        for level_item in LayoutName.SINGLE_MENU_RECT.serial_list:
            draw_mg.add_form(
                draw_id = DrawID.SINGLE_MENU_RECT,
                layout_name = level_item
            )

        # 畫關卡數字
        for index, level_item in enumerate(LayoutName.SINGLE_MENU_LEVEL.serial_list):
            level_number = index + 1
            font_mg.draw_text(
                TextID.SINGLE_MENU_LEVEL_STYLE,
                str(level_number),
                target_layout = level_item
            )

        # 畫玩家選擇關卡方塊
        user_pos: Position = layout_mg.get_item_pos(PageTable.SINGLE_MENU, LayoutName.SINGLE_MENU_USER)
        draw_mg.add_form(
            draw_id = DrawID.SINGLE_MENU_USER,
            override_pos = Position(
                user_pos.x + location_config.single_menu.gap * self.base_nav.single_menu_mg.hook_x,
                user_pos.y + location_config.single_menu.gap * self.base_nav.single_menu_mg.hook_y,
                user_pos.z
            )
        )

    def SINGLE(self):
        dt = global_timer.get_dt()
        game_mg.render()
        game_mg.update(dt)

    def SYS_CONFIG(self):
        # 選項
        font_mg.draw_json_text(TextID.SYS_SONG_MAIN)

        # 音量大小方塊
        current_vol = self.base_nav.sys_config_mg.state.get(SaveID.SYS_VOLUME)
        song_block_size: Size = layout_mg.get_item_size(PageTable.SYS_CONFIG, LayoutName.SYS_SONG_BLOCK)
        draw_mg.add_form(
            draw_id = DrawID.SYS_SONG_BLOCK_CELL,
            override_size = Size(
                (song_block_size.width // ConfigVar.WIDTH_BLOCK) * current_vol,
                (song_block_size.height // ConfigVar.HEIGHT_BLOCK)
            )
        )

        # 玩家選擇方塊
        user_pos: Position = layout_mg.get_item_pos(PageTable.SYS_CONFIG, LayoutName.SYS_SONG_USER)
        main_size: Size = layout_mg.get_item_size(PageTable.SYS_CONFIG, LayoutName.SYS_SONG_MAIN)
        main_one_height = main_size.height // ScaleSysConfigVar.main_quantity
        draw_mg.add_form(
            draw_id = DrawID.SYS_SONG_USER,
            override_pos = Position(
                user_pos.x,
                user_pos.y + self.base_nav.sys_config_mg.hook_y * main_one_height,
                user_pos.z
            )
        )

        # 歌曲名稱
        index = self.base_nav.sys_config_mg.state.get(SaveID.SYS_SONG)
        font_mg.draw_text(TextID.SYS_SONG_NAME, self.base_nav.sys_config_mg.files_name[index])

        # 調整視窗大小數值顯示
        index = self.base_nav.sys_config_mg.state.get(SaveID.SYS_SCALE)
        font_mg.draw_text(TextID.SYS_WINDOW_SCALE, TextContent.SYS_WINDOW_SCALE_NUMBER[index])

    def HELP(self):
        # 玩家選擇 img_panel
        img_mg.switch_image_idx(LayoutName.HELP_PANEL, self.base_nav.help_mg.hook_x)

        # 標題文字
        for idx in range(3):
            alpha_percent = HelpConfig.title_alpha[self.base_nav.help_mg.hook_x][idx]
            font_mg.draw_json_text(
                TextID.HELP_DYNAMIC_TITLE,
                index = idx,
                alpha = alpha_percent,
                align = Align.CENTER,
                offset_pos = Position(location_config.help.title_gap_y_plus * idx, 0, 0)
            )

        # 遊戲說明文字
        font_mg.draw_json_text(
            text_id = TextID.HELP_DYNAMIC_DESC,
            index = self.base_nav.help_mg.hook_x,
            align = Align.BOTTOM_LEFT
        )

    def EXIT(self):
        central_mg.running = False

page_navigation = PageNavigation(base_nav)



class PageBoot():
    ''' 只會在初次進入當前頁面時載入一次下次刷屏不會進來，但下次進入頁面又會進來 '''
    def MENU(self):
        pass

    def SINGLE_MENU(self):
        pass

    def SINGLE(self):
        if page_mg.boot_mode == BootMode.FULL:
            game_mg.load_level(GameContext.level)

    def SYS_CONFIG(self):
        draw_mg.clear_map(PageTable.SYS_CONFIG)
        # 音量網格線
        draw_mg.add_grid(draw_id = DrawID.SYS_SONG_BLOCK_GRID, fixed = True)

    def HELP(self):
        pass

    def EXIT(self):
        pass

page_boot = PageBoot()
