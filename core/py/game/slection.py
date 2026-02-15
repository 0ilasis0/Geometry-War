from typing import TYPE_CHECKING, List

from py.game.variable import GameType

if TYPE_CHECKING:
    from py.game.building.entity import BuildingEntity

class SelectionManager:
    def __init__(self):
        self._selected: List["BuildingEntity"] = []

    def update(self, dt: float):
        """
        每幀自動掃描選取列表
        如果建築物被佔領 (Owner 變更) 或死亡，直接從選取列表中移除。
        這樣 UI 和 InteractionManager 就不需要再做額外的防呆檢查。
        """
        if not self._selected: return

        # 過濾邏輯：只保留「擁有者是玩家」的建築
        valid_selection = [
            b for b in self._selected
            if b.stats.owner == GameType.Owner.PLAYER
        ]

        # 如果數量有變化 (代表有建築被踢掉了)，更新列表
        if len(valid_selection) != len(self._selected):
            self._selected = valid_selection

    @property
    def selected_entity(self)-> "BuildingEntity | None":
        """ 取得當前主要選取的建築 (單選時用) """
        return self._selected[0] if self._selected else None

    @property
    def selected_entities(self) -> List["BuildingEntity"]:
        """ 取得所有被選取的建築 (多選時用) """
        return self._selected

    @property
    def is_multi_select(self) -> bool:
        """ 是否處於多選狀態 """
        return len(self._selected) > 1

    def select(self, entity: "BuildingEntity", clear_prev: bool = True):
        """ 選取單一建築 """
        if clear_prev:
            self.deselect()
        if entity not in self._selected:
            self._selected.append(entity)

    def add_to_selection(self, entity: "BuildingEntity"):
        """ 加入多選列表 """
        self.select(entity, clear_prev=False)

    def deselect(self):
        """ 取消選取 """
        self._selected.clear()

selection_mg = SelectionManager()
