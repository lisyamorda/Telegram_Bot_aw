# -*- coding: utf-8 -*-
# import sqlprovider

Users = {}


class User:
    def __init__(self, uid, username, first_name='Anonym', last_name='Anon', page=None):
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.cur_page = page
        self.history = []
        new_user(self)

    def goto(self, page):
        self.history.append(self.cur_page)
        self.cur_page = page

    def back(self):
        try:
            print(self.history)
            print(self.history[-1])
            print(self.history[0])
            if self.history[-1] is not None:
                self.cur_page = self.history[-1]
                self.history.remove(self.cur_page)
            print(self.history)
            print(self.history[-1])
            print(self.history[0])
        except Exception:
            pass


def is_registered(user):
    return user in Users


def get_user(uid):
    if uid in Users:
        return Users[uid]
    else:
        return None


def new_user(user):
    if not is_registered(user):
        Users[user.uid] = user


