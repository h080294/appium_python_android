#!usr/bin/python
# -*- coding:utf-8 -*-
import subprocess

from BaseDevicePreProcess import *

class VIVOV3MAXPreProcess(BaseDevicePreProcess):

    def __init__(self,tester):
        super(VIVOV3MAXPreProcess, self).__init__(tester)

    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid, DataProvider.niceapk)
        subprocess.call(cmd, shell=True)
        time.sleep(3)


    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 启动app并处理GPS弹窗" % self.tester.device.devicename)

            # self.tester.find_element_by_uiautomator_and_tap("android:id/button1")
            time.sleep(7)
            self.tester.tap_screen(340, 1215)

            # self.tester.find_element_by_uiautomator_and_tap("vivo:id/vivo_adb_install_ok_button")
            time.sleep(7)
            self.tester.tap_screen(303, 1846)

            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)

            self.driver.launch_app()


            #GPS权限
            # self.tester.find_element_by_uiautomator_and_tap("android:id/button1")
            time.sleep(7)
            self.tester.tap_screen(324, 1240)

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def login_success_process(self):
        try:
            Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)
            #联系人权限
            time.sleep(7)
            self.tester.tap_screen(320, 1244)

            self.tester.find_element_by_id_and_tap('android:id/button1')

        except Exception,e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def get_permission_process(self):
        try:
            Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            #相机权限
            self.tester.find_element_by_uiautomator_and_tap("android:id/button1")

            #录音权限
            self.tester.find_element_by_uiautomator_and_tap("android:id/button1")

            #关闭取景框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)