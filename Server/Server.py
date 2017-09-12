#!usr/bin/python
# -*- coding:utf-8 -*-

from common.Log import *
import subprocess
import time
class Server:
    def __init__(self, deviceobject):
        self.logger = Log.logger
        self._deviceobject = deviceobject
        self._cmd = "appium -p %s -bp %s -U %s --session-override" % (
        self._deviceobject.serverport, self._deviceobject.bootstrapport, self._deviceobject.deviceid)

    def start(self):
        self.kill(self._deviceobject.serverport)
        time.sleep(3)
        info = u"启动设备:%s 对应的Appium Server" % self._deviceobject.devicename
        self.logger.info(info)
        self.logger.info(self._cmd)
        subprocess.call(self._cmd,shell=True)

    def stop(self):
        self.kill(self._deviceobject.serverport)

    def kill(self, port):
        cmd = "lsof -i:%s|awk 'NR==2{print $2}'" % port
        self.logger.info(cmd)
        pid = os.popen(cmd).read()
        cmd = "kill -9 %s" % pid
        os.popen(cmd).read()

    def list_connect_devices(self):
        info = u"已连接的设备： %s ------ %s" % (self._deviceobject.deviceid, self._deviceobject.devicename)
        self.logger.info(info)

    def list_disconnect_devices(self):
        info = u"！！！设备丢失！！！： %s ------ %s" % (self._deviceobject.deviceid, self._deviceobject.devicename)
        self.logger.info(info)
