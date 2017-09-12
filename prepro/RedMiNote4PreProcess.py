#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *

class RedMiNote4PreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(RedMiNote4PreProcess, self).__init__(tester)

    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid, DataProvider.niceapk)
        subprocess.call(cmd,shell=True)

    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 启动app并处理GPS弹窗" % self.tester.device.devicename)

            self.tester.find_element_by_id_and_tap('com.miui.securitycenter:id/do_not_ask_checkbox')
            self.tester.find_element_by_id_and_tap('android:id/button2')

            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)
            self.driver.launch_app()

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def login_success_process(self):
        try:
            Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)

            for i in range(0, 3):
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')
                time.sleep(1)

            # nice的授权通讯录弹窗
            # self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_ok')  #无法点击控件
            time.sleep(2)
            # self.tester.tap_screen(555, 1360)
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_ok')

            # 系统的授权弹窗
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

        except Exception,e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def get_permission_process(self):
        try:
            Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            # self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            #录音权限
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')
            time.sleep(1)
            #视频权限
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')
            #关闭取景框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)