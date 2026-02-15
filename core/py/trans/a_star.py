import ctypes

from py.path.manager import PathConfig
from py.trans.base import CInterfaceBase
from py.trans.variable import FunctionName, VarConfig
from py.variable import GridPoint


class AStarInterface(CInterfaceBase):
    def __init__(self):
        super().__init__(PathConfig.a_star.dll, FunctionName.SOLVE_A_STAR.value)

        # --- 設定 A* 函式傳入/回傳參數規格 ---
        self.c_func.argtypes = [
            ctypes.POINTER(VarConfig.A_STAR_MAP.value),
            VarConfig.A_STAR_W_H.value, VarConfig.A_STAR_W_H.value,
            VarConfig.A_STAR_POINT.value, VarConfig.A_STAR_POINT.value,
            VarConfig.A_STAR_POINT.value, VarConfig.A_STAR_POINT.value,
            ctypes.POINTER(VarConfig.A_STAR_OUT_BUFFER.value),
        ]
        self.c_func.restype = VarConfig.A_STAR_REBACK.value

    def find_path(self, a_star_mg, start: GridPoint, end: GridPoint):
        # 呼叫前請確保 a_star_mg.c_map 與 out_buffer 已初始化
        steps = self.c_func(
            ctypes.cast(a_star_mg.c_map, ctypes.POINTER(VarConfig.A_STAR_MAP.value)),
            a_star_mg.width, a_star_mg.height,
            start.col, start.row,
            end.col, end.row,
            ctypes.cast(a_star_mg.out_buffer, ctypes.POINTER(VarConfig.A_STAR_OUT_BUFFER.value)),
        )

        if steps < 0: return []

        # 解析回傳
        path = []
        for i in range(steps):
            # C 回傳格式: [x0, y0, x1, y1...]
            path.append((a_star_mg.out_buffer[i * 2], a_star_mg.out_buffer[i * 2 + 1]))
        return path
