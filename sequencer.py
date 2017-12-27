# -*- coding: utf-8 -*-


# Преобразуем строку обрамленную [] в функцию
# Функция статик возвращяет данные из схемы
# Функция актион выполняет последовательность действий в контексте оперирую аргументами
class Sequence:
    def __init__(self, static_handler=None, action_handler=None, dynamic_handler=None):
        self.static = static_handler
        self.action = action_handler
        self.dynamic = dynamic_handler

    def parse(self, data):
        items = data[1:-1].split(' ')
        if items[0] == 'static':
            table_name = items[1].split('=')[1]
            cname = items[2].split('=')[1]
            column = items[3].split('=')[1]
            return self.static(table_name, cname, column)
        if items[0] == 'action':
            a_context = items[1].split('=')[1]
            a_action = items[2].split('=')[1]
            a_args = items[3].split(',')
            return self.action(a_context, a_action, a_args)
        if items[0] == 'dynamic':
            pass


def static(table_name, cname, column):
    print("[Table: %s Code_Name: %s Column: %s]" % (table_name, cname, column))


# Действие в контексте с учетом аргументов
def action(a_context, a_action, a_args):
    print("[Context: %s Action: %s Args: %s]" % (a_context, a_action, a_args))


# Операция над базой данных
def dynamic(): pass


def test():
    tstseq = Sequence(static, action, dynamic)
    tstseq.parse('[static type=static_string cname=welcome data=text]')
    tstseq.parse('[action type=user action=new some_login,non_sec_pass,date]')


if __name__ == '__main__':
    test()