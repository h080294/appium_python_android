#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *
import subprocess
from common.DataProvider import *

class MZM2NotePreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(MZM2NotePreProcess, self).__init__(tester)

    #魅族情况太特殊，安装都得继承然后单独处理,弹出的adb安装权限直接阻塞了Server运行
    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid,DataProvider.niceapk)
        subprocess.call(cmd,shell=True)

    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 安装app并处理GPS弹窗" % self.tester.device.devicename)

            element = self.tester.find_element_by_id('android:id/button1',20)
            if element != None:
                self.action.tap(element).perform()

            #启动app
            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)
            self.driver.launch_app()

            # nice获取手机GPS权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

            # nice获取手机识别码权限
            time.sleep(1)

            element = self.tester.find_element_by_id('android:id/button1',20)
            if element != None:
                self.action.tap(element).perform()

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def login_success_process(self):
        try:
            Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)

            #联系人权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def get_permission_process(self):
        try:
            Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)

            #打开取景窗
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            #录音权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

            # 视频权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

            #关闭取景框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)




