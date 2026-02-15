from enum import Enum
from typing import TYPE_CHECKING

from py.debug import dbg
from py.ui_layout.name.registry import LayoutNameLoader, LayoutNameRegistry
from py.variable import PageTable


class LayoutName(str, Enum):
    '''
    一般 static_name ： 直接用 LayoutName.name 取出名稱
    大量dynaic_name ： 使用 get_name 取出名稱
    '''
    # 這段 '給 VS Code 看的' 宣告，實際不會跑
    if TYPE_CHECKING:
        serial_list: list[str]
        count: int

    def __new__(cls, content, count = 1):
        '''
        自定義的 Enum，支援自動產生序列名稱
        定義格式: 名稱 = ('字串值', 數量)
        如果沒有寫數量，預設為 1
        '''
        # 建立字串物件 (這一步保證了它依然是 str)
        obj = str.__new__(cls, content)

        # 設定 Enum 的實際值 (必須是字串)
        obj._value_ = content

        # 將數量存為這個成員的屬性
        obj.count = count

        # 順便直接生成 list 存起來，這樣以後直接讀屬性就好，不用再運算
        if count > 1:
            obj.serial_list = [f'{content}_{i}' for i in range(count)]
        else:
            obj.serial_list = [content]

        return obj

    @staticmethod
    def get_name(page: PageTable, index: int = 0, *path_parts) -> str | None:
        '''
        單一名稱尋找(用於非static_name)
        自動拼字 + 自動去 Registry 查證
        '''
        # 處理參數 (把 Enum 轉字串，組合成 Group Key)
        # 例如: 1, ARCH -> '1_ARCH'
        str_parts = [p.value if isinstance(p, Enum) else str(p) for p in path_parts]
        cat_name = '_'.join(str_parts)

        # 呼叫自己的拼字邏輯
        # 產生 'SINGLE_1_ARCH_0'
        target_name = LayoutNameLoader.create_name(page, (cat_name, index))

        # 去 Registry 確認
        if LayoutNameRegistry.exists(target_name):
            return target_name

        dbg.war(f'the {target_name} is not registered.')
        return None


    ''' --- 定義區域 ---  '''
    # BASE
    BASE_NUMBER_BIG         = ('BASE_NUMBER_BIG', 2)

    # BACKGROUND
    MENU_BG                 = 'MENU_BG'
    SINGLE_BG               = 'SINGLE_BG'
    SINGLE_MENU_BG          = 'SINGLE_MENU_BG'
    DOUBLE_BG               = 'DOUBLE_BG'
    ENDLESS_BG              = 'ENDLESS_BG'
    SYS_CONFIG_BG           = 'SYS_CONFIG_BG'
    HELP_BG                 = 'HELP_BG'
    RANK_BG                 = 'RANK_BG'

    # MENU
    MENU_BT_BOARD           = 'MENU_BT_BOARD'
    MENU_MAIN               = 'MENU_MAIN'
    MENU_USER               = 'MENU_RECT'

    # GAME
    SINGLE_MENU_MAIN        = 'SINGLE_MENU_MAIN'
    SINGLE_MENU_USER        = 'SINGLE_MENU_USER'
    SINGLE_MENU_RECT        = ('SINGLE_MENU_RECT', 10)
    SINGLE_MENU_LEVEL       = ('SINGLE_MENU_LEVEL', 10)

    GAME_OVER               = 'GAME_OVER'
    GAME_TEACH              = 'GAME_TEACH'

    GAME_BUILDING_ARMY      = 'GAME_BUILDING_ARMY'
    GAME_SELECT_CIRCLE      = 'GAME_SELECT_CIRCLE'
    GAME_CASTLE_RANGE_CIRCLE= 'GAME_CASTLE_CIRCLE'
    GAME_STATUS_BAR         = 'GAME_STATUS_BAR'
    GAME_STATUS_WORD        = 'GAME_STATUS_FONT'
    GAME_JELLY_WORD         = 'GAME_JELLY_WORD'
    GAME_UPGRADE            = 'GAME_UPGRADE'
    GAME_UPGRADE_USER       = 'GAME_UPGRADE_USER'
    GAME_UPGRADE_USER_PRICE = 'GAME_UPGRADE_USER_WORD'
    GAME_VFX_LAB_IMPACT     = 'GAME_VFX_LAB_IMPACT'
    GAME_VFX_LAB_READY      = 'GAME_VFX_LAB_READY'
    GAME_PROGRESS_BAR       = 'GAME_PROGRESS_BAR'
    GAME_FACTION_BAR_COLOR  = 'GAME_FACTION_BAR_COLOR'
    GAME_FACTION_BAR        = 'GAME_FACTION_BAR'
    GAME_FACTION_BAR_ARMY   = 'GAME_FACTION_BAR_ARMY'
    GAME_ABILITY            = ('GAME_ABILITY', 3)
    GAME_ABILITY_PRICE      = 'GAME_ABILITY_WORD'
    GAME_BECOME             = ('GAME_BECOME', 3)
    GAME_BECOME_PRICE       = 'GAME_BECOME_PRICE'

    OBSTACLE_BOARD          = 'OBSTACLE_BOARD'
    OBSTACLE_PEN1           = ('OBSTACLE_PEN1', 2)
    OBSTACLE_PEN3           = 'OBSTACLE_PEN3'
    OBSTACLE_PEN_CROSS      = 'OBSTACLE_PEN_CROSS'
    OBSTACLE_COMPASS        = ('OBSTACLE_COMPASS', 2)
    OBSTACLE_ERASER         = 'OBSTACLE_ERASER'
    OBSTACLE_RULER          = 'OBSTACLE_RULER'

    # SYS_CONFIG
    SYS_SONG_MAIN           = 'SYS_SONG_MAIN'
    SYS_SONG_USER           = 'SYS_SONG_RECT'
    SYS_SONG_NAME           = 'SYS_SONG_NAME'
    SYS_SONG_BLOCK          = 'SYS_SONG_BLOCK'
    SYS_WINDOW_SCALE        = 'SYS_WINDOW_SCALE'

    # HELP
    HELP_PANEL              = 'HELP_PANEL'
    HELP_LACE               = 'HELP_LACE'
    HELP_OPTION_TITLE       = 'HELP_OPTION_TITLE'
    HELP_OPTION_DESC        = 'HELP_OPTION_DESC'
