from dataclasses import dataclass, fields
from enum import Enum
from typing import Tuple

from py.game.ai.profile.variable import AIParam


@dataclass
class AIProfile:
    """
    [AI 指揮官人格設定檔]
    決定 AI 的戰術風格、反應速度與決策偏好。
    """
    name: str = "Standard AI"

    # =========================================================================
    # [Metabolism] 基礎代謝與反應速度
    # =========================================================================
    strategy_interval: float = 4.0      # 思考策略間隔 (秒)
    think_interval: float = 1.2         # 大腦決策間隔 (秒)
    action_interval: float = 0.4        # 動作執行間隔 (秒)
    random_time_rate: Tuple[float, float] = (0.7, 1.3) # 反應時間隨機波動範圍
    max_batch_actions: int = 3          # 單次思考最多下達幾個指令 (多工能力)
    max_actions_per_frame: int = 2      # 每幀能做事情的最大件數

    # =========================================================================
    # [Economy & Build] 經濟與建設偏好
    # =========================================================================
    # 決定蓋什麼建築的傾向 (數值越高越愛蓋)
    bias_build_castle: float = 1.0      # 城堡 (人口/防禦)
    bias_build_production: float = 1.2  # 工廠 (產兵/進攻)
    bias_build_lab: float = 0.8         # 實驗室 (科技/魔法)

    # 決定升級什麼建築的權重 (Multiplier)
    weight_upgrade_base: float = 1.5        # 升級總體意願
    weight_upgrade_prototype: float = 3.0   # 地基變身 (最優先)
    weight_upgrade_castle: float = 1.0      # 升級城堡
    weight_upgrade_production: float = 1.2  # 升級工廠
    weight_upgrade_lab: float = 0.8         # 升級實驗室
    bonus_upgrade_unlock_skill: float = 2.0 # 如果升級這個建築能解鎖我 "想要" 的技能

    # 特殊升級加成 (如果升級會帶來這些效果，AI 會更想升)
    bonus_upgrade_speed: float = 1.5    # 跑速提升加成
    bonus_upgrade_defense: float = 1.2  # 防禦提升加成

    # =========================================================================
    # [Combat - Attack] 進攻策略
    # =========================================================================
    weight_attack: float = 2.0          # 主動進攻總意願 (戰略狀態會動態修改此值)

    # 對敵方建築的謹慎度
    threshold_attack_base: float = 3.0
    # 對中立生物的謹慎度
    threshold_attack_neutral: float = 1.5
    # 攻打防禦塔/城堡時的額外安全係數
    threshold_attack_castle_buffer: float = 2.5

    # 目標價值評估 (決定打誰)
    val_attack_castle: float = 1.0      # 打城堡的價值權重
    val_attack_production: float = 1.5  # 打工廠的價值權重 (斷敵糧草)
    val_attack_lab: float = 1.2         # 打實驗室的價值權重
    val_attack_neutral: float = 1.2     # 打中立怪的價值權重 (練功)

    # 進攻門檻
    min_attack_reserve: int = 5         # 建築內至少留多少兵才肯單獨出擊
    attack_win_margin: float = 6.0     # 單體攻擊時，戰力需高出防禦多少才打

    # =========================================================================
    # [Combat - Swarm] 協同攻擊 (集結)
    # =========================================================================
    swarm_interval: float = 3.0         # 每幾秒評估一次集結
    swarm_trigger_ratio: float = 0.65   # 全國總兵力達人口上限多少比例才考慮集結
    swarm_win_margin: float = 1.2       # 集結戰力需是敵方防禦的幾倍
    swarm_response_time: float = 8.0    # 只有能在幾秒內抵達的隊友會被徵召

    # =========================================================================
    # [Combat - Defense] 防守策略
    # =========================================================================
    weight_defense: float = 1.2         # 防守/救援總意願
    min_defense_reserve: int = 5        # 救援別人時，自己家裡至少要留多少兵
    defense_scan_range: int = 25        # 救援掃描範圍 (格)

    # =========================================================================
    # [Lab & Magic] 實驗室與技能
    # =========================================================================
    weight_use_skill: float = 4.0       # 使用技能的總意願

    # 技能偏好 (Bias)
    bias_skill_ice: float = 1.0         # 冰凍 (控場)
    bias_skill_weak: float = 1.2        # 虛弱 (削弱)
    bias_skill_demon: float = 1.5       # 惡魔 (大招)

    # 當 AI 決定要存大招時，運補的急迫度倍率
    bias_lab_saving: float = 3.0
    # 實驗室日常運補的偏好
    bias_lab_supply: float = 1.2
    # 實驗室兵量低於多少比例開始請求運補
    lab_min_army_ratio: float = 0.3

    # 實驗室運補 (為了存錢做藥)
    lab_min_army_ratio: float = 0.3     # 實驗室兵量低於多少比例開始請求運補

    # 技能目標偏好 (數值越高越喜歡對該目標放招)
    # 冰凍 (Ice)：傾向控場，阻止對方大軍或防禦
    bias_ice_castle: float = 1.5      # 冰城堡 (阻止反擊/生兵)
    bias_ice_production: float = 0.8  # 冰工廠
    bias_ice_lab: float = 1.0         # 冰實驗室 (阻止放招)

    # 虛弱 (Weak)：傾向削弱產能
    bias_weak_castle: float = 0.8
    bias_weak_production: float = 3.0 # 毒工廠 (效益最大)
    bias_weak_lab: float = 1.2

    # 惡魔 (Demon)：傾向搶奪高價值目標
    bias_demon_neutral: float = 1.2   # 搶中立怪 (擴張)
    bias_demon_enemy: float = 1.0     # 搶敵人 (削弱)

    # =========================================================================
    # [Logistics] 後勤運補
    # =========================================================================
    weight_transfer: float = 0.8        # 運補總權重
    bias_frontline_supply: float = 1.5  # 對前線(危險區)的運補偏好

    def __post_init__(self):
        """
        [安全性檢查]
        確保 AIProfile 的屬性與 AIParam Enum 完全同步。
        如果兩邊不一致，會在啟動時報錯，防止參數名稱打錯。
        """
        # 取得目前 Profile 所有欄位名稱的集合
        profile_fields = {f.name for f in fields(self)}

        # 排除掉不是參數的欄位 (例如 name)
        # 這裡假設 AIParam 裡面的都是我們關心的參數
        for param in AIParam:
            attr_name = param.value
            if attr_name not in profile_fields:
                raise AttributeError(f"[AIProfile] Missing field defined in AIParam: '{attr_name}'")
