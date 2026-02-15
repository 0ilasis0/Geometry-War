import time
from typing import TYPE_CHECKING

from py.game.ai.command.brain_logic.combat import CombatEvaluator
from py.game.ai.command.brain_logic.economy import EconomyEvaluator
from py.game.ai.command.brain_logic.lab import LabEvaluator
from py.game.ai.command.brain_logic.logistics import LogisticsEvaluator
from py.game.ai.variable import AIActionKey

if TYPE_CHECKING:
    from py.game.ai.command.manager import AICommander


class AIBrain:
    def __init__(self, commander: "AICommander"):
        self.cmd = commander

        # 初始化各部門
        self.economy = EconomyEvaluator(commander)
        self.combat = CombatEvaluator(commander)
        self.lab = LabEvaluator(commander)
        self.logistics = LogisticsEvaluator(commander)

    def think(self, dt: float) -> list | None:
        """ 綜合評估並回傳最高分的一批決策 """
        actions = []
        busy_entities = set() # 記錄本幀已接單的建築

        # 經濟 (建設/升級)
        actions.extend(self.economy.evaluate())

        # 科技 (技能製作/施放)
        actions.extend(self.lab.evaluate(busy_entities))

        # 戰鬥 (進攻/防守/集結)
        actions.extend(self.combat.evaluate(dt, busy_entities))

        # 後勤 (運補/溢出處理)
        actions.extend(self.logistics.evaluate(busy_entities))

        if not actions: return None

        # 統整與過濾
        # 補上時間戳 (如果子模組沒補的話)
        now = time.time()
        for act in actions:
            if AIActionKey.OVER_TIME not in act:
                act[AIActionKey.OVER_TIME] = now

        # 排序取最高分
        actions.sort(key=lambda x: x[AIActionKey.SCORE], reverse=True)

        final_actions = []
        locked_entities = set()
        limit = self.cmd.profile.max_batch_actions

        for act in actions:
            if len(final_actions) >= limit: break

            source = act.get(AIActionKey.SOURCE)
            target = act.get(AIActionKey.TARGET)

            # 收集所有參與者
            participants = []
            if source: participants.append(source)
            if target: participants.append(target)

            # 檢查衝突：只要有任何一個參與者已經被鎖定，這個動作就跳過
            if any(p in locked_entities for p in participants): continue

            # 執行鎖定：將所有參與者加入鎖定名單
            final_actions.append(act)
            locked_entities.update(participants)

        return final_actions
