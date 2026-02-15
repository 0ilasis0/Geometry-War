from typing import TYPE_CHECKING, List, Tuple

from py.game.ai.logic.path_analyzer import PathAnalyzer
from py.game.ai.logic.search import TargetSelector
from py.game.ai.variable import AIActionKey, AIActionType
from py.game.building.logic.variable import (LabConfig, LabConfigKey,
                                             LabSkillType)
from py.game.variable import GameType

if TYPE_CHECKING:
    from py.game.ai.command.manager import AICommander
    from py.game.building.entity import BuildingEntity


class LogisticsEvaluator:
    def __init__(self, commander: "AICommander"):
        self.cmd = commander
        self.profile = commander.profile

    def evaluate(self, busy_entities: set) -> List[dict]:
        """ 評估運補決策 (Pull & Push) """
        actions = []

        # 需求驅動 (Pull): 前線或實驗室缺兵
        needy_requests = self._analyze_pull_requests()
        pull_actions = self._solve_pull_actions(needy_requests, busy_entities)
        actions.extend(pull_actions)

        # 溢出驅動 (Push): 後方爆倉
        overflow_sources = self._analyze_push_sources(busy_entities)
        push_actions = self._solve_push_actions(overflow_sources, busy_entities)
        actions.extend(push_actions)

        return actions

    # =========================================================================
    #  Pull Logic (需求端)
    # =========================================================================

    def _analyze_pull_requests(self) -> List[Tuple["BuildingEntity", float]]:
        """ 掃描誰需要兵 (回傳: [(Building, Urgency), ...]) """
        requests = []
        for b in self.cmd.my_buildings:
            if self._is_weak(b): continue
            stats = b.stats
            urgency = 0.0

            if stats.arch == GameType.Arch.LAB:
                urgency = self._calc_lab_urgency(b)
            else:
                # 只要是前線建築(包含工廠)，被打都需要補給
                urgency = self._calc_frontline_urgency(b)

            if urgency > 0:
                requests.append((b, urgency))

        # 急迫度高的排前面
        requests.sort(key=lambda x: x[1], reverse=True)
        return requests

    def _calc_lab_urgency(self, lab: "BuildingEntity") -> float:
        stats = lab.stats
        base_need = stats.max_army_capacity * self.profile.lab_min_army_ratio

        # 這裡需要知道實驗室想做什麼藥，才能決定要運多少錢
        wanted_skill = self._get_preferred_skill(stats.level)
        skill_cost = LabConfig.SKILL[wanted_skill][LabConfigKey.COST]
        target_need = max(base_need, skill_cost)

        if stats.army < target_need:
            shortage_ratio = 1.0 - (stats.army / max(target_need, 1.0))

            bias = self.profile.bias_lab_supply

            # 如果已經滿足基本運作，代表現在是在 "存大招"，提高權重
            if stats.army >= base_need:
                bias = self.profile.bias_lab_saving * self._get_skill_bias(wanted_skill)

            return shortage_ratio * bias
        return 0.0

    def _calc_frontline_urgency(self, building: "BuildingEntity") -> float:
        """ 計算防禦運補需求 """
        margin = self.cmd.calculate_safety_margin(building)
        target_margin = 4.5

        if margin < target_margin:
            gap = target_margin - margin
            urgency = (gap / 10.0) * self.profile.bias_frontline_supply

            # 城堡稍微再重要一點
            if building.stats.arch == GameType.Arch.CASTLE:
                urgency *= 1.2

            return max(urgency, 0.0)
        return 0.0

    def _solve_pull_actions(self, requests: list, busy_entities: set) -> List[dict]:
        actions = []
        for receiver, urgency in requests:
            if receiver in busy_entities: continue

            best_sender = None
            max_score = 0.0

            for sender in self.cmd.my_buildings:
                if self._is_weak(sender): continue
                if sender == receiver or sender in busy_entities: continue
                if sender.stats.army <= self.profile.min_defense_reserve: continue
                if self.cmd.calculate_threat_score(sender) > 0: continue

                unit_atk, unit_speed = self.cmd.get_unit_stats(sender)
                dist_sq = sender.grid_point.dist_sq_to(receiver.grid_point)

                if dist_sq > 450: continue # 太遠不補

                travel_time = (dist_sq ** 0.5) / unit_speed

                # --- 快速危險評估 (使用直線採樣) ---
                steps = max(5, int(travel_time // 2))
                estimated_loss = PathAnalyzer.estimate_danger_linear(
                    start = sender.grid_point,
                    end = receiver.grid_point,
                    unit_speed = unit_speed,
                    enemy_buildings = self.cmd.enemy_buildings,
                    steps = steps
                )

                if estimated_loss > (sender.stats.army * 0.5): continue

                effective_amount = sender.stats.army - estimated_loss
                raw_power = effective_amount * unit_atk
                score = (urgency * 10.0 + raw_power) / max(travel_time, 0.5)

                if score > max_score:
                    max_score = score
                    best_sender = sender

            if best_sender and max_score > 0:
                score_final = max_score * self.profile.weight_transfer
                actions.append({
                    AIActionKey.TYPE: AIActionType.TRANSFER,
                    AIActionKey.SCORE: score_final,
                    AIActionKey.TARGET: receiver,
                    AIActionKey.SOURCE: best_sender,
                    AIActionKey.OWNER: receiver.stats.owner
                })
                busy_entities.add(best_sender)
                busy_entities.add(receiver)
        return actions

    # =========================================================================
    #  Push Logic (供給端/溢出)
    # =========================================================================

    def _analyze_push_sources(self, busy_entities: set) -> List["BuildingEntity"]:
        overflow_sources = []
        for b in self.cmd.my_buildings:
            if b in busy_entities: continue

            if self._is_weak(b):
                if b.stats.army > 0:
                    overflow_sources.append(b)
                continue

            # 接近上限且無事可做
            if b.stats.army >= (b.stats.max_army_capacity * 0.95):
                overflow_sources.append(b)
        return overflow_sources

    def _solve_push_actions(self, sources: list["BuildingEntity"], busy_entities: set) -> List[dict]:
        actions = []
        if not sources: return actions

        # 建立潛在倉庫列表
        warehouses = []
        for b in self.cmd.my_buildings:
            if self._is_weak(b): continue
            if b in busy_entities: continue
            if b.stats.army >= (b.stats.max_army_capacity * 0.8): continue

            priority = 1.0
            if b.stats.arch in (GameType.Arch.CASTLE, GameType.Arch.LAB): priority = 1.5
            elif b.stats.arch == GameType.Arch.PRODUCTION: priority = 0.8

            warehouses.append((b, priority))

        for source in sources:
            best_wh: "BuildingEntity" = None
            min_weighted_dist = float('inf')

            for wh, priority in warehouses:
                if wh == source: continue
                dist_sq = source.grid_point.dist_sq_to(wh.grid_point)
                weighted_dist = dist_sq / priority
                if weighted_dist < min_weighted_dist:
                    min_weighted_dist = weighted_dist
                    best_wh = wh

            if best_wh:
                # 存入倉庫
                score = 3.0 + (source.stats.army / 10.0)

                if self._is_weak(source): score += 20.0

                actions.append({
                    AIActionKey.TYPE: AIActionType.TRANSFER,
                    AIActionKey.SCORE: score,
                    AIActionKey.TARGET: best_wh,
                    AIActionKey.SOURCE: source,
                    AIActionKey.OWNER: best_wh.stats.owner
                })
                busy_entities.add(source)
            else:
                # 沒倉庫可存 -> 強制進攻最近的敵人 (Total War)
                enemy, _, _ = TargetSelector.find_best_target(source, self.cmd.enemy_buildings, top_k=1)
                if enemy:
                    atk_score = 5.0

                    if self._is_weak(source): atk_score = 15.0

                    actions.append({
                        AIActionKey.TYPE: AIActionType.ATTACK,
                        AIActionKey.SCORE: atk_score,
                        AIActionKey.TARGET: enemy,
                        AIActionKey.SOURCE: source,
                        AIActionKey.OWNER: enemy.stats.owner
                    })

        return actions

    # =========================================================================
    #  Helper Methods (技能偏好)
    #  這些邏輯在運補時也需要，用來判斷實驗室是否在存大招
    # =========================================================================

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

    def _is_weak(self, building: "BuildingEntity") -> bool:
        """ 檢查建築是否處於虛弱狀態 (Weak) """
        return LabSkillType.WEAK in building.active_effects
