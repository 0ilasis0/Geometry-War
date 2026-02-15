import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    ext_path = str(Path(sys.executable).parent)
    if ext_path not in sys.path:
        sys.path.insert(0, ext_path)

import py.init
import py.input.mouse.interaction
import pygame
from py.base import central_mg
from py.debug import dbg, simple_pro
from py.input.keyboard.manager import keyboard_mg
from py.input.mouse.manager import mouse_mg
from py.interrupt import main_interrupt
from py.page.main import main_page
from py.rendering.manager import render_mg
from py.screen.main import submit_static_img
from py.screen.reload_screen import reload_sys_window_scale

while central_mg.running:
    # 觀看fps
    if dbg.enable:
        simple_pro.start_frame()
        simple_pro.end_frame_and_report()

    # 事件處理，包含鍵盤中斷以及內部設定中斷
    for event in pygame.event.get():
        central_mg.leave_game(event)    # 檢查全局退出
        keyboard_mg.execute_key(event)  # 鍵盤按鍵檢查
        mouse_mg.handle_event(event)    # 滑鼠觸發檢查
        main_interrupt(event)

    # 更新時間
    central_mg.update_clock()
    # 決定是否載入新比例的螢幕
    reload_sys_window_scale()

    submit_static_img()

    main_page()

    render_mg.render_all()

    pygame.display.flip()  # 更新整個畫面

pygame.quit()
sys.exit()
