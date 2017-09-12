#!usr/bin/python
# -*- coding:utf-8 -*-

from common.Log import *
from Server import *
from common.DeviceManager import *
import threading

class ServerManager:
    def __init__(self):

        self.testdevices = DeviceManager.testdevices
        self.disconnectdevices = DeviceManager.disconnectdevices
        self.serverobjects = []
        self.threads = []
        self.logger = Log.logger

    def start_all_server(self):
        for deviceid,device in self.testdevices.iteritems():
            server = Server(device)
            self.serverobjects.append(server)
            thread1 = threading.Thread(target=server.start)
            thread1.start()

    def stop_all_server(self):
        for server in self.serverobjects:
            server.stop()

    def list_devices(self):
        info = u"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~已连接的设备~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        self.logger.info(info)
        for deviceid,device in self.testdevices.iteritems():
            server = Server(device)
            server.list_connect_devices()
        info = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        self.logger.info(info)

    def list_disconnect_devices(self):
        info = u"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~丢失的设备~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        self.logger.info(info)
        for deviceid, device in self.disconnectdevices.iteritems():
            server = Server(device)
            server.list_disconnect_devices()
        info = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        self.logger.info(info)




