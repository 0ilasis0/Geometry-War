class GridParameter:
    SINGLE_MENU_LEVEL_ROW = 2
    SINGLE_MENU_LEVEL_COLS = 5

class GridThing:
    LOCK_SWITCH_ = 'lock_switch'
    LOCK = 'lock'
    UNLOCK = 'unlock'

class HelpConfig:
    # hook_x 透明度矩陣
    # 例：title_alpha[hook_x][item_index] 表示對應透明度
    title_alpha = [
        [100, 20, 20],
        [20, 100, 30],
        [20, 20, 100],
    ]
