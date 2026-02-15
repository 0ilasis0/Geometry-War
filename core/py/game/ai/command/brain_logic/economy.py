from typing import TYPE_CHECKING, List, Optional, Tuple

from py.game.ai.variable import AIActionKey, AIActionType
from py.game.building.logic.variable import (LabConfig, LabConfigKey,
                                             LabSkillType, PrototypeConfig)
from py.game.variable import GameType

if TYPE_CHECKING:
    from py.game.ai.command.manager import AICommander
    from py.game.building.entity import BuildingEntity
    from py.game.building.logic.upgrade import UpgradeComponent

class EconomyEvaluator:
    def __init__(self, commander: "AICommander"):
        self.cmd = commander
        self.profile = commander.profile

    def evaluate(self) -> List[dict]:
        actions = []

        # 評估建設
        for proto in self.cmd.my_prototypes:
            best_arch, score = self._eval_build(proto)
            if score > 0:
                actions.append({
                    AIActionKey.TYPE: AIActionType.BUILD,
                    AIActionKey.SCORE: score,
                    AIActionKey.TARGET: proto,
                    AIActionKey.SOURCE: proto,
                    AIActionKey.ARCH: best_arch,
                    AIActionKey.OWNER: proto.stats.owner
                })

        # 評估升級
        for b in self.cmd.my_buildings:
            score = self._eval_upgrade(b)
            if score > 0:
                actions.append({
                    AIActionKey.TYPE: AIActionType.UPGRADE,
                    AIActionKey.SCORE: score,
                    AIActionKey.TARGET: b,
                    AIActionKey.SOURCE: b,
                    AIActionKey.OWNER: b.stats.owner
                })

        return actions

    def _eval_build(self, proto: "BuildingEntity") -> Tuple[Optional[GameType.Arch], float]:
        """ 評估地基變身 """
        threat_score = self.cmd.calculate_threat_score(proto)
        scores = {}

        # 根據戰況與 Profile 決定蓋什麼
        scores[GameType.Arch.CASTLE] = (1.0 + threat_score * 0.5) * self.profile.bias_build_castle
        scores[GameType.Arch.PRODUCTION] = (2.0 - threat_score * 0.5) * self.profile.bias_build_production
        scores[GameType.Arch.LAB] = (2.0 - threat_score * 0.5) * self.profile.bias_build_lab

        best_arch = max(scores, key = scores.get)
        cost = PrototypeConfig.get_cost(best_arch)

        if cost is not None and proto.stats.army >= cost:
            return best_arch, scores[best_arch] * self.profile.weight_upgrade_prototype
        return None, 0.0

    def _eval_upgrade(self, building: "BuildingEntity") -> float:
        """ 評估升級：考量 性價比 + 速度成長潛力 """
        stats = building.stats
        if stats.level >= stats.max_level: return 0.0
        if stats.army < stats.upgrade_cost_army: return 0.0

        base_score = (stats.army / stats.upgrade_cost_army) * 2.0 * self.profile.weight_upgrade_base
        tactical_bonus = 0.0

        upgrade_comp: "UpgradeComponent" = building.upgrade_comp
        base_data = upgrade_comp.base_data

        if base_data.jelly_speed_grid_growth > 0:
            growth_factor = base_data.jelly_speed_grid_growth / 4
            tactical_bonus += growth_factor * (self.profile.bonus_upgrade_speed - 1.0) * 5.0

        if base_data.defence_rate_growth > 0:
            growth_factor = base_data.defence_rate_growth
            tactical_bonus += growth_factor * (self.profile.bonus_upgrade_defense - 1.0) * 5.0

        if building.stats.arch == GameType.Arch.PRODUCTION:
            tactical_bonus += self.profile.weight_upgrade_production
        elif building.stats.arch == GameType.Arch.CASTLE:
            tactical_bonus += self.profile.weight_upgrade_castle
        elif building.stats.arch == GameType.Arch.LAB:
            tactical_bonus += self.profile.weight_upgrade_lab

        final_score = base_score * (1.0 + tactical_bonus)

        if building.stats.arch == GameType.Arch.LAB:
            # 預測下一級
            next_level = building.stats.level + 1

            # 取得我最想要的技能 (AI 想要 Profile 裡權重最高的那個技能)
            wanted_skill = self._get_most_wanted_skill()

            # 檢查下一級是否剛好解鎖這個技能
            if self._is_skill_unlocked_at(wanted_skill, next_level):
                final_score *= self.profile.bonus_upgrade_unlock_skill

        # 安全係數懲罰 (太危險不升級，留著生兵)
        margin = self.cmd.calculate_safety_margin(building)
        if margin < 0:
            penalty = 1.0 / (abs(margin) + 1.0)
            final_score *= penalty
        elif margin < 2.5:
            final_score *= 0.9

        return final_score

    def _get_most_wanted_skill(self) -> LabSkillType:
        """ 找出目前 Profile 權重最高的技能 """
        scores = {
            LabSkillType.ICE: self.profile.bias_skill_ice,
            LabSkillType.WEAK: self.profile.bias_skill_weak,
            LabSkillType.DEMON: self.profile.bias_skill_demon,
        }
        return max(scores, key=scores.get)

    def _is_skill_unlocked_at(self, skill: LabSkillType, level: int) -> bool:
        """ 檢查該等級是否 *剛好* 解鎖了該技能 """
        req_level = LabConfig.SKILL[skill].get(LabConfigKey.LEVEL, 0)
        return level == req_level
