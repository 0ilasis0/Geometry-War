from collections import defaultdict
from typing import TYPE_CHECKING, Dict, List
from weakref import WeakSet

from py.debug import dbg
from py.game.building.variable import BuildingStatsKey
from py.game.faction.variable import (Faction, FactionKey, FactionStats,
                                      PowerEntity)
from py.game.variable import GameType, GameTypeMap

if TYPE_CHECKING:
    from py.game.building.entity import BuildingEntity


class FactionManager:
    def __init__(self):
        # [實體註冊表] 使用 WeakSet 避免記憶體洩漏 (Entity 死亡後會自動消失)
        # Key: Owner Enum, Value: 該陣營的所有單位(建築+兵)
        self._registry: dict[GameType.Owner, WeakSet] = defaultdict(WeakSet)

        # [國家物件表] 儲存所有陣營的高層狀態
        self.factions: Dict[GameType.Owner, Faction] = {}

        # 預先初始化所有可能的 Faction 物件
        for owner in GameType.Owner:
            self.factions[owner] = Faction(owner = owner)

    def setup_level(self, level_config: dict):
        """ 解析關卡設定，激活參與的陣營 """
        self.clear() # 重置所有狀態

        # 取得建築列表 Key
        arch_list_key = GameTypeMap.get_value(GameType.Genre.ARCH)
        if not arch_list_key:
            dbg.error(f'Arch key not found in GameTypeMap')
            return

        # 掃描關卡資料，標記參與者
        building_list = level_config.get(arch_list_key, [])
        for b_data in building_list:
            owner = b_data.get(BuildingStatsKey.OWNER)
            if owner:
                self.factions[owner].is_active = True

        active_names = [f.owner.name for f in self.factions.values() if f.is_active]
        dbg.log(f"[FactionManager] Level participants: {active_names}")

    def clear(self):
        """ 清空上一關的殘留資料 """
        self._registry.clear()
        for faction in self.factions.values():
            faction.reset()

    # =========================================================================
    # [Entity Management] 實體註冊 (生/死/轉移)
    # =========================================================================

    def register(self, entity: PowerEntity):
        """
        [出生登記]
        當任何有戰鬥力的東西生成時呼叫此方法
        """
        owner = entity.stats.owner
        if owner:
            self._registry[owner].add(entity)

    def unregister(self, entity: PowerEntity):
        """
        [死亡除戶]
        當物件死亡或被銷毀時呼叫
        """
        owner = entity.stats.owner
        if owner and entity in self._registry[owner]:
            self._registry[owner].remove(entity)

    def transfer_owner(self, entity: PowerEntity, old_owner: GameType.Owner, new_owner: GameType.Owner):
        """ [所有權轉移] 例如建築被佔領 """
        if entity in self._registry[old_owner]:
            self._registry[old_owner].remove(entity)
        self._registry[new_owner].add(entity)

    # =========================================================================
    # [Strategic Update] 戰略數據更新
    # =========================================================================
    def update_strategic_stats(self):
        """
        負責更新 Faction 物件內的數據，並檢查是否陣亡。
        """
        for owner, faction in self.factions.items():
            if not faction.is_active: continue
            if faction.is_defeated: continue

            # 計算數據
            stats = self._calculate_realtime_stats(owner)

            # 更新到物件中
            faction.total_army = stats.total_army
            faction.building_count = stats.building_count
            faction.production_rate = stats.production_rate
            faction.factory_count = stats.factory_count

            # 判斷是否陣亡
            if owner != GameType.Owner.NEUTRAL:
                if faction.total_army <= 0 and faction.building_count <= 0:
                    faction.mark_defeated()

    def update_strategic_stats(self):
        """
        負責更新 Faction 物件內的快取數據，並檢查是否陣亡。
        """
        for owner, faction in self.factions.items():
            # 只處理本局活躍且尚未陣亡的國家
            if not faction.is_active: continue
            if faction.is_defeated: continue

            # 執行計算
            stats = self._calculate_realtime_stats(owner)

            # 更新快取
            faction.total_army = stats.total_army
            faction.production_rate = stats.production_rate
            faction.building_count = stats.building_count
            faction.factory_count = stats.factory_count

            # 自動判斷陣亡
            if faction.total_army <= 0 and faction.building_count <= 0:
                faction.mark_defeated()

    def _calculate_realtime_stats(self, owner: GameType.Owner) -> FactionStats:
        """ 內部運算：遍歷 WeakSet 統計人頭 """
        stats = FactionStats()

        if owner not in self._registry:
            return stats

        # 複製一份集合避免遍歷時變動
        entities: List["BuildingEntity"] = list(self._registry[owner])

        for entity in entities:
            if getattr(entity.stats, FactionKey.IS_DEAD.value, False): continue

            # 累加兵量
            if hasattr(entity.stats, FactionKey.ARMY.value):
                stats.total_army += entity.stats.army
            # 判斷是否為建築
            if hasattr(entity.stats, FactionKey.ARCH.value):
                stats.building_count += 1

                # 累加產能
                rate = getattr(entity.stats, FactionKey.RATE_OF_PRODUCTION.value, 0.0)
                if rate > 0:
                    stats.factory_count += 1
                    stats.production_rate += rate

        return stats

    # =========================================================================
    # [Public API] 外部查詢介面
    # =========================================================================

    def get_faction(self, owner: GameType.Owner) -> Faction:
        """ 取得陣營物件 (讀取數據用) """
        return self.factions.get(owner)

    def get_alive_enemy_factions(self, exclude_owner: GameType.Owner = GameType.Owner.PLAYER) -> List[Faction]:
        """ 取得目前還活著的敵人列表 (供 AI 索敵用) """
        return [
            f for f in self.factions.values()
            if f.is_active
            and not f.is_defeated
            and f.owner != exclude_owner # 排除非敵對 (通常是自己)
            and f.owner != GameType.Owner.NEUTRAL
        ]

    def is_player_alive(self) -> bool:
        """ 快速檢查玩家是否存活 """
        p = self.factions.get(GameType.Owner.PLAYER)
        return p.is_active and not p.is_defeated
