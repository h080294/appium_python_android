#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *

class MEITUM4PreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(MEITUM4PreProcess, self).__init__(tester)


    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 启动app并处理GPS弹窗" % self.tester.device.devicename)

            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)

            self.driver.launch_app()

            time.sleep(7)

            # 获取允许弹框的坐标并点击
            print '干掉允许按钮,程序往下继续执行'
            self.driver.swipe(488, 710, 488, 710, 5)

        except Exception, e:
            Log.logger.info(u"设备：%s 发生错误" % self.tester.device.devicename)
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def login_success_process(self):
        try:
            Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)

            time.sleep(4)
            print '允许授权通讯录权限'
            self.driver.swipe(493,705,493,705,5)

        except Exception, e:
            Log.logger.info(u"设备：%s 发生错误" % self.tester.device.devicename)
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def get_permission_process(self):
        Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)
        try:
            #打开取景框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            #摄像头权限
            time.sleep(2)
            print '授权摄像头权限'
            self.driver.swipe(500,721,500,721,5)

            # 录音权限
            time.sleep(6)
            print '授权录音权限'
            self.driver.swipe(490,722,490,722,5)

            time.sleep(1)
            # 退出取景框，回到发现页面
            if self.tester.is_element_exist('com.nice.main:id/titlebar_return',3):
                self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')
            else:
                self.tester.back_to_feed()
        except Exception, e:
            Log.logger.info(u"设备：%s 发生错误" % self.tester.device.devicename)
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)