#!usr/bin/python
# -*- coding:utf-8 -*-
import os
import re
from DataProvider import *
from Log import *
import requests


class DeviceManager(object):

    # 连接的设备ID
    connectdeviceid = []

    # 待测的设备对象
    testdevices = {}

    # 已建立服务的设备
    serverdevices = {}

    # 设备库中未连接的设备
    disconnectdevices = {}

    # 连接设备imei
    connectimei = []

    logger = None

    @classmethod
    def get_connect_deviceid(cls):
        p = os.popen('adb devices')
        outstr = p.read()
        cls.connectdeviceid = re.findall(r'(\w+)\s+device\s',outstr)
        if 0 == len(cls.connectdeviceid):
            Log.logger.warn(u'没有adb连接的设备')
        else:
            return cls.connectdeviceid

    # Server用来获得已链接自己的服务器
    @classmethod
    def get_test_device(cls):
        for deviceid in cls.connectdeviceid:
            if DataProvider.devices.has_key(deviceid):
                cls.testdevices[deviceid] = DataProvider.devices[deviceid]
            else:
                Log.logger.warn(u'设备: %s 不在配置列表中' % deviceid)

        if len(cls.testdevices) == 0:
            Log.logger.warn(u'没有待测试的设备')


    # 客户端用来获取server上已经建立好服务的设备
    @classmethod
    def get_server_test_device(cls):
        for deviceid,device in DataProvider.devices.iteritems():
            url = "http://%s:%s/wd/hub" % (device.server,device.serverport)
            response = None
            try:
                response = requests.request("get", url)
            except requests.RequestException,e:
                pass
            if response != None:
                cls.serverdevices[deviceid] = device
            else:
                cls.disconnectdevices[deviceid] = device

    @classmethod
    def get_connect_device_imei(cls):
        for device in cls.connectdeviceid:
            cmd = "adb -s %s shell service call iphonesubinfo 1 | awk -F \"'\" '{print $2}' | sed '1 d' | tr -d '.' | awk '{print}' ORS=" % device
            p = os.popen(cmd)
            outstr = p.read()
            print device,
            print outstr

    @classmethod
    def get_device_info(cls, deviceId):
        mode = "ro.product.model"
        release = "ro.build.version.release"
        getmode = "adb -s %s shell cat /system/build.prop |grep %s" % (deviceId, mode)
        getrelease = "adb -s %s shell cat /system/build.prop |grep %s" % (deviceId, release)
        p1 = os.popen(getmode)
        p2 = os.popen(getrelease)
        modename = p1.read()
        releasename = p2.read()
        print deviceId
        print modename, releasename


if __name__ == "__main__":
    DeviceManager.get_connect_deviceid()



