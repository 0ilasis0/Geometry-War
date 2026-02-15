from typing import Dict, List, Tuple

from py.game.ai.profile.personality import AITraits, TraitData
from py.game.variable import GameType

TraitMix = List[Tuple[TraitData, float]]

class AIConfig:
    """
    [AI 配置表]
    定義各個陣營顏色預設的性格組合。
    """
    # 預設的陣營性格映射表
    FACTION_DEFAULTS: Dict[GameType.Owner, TraitMix] = {

        # --- 紅色：狂戰士流 (高壓快攻) ---
        GameType.Owner.RED: [
            (AITraits.BERSERKER, 7.0),
            (AITraits.EXPANSIONIST, 3.0),
            (AITraits.GUERILLA, 1.0), # 加一點游擊，稍微會偷襲工廠
            (AITraits.FRENZY, 1.0)
        ],

        # --- 綠色：蟲群流 (無腦暴兵) ---
        GameType.Owner.GREEN: [
            (AITraits.HIVEMIND, 4.0),
            (AITraits.EXPANSIONIST, 3.0),
            (AITraits.TURTLE, 0.5),
            (AITraits.LIGHTNING_REFLEXES, 1.0)
        ],

        # --- 黃色：大法師流 (存錢放惡魔) ---
        GameType.Owner.YELLOW: [
            (AITraits.ECONOMIST, 2.0),
            (AITraits.ARCHMAGE, 2.0),
            (AITraits.NECROMANCER, 3.0),
            (AITraits.TURTLE, 1.0),
            (AITraits.DEEP_THINKER, 1.0)
        ],

        # --- 紫色：幻術師流 (控場消耗 + 穩定節奏) ---
        GameType.Owner.PURPLE: [
            (AITraits.SPELL_WEAVER, 5.0),       # 主戰略：高頻率施法 (不存大招)
            (AITraits.SABOTEUR, 3.0),           # 副戰略：針對敵方後勤 (冰工廠/毒實驗室)
            (AITraits.GUERILLA, 2.0),           # 小戰略：游擊騷擾
            (AITraits.TURTLE, 1.0),             # 保守一點
            (AITraits.CLOCKWORK, 1.0)
        ],
    }

    @staticmethod
    def get_traits_for_faction(owner: GameType.Owner) -> TraitMix:
        """ 取得該陣營的性格配方，如果沒有定義則回傳空列表 (標準 AI) """
        return AIConfig.FACTION_DEFAULTS.get(owner, [])
