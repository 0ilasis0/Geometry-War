from typing import Any, Callable

from py.debug import dbg
from py.game.variable import GameType
from py.input.mouse.variable import IHoverHandler
from py.ui_layout.name.identifiers import LayoutName


class MouseRegistry:
    """
    負責儲存 UI 名稱與對應函式 (Callback) 的關係。
    """
    # 儲存 UI 點擊事件
    _UI_CLICK_MAP: dict[LayoutName, Callable] = {}

    # 儲存遊戲世界點擊處理器
    _BUILDING_HANDLERS: dict[GameType.Arch | None, Callable] = {}

    # 儲存 滑鼠移動事件
    _BUILDING_HOVER_HANDLERS: dict[GameType.Arch | None, tuple[Callable, Callable]] = {}

    @classmethod
    def register_ui(cls, layout_name: LayoutName):
        """ [裝飾器] 用來將函式註冊到特定的 UI 按鈕上 """
        def decorator(func: Callable):
            if layout_name in cls._UI_CLICK_MAP:
                dbg.war(f"[MouseRegistry] Overwriting handler for {layout_name}")

            cls._UI_CLICK_MAP[layout_name] = func
            return func
        return decorator

    @classmethod
    def register_building(cls, arch_type: GameType.Arch | None):
        """ [裝飾器] 針對「特定種類」的建築註冊點擊行為 """
        def decorator(func: Callable):
            if arch_type in cls._BUILDING_HANDLERS:
                dbg.war(f"[MouseRegistry] Overwriting handler for {arch_type}")

            cls._BUILDING_HANDLERS[arch_type] = func
            return func
        return decorator

    @classmethod
    def register_building_hover(cls, arch_type: GameType.Arch | None):
        """ [裝飾器] 註冊建築的 Hover 行為 (Enter, Exit) """
        def decorator(handler_cls: type[IHoverHandler]):
            if arch_type in cls._BUILDING_HOVER_HANDLERS:
                dbg.war(f"[MouseRegistry] Overwriting handler for {arch_type}")

            cls._BUILDING_HOVER_HANDLERS[arch_type] = handler_cls()
            return handler_cls
        return decorator

    @classmethod
    def execute_ui(cls, layout_name: LayoutName) -> bool:
        """ 執行 UI 對應的函式，若有執行回傳 True """
        handlers = cls._UI_CLICK_MAP.get(layout_name, None)

        if not handlers: return False

        try:
            handlers()
            return True
        except Exception as e:
            dbg.error(f"[MouseRegistry] Error executing {layout_name}: {e}")
        return False

    @classmethod
    def execute_world(cls, building_entity: GameType.Arch | None):
        """
        根據傳入的建築物件，自動判斷要呼叫哪個函式
        """
        arch = building_entity.stats.arch if building_entity else None

        if arch in cls._BUILDING_HANDLERS:
            handler = cls._BUILDING_HANDLERS[arch]
        else:
            handler = cls._BUILDING_HANDLERS.get(None)

        if not handler: None

        handler(building_entity)

    @classmethod
    def execute_building_hover(cls, building_entity: GameType.Arch, is_enter: bool):
        """
        執行 Hover 邏輯
        :param is_enter: True 為移入，False 為移出
        """
        arch = building_entity.stats.arch

        if arch in cls._BUILDING_HOVER_HANDLERS:
            handler = cls._BUILDING_HOVER_HANDLERS.get(arch)
        else:
            handler = cls._BUILDING_HOVER_HANDLERS.get(None)

        if not handler: return

        if is_enter:
            handler.on_enter(building_entity)
        else:
            handler.on_exit(building_entity)
