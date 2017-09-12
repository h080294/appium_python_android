#coding=utf-8
from BaseDevicePreProcess import *


class XIAOMINOTEPreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(XIAOMINOTEPreProcess, self).__init__(tester)

    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid,DataProvider.niceapk)
        subprocess.call(cmd,shell=True)


        # if self.tester.is_element_exist('android:id/button2',5):
        # self.tester.find_element_by_id_and_tap('android:id/button2')
        # else:
        #     pass

    def install_process(self):
        Log.logger.info(u"设备：%s 启动app并处理GPS弹窗" % self.tester.device.devicename)

        self.tester.find_element_by_id_and_tap('android:id/button2')
        try:

            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)

            self.driver.launch_app()
            #self.tester.find_element_by_id_and_tap('android:id/button2')
        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def login_success_process(self):
        try:
            Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)


            #授权通讯录弹框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_ok')

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
            #self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            # 摄像头权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

            # 录音权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

            # 退出取景框，回到发现页面
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_close')
        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

