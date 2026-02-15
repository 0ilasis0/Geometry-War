from typing import TYPE_CHECKING, List

import pygame
from py.debug import dbg
from py.game.context import GameContext
from py.game.obstacle.preset import LEVEL_CONFIG_MAP
from py.game.obstacle.variable import ObstacleEntity, ObstacleSpawnData
from py.screen.image.manager.core import img_mg
from py.screen.image.preset import IMAGE_RESOURCE_MAP
from py.ui_layout.main import layout_mg
from py.ui_layout.variable import PosZLayer
from py.variable import GridPoint, Position, Size

if TYPE_CHECKING:
    from py.game.map.world_map import GameWorldMap


class ObstacleManager:
    def __init__(
        self,
        world_map: "GameWorldMap",
    ):
        self.world_map = world_map
        self.obstacles: List[ObstacleEntity] = []

        self.cvt = None
        self.cell_mask = None

    # =========================================================================
    # 公開介面：關卡載入與卸載
    # =========================================================================

    def _ensure_resources(self):
        """ 確保依賴資源已初始化 (Lazy Load) """
        self.cvt = GameContext.grid_cvt

        # 建立格子 Mask
        if self.cell_mask is None and self.cvt is not None:
            cell_w, cell_h = int(self.cvt.cell_w), int(self.cvt.cell_h)
            self.cell_mask = pygame.mask.Mask((cell_w, cell_h))
            self.cell_mask.fill()

    def load_level(self, level: int):
        """ 載入指定關卡的所有障礙物 """
        self._ensure_resources()
        self.clear()

        config_page = LEVEL_CONFIG_MAP.get(GameContext.page)
        if not config_page:
            dbg.war(f"[Obstacle] No config found for page: {GameContext.page}")
            return

        config_level = config_page.get(level)
        if not config_level:
            dbg.war(f"[Obstacle] No config found for level: {level}")
            return

        dbg.log(f"[Obstacle] Loading page {GameContext.page} level: {level} with {len(config_level.obstacles)} obstacles.")

        for spawn_data in config_level.obstacles:
            self._create_obstacle_instance(spawn_data)

    def render(self):
        for obs in self.obstacles:
            pixel_pos = GameContext.grid_cvt.grid_to_pos(obs.grid_origin)
            pixel_pos.z = PosZLayer.UI_ELEMENT_1

            img_mg.draw_image_dynamic(
                image_id = obs.layout_item.name,
                pos = pixel_pos,
            )

    def clear(self):
        """ 清除所有障礙物 """
        if not self.obstacles: return

        count = 0
        for obs in self.obstacles:
            for grid in obs.occupied_cells:
                self.world_map.unregister_object(grid, Size(1, 1))
            count += len(obs.occupied_cells)

        self.obstacles.clear()

    # =========================================================================
    # 內部邏輯：實例化與像素掃描
    # =========================================================================

    def _create_obstacle_instance(self, data: ObstacleSpawnData):
        """ 根據生成資料 (位置 + 種類) 創建實體 """
        layout_name = data.layout_name

        item = layout_mg.get_item(GameContext.page, layout_name)
        if not item:
            dbg.war(f"[Obstacle] LayoutItem '{layout_name}' not found in {GameContext.page}.")
            return

        profile = IMAGE_RESOURCE_MAP.get(layout_name)
        if not profile:
            key = item.name if item.name in IMAGE_RESOURCE_MAP else item.img_id
            profile = IMAGE_RESOURCE_MAP.get(key)
        if not profile:
            dbg.war(f"[Obstacle] ImageProfile not found for '{layout_name}'")
            return

        surface = img_mg.get_processed_surface(profile, item.size)
        if not surface: return

        obs_mask = pygame.mask.from_surface(surface)

        target_pixel_pos = self.cvt.grid_to_pos(data.grid_pos)
        center_x = target_pixel_pos.x + item.size.width / 2
        center_y = target_pixel_pos.y + item.size.height / 2

        img_rect = surface.get_rect()
        img_rect.center = (center_x, center_y)

        ox, oy = self.cvt.origin_x, self.cvt.origin_y

        start_col = int((img_rect.left - ox) / self.cvt.cell_w)
        start_row = int((img_rect.top - oy) / self.cvt.cell_h)
        end_col = int((img_rect.right - ox) / self.cvt.cell_w) + 1
        end_row = int((img_rect.bottom - oy) / self.cvt.cell_h) + 1

        # 邊界限制
        start_col = max(0, start_col)
        start_row = max(0, start_row)
        end_col = min(self.world_map.width, end_col)
        end_row = min(self.world_map.height, end_row)

        occupied_cells = []

        # 掃描
        for c in range(start_col, end_col):
            for r in range(start_row, end_row):
                grid = GridPoint(c, r)

                cell_top_left = self.cvt.grid_to_pos(grid)

                # 計算相對偏移量: 格子相對於圖片的位置
                offset_x = int(cell_top_left.x - img_rect.left)
                offset_y = int(cell_top_left.y - img_rect.top)

                # 檢查重疊
                if obs_mask.overlap(self.cell_mask, (offset_x, offset_y)):
                    occupied_cells.append(grid)

        if not occupied_cells:
            dbg.war(f"[Obstacle] No cells occupied for {layout_name} (Mask Miss).")
            return

        # 註冊實體
        obstacle_entity = ObstacleEntity(
            layout_item = item,
            grid_origin = data.grid_pos,
            occupied_cells = occupied_cells
        )

        for grid in occupied_cells:
            self.world_map.register_object(obstacle_entity, grid, Size(1, 1))

        self.obstacles.append(obstacle_entity)
