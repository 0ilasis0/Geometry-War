from typing import TYPE_CHECKING

import pygame
from py.debug import dbg
from py.game.slection import selection_mg
from py.game.variable import GameType
from py.input.mouse.inter_sta_mg import inter_sta_mg
from py.input.mouse.register import MouseRegistry
from py.rendering.proxy import render_proxy
from py.variable import PageTable

if TYPE_CHECKING:
    from py.game.building.manager import BuildingManager
    from py.page.base import PageManager


class MouseManager:
    def __init__(self):
        self.page_mg: "PageManager" = None
        self.building_mg: "BuildingManager" = None

        # 滑鼠下的 ui,building last 儲存
        self._hovered_ui = None
        self._hovered_building = None

        # 拖曳狀態
        self._is_dragging = False
        self._drag_start_pos = None
        self._drag_start_building = None  # 起始建築

    def setup(self, page_mg, building_mg):
        """ 依賴注入 """
        self.page_mg = page_mg
        self.building_mg = building_mg

    def handle_event(self, event):
        """ 接收 Pygame 事件的統一入口 """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # 左鍵
                self._on_left_down(event.pos)
            elif event.button == 3: # 右鍵
                self._on_right_click(event.pos)

        elif event.type == pygame.MOUSEMOTION:
            self._on_mouse_move(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP: # 處理放開
            if event.button == 1: # 左鍵
                self._on_left_up(event.pos)

    def _on_left_down(self, pos: tuple[int, int]):
        current_page = self.page_mg.current_page

        # --- UI 攔截 ---
        clicked_ui = render_proxy.get_clicked_item(pos)
        if clicked_ui:
            dbg.log(f'{clicked_ui}')
            is_handled = MouseRegistry.execute_ui(clicked_ui.name)
            if is_handled: return

        # --- 遊戲建築點擊 ---
        if current_page == PageTable.SINGLE:
            clicked_building = self.building_mg.get_building_from_pixel(pos)
            if clicked_building:
                # 記錄起始點，準備開始拖曳
                self._is_dragging = True
                self._drag_start_building = clicked_building
                self._drag_start_pos = pos
                MouseRegistry.execute_world(clicked_building)
            else:
                self._is_dragging = False
                self._drag_start_building = None
                MouseRegistry.execute_world(None)

    def _on_left_up(self, pos: tuple[int, int]):
        """ 放開左鍵：結算操作 """
        if not self._is_dragging: return

        self._is_dragging = False
        target_building = self.building_mg.get_building_from_pixel(pos)

        # 如果是多選狀態 (有拖曳到其他建築)
        if target_building:
            # 多選派遣 (拖曳選了多個 -> 放開在某個建築上)
            if selection_mg.is_multi_select:
                inter_sta_mg.handle_multi_dispatch(target_building)

            # 單體拖曳派遣 (A -> 拉到 -> B)
            elif target_building != self._drag_start_building:
                inter_sta_mg.handle_multi_dispatch(target_building)

        else:
            selection_mg.deselect()

        self._drag_start_building = None

    def _on_right_click(self, pos: tuple[int, int]):
        """ 右鍵邏輯 (例如取消操作) """
        if inter_sta_mg.cancel(): return
        MouseRegistry.execute_world(None)

    def _on_mouse_move(self, pos: tuple[int, int]):
        """ 滑鼠移動時的邏輯 """
        current_page = self.page_mg.current_page
        # current_ui = render_proxy.get_clicked_item(pos)

        # if current_ui != self._hovered_ui:
        #     if self._hovered_ui:
        #         pass
        #     if current_ui:
        #         pass
        #     self._hovered_ui = current_ui

        # # 如果滑鼠在 UI 上，通常會阻擋對遊戲世界的 Hover (防止透視)
        # if current_ui:
        #     # 如果之前有指著建築，要強制 Exit
        #     if self._hovered_building:
        #         MouseRegistry.execute_building_hover(self._hovered_building, is_enter = False)
        #         self._hovered_building = None
        #     return


        # --- 遊戲世界 Hover 處理 ---
        if current_page == PageTable.SINGLE:
            current_building = self.building_mg.get_building_from_pixel(pos)

            if current_building != self._hovered_building:

                # 舊的 -> 離開
                if self._hovered_building:
                    MouseRegistry.execute_building_hover(self._hovered_building, is_enter = False)

                # 新的 -> 進入
                if current_building:
                    MouseRegistry.execute_building_hover(current_building, is_enter = True)

                # 更新記憶
                self._hovered_building = current_building

        if self._is_dragging and self._drag_start_building:
            current_building = self.building_mg.get_building_from_pixel(pos)
            if current_building and current_building != self._drag_start_building:
                if current_building.stats.owner == GameType.Owner.PLAYER:
                    selection_mg.add_to_selection(current_building)

mouse_mg = MouseManager()
