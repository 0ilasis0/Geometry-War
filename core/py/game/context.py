from typing import TYPE_CHECKING

# 只在型別檢查時成立，在程式實際執行時永遠是 False
if TYPE_CHECKING:
    from py.game.building.manager import BuildingManager
    from py.game.bullet.manager import BulletManager
    from py.game.faction.manager import FactionManager
    from py.game.jelly.manager import ArmyManager
    from py.game.map.grid_converter import GridConverter
    from py.game.map.world_map import GameWorldMap
    from py.variable import PageTable

class GameContext:
    """
    這是一個全域的資源存取點 (Service Locator)。
    由 GameManager 初始化後填入，供底層 Logic 讀取。
    """
    faction_mg: "FactionManager" = None
    building_mg:  "BuildingManager" = None
    bullet_mg: "BulletManager" = None
    army_mg: "ArmyManager" = None
    grid_cvt: "GridConverter" = None
    world_map: "GameWorldMap" = None
    page: "PageTable" = None
    level: int = None

    @classmethod
    def reset(cls):
        """ 清空資源 (換關卡或重啟時用) """
        cls.faction_mg = None
        cls.building_mg = None
        cls.bullet_mg = None
        cls.army_mg = None
        cls.grid_cvt = None
        cls.world_map = None
        cls.page = None
        cls.level = None

    @classmethod
    def map_tag(cls) -> str:
        """
        取得當前的 A* 地圖標籤
        格式範例: "L1_V0", "L1_V5"
        當這字串改變時，A* Manager 會自動知道要重新建立物理緩存
        """
        if not cls.world_map:
            return f"L{cls.level}_V0"

        return f"L{cls.level}_V{cls.world_map.version}"
