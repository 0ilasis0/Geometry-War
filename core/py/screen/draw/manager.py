import pygame
from py.base import central_mg
from py.debug import dbg
from py.rendering.proxy import render_proxy
from py.screen.draw.preset import DrawID
from py.screen.draw.variable import DrawProfile, DrawShape
from py.ui_layout.main import layout_mg
from py.variable import BOOT_PAGE, PageTable, Position, Size


class DrawManager():
    def __init__(self):
        self.draw_static_maps = {}          # 靜態畫布儲存map

        self.current_page = BOOT_PAGE

    def submit_static(self):
        """
        將 Setup 階段存好的靜態物件，提交給 RenderManager
        """
        if self.current_page not in self.draw_static_maps:
            return

        for form in self.draw_static_maps[self.current_page]:
            # 取出預先存好的 item (用於點擊判定)
            layout_item = form.get("item", None)
            z = form.get("z", 0) # 取出儲存的 Z 軸

            if form["shape"] == DrawShape.RECT:
                rect = pygame.Rect(form["place_x"], form["place_y"], form["size_x"], form["size_y"])
                render_proxy.submit(
                    z_index = z,
                    draw_func = pygame.draw.rect,
                    layout_item = layout_item,
                    hit_rect = rect,
                    surface = central_mg.current_window,
                    color = form["color"],
                    rect = rect,
                    width = form["hollow"]
                )

            elif form["shape"] == DrawShape.CIRCLE:
                cx, cy = form["place_x"], form["place_y"]
                radius = form["size_x"]
                hit_rect = pygame.Rect(cx - radius, cy - radius, radius * 2, radius * 2)

                render_proxy.submit(
                    z_index = z,
                    draw_func = pygame.draw.circle,
                    layout_item = layout_item,
                    hit_rect = hit_rect,
                    is_circle = True,
                    surface = central_mg.current_window,
                    color = form["color"],
                    center = (cx, cy),
                    radius = radius,
                    width=form["hollow"]
                )

    def add_form(
            self,
            draw_id: DrawID,
            fixed = False,
            layout_name = None,
            override_pos: Position = None,
            offset_pos: Position = Position(0, 0, 0),
            override_size: Size = None,
            override_color = None
        ):
        # (防呆)
        try:
            profile = draw_id.value
        except AttributeError:
            dbg.error(f'{draw_id} is not a valid DrawID Enum')
            return

        # 取得目標 LayoutItem
        target_name = layout_name if layout_name is not None else profile.name
        item = self._get_item_safely(target_name)

        # 決定位置
        target_pos = override_pos if override_pos is not None else (item.pos if item else None)
        if target_pos is None: return

        final_color = override_color if override_color is not None else profile.color
        if final_color is None: return

        # 決定大小
        if override_size:
            width = round(override_size.width)
            height = round(override_size.height)
        elif item:
            width = round(item.size.width)
            height = round(item.size.height)
        else: return

        # 提取基礎參數
        raw_x = round(target_pos.x + offset_pos.x)
        raw_y = round(target_pos.y + offset_pos.y)
        z_index = item.pos.z
        hollow = profile.hollow

        final_x = raw_x
        final_y = raw_y
        final_w = width
        final_h = height
        # 如果是圓形，進行「左上角 -> 圓心」與「直徑 -> 半徑」的轉換
        if profile.shape == DrawShape.CIRCLE:
            radius = width // 2 if width > 0 else 0

            final_x = raw_x + radius
            final_y = raw_y + radius
            final_w = radius
            final_h = radius

        # --- 靜態模式：存入緩存 ---
        if fixed:
            static_list = self.draw_static_maps.setdefault(self.current_page, [])

            # 這裡存進去的是已經校正過的「圓心」與「半徑」
            static_list.append({
                "name": profile.name,
                "z": z_index,
                "item": item,
                "shape": profile.shape,
                "place_x": final_x,   # Rect是左上角，Circle是圓心
                "place_y": final_y,
                "size_x": final_w,    # Rect是寬，Circle是半徑
                "size_y": final_h,    # Rect是高
                "color": final_color,
                "hollow": hollow
            })

        # --- 動態模式：即時渲染 ---
        else:
            if profile.shape == DrawShape.RECT:
                rect = pygame.Rect(final_x, final_y, final_w, final_h)
                render_proxy.submit(
                    z_index = z_index,
                    draw_func = pygame.draw.rect,
                    layout_item = item,
                    hit_rect = rect,
                    surface = central_mg.current_window,
                    color = final_color,
                    rect = rect,
                    width = hollow
                )

            elif profile.shape == DrawShape.CIRCLE:
                radius = final_w
                hit_rect = pygame.Rect(final_x - radius, final_y - radius, radius * 2, radius * 2)
                render_proxy.submit(
                    z_index = z_index,
                    draw_func = pygame.draw.circle,
                    layout_item = item,
                    hit_rect = hit_rect,
                    surface = central_mg.current_window,
                    color = final_color,
                    center = (final_x, final_y),
                    radius = radius,
                    width = hollow
                )

    def add_grid(
            self,
            draw_id: DrawID,
            fixed = False,
            layout_name = None,
        ):
        try:
            profile: DrawProfile = draw_id.value
        except AttributeError:
            dbg.error(f'{draw_id} is not a valid DrawID Enum')
            return

        target_name = layout_name if layout_name is not None else profile.name
        item = self._get_item_safely(target_name)

        if not item: return

        # 參數準備
        z_index = item.pos.z
        w_blocks = profile.width_block
        h_blocks = profile.height_block
        color = profile.color
        line_thickness = profile.hollow if profile.hollow > 0 else 1
        if profile.zoom is not None:
            zoom = profile.zoom
        elif item and h_blocks > 0:
            zoom = item.size.height / h_blocks
        else:
            dbg.error(f'item is not exisit or profile.hollow is {h_blocks} <= 0')

        start_x = round(item.pos.x)
        start_y = round(item.pos.y)
        total_height = round(h_blocks * zoom)
        total_width = round(w_blocks * zoom)

        # 靜態模式：存入 List
        if fixed:
            if self.current_page not in self.draw_static_maps:
                self.draw_static_maps[self.current_page] = []

            # 垂直線
            for x in range(w_blocks + 1):
                self.draw_static_maps[self.current_page].append({
                    "name": f"{target_name}_vline_{x}",
                    "z": z_index,
                    "item": None,
                    "shape": DrawShape.RECT,
                    "place_x": round(start_x + x * zoom),
                    "place_y": start_y,
                    "size_x": line_thickness,
                    "size_y": total_height,
                    "color": color,
                    "hollow": 0
                })
            # 水平線
            for y in range(h_blocks + 1):
                self.draw_static_maps[self.current_page].append({
                    "name": f"{target_name}_hline_{y}",
                    "z": z_index,
                    "item": None,
                    "shape": DrawShape.RECT,
                    "place_x": start_x,
                    "place_y": round(start_y + y * zoom),
                    "size_x": total_width,
                    "size_y": line_thickness,
                    "color": color,
                    "hollow": 0
                })

        # 動態模式：直接上繳 (雖然網格通常是靜態的，但保留彈性)
        else:
            # 垂直線
            for x in range(w_blocks + 1):
                rect = pygame.Rect(round(start_x + x * zoom), start_y, line_thickness, total_height)
                render_proxy.submit(
                    z_index = z_index,
                    draw_func = pygame.draw.rect,
                    layout_item = None, # 網格不互動
                    hit_rect = None,
                    surface = central_mg.current_window,
                    color = color,
                    rect = rect,
                    width = 0
                )
            # 水平線
            for y in range(h_blocks + 1):
                rect = pygame.Rect(start_x, round(start_y + y * zoom), total_width, line_thickness)
                render_proxy.submit(
                    z_index = z_index,
                    draw_func = pygame.draw.rect,
                    layout_item = None, # 網格不互動
                    hit_rect = None,
                    surface = central_mg.current_window,
                    color = color,
                    rect = rect,
                    width = 0
                )

    def _get_item_safely(self, target_name):
        # 嘗試從當前頁面找
        item = layout_mg.get_item(
            page = self.current_page,
            name = target_name,
            silent = True
        )
        if item: return item

        return None

    ''' 其他工具 '''
    def switch_page(self, page: PageTable):
        self.current_page = page

    def clear_map(self, category):
        """ 清除某頁的某頁靜態畫布 """
        self.draw_static_maps[category] = []

draw_mg = DrawManager()
