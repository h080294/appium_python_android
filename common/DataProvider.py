#!usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
from aetypes import template

import yaml
from common.Log import *
from model.Device import *
from model.User import *


class DataProvider(object):
    users = []
    devices = {}
    config = None
    niceapk = ""
    unlockapk = os.getcwd() + "apk/unlock_apk-debug.apk"
    settingapk = os.getcwd() + "apk/settings_apk-debug.apk"
    imeapk = os.getcwd() + "apk/UnicodeIME-debug.apk"
    testers = {}
    starttime = {}
    stoptime = {}
    devicenamelist = []

    @classmethod
    def init_data(cls):
        cls.init_config_yaml()
        cls.load_devices()
        cls.load_users()
        cls.load_others_config()
        cls.show_devicename_list()

    @classmethod
    def init_config_yaml(cls):
        filepath = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + '/config/config.yaml'
        with open(filepath, 'r') as stream:
            try:
                cls.config = yaml.load(stream)
            except yaml.YAMLError as exc:
                print 'yaml读取有误'
                print exc
            finally:
                stream.close()

    @classmethod
    def load_devices(cls):
        cls.devicenamelist = []
        for device in cls.config['Devices']:
            deviceobject = Device(device['deviceid'])
            deviceobject.devicename = device['devicename']
            deviceobject.serverport = device['serverport']
            deviceobject.bootstrapport = device['bootstrapport']
            deviceobject.platformname = device['platformname']
            deviceobject.platformversion = device['platformversion']
            deviceobject.server = device['server']
            cls.devices[deviceobject.deviceid] = deviceobject
            cls.devicenamelist.append(device['devicename'])
        Log.logger.info(u"配置列表中一共有 %s 台设备" % len(cls.devices))

    @classmethod
    def load_users(cls):
        for user in cls.config['Users']:
            userobject = User(user['uid'])
            userobject.username = user['username']
            userobject.mobile = user['mobile']
            userobject.password = user['password']
            cls.users.append(userobject)
        Log.logger.info(u"配置列表中一共有 %s 个用户信息" % len(cls.users))

    @classmethod
    def load_others_config(cls):
        if cls.config['NiceAPK']:
            cls.niceapk = cls.config['NiceAPK']
    @classmethod
    def show_devicename_list(cls):
        for i in range(len(cls.devicenamelist)):
            if i % 10 == 0:
                print cls.devicenamelist[i] + ','
                i += 1
            else:
                print cls.devicenamelist[i] + ',',
                i += 1

if __name__ == "__main__":
    DataProvider.init_data()
