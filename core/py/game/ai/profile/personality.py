from typing import Dict

from py.game.ai.profile.variable import AIParam

# 定義特質的類型別名 (Key 變成了 AIParam Enum)
TraitData = Dict[AIParam, float]

class AITraits:
    """
    [性格特質資料庫]
    定義每一種性格 "1個單位強度" 會對參數造成什麼影響 (加減法)。
    """
    # --- [狂戰士]：極度好戰，忽視防守，門檻極低 ---
    BERSERKER: TraitData = {
        AIParam.WEIGHT_ATTACK: 0.5,
        AIParam.WEIGHT_DEFENSE: -0.2,
        AIParam.THRESHOLD_ATTACK_BASE: -1.5,
        AIParam.THRESHOLD_ATTACK_NEUTRAL: -0.5,
        AIParam.MIN_ATTACK_RESERVE: -1.0,
        AIParam.BIAS_BUILD_PRODUCTION: 0.3,
    }

    # --- [龜縮者]：喜歡蓋塔，存錢，不主動出門 ---
    TURTLE: TraitData = {
        AIParam.WEIGHT_ATTACK: -0.3,
        AIParam.WEIGHT_DEFENSE: 0.8,
        AIParam.THRESHOLD_ATTACK_BASE: 2.0,
        AIParam.BIAS_BUILD_CASTLE: 0.5,
        AIParam.WEIGHT_UPGRADE_CASTLE: 0.4,
        AIParam.MIN_DEFENSE_RESERVE: 2.0,
    }

    # --- [科技狂]：專注實驗室與技能 ---
    TECHNOLOGIST: TraitData = {
        AIParam.BIAS_BUILD_LAB: 0.6,
        AIParam.WEIGHT_UPGRADE_LAB: 1.0,
        AIParam.WEIGHT_USE_SKILL: 1.5,
        AIParam.BIAS_LAB_SUPPLY: 0.5,
        AIParam.BONUS_UPGRADE_UNLOCK_SKILL: 1.5,
        AIParam.BIAS_WEAK_PRODUCTION: 0.5,
        AIParam.BIAS_ICE_CASTLE: 0.5,
    }

    # --- [擴張者]：喜歡搶中立，搶地盤 ---
    EXPANSIONIST: TraitData = {
        AIParam.VAL_ATTACK_NEUTRAL: 1.0,
        AIParam.THRESHOLD_ATTACK_NEUTRAL: -1.0,
        AIParam.WEIGHT_UPGRADE_PROTOTYPE: 0.5,
        AIParam.BIAS_DEMON_NEUTRAL: 0.8,
    }

    # --- [經濟學家 (The Economist)] ---
    # 風格：喜歡升級所有建築，追求質量大於數量，不輕易開戰。
    # 弱點：前期兵少，容易被快攻。
    ECONOMIST: TraitData = {
        AIParam.WEIGHT_ATTACK: -0.4,          # 不愛打架
        AIParam.WEIGHT_UPGRADE_BASE: 0.8,     # 超級愛升級
        AIParam.WEIGHT_UPGRADE_PRODUCTION: 0.5,
        AIParam.THRESHOLD_ATTACK_BASE: 2.0,   # 非必勝不打
        AIParam.MIN_ATTACK_RESERVE: 3.0,      # 家裡要存很多兵才敢出門
    }

    # --- [游擊隊 (The Guerilla)] ---
    # 風格：極度重視跑速，喜歡偷襲敵方工廠(軟柿子)，避開城堡(硬骨頭)。
    # 強項：地圖控制力強，擾亂對手節奏。
    GUERILLA: TraitData = {
        AIParam.BONUS_UPGRADE_SPEED: 2.0,     # 跑速升級權重極高
        AIParam.VAL_ATTACK_PRODUCTION: 1.5,   # 專打工廠 (斷糧)
        AIParam.VAL_ATTACK_CASTLE: -1.0,      # 討厭打城堡
        AIParam.THRESHOLD_ATTACK_BASE: -0.5,  # 稍微冒險一點也要偷襲
        AIParam.WEIGHT_TRANSFER: 0.5,         # 喜歡調動兵力
    }

    # --- [蟲群意志 (The Hive Mind)] ---
    # 風格：人海戰術，集結門檻極低，源源不絕的進攻。
    # 強項：給予持續的兵線壓力。
    HIVEMIND: TraitData = {
        AIParam.SWARM_TRIGGER_RATIO: -0.2,    # 集結門檻降低 (原本0.65 -> 0.45)
        AIParam.SWARM_INTERVAL: -1.0,         # 集結檢查更頻繁
        AIParam.BIAS_BUILD_PRODUCTION: 0.8,   # 瘋狂蓋工廠
        AIParam.MIN_ATTACK_RESERVE: -3.0,     # 家裡幾乎不留兵，全軍出擊
        AIParam.WEIGHT_UPGRADE_BASE: -0.5,    # 不愛升級，只愛暴兵
    }

    # --- [攻城大師 (Siege Breaker)] ---
    # 風格：專門針對敵方城堡，無視防禦塔的威嚇。
    # 強項：破防能力強，適合打破僵局。
    SIEGE_BREAKER: TraitData = {
        AIParam.VAL_ATTACK_CASTLE: 2.0,             # 看到城堡就眼紅
        AIParam.THRESHOLD_ATTACK_CASTLE_BUFFER: -2.0, # 不怕防禦塔 (安全係數降低)
        AIParam.BIAS_SKILL_WEAK: 1.0,               # 喜歡用虛弱技能破防
        AIParam.BIAS_WEAK_CASTLE: 1.0,              # 專毒城堡
    }

    # --- [大法師 (Archmage)] ---
    # 風格：為了存出大招(惡魔)，願意犧牲前線，極端依賴實驗室運補。
    # 強項：瞬間爆發力最強。
    ARCHMAGE: TraitData = {
        AIParam.BIAS_BUILD_LAB: 1.0,
        AIParam.WEIGHT_UPGRADE_LAB: 0.5,      # 基礎升級意願普通
        AIParam.BONUS_UPGRADE_UNLOCK_SKILL: 2.0,
        AIParam.BIAS_LAB_SAVING: 4.0,         # 存錢意志極強 (全村把錢交出來!)
        AIParam.BIAS_LAB_SUPPLY: 1.0,         # 平常也喜歡運兵去實驗室
        AIParam.WEIGHT_USE_SKILL: 2.0,        # 技能狂熱
        AIParam.BIAS_SKILL_DEMON: 2.0,        # 只想放惡魔
    }

    # --- [守護者 (Guardian)] ---
    # 風格：雖然不主動進攻，但救援隊友的意識極強，防禦範圍超大。
    # 強項：很難被單點突破，適合團隊戰。
    GUARDIAN: TraitData = {
        AIParam.WEIGHT_DEFENSE: 2.0,          # 救援權重極高
        AIParam.DEFENSE_SCAN_RANGE: 15.0,     # 救援範圍大幅增加
        AIParam.BIAS_FRONTLINE_SUPPLY: 2.0,   # 極度重視前線補給
        AIParam.BONUS_UPGRADE_DEFENSE: 1.5,   # 喜歡升級防禦
        AIParam.VAL_ATTACK_CASTLE: -0.5,      # 不愛主動打主堡
    }

    # =========================================================================
    # [實驗室專精] - 針對特定技能流派
    # =========================================================================

    # --- [冰霜術士 (Cryomancer)] ---
    # 風格：控場大師。極度喜歡使用冰凍技能，目的是拖延敵軍節奏。
    # 戰術：優先冰凍敵方工廠（斷兵源）與城堡（阻止反擊）。
    CRYOMANCER: TraitData = {
        AIParam.WEIGHT_USE_SKILL: 1.5,        # 技能使用意願高
        AIParam.BIAS_SKILL_ICE: 3.0,          # 獨愛冰凍，其他技能無感
        AIParam.BIAS_SKILL_WEAK: -0.5,        # 不太用毒
        AIParam.BIAS_SKILL_DEMON: -0.5,       # 不太存大招

        AIParam.BONUS_UPGRADE_UNLOCK_SKILL: 0.5,
        # 控場偏好
        AIParam.BIAS_ICE_PRODUCTION: 2.0,     # 讓你的工廠停擺
        AIParam.BIAS_ICE_CASTLE: 1.5,         # 讓你的主堡閉嘴
        AIParam.BIAS_ICE_LAB: 1.0,            # 封印你的實驗室
    }

    # --- [煉金術士 (Alchemist)] ---
    # 風格：持續傷害流。喜歡用虛弱(毒藥)技能，打消耗戰。
    # 戰術：認為把敵人毒殘比直接打死更有效益，喜歡折磨血厚的建築。
    ALCHEMIST: TraitData = {
        AIParam.WEIGHT_USE_SKILL: 1.5,
        AIParam.BIAS_SKILL_WEAK: 3.0,         # 毒藥狂熱
        AIParam.BIAS_SKILL_ICE: -0.5,
        AIParam.BIAS_SKILL_DEMON: -0.5,

        AIParam.BONUS_UPGRADE_UNLOCK_SKILL: 1.0,

        # 上毒偏好
        AIParam.BIAS_WEAK_CASTLE: 2.0,        # 專毒血厚的城堡
        AIParam.BIAS_WEAK_PRODUCTION: 1.5,    # 毒工廠，生出來的兵也是殘血
        AIParam.BIAS_WEAK_LAB: 0.5,
    }

    # --- [死靈法師 (Necromancer)] ---
    # 風格：與「大法師(Archmage)」不同，死靈法師更看重「奪取敵方單位」。
    # 戰術：只要對面有高等級單位，就會想辦法把它變成自己的。
    # 區別：大法師注重"存錢過程"，死靈法師注重"目標選擇"。
    NECROMANCER: TraitData = {
        AIParam.WEIGHT_USE_SKILL: 2.0,
        AIParam.BIAS_SKILL_DEMON: 4.0,        # 只想放惡魔
        AIParam.BIAS_SKILL_ICE: -1.0,         # 不屑用小招
        AIParam.BIAS_SKILL_WEAK: -1.0,

        AIParam.BONUS_UPGRADE_UNLOCK_SKILL: 3.0,
        AIParam.WEIGHT_UPGRADE_LAB: 1.0,

        # 奪舍偏好
        AIParam.BIAS_DEMON_ENEMY: 2.5,        # 優先搶敵人的
        AIParam.BIAS_DEMON_NEUTRAL: 0.5,      # 中立的加減搶
        AIParam.VAL_ATTACK_NEUTRAL: -0.5,     # 不太想殺中立怪(想留著用招換)
    }

    # --- [破壞者 (Saboteur)] ---
    # 風格：極度討厭敵人的後勤補給。
    # 戰術：專門用技能(冰/毒)癱瘓敵人的工廠與實驗室，讓對手沒兵沒科技。
    SABOTEUR: TraitData = {
        AIParam.WEIGHT_USE_SKILL: 1.2,

        # 技能偏好均衡，看情況用
        AIParam.BIAS_SKILL_ICE: 1.0,
        AIParam.BIAS_SKILL_WEAK: 1.0,

        AIParam.BONUS_UPGRADE_UNLOCK_SKILL: 0.8,

        # 目標極度針對功能性建築
        AIParam.BIAS_ICE_PRODUCTION: 2.5,     # 冰封工廠
        AIParam.BIAS_WEAK_PRODUCTION: 2.5,    # 毒化工廠
        AIParam.BIAS_ICE_LAB: 2.0,            # 封印實驗室
        AIParam.BIAS_ICE_CASTLE: -0.5,        # 不太管城堡
    }

    # --- [咒文織法者 (Spell Weaver)] ---
    # 風格：快節奏法師。不存大招，有錢就丟小招(冰/毒)。
    # 戰術：透過高頻率的低費法術騷擾對手，讓對手疲於奔命。
    SPELL_WEAVER: TraitData = {
        AIParam.WEIGHT_USE_SKILL: 3.0,        # 手上只要有藥水一定丟出去
        AIParam.BIAS_LAB_SUPPLY: 1.5,         # 運補權重高(為了回魔)
        AIParam.BIAS_LAB_SAVING: -2.0,        # 討厭存錢 (有多少花多少)
        AIParam.BIAS_SKILL_DEMON: -5.0,       # 絕不使用惡魔

        AIParam.BONUS_UPGRADE_UNLOCK_SKILL: 0.5,

        # 喜歡便宜好用的招
        AIParam.BIAS_SKILL_ICE: 1.5,
        AIParam.BIAS_SKILL_WEAK: 1.5,
    }

    # =========================================================================
    # [Metabolism Traits] 生理時鐘與反應模組
    # =========================================================================

    # --- [閃電反射 (Lightning Reflexes)] ---
    # 風格：神經傳導快，擅長微操，但大局觀稍弱。
    LIGHTNING_REFLEXES: TraitData = {
        AIParam.THINK_INTERVAL: -0.3,
        AIParam.ACTION_INTERVAL: -0.1,
        AIParam.MULTITASKING: -1,
        AIParam.APM_LIMIT: 2,
    }

    # --- [深思熟慮 (Deep Thinker)] ---
    # 風格：大腦運算量大，反應慢半拍，但一次能下達很多指令。
    DEEP_THINKER: TraitData = {
        AIParam.STRATEGY_INTERVAL: -1.0,
        AIParam.THINK_INTERVAL: 0.4,
        AIParam.ACTION_INTERVAL: 0.05,
        AIParam.MULTITASKING: 3,
    }

    # --- [狂亂 (Frenzy)] ---
    # 風格：腎上腺素爆發，動作極快，但缺乏計畫性。
    FRENZY: TraitData = {
        AIParam.STRATEGY_INTERVAL: 1.0,
        AIParam.THINK_INTERVAL: -0.4,
        AIParam.ACTION_INTERVAL: -0.15,
        AIParam.APM_LIMIT: 2,
    }

    # --- [機械化 (Clockwork)] ---
    # 風格：穩定、標準、稍微優化過的效率。
    CLOCKWORK: TraitData = {
        AIParam.THINK_INTERVAL: -0.1,
        AIParam.ACTION_INTERVAL: -0.05,
        AIParam.MULTITASKING: 1,
    }

    # --- [遲鈍 (Sluggish)] ---
    # 風格：反應慢，適合低難度或殭屍類單位。
    SLUGGISH: TraitData = {
        AIParam.THINK_INTERVAL: 0.5,
        AIParam.ACTION_INTERVAL: 0.2,
        AIParam.APM_LIMIT: -1,
    }

    # --- [超腦 (Overmind)] ---
    # 風格：作弊般的存線，全知全能 (Boss 級)。
    OVERMIND: TraitData = {
        AIParam.STRATEGY_INTERVAL: -1.0,
        AIParam.THINK_INTERVAL: -0.4,
        AIParam.ACTION_INTERVAL: -0.1,
        AIParam.MULTITASKING: 4,
        AIParam.APM_LIMIT: 3,
    }