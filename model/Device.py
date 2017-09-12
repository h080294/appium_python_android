#!usr/bin/python
#-*- coding:utf-8 -*-


class Device(object):

    def __init__(self, deviceid):
        self._deviceid = deviceid
        self._devicename = ""
        self._platformversion = ""
        self._platformname = ""
        self._bootstrapport = ""
        self._serverport = ""
        self._server = ""

    @property
    def deviceid(self):
        return self._deviceid

    @deviceid.setter
    def deviceid(self, value):
        self._deviceid = value

    @property
    def devicename(self):
        return self._devicename

    @devicename.setter
    def devicename(self, value):
        self._devicename = value

    @property
    def platformversion(self):
        return self._platformversion

    @platformversion.setter
    def platformversion(self, value):
        self._platformversion = value

    @property
    def platformname(self):
        return self._platformname

    @platformname.setter
    def platformname(self, value):
        self._platformname = value

    @property
    def bootstrapport(self):
        return self._bootstrapport

    @bootstrapport.setter
    def bootstrapport(self, value):
        self._bootstrapport = value

    @property
    def serverport(self):
        return self._serverport

    @serverport.setter
    def serverport(self, value):
        self._serverport = value

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, value):
        self._server = value










