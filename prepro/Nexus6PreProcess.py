#coding=utf-8
from BaseDevicePreProcess import *


class Nexus6PreProcess(BaseDevicePreProcess):

    def __init__(self, tester):
        super(Nexus6PreProcess, self).__init__(tester)

    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 启动app" % self.tester.device.devicename)

            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)

            self.driver.launch_app()
        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def login_success_process(self):
        try:
            Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)

            # 第一次登陆需要三个授权：位置信息，访问照片和文件，拨打电话和管理通话
            for i in range(0, 3):
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')
                time.sleep(1)

            # nice的授权通讯录弹窗
            # self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_ok')  #无法点击控件
            time.sleep(2)
            self.tester.tap_screen(700, 1660)

            # 系统的授权弹窗
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def get_permission_process(self):
        Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)
        try:

            #self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')

            #打开取景框
            time.sleep(10)
            self.tester.tap_screen(745, 2300)

            # 拍照和录制视频权限
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            # 录制音频权限
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            # 切换到拍摄页面
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            # 退出取景框，回到发现页面
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')

            time.sleep(10)
            if self.tester.is_element_exist(u'你关注人的故事和直播'):
                # 处理语言问题
                self.tester.find_element_by_id_and_tap('com.nice.main:id/btnTabProfile')
                while self.tester.is_element_exist('com.nice.main:id/layout_profile_setting') == False:
                    self.tester.swipe_down()
                self.tester.find_element_by_id_and_tap('com.nice.main:id/layout_profile_setting')
                self.tester.find_element_by_id_and_tap('com.nice.main:id/layout_setting_common')
                self.tester.find_element_by_id_and_tap('com.nice.main:id/layout_setting_language')
                time.sleep(3)

                # 简体中文语言
                if self.tester.is_element_exist(u'简体中文'):
                    self.tester.back_to_feed()
                else:
                    self.tester.find_element_by_id_and_tap('com.nice.main:id/layout_setting_language')
                    time.sleep(2)
                    self.tester.find_element_by_xpath_and_tap('//android.widget.TextView[2]')
                    self.tester.back_to_feed()
            else:
                print 'nexus6目前是简体中文'

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

