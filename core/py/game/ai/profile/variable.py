from enum import Enum


class AIParam(str, Enum):
    """
    [AI 參數鍵值表]
    對應 AIProfile 中的屬性名稱。
    繼承 str 讓它在使用 getattr/setattr 時可以直接被當作字串使用。
    """
    # --- [Metabolism] ---
    STRATEGY_INTERVAL = "strategy_interval"
    THINK_INTERVAL = "think_interval"
    ACTION_INTERVAL = "action_interval"
    MULTITASKING = "max_batch_actions"
    APM_LIMIT = "max_actions_per_frame"

    # --- [Economy & Build] ---
    BIAS_BUILD_CASTLE = "bias_build_castle"
    BIAS_BUILD_PRODUCTION = "bias_build_production"
    BIAS_BUILD_LAB = "bias_build_lab"

    # --- [Upgrade] ---
    WEIGHT_UPGRADE_BASE = "weight_upgrade_base"
    WEIGHT_UPGRADE_PROTOTYPE = "weight_upgrade_prototype"
    WEIGHT_UPGRADE_CASTLE = "weight_upgrade_castle"
    WEIGHT_UPGRADE_PRODUCTION = "weight_upgrade_production"
    WEIGHT_UPGRADE_LAB = "weight_upgrade_lab"

    BONUS_UPGRADE_SPEED = "bonus_upgrade_speed"
    BONUS_UPGRADE_DEFENSE = "bonus_upgrade_defense"
    BONUS_UPGRADE_UNLOCK_SKILL = "bonus_upgrade_unlock_skill"

    # --- [Combat - Attack] ---
    WEIGHT_ATTACK = "weight_attack"

    THRESHOLD_ATTACK_BASE = "threshold_attack_base"
    THRESHOLD_ATTACK_NEUTRAL = "threshold_attack_neutral"
    THRESHOLD_ATTACK_CASTLE_BUFFER = "threshold_attack_castle_buffer"

    VAL_ATTACK_CASTLE = "val_attack_castle"
    VAL_ATTACK_PRODUCTION = "val_attack_production"
    VAL_ATTACK_LAB = "val_attack_lab"
    VAL_ATTACK_NEUTRAL = "val_attack_neutral"

    MIN_ATTACK_RESERVE = "min_attack_reserve"
    ATTACK_WIN_MARGIN = "attack_win_margin"

    # --- [Combat - Swarm] ---
    SWARM_INTERVAL = "swarm_interval"
    SWARM_TRIGGER_RATIO = "swarm_trigger_ratio"
    SWARM_WIN_MARGIN = "swarm_win_margin"
    SWARM_RESPONSE_TIME = "swarm_response_time"

    # --- [Combat - Defense] ---
    WEIGHT_DEFENSE = "weight_defense"
    MIN_DEFENSE_RESERVE = "min_defense_reserve"
    DEFENSE_SCAN_RANGE = "defense_scan_range"

    # --- [Lab & Magic] ---
    WEIGHT_USE_SKILL = "weight_use_skill"

    BIAS_SKILL_ICE = "bias_skill_ice"
    BIAS_SKILL_WEAK = "bias_skill_weak"
    BIAS_SKILL_DEMON = "bias_skill_demon"

    BIAS_LAB_SAVING = "bias_lab_saving"
    BIAS_LAB_SUPPLY = "bias_lab_supply"
    LAB_MIN_ARMY_RATIO = "lab_min_army_ratio"

    # 技能目標偏好
    BIAS_ICE_CASTLE = "bias_ice_castle"
    BIAS_ICE_PRODUCTION = "bias_ice_production"
    BIAS_ICE_LAB = "bias_ice_lab"

    BIAS_WEAK_CASTLE = "bias_weak_castle"
    BIAS_WEAK_PRODUCTION = "bias_weak_production"
    BIAS_WEAK_LAB = "bias_weak_lab"

    BIAS_DEMON_NEUTRAL = "bias_demon_neutral"
    BIAS_DEMON_ENEMY = "bias_demon_enemy"

    # --- [Logistics] ---
    WEIGHT_TRANSFER = "weight_transfer"
    BIAS_FRONTLINE_SUPPLY = "bias_frontline_supply"