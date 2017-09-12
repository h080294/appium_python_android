#!usr/bin/python
# -*- coding:utf-8 -*-


class User(object):

    def __init__(self,uid):
        self._uid = uid
        self.username = ""
        self._mobile = ""
        self._password = ""

    @property
    def username(self):
        return self.username

    @username.setter
    def username(self,value):
        self._username = value

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self,value):
        self._uid = value

    @property
    def mobile(self):
        return self._mobile

    @mobile.setter
    def mobile(self,value):
        self._mobile = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,value):
        self._password = value



