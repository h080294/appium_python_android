#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *

class RedMi1sPreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(RedMi1sPreProcess, self).__init__(tester)

    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 启动app并处理GPS弹窗" % self.tester.device.devicename)

            element = self.tester.find_element_by_id("com.kingroot.kinguser:id/checkbox_remember",20)
            if element != None:
                self.action.tap(element).perform()
                self.tester.find_element_by_id_and_tap('com.kingroot.kinguser:id/button_right')


            element = self.tester.find_element_by_id("com.android.packageinstaller:id/ok_button",60)
            if element != None:
                self.action.tap(element).perform()

            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)

            self.driver.launch_app()

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def login_success_process(self):
        try:
            Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)
            # #联系人权限
            # self.tester.find_element_by_id_and_tap('com.lbe.security.miui:id/accept')
        except Exception,e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def get_permission_process(self):
        try:
            Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            # #录音权限
            # self.tester.find_element_by_id_and_tap('com.lbe.security.miui:id/accept')

            #关闭取景框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)