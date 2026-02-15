import array
from typing import Iterator

from py.game.map.variable import GridMapMarking
from py.variable import GridPoint, Size


class GameWorldMap:
    def __init__(self, cols: int, rows: int):
        self.width: int = cols
        self.height: int = rows

        # 佔用該格的物件(給 Python 用，邏輯層)
        self.occupation: dict[GridPoint, object] = {}
        # 佔用該格的物件(給 C 用，物理層)
        # 使用 array ('b' 代表 有號 1 byte 整數)，極省記憶體且連續
        self.collision_map = array.array('b', [0] * (cols * rows))

        self.version: int = 0

    def reload_setup(self, cols: int, rows: int):
        self.width = cols
        self.height = rows
        self.occupation.clear()
        self.collision_map = array.array('b', [0] * (cols * rows))

    def is_area_free(self, start_grid: GridPoint, size: Size, ignore_obj = None) -> bool:
        """
        檢查一塊區域是否完全沒被佔用
        ignore_obj: 移動建築時，忽略自己原本佔用的格子
        """
        # 這裡使用 generator，迴圈跑到一半發現不行就會立刻停，不會浪費時間算後面的格子
        for cell in self._iter_cells(start_grid, size):
            if not self._is_within_bounds(cell):
                return False

            obj = self.occupation.get((cell.col, cell.row))

            if obj is not None and obj != ignore_obj:
                return False
        return True

    def register_object(self, obj: object, start_grid: GridPoint, size: Size):
        """ 註冊物件：同時更新 Dict 和 List """
        for cell in self._iter_cells(start_grid, size):
            if self._is_within_bounds(cell):
                # 邏輯層
                self.occupation[(cell.col, cell.row)] = obj
                # 物理層
                idx = self._get_idx(cell)
                self.collision_map[idx] = GridMapMarking.WALL

        self.version += 1

    def unregister_object(self, start_grid: GridPoint, size: Size):
        """ 移除物件：同時更新 Dict 和 List """
        for cell in self._iter_cells(start_grid, size):
            if self._is_within_bounds(cell):
                # 邏輯層 (使用 pop 安全移除，若 key 不在也不會報錯)
                self.occupation.pop((cell.col, cell.row), None)

                # 物理層
                idx = self._get_idx(cell)
                self.collision_map[idx] = GridMapMarking.VACUITY

        self.version += 1

    def get_object_at(self, grid: GridPoint) -> object | None:
        """ 查詢該格子上是誰 """
        return self.occupation.get((grid.col, grid.row))

    def get_access_point(self, building_grid: GridPoint, size: Size, target_grid: GridPoint) -> GridPoint | None:
        """
        [取得出入口]
        尋找建築物 "周圍一圈" 的空格，並回傳距離目標最近的那一格。
        解決建築物體積導致 A* 起點被牆壁包圍的問題。
        """

        # 找出建築物邊緣的所有候選格子
        candidates = []

        # 建築物範圍: [col, row] 到 [col + w, row + h]
        start_c, start_r = int(building_grid.col), int(building_grid.row)
        w, h = size.width, size.height

        # 掃描上下邊緣 (含角落)
        for c in range(start_c - 1, start_c + w + 1):
            candidates.append(GridPoint(c, start_r - 1))     # 上邊緣
            candidates.append(GridPoint(c, start_r + h))     # 下邊緣

        # 掃描左右邊緣 (不含已掃過的角)
        for r in range(start_r, start_r + h):
            candidates.append(GridPoint(start_c - 1, r))     # 左邊緣
            candidates.append(GridPoint(start_c + w, r))     # 右邊緣

        # 過濾出合法的格子 (在地圖內 且 不是牆壁)
        valid_points = []
        for p in candidates:
            if not self._is_within_bounds(p): continue

            # 檢查是否為牆壁 (注意：這裡直接查 collision_map)
            idx = self._get_idx(p)
            if self.collision_map[idx] == 0: # 0 代表路
                valid_points.append(p)

        if not valid_points:
            return None # 建築物被完全包圍了

        # 找出距離目標最近的那個點 (曼哈頓距離)
        best_point = None
        min_dist = float('inf')

        for p in valid_points:
            dist = abs(p.col - target_grid.col) + abs(p.row - target_grid.row)
            if dist < min_dist:
                min_dist = dist
                best_point = p

        return best_point

    def clear(self):
        self.occupation.clear()
        self.collision_map = array.array('b', [0] * (self.width * self.height))

        self.version = 0

    def _is_within_bounds(self, grid: GridPoint) -> bool:
        """ 檢查座標是否在地圖範圍內 """
        return 0 <= grid.col < self.width and 0 <= grid.row < self.height

    def _iter_cells(self, start: GridPoint, size: Size) -> Iterator[GridPoint]:
        """ 使用 yield 產生器，避免建立大量暫存 list """
        for c in range(size.width):
            for r in range(size.height):
                yield GridPoint(start.col + c, start.row + r)

    def _get_cells(self, start: GridPoint, size: Size) -> list[GridPoint]:
        """ 取得矩形範圍內的所有格子 """
        cells = []
        for c in range(size.width):
            for r in range(size.height):
                cells.append(GridPoint(start.col + c, start.row + r))
        return cells

    def _get_idx(self, grid: GridPoint) -> int:
        """ 將 2D 座標轉為 1D 索引 """
        return grid.row * self.width + grid.col
