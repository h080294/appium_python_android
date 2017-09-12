#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *

class Coopad9729blackPreprocess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(Coopad9729blackPreprocess, self).__init__(tester)


    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 启动app并处理GPS弹窗" % self.tester.device.devicename)

            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)

            self.driver.launch_app()

            #处理获取地理位置弹框
            self.tester.find_element_by_id_and_tap('com.yulong.android.seccenter:id/alertdlg_allowed')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def login_success_process(self):
        try:
            Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)

            #获取联系人权限
            self.tester.find_element_by_id_and_tap('com.yulong.android.seccenter:id/alertdlg_allowed')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def get_permission_process(self):
        Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)
        try:
            #打开取景框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            #视频权限
            self.tester.find_element_by_id_and_tap('com.yulong.android.seccenter:id/alertdlg_allowed')
            #录音权限
            self.tester.find_element_by_id_and_tap('com.yulong.android.seccenter:id/alertdlg_allowed')

            self.tester.press_keycode(4)

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)