from py.hmi.base import HMIBaseManager
from py.variable import PageTable


class SingleHmiManager(HMIBaseManager):
    """
    [Controller] 遊戲頁面的控制器
    職責：接收鍵盤指令，轉發給 TetrisCore (Player) 執行動作
    """
    def __init__(self, base_nav):
        # 繼承 Base，這樣 KeyboardManager 才能通用地呼叫 on_up/on_down...
        super().__init__(base_nav, PageTable.SINGLE)
