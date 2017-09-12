#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *

class SumSingS4PreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(SumSingS4PreProcess, self).__init__(tester)


    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 启动app并处理GPS弹窗" % self.tester.device.devicename)

            time.sleep(5)
            if self.tester.is_element_exist(u'静默安装拦截', 10):
                self.tester.find_element_by_id_and_tap('com.kingroot.kinguser:id/checkbox_remember')
                self.tester.find_element_by_id_and_tap('com.kingroot.kinguser:id/button_right')

            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)

            #点击确认应用程序许可按钮
            self.tester.find_element_by_id_and_tap('com.android.settings:id/button')

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
            #打开取景框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            # 退出取景框，回到发现页面
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')
        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)