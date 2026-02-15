import ctypes

from py.debug import dbg
from py.trans.variable import VarConfig


class CInterfaceBase:
    def __init__(self, full_path, func_name):
        """
        通用載入器
        載入 C Shared Library (.dll)
        """
        try:
            self.lib = ctypes.CDLL(full_path)
            # 將c 函式抓出來
            self.c_func = getattr(self.lib, func_name)
            dbg.log(f"[系統] 成功載入 C 模組: {full_path}")
        except OSError as e:
            dbg.error(f"無法載入路徑", e)
            raise

    @staticmethod
    def list_to_c_array(py_list, data_form = VarConfig.BASE):
        """
        通用的 List 轉 C Array 工具
        先分配需要的記憶體大小，在將指標內的資料輸入
        """
        return (data_form * len(py_list))(*py_list)
