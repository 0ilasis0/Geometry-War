from py.debug import dbg
from py.game.building.entity import BuildingEntity
from py.game.building.logic.castle import CastleLogic
from py.game.building.logic.lab import LabLogic
from py.game.building.logic.production import ProductionLogic
from py.game.building.logic.prototype import PrototypeLogic
from py.game.building.logic.upgrade import UpgradeComponent
from py.game.building.variable import BaseStatsData, BuildingStats
from py.game.bullet.variable import BulletVar
from py.game.variable import EntitySpan, GameMaxVar, GameType, GameTypeMap
from py.variable import GridPoint

# --- [註冊系統] ---
BUILDING_REGISTRY = {}

def register_building(building_type):
    def decorator(func):
        BUILDING_REGISTRY[building_type] = func
        return func
    return decorator

class BuildingFactory:
    """
    靜態工廠類別：負責組裝建築實體，以及處理建築變身
    """

    # =========================================================================
    # 配置生成區 (Configuration Generators)
    # 只負責產生數據 (Stats, BaseData, LogicClass)，不負責生成實體
    # =========================================================================

    @staticmethod
    def _get_prototype_config(owner: GameTypeMap, grid_pos: GridPoint, army: int, level: int):
        base_data = BaseStatsData(
            base_army_cap = 10,
        )
        stats = BuildingStats(
            arch = GameType.Arch.PROTOTYPE,
            grid_point = grid_pos,
            owner = owner,
            level = level,
            max_level = GameMaxVar.LEVEL_PROTOTYPE,
            army = army,
            defense = 0.5,
            rate_of_production = 0.2, # 初始生產慢
        )
        return stats, base_data, PrototypeLogic

    @staticmethod
    def _get_production_config(owner: GameTypeMap, grid_pos: GridPoint, army: int, level: int):
        base_data = BaseStatsData(
            base_army_cap = 10,
            prod_rate_base = 0.8,
            prod_rate_growth = 0.3
        )
        stats = BuildingStats(
            arch = GameType.Arch.PRODUCTION,
            grid_point = grid_pos,
            owner = owner,
            level = level,
            max_level = GameMaxVar.LEVEL_PRODUCTION,
            army = army,
        )
        return stats, base_data, ProductionLogic

    @staticmethod
    def _get_castle_config(owner: GameTypeMap, grid_pos: GridPoint, army: int, level: int):
        base_data = BaseStatsData(
            base_army_cap = 20,
            castle_enable = True,
            base_defense = 1.2,
            defence_rate_growth = 0.2,
            base_bullet_damage = 1.2,
            bullet_damage_rate_groth = 0.2,
            base_rate_of_fire = 1.0,
            rate_of_fire_growth = 0.1
        )
        stats = BuildingStats(
            arch = GameType.Arch.CASTLE,
            grid_point = grid_pos,
            owner = owner,
            level = level,
            max_level = GameMaxVar.LEVEL_CASTLE,
            army = army,
            effective_grid_range = EntitySpan.CASTLE_RANGE.width,
            bullet_speed_grid = BulletVar.MOVE_SPEED_GRID.value
        )
        return stats, base_data, CastleLogic

    @staticmethod
    def _get_lab_config(owner: GameTypeMap, grid_pos: GridPoint, army: int, level: int):
        base_data = BaseStatsData(
            base_army_cap = 50,
            jelly_speed_grid_growth = 4
        )
        stats = BuildingStats(
            arch = GameType.Arch.LAB,
            grid_point = grid_pos,
            owner = owner,
            level = level,
            max_level = GameMaxVar.LEVEL_LAB,
            army = army,
        )
        return stats, base_data, LabLogic

    # =========================================================================
    # 實體創建區 (Builders)
    # 呼叫配置生成器，並組裝 new BuildingEntity
    # =========================================================================

    @staticmethod
    @register_building(GameType.Arch.PROTOTYPE)
    def build_prototype(owner: GameTypeMap, grid_pos: GridPoint, army: int = 0, level: int = 0) -> BuildingEntity:
        stats, base_data, LogicClass = BuildingFactory._get_prototype_config(owner, grid_pos, army, level)
        entity = BuildingEntity(stats, grid_pos, None, base_data)
        entity.logic_comp = LogicClass(entity)
        return entity

    @staticmethod
    @register_building(GameType.Arch.PRODUCTION)
    def build_production(owner: GameTypeMap, grid_pos: GridPoint, army: int = 0, level: int = 0) -> BuildingEntity:
        stats, base_data, LogicClass = BuildingFactory._get_production_config(owner, grid_pos, army, level)
        entity = BuildingEntity(stats, grid_pos, None, base_data)
        entity.logic_comp = LogicClass(entity)
        return entity

    @staticmethod
    @register_building(GameType.Arch.LAB)
    def build_laboratory(owner: GameTypeMap, grid_pos: GridPoint, army: int = 0, level: int = 0) -> BuildingEntity:
        stats, base_data, LogicClass = BuildingFactory._get_lab_config(owner, grid_pos, army, level)
        entity = BuildingEntity(stats, grid_pos, None, base_data)
        entity.logic_comp = LogicClass(entity)
        return entity

    @staticmethod
    @register_building(GameType.Arch.CASTLE)
    def build_castle(owner: GameTypeMap, grid_pos: GridPoint, army: int = 0, level: int = 0) -> BuildingEntity:
        stats, base_data, LogicClass = BuildingFactory._get_castle_config(owner, grid_pos, army, level)
        entity = BuildingEntity(stats, grid_pos, None, base_data)
        entity.logic_comp = LogicClass(entity)
        return entity

    # =========================================================================
    # 變身邏輯
    # 原地修改現有實體，實現「地基 -> 建築」
    # =========================================================================

    @staticmethod
    def transform_entity(entity: BuildingEntity, target_arch: GameType.Arch):
        """
        將 entity 原地轉換為 target_arch 類型。
        保留：grid_pos, owner
        繼承：army
        重置：stats, logic_comp, upgrade_comp
        """
        saved_owner = entity.stats.owner
        saved_grid = entity.grid_point
        saved_army = entity.stats.army

        # 取得新配置 (預設變身後為等級 1)
        new_level = 0
        new_stats = None
        new_base_data = None
        NewLogicClass = None

        if target_arch == GameType.Arch.CASTLE:
            new_stats, new_base_data, NewLogicClass = BuildingFactory._get_castle_config(saved_owner, saved_grid, saved_army, new_level)
        elif target_arch == GameType.Arch.PRODUCTION:
            new_stats, new_base_data, NewLogicClass = BuildingFactory._get_production_config(saved_owner, saved_grid, saved_army, new_level)
        elif target_arch == GameType.Arch.LAB:
            new_stats, new_base_data, NewLogicClass = BuildingFactory._get_lab_config(saved_owner, saved_grid, saved_army, new_level)
        else:
            dbg.error(f'{target_arch} is not exisit in GameType.Arch')
            return

        if not new_stats:
            dbg.error(f">> Error: Cannot transform to unknown arch {target_arch}")
            return

        # 替換數值
        entity.stats = new_stats
        entity.upgrade_comp = UpgradeComponent(entity, new_base_data)
        entity.logic_comp = NewLogicClass(entity)
