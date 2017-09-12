#!usr/bin/python
# -*- coding:utf-8 -*-

from common.DeviceManager import *
from common.Log import *
from common.DataProvider import *
import sys
import os
from Server.ServerManager import ServerManager

def run():
    # 初始化日志配置
    Log.create_log_file()

    Log.logger.info(u"加载设备及用户配置信息")
    DataProvider.init_data()

    Log.logger.info(u"获得ADB连接的设备")
    DeviceManager.get_connect_deviceid()

    if 0 == len(DeviceManager.connectdeviceid):
        Log.logger.info(u"没有连接的设备")
        sys.exit()
    else:
        Log.logger.info(u"当前已连接设备数: %s" % len(DeviceManager.connectdeviceid))

    Log.logger.info(u"获得待测试的设备")
    DeviceManager.get_test_device()
    DeviceManager.get_server_test_device()

    servermanager = ServerManager()
    servermanager.list_devices()

    if len(DeviceManager.disconnectdevices) > 0:
        Log.logger.info(u"丢失备数: %s" % len(DeviceManager.disconnectdevices))

    servermanager.list_disconnect_devices()
    servermanager.start_all_server()

if __name__ == "__main__":
    run()