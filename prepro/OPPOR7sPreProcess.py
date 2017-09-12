#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *

class OPPOR7sPreProcess(BaseDevicePreProcess):

    def __init__(self, tester):
        super(OPPOR7sPreProcess, self).__init__(tester)

    # 无法获取空间信息，使用坐标点击
    def install_process(self):
        Log.logger.info(u"设备：%s 处理安装中各种弹窗" % self.tester.device.devicename)

        try:
            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)
            self.driver.launch_app()
            # 点击弹窗不再提醒GPS允许
            self.tester.find_element_by_id_and_tap('oppo:id/remember_cb')
            time.sleep(2)
            # 点击GPS允许
            self.tester.find_element_by_id_and_tap('android:id/button1')
        except TimeoutException, e:
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
            self.tester.find_element_by_id_and_tap('oppo:id/remember_cb')
            self.tester.find_element_by_id_and_tap('android:id/button1')

            #录音权限
            self.tester.find_element_by_id_and_tap('oppo:id/remember_cb')
            self.tester.find_element_by_id_and_tap('android:id/button1')

            #关闭取景框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)



