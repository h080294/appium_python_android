#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *
from appium.webdriver.webelement import WebElement
import subprocess

class LianXiangK30TPreProcess(BaseDevicePreProcess):

    def __init__(self,tester):
        super(LianXiangK30TPreProcess, self).__init__(tester)

    # def install_app(self):
    #     Log.logger.info(u"设备：%s 安装时弹出获取权限弹框" % self.tester.device.devicename)
    #     try:
    #
    #     except:
    #         traceback.print_exc()

    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 处理安装中各种弹窗" % self.tester.device.devicename)

            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().resourceId(\"com.lenovo.safecenter:id/btn_install\").textContains(\"确定\")')

            # 启动app
            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)
            self.driver.launch_app()

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def login_success_process(self):
        try:
            Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def get_permission_process(self):
        Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)
        try:
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            #关闭取景框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)



