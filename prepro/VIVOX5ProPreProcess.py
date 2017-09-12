#!usr/bin/python
# -*- coding:utf-8 -*-
import subprocess

from BaseDevicePreProcess import *

class VIVOX5ProPreProcess(BaseDevicePreProcess):

    def __init__(self, tester):
        super(VIVOX5ProPreProcess, self).__init__(tester)

    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid, DataProvider.niceapk)
        subprocess.call(cmd, shell=True)
        time.sleep(3)

    def install_process(self):
        Log.logger.info(u"设备：%s 处理安装中各种弹窗" % self.tester.device.devicename)

        try:
            # 点击安装时adb授权提示
            self.tester.find_element_by_id_and_tap('vivo:id/vivo_adb_install_ok_button')

            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)

            # 启动APP
            self.driver.launch_app()

            # GPS权限
            # self.tester.find_element_by_uiautomator_and_tap("android:id/button1")  #奇怪的弹窗，无法正常点击，用坐标代替
            time.sleep(3)
            self.tester.tap_screen(287, 1250)

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def login_success_process(self):
        Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)
        try:
            self.tester.find_element_by_id_and_tap('android:id/button1')
        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def get_permission_process(self):
        Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)
        try:
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            #摄像机权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

            #录音权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

            #关闭取景框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)



