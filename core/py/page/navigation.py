from py.base import Stack
from py.debug import dbg
from py.font.manager import font_mg
from py.hmi.config.manager import SysConfigManager
from py.hmi.help.manager import HelpManager
from py.hmi.menu.manager import MenuManager
from py.hmi.single.manager import SingleHmiManager
from py.hmi.single_menu.manager import SingleMenuManager
from py.input.keyboard.manager import keyboard_mg
from py.page.base import page_mg
from py.page.tree_path import tree_path_table
from py.screen.draw.manager import draw_mg
from py.screen.image.manager.core import img_mg
from py.variable import BOOT_PAGE, PageTable


class PageNavigator:
    def __init__(self, tree_path_table: dict, start_page: PageTable):
        self.tree_path_table = tree_path_table
        # 此Stack，專門存 PageTable
        self.history = Stack(start_page)

    def get_next_page_by_index(self, current_page: PageTable, index: int) -> PageTable | None:
        """ [查詢] 根據樹狀結構，查找下一個頁面 """
        node = self.tree_path_table.get(current_page)
        if not node:
            dbg.error(f"Page {current_page} not found in tree")
            return None

        return node.family_table.get(index)

    def visit(self, current_page: PageTable, next_page: PageTable):
        """ [動作] 執行前往下一頁的邏輯  """
        if not next_page: return

        # 判斷是否為「子頁面」
        node = self.tree_path_table.get(current_page)
        is_child = False

        # 確保 node 存在且 family_table 存在
        if node and hasattr(node, 'family_table') and next_page in node.family_table.values():
            is_child = True

        # 如果是子頁面，把「當前頁面」存起來，以便返回
        if is_child:
            self.history.push(current_page)

    def back(self) -> PageTable | None:
        return self.history.pop()

    def get_current_history_depth(self):
        return self.history.size()

    def reset_to_root(self):
        """ 清空歷史紀錄，只留根節點 """
        self.history.clear()
        self.history.push(BOOT_PAGE)
        return BOOT_PAGE



class BasePageNavigation:
    def __init__(self, tree_path_table) -> None:
        # 初始化 Navigator
        self.navigator = PageNavigator(tree_path_table, BOOT_PAGE)

        # 初始化 HMI Managers
        self.setup()

    def setup(self):
        self.menu_mg = MenuManager(self)
        self.single_menu_mg = SingleMenuManager(self)
        self.single_mg = SingleHmiManager(self)
        self.help_mg = HelpManager(self)
        self.sys_config_mg = SysConfigManager(self)

    def handle_tree_navigation(self, current_table: PageTable, selected_index: int):
        """
        [樹狀導航]
        由 ListManager 呼叫，負責查表並執行跳轉
        """
        # 問路 (只查詢，不改變狀態)
        next_page = self.navigator.get_next_page_by_index(current_table, selected_index)

        if next_page:
            # 執行前往 (改變 Stack 狀態 + 切換畫面)
            self.go_to_page(current_table, next_page)
        else:
            dbg.log(f"No next page defined for index {selected_index}")

    def go_to_page(self, current_page: PageTable, next_page: PageTable):
        ''' [前往下一頁] '''
        # 更新導航狀態 (是否 Push Stack 由 Navigator 決定)
        self.navigator.visit(current_page, next_page)

        # 執行切換動作 (通知所有人)
        self.switch_page(current_page, next_page)

    def back_to_prev(self, current_table: PageTable):
        ''' [返回上一頁] '''
        # 從 Stack 取得上一頁
        prev_page = self.navigator.back()

        if prev_page:
            # 執行切換動作
            self.switch_page(current_table, prev_page)
        else:
            dbg.log("No previous page in stack (Already at Root)")

    def switch_page(self, current_table: PageTable, change_page: PageTable):
        '''
        [執行切換]
        負責通知所有 Manager 切換 Context (副作用層)
        '''
        # 刷新資源 Manager
        img_mg.switch_page(change_page)
        draw_mg.switch_page(change_page)
        font_mg.switch_page(change_page)

        # 更新 PageManager 狀態
        page_mg.switch_page(change_page)
        page_mg.switch_boot(change_page)

        # 更新 KeyboardManager
        keyboard_mg.switch_page(change_page)

base_nav = BasePageNavigation(tree_path_table)
