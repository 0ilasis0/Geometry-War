import random
from typing import TYPE_CHECKING, List

from py.game.ai.logic.path_analyzer import PathAnalyzer
from py.game.ai.logic.search import TargetSelector
from py.game.ai.variable import AIActionKey, AIActionType
from py.game.variable import GameType

if TYPE_CHECKING:
    from py.game.ai.command.manager import AICommander
    from py.game.building.entity import BuildingEntity

class CombatEvaluator:
    def __init__(self, commander: "AICommander"):
        self.cmd = commander
        self.profile = commander.profile
        # [狀態封裝] 只有戰鬥模組需要關心集結倒數
        self._swarm_timer = self.profile.swarm_interval

    def evaluate(self, dt: float, busy_entities: set) -> List[dict]:
        actions = []

        # 防守
        actions.extend(self._eval_defense_batch())

        # 集結
        self._swarm_timer -= dt
        if self._swarm_timer <= 0:
            actions.extend(self._eval_swarm_attack(busy_entities))
            self._swarm_timer = self.profile.swarm_interval

        # 單體攻擊 (隨機抽樣優化)
        # 只挑選沒事做的建築
        idle_buildings = [b for b in self.cmd.my_buildings if b not in busy_entities]
        if idle_buildings:
            # 限制運算量：每次只讓 10 個閒置建築思考進攻
            sample_size = min(len(idle_buildings), 10)
            attack_candidates = random.sample(idle_buildings, sample_size)
            actions.extend(self._eval_attack_batch(busy_entities, candidates=attack_candidates))

        return actions

    def _eval_defense_batch(self) -> list:
        """ [防守決策] """
        actions = []
        distressed_buildings = []

        for b in self.cmd.my_buildings:
            if self.cmd.calculate_safety_margin(b) < 0:
                distressed_buildings.append(b)

        if not distressed_buildings: return actions

        potential_targets = distressed_buildings
        for savior in self.cmd.my_buildings:
            if savior in distressed_buildings: continue
            if self.cmd.calculate_safety_margin(savior) < 3.0 : continue
            if savior.stats.army < self.profile.min_defense_reserve: continue

            best_victim, path_len, path = TargetSelector.find_best_target(savior, potential_targets, top_k=3)

            if not best_victim or not path or path_len > 30: continue

            danger_cost = PathAnalyzer.calculate_danger_cost(path, self.cmd.enemy_buildings, savior)
            arrival_army = savior.stats.army - danger_cost

            if arrival_army < (savior.stats.army * 0.6) or arrival_army < 5: continue

            # 呼叫 Strategy 取得戰略價值
            victim_val = self.cmd.get_strategic_value(best_victim)

            score = (victim_val * 5.0) + (arrival_army / 10.0)
            score /= max(path_len, 1.0)
            score *= self.profile.weight_defense

            actions.append({
                AIActionKey.TYPE: AIActionType.DEFEND,
                AIActionKey.SCORE: score,
                AIActionKey.TARGET: best_victim,
                AIActionKey.SOURCE: savior,
                AIActionKey.OWNER: best_victim.stats.owner
            })

        return actions

    def _eval_swarm_attack(self, busy_entities: set) -> list:
        """ [協同攻擊] """
        if not self.cmd.my_buildings: return []

        my_total_army = sum(b.stats.army for b in self.cmd.my_buildings)
        my_total_cap = sum(b.stats.max_army_capacity for b in self.cmd.my_buildings)
        current_ratio = my_total_army / max(my_total_cap, 1.0)

        if current_ratio < self.profile.swarm_trigger_ratio: return []

        actions = []
        all_targets = self.cmd.enemy_buildings + self.cmd.neutral_targets

        # 根據戰略價值排序目標
        potential_targets = sorted(
            all_targets,
            key = lambda b: self.cmd.get_strategic_value(b),
            reverse = True
        )

        for target in potential_targets:
            enemy_defense = target.stats.army * target.stats.defense
            if target.stats.owner != GameType.Owner.NEUTRAL:
                enemy_defense += 5.0

            attackers = []
            total_attack_power = 0.0

            for ally in self.cmd.my_buildings:
                if ally in busy_entities: continue
                if ally.stats.army < self.profile.min_attack_reserve: continue

                dist = ally.grid_point.dist_to(target.grid_point)
                unit_atk, unit_speed = self.cmd.get_unit_stats(ally)
                travel_time = dist / unit_speed

                if travel_time > self.profile.swarm_response_time: continue

                # 簡單路徑評估
                estimated_loss = PathAnalyzer.estimate_danger_linear(
                    start = ally.grid_point,
                    end = target.grid_point,
                    unit_speed = unit_speed,
                    enemy_buildings = self.cmd.enemy_buildings,
                    steps = max(5, int(travel_time // 2))
                )
                arrival_army = max(0.0, ally.stats.army - estimated_loss)
                if arrival_army < (ally.stats.army * 0.6): continue

                power = arrival_army * unit_atk
                attackers.append((ally, power))
                total_attack_power += power

            required_power = enemy_defense * self.profile.swarm_win_margin

            if total_attack_power > required_power:
                # 發起集結！
                score = (total_attack_power - enemy_defense) / 10 + self.cmd.get_strategic_value(target)

                for ally, power in attackers:
                    actions.append({
                        AIActionKey.TYPE: AIActionType.ATTACK,
                        AIActionKey.SCORE: score,
                        AIActionKey.TARGET: target,
                        AIActionKey.SOURCE: ally,
                        AIActionKey.OWNER: target.stats.owner
                    })
                    busy_entities.add(ally) # 立即標記忙碌，避免被單體攻擊選中

                # 集結只選定一個目標，發動後就結束本次判斷
                return actions

        return actions

    def _eval_attack_batch(self, busy_entities: set, candidates: List["BuildingEntity"] = None) -> list:
        """ [單體進攻決策] """
        actions = []
        targets = self.cmd.enemy_buildings + self.cmd.neutral_targets
        if not targets: return actions

        # 這樣就算他們很遠，我們也會嘗試評估
        high_value_targets = sorted(
            targets,
            key=lambda t: self.cmd.get_strategic_value(t),
            reverse=True
        )[:3]

        source_list = candidates if candidates is not None else self.cmd.my_buildings

        for source in source_list:
            if source in busy_entities: continue
            if source.stats.army < self.profile.min_attack_reserve: continue

            candidates_with_path = []

            # 加入最近的目標
            local_best, local_dist, local_path = TargetSelector.find_best_target(source, targets, top_k=3)
            if local_best:
                candidates_with_path.append((local_best, local_dist, local_path))

            # 強制加入高價值目標
            for hv_target in high_value_targets:
                if hv_target == local_best: continue
                if hv_target == source: continue
                if hv_target.stats.owner == source.stats.owner: continue

                hv_best, hv_dist, hv_path = TargetSelector.find_best_target(source, [hv_target], top_k=1)

                if hv_best and hv_path:
                    candidates_with_path.append((hv_target, hv_dist, hv_path))

            # --- [評分階段] ---
            best_action_data = None
            max_score = -float('inf')

            for target, path_len, path in candidates_with_path:
                # 安全性評估 (使用 path)
                danger_cost = PathAnalyzer.calculate_danger_cost(path, self.cmd.enemy_buildings, source)
                arrival_army = source.stats.army - danger_cost
                if arrival_army <= 0: continue

                # 門檻計算
                is_neutral = target.stats.owner == GameType.Owner.NEUTRAL
                is_castle = target.stats.arch == GameType.Arch.CASTLE

                threshold = self.profile.threshold_attack_neutral if is_neutral else self.profile.threshold_attack_base
                if not is_neutral and is_castle:
                    threshold += self.profile.threshold_attack_castle_buffer

                # 優勢計算
                unit_atk, unit_speed = self.cmd.get_unit_stats(source)
                target_defense = target.stats.army * target.stats.defense
                advantage = (arrival_army * unit_atk) - target_defense

                if advantage > threshold:
                    # 時間懲罰
                    time_penalty = max(path_len / unit_speed, 1.0)

                    score = (advantage + 10) / (time_penalty ** 0.5)
                    score *= self.cmd.get_strategic_value(target)

                    if is_neutral:
                        score *= self.profile.val_attack_neutral

                    score *= self.profile.weight_attack

                    if score > max_score:
                        max_score = score
                        best_action_data = {
                            AIActionKey.TYPE: AIActionType.ATTACK,
                            AIActionKey.SCORE: score,
                            AIActionKey.TARGET: target,
                            AIActionKey.SOURCE: source,
                            AIActionKey.OWNER: target.stats.owner
                        }

            if best_action_data:
                actions.append(best_action_data)

        return actions
