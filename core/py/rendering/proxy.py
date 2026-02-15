from operator import itemgetter
from typing import TYPE_CHECKING, Callable, List, Tuple

import pygame
from py.debug import dbg
from py.rendering.manager import render_mg

if TYPE_CHECKING:
    from py.ui_layout.variable import LayoutItem


class RenderProxy:
    # 儲存結構: (z_index, rect, layout_item)
    _active_click_zones: List[Tuple[int, pygame.Rect, "LayoutItem"]] = []

    @classmethod
    def reset_frame(cls):
        """ 清空上一幀的點擊區域 """
        cls._active_click_zones.clear()

    @classmethod
    def submit(
        cls,
        z_index: int,
        draw_func: Callable,
        *args,
        layout_item: "LayoutItem | None" = None,
        hit_rect: pygame.Rect | None = None,
        is_circle: bool = False,
        **kwargs
    ):
        """
        統一繪製入口
        """
       # 註冊點擊區域
        if layout_item and hit_rect:
            radius_sq = 0.0
            if is_circle:
                # 假設 hit_rect 是外接矩形，半徑 = 寬 / 2
                r = hit_rect.width / 2
                radius_sq = r * r

            cls._active_click_zones.append((z_index, hit_rect, layout_item, is_circle, radius_sq))

        # 轉發繪圖
        render_mg.add_task(z_index, draw_func, *args, **kwargs)

    @classmethod
    def get_clicked_item(cls, mouse_pos: Tuple[int, int]) -> "LayoutItem | None":
        if not cls._active_click_zones: return None

        sorted_zones = sorted(cls._active_click_zones, key = itemgetter(0))
        mx, my = mouse_pos

        # dbg.log(f"--- Click Test at {mouse_pos} | Total Zones: {len(sorted_zones)}:{sorted_zones} ---")

        for _, rect, item, is_circle, radius_sq in reversed(sorted_zones):
            if not rect.collidepoint(mouse_pos): continue

            # 如果是矩形，上面通過了就代表中了
            if not is_circle:
                return item

            # 如果是圓形，做進一步精確檢查 (距離平方公式)
            else:
                # 圓心座標 (假設 rect 是置中的)
                cx, cy = rect.centerx, rect.centery
                dist_sq = (mx - cx)**2 + (my - cy)**2

                if dist_sq <= radius_sq:
                    return item

        return None

render_proxy = RenderProxy
