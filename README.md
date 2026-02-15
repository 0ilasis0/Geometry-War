# 🔷 Geometry War (幾何戰爭)

此專題為作者於自學 **Python、AI 與 C 語言協同運作** 時所開發的一個完整塔防策略遊戲。
專案重點在於 **底層遊戲引擎架構的實現** 與 **系統模組化設計**，主要特色如下：

- **混合語言架構**：Python 負責邏輯與渲染，底層 A* 尋路算法由 C 語言編譯之 DLL 執行。
- **所見即所得 (WYSIWYG)**：基於 RenderProxy 的互動系統，解決 UI 遮擋與點擊穿透問題。
- **資料驅動 (Data-Driven)**：UI 佈局、文字內容皆由 JSON 動態載入，方便擴充與維護。
- **模組化資源管線**：自動化 Sprite 切割、圖片變換與快取管理。

---

## 🎮 主要功能與遊戲說明

### 塔防戰鬥機制
- **網格建造**：玩家需在有限的地圖網格上，策略性地配置防禦塔。
- **資源管理**：透過擊敗敵人或建造生產單位獲取資源，用於升級或建造更多防禦。
- **勝利條件**：將場上所有非中立（灰色）與敵方建築染上我方顏色即獲勝。

---

## 📖 遊戲說明 (Gameplay)

本遊戲為策略塔防類型，玩家需透過建造幾何建築來抵禦敵人並擴張領地。

1. 建築單位介紹
- **🏭 工廠 (圓形)**：生產核心。等級越高，生產士兵/資源的速度越快。
- **🏰 城堡 (方形)**：防禦核心。對範圍內的敵人進行砲擊，升級可提升射速與傷害。
- **🧪 實驗室 (三角形)**：戰術核心。提供特殊技能（如：癱瘓敵方建築、腐蝕敵兵、策反單位）。
- **💠 地基 (菱形)**：基礎單位。可轉型為上述三種建築，自身具備微弱的生產與防禦能力。

2. 遊戲機制
- **升級系統**：當建築右下角出現「藍色箭頭」時，代表資源足夠，點擊即可消耗士兵進行升級。
- **屬性識別**：建築頭頂的幾何圖形數量代表等級；下方圖示分別代表容量、產兵效率、移速與防禦力。
- **勝利條件**：將場上所有非中立（灰色）與敵方建築染上我方顏色即獲勝。

---

## 🖼️ 截圖展示
![screenshot1](screenshot/screenshot1.png)
![screenshot2](screenshot/screenshot2.png)
![screenshot3](screenshot/screenshot3.png)
![screenshot4](screenshot/screenshot4.png)
![screenshot5](screenshot/screenshot5.png)
![screenshot6](screenshot/screenshot6.png)

---

## 💡 技術亮點 (Technical Highlights)
### 1. Python/C 混合編程 (C Extensions)
為了突破 Python 在大量迴圈運算上的效能瓶頸，本專案將 A (A-Star) 路徑搜尋演算法* 使用 C 語言重寫。
整合方式：編譯為 core/dll/a_star.dll，並透過 ctypes 與 Python 介接。
效益：大幅提升了敵人尋路與大量單位移動的運算效率。

### 2. 渲染代理 (Render Proxy)
實作 Render-as-Registration (渲染即註冊) 機制解決 UI 互動問題：
機制：每一幀繪製時，物件將自身的 Collision Rect 與 Z-Index 註冊到 RenderProxy。
判定：點擊時，代理器反向遍歷（Reversed Z-Order）判定最上層物件。
結果：徹底根除「點擊到被遮擋物件」的 Bug，實現精確的滑鼠互動。

### 3. 自動化資源管線
ImgManager：實作 Sprite Sheet 自動切割、圖片動態變換 (Scale/Rotate) 與雜湊快取 (Hash Caching)。
FontManager：支援多語言 JSON 對照與排版渲染。

---

## ⚙️ 核心特性
- 混合語言架構 (Hybrid Architecture)：Python 負責邏輯與渲染，C 語言負責密集運算 (A*)。
- 資料驅動 (Data-Driven)：UI 佈局、文字內容、關卡設定皆由 JSON 動態載入。
- 所見即所得 (WYSIWYG)：解決 UI 遮擋與點擊穿透問題的互動系統。

---

## 🤖 AI 決策系統 (AI Decision System)
本專案實作了一套分層式 (Hierarchical) 與 效用導向 (Utility-based) 的 AI 架構，模擬真實玩家的戰略思考流程。AI 不僅僅是隨機行動，而是具備「感知 -> 戰略分析 -> 戰術決策 -> 執行」的完整迴路。

### 三層式大腦架構 (Brain Architecture)
AI 的運作分為三個層級，確保決策的邏輯性與執行效率：

1. 戰略層 (Strategy Layer)：StrategyAnalyzer
- **職責**：分析全場局勢（敵我兵力比、產能差距）。
- **動態狀態機**：根據局勢切換模式（如 `EARLY_EXPAND` 開局擴張、`SURVIVAL` 劣勢龜縮）。
- **影響**：動態調整 `AIProfile` 全域權重。

- 影響：動態調整 AIProfile 中的全域權重（例如：劣勢時大幅提升 weight_defense）。

2. 戰術層 (Tactical Layer)：AIBrain & Evaluators
- **職責**：具體的行動評估。包含 `Combat` (戰鬥)、`Economy` (經濟)、`Logistics` (後勤)、`Lab` (科技) 四大模組。
- **路徑分析**：引入 `PathAnalyzer` 預估路徑戰損，避免自殺式攻擊。

3. 執行層 (Execution Layer)：AIExecutor
- **職責**：將抽象指令轉換為具體操作。
- **擬人化**：引入 `action_interval` (APM限制) 與隨機波動，模擬人類操作延遲。

### 性格特質系統 (Personality Traits)
不同顏色的 AI 擁有截然不同的行為模式，透過 AIProfile 與 TraitData 進行參數化配置。系統支援多重特質疊加 (Trait Mixing)，創造出豐富的對手體驗：

| 陣營顏色 | 性格流派 | 行為特徵 |
| :--- | :--- | :--- |
| **🟥 紅色** | **狂戰士 (Berserker)** | 極具侵略性，忽視防禦塔威脅，偏好快攻與游擊 (Guerilla)。 |
| **🟩 綠色** | **蟲群 (Hivemind)** | 不重視科技升級，專注於佔領中立資源與無腦暴兵，集結門檻極低。 |
| **🟨 黃色** | **大法師 (Archmage)** | 保守防禦 (Turtle)，極度重視存錢，只為了頻繁施放高階魔法 (惡魔)。 |
| **🟪 紫色** | **幻術師 (Spell Weaver)** | 高頻率施放低費法術 (冰/毒) 干擾玩家經濟，針對敵方後勤進行破壞 (Saboteur)。 |

### 決策權重範例 (Utility Function)
AI 的決策並非寫死 (Hard-coded)，而是基於 效用函數 (Utility Function) 計算。例如在評估「是否進攻」時：
> **Score** = [(我方預估剩餘兵力 × 攻擊力) - 敵方防禦] / (路徑時間 ^ 0.5) × 戰略價值 × 性格修正
這使得 AI 在面對不同地圖與局勢時，能展現出非線性的、類似直覺的應對策略。

---

## 📂 目錄結構（主要檔案 / 模組概覽）

```text

Geometry War/
├── background/             # 遊戲背景圖片資源
├── core/                   # 核心程式碼庫
│   ├── c_inc/              # C 語言標頭檔 (Headers)
│   ├── c_src/              # C 語言原始碼
│   │   └── a_star/         # 高效能 A* 路徑搜尋演算法實作
│   ├── dll/                # 編譯完成的動態連結庫 (a_star.dll)
│   ├── py/                 # Python 模組與管理器
│   │   ├── a_star/         # Python 對 C DLL 的介接層 (ctypes wrapper)
│   │   ├── font/           # 字型管理器 (FontManager)
│   │   ├── game/           # 遊戲核心邏輯 (Building, Enemy, Tower)
│   │   ├── hmi/            # 人機介面 (Human-Machine Interface)
│   │   ├── input/          # 輸入處理 (Mouse, Keyboard)
│   │   ├── json/           # JSON 設定檔讀取與解析
│   │   ├── page/           # 頁面狀態機與導航 (PageStateManager)
│   │   ├── path/           # 路徑管理與運算
│   │   ├── rendering/      # 渲染核心 (RenderProxy, RenderManager)
│   │   ├── resource/       # 資源載入器
│   │   ├── screen/         # 螢幕顯示管理 (ImgManager, DrawManager)
│   │   ├── trans/          # 轉場效果處理
│   │   ├── ui_layout/      # UI 佈局系統 (LayoutManager)
│   │   ├── compile_dll.py  # C 語言自動編譯腳本
│   │   └── ...             # 基礎模組 (base, debug, variable, interrupt 等)
│   └── game_main.py        # Python 原始碼進入點 (Entry Point)
├── data/                   # 遊戲數值與設定資料 (JSON)
├── font/                   # 字體檔案 (.ttf, .otf)
├── img/                    # 遊戲 Sprite 圖片素材
├── screenshot/             # README 展示用截圖
├── song/                   # 音效與背景音樂資源
├── game_main.exe           # 已打包的可執行檔 (Windows Build)
├── images.ico              # 程式圖示
└── README.md               # 專案說明文件

```

## 🚀 如何執行
### 方式一：直接執行 (Windows)
雙擊根目錄下的 game_main.exe 即可直接遊玩，無需安裝 Python 環境。

### 方式二：從原始碼執行 (開發者)
1. 環境需求
Python 3.10+
GCC 編譯器 (若需重新編譯 DLL)

2. 安裝依賴
pip install pygame-ce

3. 執行遊戲
python core/game_main.py

---

## ⌨️ 操作說明（預設鍵位）
### 滑鼠控制
- 左鍵：選取單位 / 建造建築 / 點擊 UI / 拖曳框選多個單位。
- 右鍵：取消選取 / 移除建築。

### 鍵盤控制
- 方向鍵：選單選項移動。
- Enter：確認。
- Backspace：返回上一頁。

---

## 📝 專案挑戰與架構決策 (Technical Decisions)
### 1. 解決 UI 互動的狀態同步問題
* **挑戰**：在早期的開發中，使用 `is_visible` 變數來管理按鈕點擊，常導致「看得到點不到」或「隱藏了卻還能點」的狀態不同步 Bug。
* **決策**：放棄傳統的狀態標記，設計了 **RenderProxy (渲染代理)** 模式。
* **實作**：採用 **「渲染即註冊 (Render-as-Registration)」** 機制——只有在當前幀被繪製的物件，才會被註冊到點擊判定列表中。這確保了邏輯與畫面的絕對一致性 (WYSIWYG)。

### 2. 突破 Python 運算瓶頸
* **挑戰**：當場上單位超過 100 個且同時進行尋路時，Python 的直譯器效能成為瓶頸，FPS 顯著下降。
* **決策**：採用 **混合語言編程 (Hybrid Programming)**。
* **實作**：識別出 A* 演算法為熱點 (Hotspot)，將其以 **C 語言** 重寫並編譯為 DLL。透過 `ctypes` 進行記憶體指針操作，在不犧牲 Python 開發效率的前提下，大幅提升了核心運算速度。

### 3. 設計擬人化的 AI 對手
* **挑戰**：傳統的狀態機 (FSM) AI 容易流於形式，缺乏戰略深度與變化。
* **決策**：實作 **分層式效用 AI (Hierarchical Utility AI)** 與 **性格特質 (Personality Traits)** 系統。
* **實作**：
    * **分層架構**：將 AI 拆解為 戰略 (Strategy) -> 戰術 (Tactical) -> 執行 (Execution) 三層，模擬人類「觀察局勢 -> 擬定計畫 -> 下達指令」的思考流。
    * **性格參數**：透過 `AIProfile` 配置不同陣營的參數（如：狂戰士忽視防禦、大法師偏好存錢），創造出多樣化的對局體驗。

### 4. 資料驅動 (Data-Driven) 的模組化設計
* **挑戰**：遊戲內容（如建築數值、UI 佈局、多語言文本）頻繁調整，硬編碼 (Hard-code) 導致維護困難。
* **決策**：建立完整的 JSON 資源管線。
* **實作**：所有的遊戲數值、介面座標、文字內容皆抽離至 JSON 檔案。這不僅實現了邏輯與數據的分離，也為未來支援 Mod 或熱更新打下基礎。
