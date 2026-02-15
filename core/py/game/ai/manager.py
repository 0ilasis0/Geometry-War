from typing import List

from py.debug import dbg
from py.game.ai.command.manager import AICommander
from py.game.ai.profile.base import AIProfile
from py.game.ai.profile.faction_config import AIConfig
from py.game.ai.profile.factory import AIProfileFactory
from py.game.context import GameContext
from py.game.variable import GameType


class AIManager:
    def __init__(self):
        self.commanders: List[AICommander] = []

    def setup_level(self):
        """
        根據關卡設定，自動掃描有哪些敵對陣營，並生成 AI
        """
        self.commanders.clear()

        enemy_factions = GameContext.faction_mg.get_alive_enemy_factions()

        if not enemy_factions:
            # dbg.war("[AIManager] No enemies found in this level.")
            return

        for faction in enemy_factions:
            self._create_commander(faction.owner)

        names = [f.owner.name for f in enemy_factions]
        dbg.log(f"[AIManager] Commanders initialized for: {names}")

    def _create_commander(self, owner: GameType.Owner):
        # 取得標準設定 (白紙)
        standard_profile = AIProfile()

        #  從 Config 取得該陣營的性格配方
        traits_mix = AIConfig.get_traits_for_faction(owner)

        # 透過工廠生成最終 Profile
        final_profile = AIProfileFactory.create_mixed_profile(standard_profile, traits_mix)

        # 設定名字方便 Debug
        final_profile.name = f"AI_{owner.name}"

        # 建立指揮官
        ai = AICommander(owner, final_profile)
        self.commanders.append(ai)

    def update(self, dt: float):
        """ 每一幀更新所有指揮官 """
        for cmd in self.commanders:
            cmd.update(dt)
