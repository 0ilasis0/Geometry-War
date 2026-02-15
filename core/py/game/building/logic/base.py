from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py.game.building.entity import BuildingEntity

class BuildingLogic(ABC):
    def __init__(self, building: "BuildingEntity"):
        self.building = building  # 持有建築實體引用

    @abstractmethod
    def update(self, dt: float):
        """ 每幀執行的逻辑 """
        pass
