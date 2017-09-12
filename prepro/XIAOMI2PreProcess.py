#coding=utf-8
from BaseDevicePreProcess import *


class XIAOMI2PreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(XIAOMI2PreProcess, self).__init__(tester)

    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 启动app并处理GPS弹窗" % self.tester.device.devicename)

            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)

            self.driver.launch_app()
        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def login_success_process(self):
        try:
            Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)


            #授权通讯录弹框
           # self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_ok')

            #授权联系人权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def get_permission_process(self):
        Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)
        try:
            #打开取景框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            element = self.tester.find_element_by_id("android:id/button1")
            if element != None:
                self.action.tap(element).perform()

            element = self.tester.find_element_by_id("android:id/button1",20)
            if element != None:
                self.action.tap(element).perform()

            # 退出取景框，回到发现页面
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

