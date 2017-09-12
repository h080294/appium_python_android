#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *

class SumSing9152PreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(SumSing9152PreProcess, self).__init__(tester)


    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 启动app并处理GPS弹窗" % self.tester.device.devicename)
            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)

            self.driver.launch_app()


            #self.tester.find_element_by_uiautomator_and_tap(u'new UiSelector().textContains(\"允许\").fromParent(new UiSelector().className(\"android.widget.Button\"))')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def login_success_process(self):
        try:
            Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)

            # self.tester.find_element_by_uiautomator_and_tap(
            #     u'new UiSelector().textContains(\"允许\").fromParent(new UiSelector().className(\"android.widget.Button\"))')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def get_permission_process(self):
        Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)
        try:
            # 打开取景框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')

            # 切换到拍摄tab
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            self.tester.press_keycode(4)

            time.sleep(1)
        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)