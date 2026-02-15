from typing import TYPE_CHECKING, List, Optional, Tuple

from py.game.ai.variable import AIActionKey, AIActionType
from py.game.building.logic.variable import (LabConfig, LabConfigKey,
                                             LabSkillType)
from py.game.variable import GameType

if TYPE_CHECKING:
    from py.game.ai.command.manager import AICommander
    from py.game.building.entity import BuildingEntity
    from py.game.building.logic.lab import LabLogic

class LabEvaluator:
    def __init__(self, commander: "AICommander"):
        self.cmd = commander
        self.profile = commander.profile

    def evaluate(self, busy_entities: set) -> List[dict]:
        actions = []

        for lab in self.cmd.my_buildings:
            if lab.stats.arch != GameType.Arch.LAB: continue
            if lab in busy_entities: continue

            logic: "LabLogic" = getattr(lab, "logic_comp", None)
            if not logic: continue

            ready_skill = logic.get_ready_skill()

            # [情境 A] 手上有做好的藥水 -> 尋找目標施放
            if ready_skill:
                target, score = self._find_best_skill_target(lab, ready_skill)
                final_score = score * self.profile.weight_use_skill * 3.0

                if target and final_score > 0:
                    actions.append({
                        AIActionKey.TYPE: AIActionType.LAB_SKILL,
                        AIActionKey.SCORE: final_score,
                        AIActionKey.TARGET: target,
                        AIActionKey.SOURCE: lab,
                        AIActionKey.SKILL: ready_skill,
                        AIActionKey.OWNER: target.stats.owner
                    })

            # [情境 B] 閒置中 -> 決定製作什麼藥水
            elif logic.can_cast():
                skill_to_brew = self._get_preferred_skill(lab.stats.level)
                if not skill_to_brew: continue

                cost = LabConfig.SKILL[skill_to_brew][LabConfigKey.COST]

                if lab.stats.army >= cost:
                    bias = self._get_skill_bias(skill_to_brew)
                    score = bias * self.profile.weight_use_skill

                    actions.append({
                        AIActionKey.TYPE: AIActionType.LAB_SKILL,
                        AIActionKey.SCORE: score,
                        AIActionKey.TARGET: lab,
                        AIActionKey.SOURCE: lab,
                        AIActionKey.SKILL: skill_to_brew,
                        AIActionKey.OWNER: lab.stats.owner
                    })

        return actions

    def _find_best_skill_target(self, lab, skill_type) -> Tuple[Optional["BuildingEntity"], float]:
        """ 幫手中的藥水找一個受害者 """

        # 準備候選名單
        # 惡魔可以打中立，其他只能打敵人
        if skill_type == LabSkillType.DEMON:
            candidates = self.cmd.enemy_buildings + self.cmd.neutral_targets
        else:
            candidates = self.cmd.enemy_buildings

        if not candidates: return None, 0.0

        best_target = None
        max_score = 0.0

        # 評分函數
        for target in candidates:
            score = 0.0
            stats = target.stats

            # --- [ICE] 冰凍邏輯 ---
            if skill_type == LabSkillType.ICE:
                # 基礎分：兵越多越值得冰 (控場效益)
                score = stats.army / 10.0

                # 建築類型加權
                if stats.arch == GameType.Arch.CASTLE:
                    score *= self.profile.bias_ice_castle
                elif stats.arch == GameType.Arch.PRODUCTION:
                    score *= self.profile.bias_ice_production
                elif stats.arch == GameType.Arch.LAB:
                    score *= self.profile.bias_ice_lab

            # --- [WEAK] 虛弱邏輯 ---
            elif skill_type == LabSkillType.WEAK:
                # 基礎分：兵越多越值得毒 (百分比扣血效益)
                score = stats.army / 10.0

                # 建築類型加權
                if stats.arch == GameType.Arch.CASTLE:
                    score *= self.profile.bias_weak_castle
                elif stats.arch == GameType.Arch.PRODUCTION:
                    score *= self.profile.bias_weak_production
                elif stats.arch == GameType.Arch.LAB:
                    score *= self.profile.bias_weak_lab

            # --- [DEMON] 惡魔邏輯 ---
            elif skill_type == LabSkillType.DEMON:
                # 基礎分：兵量 + 等級 (搶過來直接變戰力)
                score = (stats.army * 2.0) + (stats.level * 10.0)

                # 針對實驗室的額外加分 (搶別人的藥水)
                if stats.arch == GameType.Arch.LAB:
                    l_logic: "LabLogic" = getattr(target, "logic_comp", None)
                    if l_logic and l_logic.active_skill:
                        score += 100.0 # 搶到就是賺到

                # 陣營偏好
                if stats.owner == GameType.Owner.NEUTRAL:
                    score *= self.profile.bias_demon_neutral
                else:
                    score *= self.profile.bias_demon_enemy

            # 更新最高分
            if score > max_score:
                max_score = score
                best_target = target

        # 戰略價值修正
        if best_target:
            strategic_bonus = self.cmd.get_strategic_value(best_target)
            max_score *= (1.0 + strategic_bonus * 0.1)

        return best_target, max_score

    def _get_preferred_skill(self, current_lab_level: int) -> LabSkillType:
        scores = {}
        if current_lab_level >= LabConfig.SKILL[LabSkillType.ICE][LabConfigKey.LEVEL]:
            scores[LabSkillType.ICE] = self.profile.bias_skill_ice

        if current_lab_level >= LabConfig.SKILL[LabSkillType.WEAK][LabConfigKey.LEVEL]:
            scores[LabSkillType.WEAK] = self.profile.bias_skill_weak

        if current_lab_level >= LabConfig.SKILL[LabSkillType.DEMON][LabConfigKey.LEVEL]:
            scores[LabSkillType.DEMON] = self.profile.bias_skill_demon

        if not scores: return None

        return max(scores, key=scores.get)

    def _get_skill_bias(self, skill_type) -> float:
        if skill_type == LabSkillType.ICE: return self.profile.bias_skill_ice
        if skill_type == LabSkillType.WEAK: return self.profile.bias_skill_weak
        if skill_type == LabSkillType.DEMON: return self.profile.bias_skill_demon
        return 1.0
