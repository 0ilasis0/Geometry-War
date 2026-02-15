'''只有在更新/特殊情況需要用到，一班正常遊玩時請關掉-------------------------'''
# .dll更新並生成，若是無更新請關掉以免消耗資源
# from py.compile_dll import CompileAndLoadDll
# CompileAndLoadDll()

'''只有在更新/特殊情況需要用到，一班正常遊玩時請關掉-------------------------'''
import pygame

pygame.init()
from py.a_star.main import a_star_mg
from py.debug import dbg
from py.game.manager import game_mg
from py.input.keyboard.manager import keyboard_mg
from py.input.mouse.manager import mouse_mg
from py.json.manager import json_mg
from py.page.base import page_mg
from py.page.main import page_boot, page_navigation
from py.page.navigation import base_nav
from py.screen.main import img_mg
from py.ui_layout.main import layout_collection
from py.ui_layout.name.init import layout_name_init_static_names
from py.variable import PageTable

keymaps = {}
for page in PageTable:
    func = getattr(page_navigation, page.name, None)
    if func:
        keymaps[page] = func
    else:
        dbg.war(f"Warning: No main loop function found for {page.name}")
        pass

#
# 初始化set
#
''' base '''
a_star_mg.setup()

''' location_layout '''
layout_name_init_static_names()
layout_collection.check_integrity()

''' screen '''
img_mg.reload_setup()

''' page '''
#註冊 Callback
for page in PageTable:
    # 檢查 PageInit 是否有對應方法
    if hasattr(page_boot, page.name):
        fcn = getattr(page_boot, page.name)
        page_mg.register_init_fcn(page, fcn)

page_mg.setup(keymaps)

''' song '''
pygame.mixer.init()

''' keyboard '''
keyboard_mg.setup(
    menu_mg = base_nav.menu_mg,
    single_mg = base_nav.single_mg,
    single_menu_mg = base_nav.single_menu_mg,
    sys_config_mg = base_nav.sys_config_mg,
    help_mg = base_nav.help_mg
)
mouse_mg.setup(
    page_mg = page_mg,
    building_mg = game_mg.building_mg
)


#
# other
#
''' font '''
# 如果找 read_list_json 直接去 json_manager __init__進行設定

''' page '''
# 對第一次的MENU做BOOT
page_mg.load_page_boot(page_mg.current_page)

# 確認 word_list_data / word_dict_data 清單
dbg.dump(json_mg.json_data)

# 確認name的儲存
from py.ui_layout.name.registry import LayoutNameRegistry

dbg.dump(LayoutNameRegistry._active_names)
