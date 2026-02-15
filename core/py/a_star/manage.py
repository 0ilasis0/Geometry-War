from py.debug import dbg
from py.trans.a_star import AStarInterface
from py.trans.base import CInterfaceBase
from py.trans.variable import VarConfig
from py.variable import GridPoint


class ManageAStar():
    def __init__(self) -> None:
        self.last_map_name = None
        self.width = 0
        self.height = 0

        # 存 C 的指標
        self.c_map = None
        # 存 C 的結果 buffer
        self.out_buffer = None

        self.store_paths = {}

        # AStarInterface 實體
        self.inf = None

    def setup(self):
        try:
            self.inf = AStarInterface()
        except Exception as e:
            dbg.error("a_star 初始化失敗:", e)

    def update_map_from_grid_data(self, grid_data, map_name_tag: str):
        """
        直接從 GridMapData 讀取 1D 物理碰撞表
        grid_data: GridMapData 實體
        map_name_tag: 地圖版本標籤 (例如 "Level_1_v5")
        """
        # 檢查快取：如果地圖版本沒變，就不需要重新 allocate 記憶體
        if self.last_map_name == map_name_tag: return

        self.clear_cache()

        self.last_map_name = map_name_tag
        self.width = grid_data.width
        self.height = grid_data.height

        self.c_map = CInterfaceBase.list_to_c_array(
            grid_data.collision_map,
            VarConfig.A_STAR_POINT.value
        )

        # 重設輸出 Buffer (大小 = 寬 * 高 * 2 (存 x, y))
        total_size = self.width * self.height
        self.out_buffer = (VarConfig.A_STAR_OUT_BUFFER.value * (total_size * 2))()

        dbg.log(f"[A*] Map updated to: {map_name_tag} ({self.width}x{self.height})")

    def clear_cache(self):
        """ 清空所有已儲存的路徑 """
        if not self.store_paths: return
        self.store_paths.clear()

a_star_mg = ManageAStar()
