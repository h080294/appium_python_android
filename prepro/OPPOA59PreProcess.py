#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *

class OPPOA59PreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(OPPOA59PreProcess, self).__init__(tester)

    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid,DataProvider.niceapk)
        subprocess.call(cmd,shell=True)

    def install_process(self):
        Log.logger.info(u"设备：%s 处理安装中各种弹窗" % self.tester.device.devicename)
        try:
            time.sleep(5)
            if self.tester.is_element_exist(u'静默安装拦截',10):
                self.tester.find_element_by_id_and_tap('com.kingroot.kinguser:id/checkbox_remember')
                self.tester.find_element_by_id_and_tap('com.kingroot.kinguser:id/button_right')

            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/btn_allow_once',60)
        except TimeoutException,e:
            traceback.print_exc()
        finally:
            try:
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/bottom_button_two')
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/bottom_button_two')
                self.tester.find_element_by_id_and_tap('oppo:id/remember_cb')
                self.tester.find_element_by_id_and_tap('android:id/button1')
            except Exception, e:
                traceback.print_exc()
                DriverManager.quit_driver(self.tester.device.deviceid)

    def login_success_process(self):
        Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)
        try:
            self.tester.find_element_by_id_and_tap('android:id/button1')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_cancel')
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
