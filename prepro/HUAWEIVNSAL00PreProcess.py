#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *


class HUAWEIVNSAL00PreProcess (BaseDevicePreProcess):

    def __init__(self, tester):
        super(HUAWEIVNSAL00PreProcess, self).__init__(tester)

    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 处理安装提示" % self.tester.device.devicename)

            # self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/decide_to_continue')
            # self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/goinstall')

            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)

            self.driver.launch_app()

            # 已安装应用列表权限
            self.tester.find_element_by_id_and_tap('com.huawei.systemmanager:id/btn_allow')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def login_success_process(self):
        try:
            Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)

            # 权限申请
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')
            time.sleep(1)
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_ok')
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            Log.logger.info(u"设备：%s 没有成功授权通讯录" % self.tester.device.devicename)

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def get_permission_process(self):
        Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)
        try:
            #打开取景框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')
            if self.tester.is_element_exist('com.huawei.systemmanager:id/btn_allow'):
                self.tester.tap_screen(730, 1170)
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')
            time.sleep(1)

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)