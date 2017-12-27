# -*- coding: utf-8 -*-
import sqlite3
import threading
SQL_SELECT_STATICTEXT = "SELECT text FROM static_strings WHERE cname = '%s'"
SQL_SELECT_STATICFULL = "SELECT * FROM '%s' WHERE cname = '%s'"
SQL_SELECT_STATICARREY = "SELECT %s FROM '%s' WHERE cname = '%s'"
SQL_SELECT_CNBYTXT = "SELECT cname FROM static_strings WHERE text = '%s' "
SQL_SELECT_CNBYSTCN = "SELECT action FROM inputs WHERE static_string = '%s' "


lock = threading.Lock()


class Provider:

    def __init__(self, database):
        self.db = database
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_static_text(self, cname):
        with self.connection:
            res = ''
            try:
                lock.acquire(True)
                res = self.cursor.execute(SQL_SELECT_STATICTEXT % (cname,)).fetchone()[0]
            finally:
                lock.release()
                return res

    def get_static_data(self, table, cname):
        with self.connection:
            res = ()
            try:
                lock.acquire(True)
                res = self.cursor.execute(SQL_SELECT_STATICFULL % (table, cname)).fetchone()
            finally:
                lock.release()
                return res

    def get_static_array(self, column, table, cname):
        with self.connection:
            result = []
            res = ()
            try:
                lock.acquire(True)
                for inst in self.cursor.execute(SQL_SELECT_STATICARREY % (column, table, cname)).fetchall():
                    result += inst
            finally:
                lock.release()
            return result

    def get_action_by_text(self, txt):
        with self.connection:
            stcn = ()
            input = ''
            try:
                # print('DUBLE DUNGER')
                lock.acquire(True)
                # print('pre acq')
                stcn = self.cursor.execute(SQL_SELECT_CNBYTXT % (txt,)).fetchone()[0]
                itcn = self.cursor.execute(SQL_SELECT_CNBYSTCN % (stcn,)).fetchone()[0]
                # print('pffff')
                # input = Input(self, itcn)
                input = itcn
                # print('super pfff')
                # print(input)
            finally:
                lock.release()
                return input

    def close(self):
        self.connection.close()


class Page:
    table_name = 'pages'

    def __init__(self, provider, cname):
        self.cname, self.priority, self.content, cname_menu = provider.get_static_data(self.table_name, cname)
        self.menu = Menu(provider, cname_menu)


class Menu:
    table_name = 'menus_inputs'
    input_column = 'input'

    def __init__(self, provider, cname):
        self.cname = cname
        self.inputs = []
        for cname_input in provider.get_static_array(self.input_column, self.table_name, cname):
            self.inputs += [Input(provider, cname_input)]


class Input:
    table_name = 'inputs'

    def __init__(self, provider, cname):
        self.cname, self.static_string, self.action = provider.get_static_data(self.table_name, cname)
        self.text = provider.get_static_text(self.static_string)




def test():
    tstvider = Provider('./static.db')
    print(tstvider.get_static_text('welcome'))
    print(tstvider.get_static_data('pages', 'welcome_page'))
    print(tstvider.get_static_array('input', 'menus_inputs', 'main_map'))
    tst_page = Page(tstvider, 'welcome_page')
    print(tst_page.cname)
    print(tst_page.content)
    tst_menu = tst_page.menu
    print(tst_menu.cname)
    for tst_inputs in tst_menu.inputs:
        print(tst_inputs.text)


if __name__ == '__main__':
    test()
