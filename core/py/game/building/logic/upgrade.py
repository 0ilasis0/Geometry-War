from typing import TYPE_CHECKING

from py.debug import dbg
from py.game.context import GameContext
from py.game.jelly.variable import ARCH_TO_JOB_MAP, JELLY_BASE_CONFIG
from py.game.variable import GameType

if TYPE_CHECKING:
    from py.game.building.entity import BuildingEntity
    from py.game.building.variable import BaseStatsData, BuildingStats

class StatsCalculator:
    """ [公式庫] 負責執行數值計算 """
    @staticmethod
    def calculate_stats(stats: "BuildingStats", data: "BaseStatsData", arch: GameType.Arch):
        """ 根據 stats.level 與 data 設定，計算出當前數值 """
        # 只有基本值沒有成長率的才會使用此level
        cal_level = stats.level + 1

        stats.max_army_capacity = int(data.base_army_cap * cal_level)
        job = ARCH_TO_JOB_MAP.get(arch)
        base_config = JELLY_BASE_CONFIG.get(job)

        # "升到下一級" 的費用。如果已達滿級，費用設為 0
        if stats.level < stats.max_level:
            base_cost = int(data.base_army_cap * data.cost_factor)
            stats.upgrade_cost_army = base_cost * cal_level
        else:
            stats.upgrade_cost_army = 0

        # Castle 特殊處理
        if data.castle_enable:
            stats.defense = data.base_defense + (stats.level * data.defence_rate_growth)
            stats.bullet_damage = data.base_bullet_damage + (stats.level * data.bullet_damage_rate_groth)
            stats.rate_of_fire = data.base_rate_of_fire - (stats.level * data.rate_of_fire_growth)

        # 生產速率 (Production 特殊處理)
        if data.prod_rate_base > 0:
            stats.rate_of_production = data.prod_rate_base + (stats.level * data.prod_rate_growth)

        # Jelly 特殊處理
        if base_config:
            stats.jelly_attack = base_config.attack + (stats.level * data.jelly_attack_growth)
            stats.jelly_speed_grid = base_config.move_speed_grid + (stats.level * data.jelly_speed_grid_growth)
            stats.jelly_speed = GameContext.grid_cvt.col_to_px(stats.jelly_speed_grid)
        else:
            dbg.error(f'arch:{arch},job{job} base_config is not exisit')

class UpgradeComponent:
    """ 掛載在建築身上，負責持有設定檔與執行升級動作 """
    def __init__(self, entity: "BuildingEntity", base_data: "BaseStatsData"):
        self.entity = entity
        self.stats = entity.stats
        self.base_data = base_data

        # 初始化時，強制計算一次，確保 Factory 建立出來的數值是經過公式驗證的
        self.refresh_stats()

    def refresh_stats(self):
        """ 根據當前等級重新刷新數值 """
        StatsCalculator.calculate_stats(self.stats, self.base_data, self.stats.arch)
        # 更新圖片狀態
        self.entity.refresh_img_id_cache()

    def perform_upgrade(self) -> bool:
        """ 嘗試執行升級 """
        # 檢查是否滿級
        if self.stats.level >= self.stats.max_level: return False

        # 檢查費用
        cost = self.stats.upgrade_cost_army
        if self.stats.army < cost: return False

        # 執行扣款與升級
        self.stats.army -= cost
        self.stats.level += 1

        # 刷新數值 (這會算出新的上限、防禦力、與下一級的費用)
        self.refresh_stats()

        return True
