from py.game.variable import GridParamsType
from py.variable import GridPoint, Position, Size


class GridConverter:
    def __init__(self, start_x, start_y, cell_width, cell_height):
        self.update_params(start_x, start_y, cell_width, cell_height)
        # 用來裝過去網格位置的資料
        self.old_grid_params: dict | None = None

    def update_params(self, origin_x, origin_y, cell_width, cell_height):
        """ 當視窗縮放時，重新設定網格參數 """
        try:
            self.old_grid_params = {
                GridParamsType.ORIGIN_X: self.origin_x,
                GridParamsType.ORIGIN_Y: self.origin_y,
                GridParamsType.CELL_W:   self.cell_w,
                GridParamsType.CELL_H:   self.cell_h
            }
        except AttributeError:
            self.old_grid_params = {
                GridParamsType.ORIGIN_X: origin_x,
                GridParamsType.ORIGIN_Y: origin_y,
                GridParamsType.CELL_W:   cell_width,
                GridParamsType.CELL_H:   cell_height
            }

        self.origin_x = origin_x
        self.origin_y = origin_y
        self.cell_w = cell_width
        self.cell_h = cell_height

    def get_block_rect(self, grid_pos: GridPoint, grid_span: Size) -> tuple[Position, Size]:
        """
        計算多格建築物的 (螢幕座標, 螢幕大小)
        grid_pos: 左上角的網格座標
        grid_span: 佔用幾格 (例如 2x2)
        """
        # 計算左上角像素位置
        px_start = self.origin_x + grid_pos.col * self.cell_w
        py_start = self.origin_y + grid_pos.row * self.cell_h

        # 計算總像素大小
        total_w = self.cell_w * grid_span.width
        total_h = self.cell_h * grid_span.height

        return (
            Position(int(px_start), int(py_start), 0),
            Size(round(total_w), round(total_h))
        )

    def calc_virtual_grid(self, pixel_pos: Position) -> tuple[float, float]:
        """
        根據給定的網格參數，將像素逆推回虛擬網格 (Float)
        這可以避免外部程式碼一直重複寫 (x - ox) / cw 這種公式
        """
        ox = self.old_grid_params.get(GridParamsType.ORIGIN_X)
        oy = self.old_grid_params.get(GridParamsType.ORIGIN_Y)
        cw = self.old_grid_params.get(GridParamsType.CELL_W)
        ch = self.old_grid_params.get(GridParamsType.CELL_H)

        v_col = (pixel_pos.x - ox) / cw
        v_row = (pixel_pos.y - oy) / ch
        return v_col, v_row

    def pos_to_grid(self, pos: Position) -> GridPoint:
        """ 將點擊座標轉回網格索引 """
        col = int((pos.x - self.origin_x) // self.cell_w)
        row = int((pos.y - self.origin_y) // self.cell_h)
        return GridPoint(col, row)

    def grid_to_pos(self, grid_point: GridPoint) -> Position:
        """ 支援小數點的網格轉像素 """
        px = self.origin_x + grid_point.col * self.cell_w
        py = self.origin_y + grid_point.row * self.cell_h
        return Position(px, py, 0)

    def grid_to_size(self, old_size: Size) -> Size:
        """ 同時轉換寬高為像素長度 """
        return Size(self.col_to_px(old_size.width), self.row_to_py(old_size.height))

    def get_pixel_center(self, grid: GridPoint) -> Position:
        """
        取得指定網格的中心點像素座標
        """
        # 計算左上角
        top_left_x = self.origin_x + grid.col * self.cell_w
        top_left_y = self.origin_y + grid.row * self.cell_h

        # 加上半個格子的寬高
        center_x = top_left_x + (self.cell_w / 2)
        center_y = top_left_y + (self.cell_h / 2)

        return Position(center_x, center_y, 0)

    def get_block_center(self, grid_point: GridPoint, grid_span: Size, pos_z: int = 0) -> Position:
        """
        計算某個格位(或佔地範圍)的螢幕中心點
        """
        # 先取得左上角座標與大小 (利用現有的函式)
        top_left_pos, size = self.get_block_rect(grid_point, grid_span)

        # 計算中心
        center_x = top_left_pos.x + (size.width / 2)
        center_y = top_left_pos.y + (size.height / 2)

        return Position(center_x, center_y, pos_z)

    def px_to_col(self, px_len: float) -> float:
        return px_len / self.cell_w

    def py_to_row(self, py_len: float) -> float:
        return py_len / self.cell_h

    def col_to_px(self, col: float) -> float:
        """ 將網格寬度轉換為像素長度 """
        return col * self.cell_w

    def row_to_py(self, row: float) -> float:
        """ 將網格高度轉換為像素長度 """
        return row * self.cell_h

    def is_valid_grid(self, grid: GridPoint, max_x: int, max_y: int) -> bool:
        """ (選用) 檢查座標是否在合法地圖範圍內 """
        return 0 <= grid.col < max_x and 0 <= grid.row < max_y
