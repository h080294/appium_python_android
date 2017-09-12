#!usr/bin/python
# -*- coding:utf-8 -*-
# 正常的case用例

import sys

sys.path.append('..')
from common.BaseTestCase import *


class test_story_pub_image(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_001_story_pub_image(self):
        """
        检查音量键拍照，后置摄像头，夜间模式，滤镜，画笔，文字
        """
        # 进入story拍摄页面
        self.tester.swipe_right()
        time.sleep(3)

        # 干掉发story的引导浮层
        for num in range(2):
            self.tester.tap_screen_center()

        if self.tester.is_element_exist('com.nice.main:id/record_btn',3)==False:
            self.tester.screenshot(u'设备不支持发story')
            self.tester.press_keycode(4)
        else:
            # 音量键拍照过程录制视频
            self.tester.start_screen_record(u'story音量键拍摄照片')

            # 如果设备支持美颜模式，则点击美颜按钮
            if self.tester.is_element_exist('com.nice.main:id/beauty_auto'):
                self.tester.find_element_by_id_and_tap('com.nice.main:id/beauty_auto')
            else:
                self.tester.screenshot(u'story没找到美颜按钮')

            # 如果设备存在夜间模式，则点击夜间模式按钮
            if self.tester.is_element_exist('com.nice.main:id/night_mode',3):
                self.tester.find_element_by_id_and_tap('com.nice.main:id/night_mode')
            else:
                self.tester.screenshot(u'story没找到夜间模式按钮')

            # 按音量键拍照
            self.tester.press_keycode(25)

            time.sleep(5)

            # 滑动切换滤镜
            for i in range(5):
                self.tester.swipe_right()

            # 停止视频录制
            self.tester.stop_screen_record(u'story音量键拍摄照片')

            # 点击画笔，并绘制画笔路线
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_draw')
            self.tester.swipe_screen(self.tester.device_width/4, self.tester.device_height/4,
                                     self.tester.device_width/4, self.tester.device_height/4*3)

            # 点击画笔粗细线条，调整画笔粗细
            self.tester.find_element_by_id_and_tap('com.nice.main:id/civ')

            # 点击荧光画笔，并绘制路线
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_highlighter')
            time.sleep(3)
            self.tester.swipe_screen(self.tester.device_width/2, self.tester.device_height/4,
                                     self.tester.device_width/2, self.tester.device_height/4*3)

            # 切换画笔颜色绘制路线
            try:
                self.tester.find_element_by_xpath_and_tap('//android.widget.ImageView[6]')
            except:
                time.sleep(1)

            time.sleep(3)
            self.tester.swipe_screen(self.tester.device_width/4*3, self.tester.device_height/4,
                                     self.tester.device_width/4*3, self.tester.device_height/4*3)

            # 点击确定退出画笔
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_save')

            # 点击文案，并输入文案
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_add_text')
            self.tester.find_element_by_id_and_send_keys('com.nice.main:id/et_story', 'autotest')

            # 点击确定退出文案编辑状态
            # self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_save')
            self.tester.press_keycode(4)
            # story编辑结果
            self.tester.screenshot(u'storystory图片编辑结果')

            # 点击下一步进入发布预览页
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_edit_complete')

            # 处理第一次进入发布预览页的引导提示
            if self.tester.is_element_exist('com.nice.main:id/story_scene_info_close', 5):
                self.tester.find_element_by_id_and_tap('com.nice.main:id/story_scene_info_close')

            # 发布story
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_post_btn')

            # 等待上传故事
            time.sleep(10)

            # Feed页 发布结果
            self.tester.screenshot(u'storystory图片发布完成')

            # 进入我的story查看
            if self.tester.is_element_exist(u'我的故事'):
                self.tester.find_element_by_xpath_and_tap(
                    '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[2]')
            else:
                self.tester.screenshot(u'story未找到我的故事')
                return

            self.tester.start_screen_record(u'story检查我发布的故事')

            # 处理看story蒙层问题
            time.sleep(2)
            if self.tester.is_element_exist(u'点击屏幕两侧切换照片'):
                self.tester.tap_screen_center()

            # 等待播放完毕返回feed
            if self.tester.is_element_exist('com.nice.main:id/btnTabSubscription', timeout=20):
                self.tester.stop_screen_record(u'story检查前置拍摄的故事')
            elif self.tester.is_element_exist('com.nice.main:id/img_return'):
                try:
                    self.tester.driver.find_element_by_id('com.nice.main:id/img_return').click()
                except:
                    print "try to tap close button failed"
                self.tester.stop_screen_record(u'story检查前置拍摄的故事')
            else:
                self.tester.stop_screen_record(u'story检查前置拍摄的故事')
                self.tester.back_to_feed()

            self.tester.stop_screen_record(u'story检查我发布的故事')

            # 清理我发布的故事
            self.tester.clear_pub_story()
            self.tester.back_to_feed()

    def test_002_story_pub_image(self):
        """
        检查前置摄像头，美颜拍照
        """

        # 进入story拍摄页面
        self.tester.swipe_right()
        time.sleep(3)

        if self.tester.is_element_exist('com.nice.main:id/record_btn',3)==False:
            self.tester.screenshot(u'设备不支持发story')
            self.tester.press_keycode(4)
        else:
            # 如果设备支持美颜模式，则点击美颜按钮
            if self.tester.is_element_exist('com.nice.main:id/beauty_auto'):
                self.tester.find_element_by_id_and_tap('com.nice.main:id/beauty_auto')
            else:
                self.tester.screenshot(u'story没找到美颜按钮')

            # 如果设备存在夜间模式，则点击夜间模式按钮
            if self.tester.is_element_exist('com.nice.main:id/night_mode'):
                self.tester.find_element_by_id_and_tap('com.nice.main:id/night_mode')
                self.tester.screenshot(u'story没找到夜间模式按钮')

            # 音量键拍照过程录制视频
            self.tester.start_screen_record(u'story前置摄像头音量键拍摄照片')

            # 切换摄像头至前置
            self.tester.find_element_by_id_and_tap('com.nice.main:id/switch_camera')
            time.sleep(5)

            # 按音量键拍照
            self.tester.press_keycode(25)

            # 等待照片处理完
            self.tester.wait_element('com.nice.main:id/story_draw')

            # 停止视频录制
            self.tester.stop_screen_record(u'story前置摄像头音量键拍摄照片')

            # story编辑结果
            self.tester.screenshot(u'storystory前置摄像头编辑结果')

            # 点击下一步进入发布预览页
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_edit_complete')
            time.sleep(4)

            # 发布story
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_post_btn')

            # 等待发布&点击feed
            time.sleep(10)
            self.tester.wait_element('com.nice.main:id/btnTabSubscription')

            # Feed页 发布结果
            self.tester.screenshot(u'storystory发布完成')

            # 进入我的story查看
            if self.tester.is_element_exist(u'我的故事'):
                self.tester.find_element_by_xpath_and_tap(
                    '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[2]')
            else:
                self.tester.screenshot(u'story未找到我的故事')
                return

            self.tester.start_screen_record(u'story检查前置拍摄的故事')

            # 等待播放完毕返回feed
            if self.tester.is_element_exist('com.nice.main:id/btnTabSubscription', timeout=20):
                self.tester.stop_screen_record(u'story检查前置拍摄的故事')
            elif self.tester.is_element_exist('com.nice.main:id/img_return'):
                try:
                    self.tester.driver.find_element_by_id('com.nice.main:id/img_return').click()
                except:
                    print "try to tap close button failed"
                self.tester.stop_screen_record(u'story检查前置拍摄的故事')
            else:
                self.tester.stop_screen_record(u'story检查前置拍摄的故事')
                self.tester.back_to_feed()

            # 清理我发布的故事
            self.tester.clear_pub_story()
            self.tester.back_to_feed()

    def test_003_story_pub_image(self):
        """
        检查非音乐滤镜拍照，滤镜，文字，画笔
        """
        # 进入story拍摄页面
        self.tester.swipe_right()
        time.sleep(3)

        if self.tester.is_element_exist('com.nice.main:id/record_btn',3)==False:
            self.tester.screenshot(u'设备不支持发story')
            self.tester.press_keycode(4)
        else:
            self.tester.find_element_by_id_and_tap('com.nice.main:id/lens_enter')
            time.sleep(15)

            #找到拍摄按钮右侧的滤镜控件中心点坐标，点击
            element = self.tester.driver.find_element_by_xpath('//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[5]')
            self.tester.get_center_coor_and_tap(element)
            time.sleep(4)

            #点击拍摄照片
            self.tester.find_element_by_id_and_tap('com.nice.main:id/record_btn')

            time.sleep(5)

            # 滑动切换滤镜
            for i in range(0, 5):
                self.tester.swipe_right()

            # 点击画笔，并绘制画笔路线
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_draw')
            time.sleep(3)
            self.tester.swipe_screen(self.tester.device_width / 4, self.tester.device_height / 4,
                                     self.tester.device_width / 4, self.tester.device_height / 4 * 3)

            # 点击画笔粗细线条，调整画笔粗细
            self.tester.find_element_by_id_and_tap('com.nice.main:id/civ')

            # 点击荧光画笔，并绘制路线
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_highlighter')
            time.sleep(3)
            self.tester.swipe_screen(self.tester.device_width / 2, self.tester.device_height / 4,
                                     self.tester.device_width / 2, self.tester.device_height / 4 * 3)

            # 切换画笔颜色绘制路线
            try:
                self.tester.find_element_by_xpath_and_tap('//android.widget.ImageView[6]')
            except:
                time.sleep(1)

            time.sleep(3)
            self.tester.swipe_screen(self.tester.device_width / 4 * 3, self.tester.device_height / 4,
                                     self.tester.device_width / 4 * 3, self.tester.device_height / 4 * 3)

            # 点击确定退出画笔
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_save')

            # 点击文案，并输入文案
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_add_text')
            self.tester.find_element_by_id_and_send_keys('com.nice.main:id/et_story', 'autotest')

            # 点击确定退出文案编辑状态
            # self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_save')
            self.tester.press_keycode(4)

            # story编辑结果
            self.tester.screenshot(u'storystory非音乐滤镜图片编辑结果')

            # 点击下一步进入发布预览页
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_edit_complete')
            time.sleep(4)

            # 处理第一次进入发布预览页的引导提示
            if self.tester.is_element_exist('com.nice.main:id/story_scene_info_close'):
                self.tester.find_element_by_id_and_tap('com.nice.main:id/story_scene_info_close')

            # 发布story
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_post_btn')

            # 点击feed
            self.tester.wait_element('com.nice.main:id/btnTabSubscription')

            # Feed页 发布结果
            self.tester.screenshot(u'storystory非音乐滤镜图片发布完成')

            # 等待上传故事
            time.sleep(5)

            # 进入我的story查看
            if self.tester.is_element_exist(u'我的故事'):
                self.tester.find_element_by_xpath_and_tap(
                    '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[2]')
            else:
                self.tester.screenshot(u'story未找到我的故事')
                return

            self.tester.start_screen_record(u'story检查非音乐滤镜拍摄的故事')

            if self.tester.is_element_exist(u'点击屏幕两侧切换照片', timeout=5):
                self.tester.tap_screen_center()

            # 等待播放完毕返回feed
            if self.tester.is_element_exist('com.nice.main:id/btnTabSubscription', timeout=100):
                self.tester.stop_screen_record(u'story检查非音乐滤镜拍摄的故事')
            elif self.tester.is_element_exist('com.nice.main:id/img_return'):
                try:
                    self.tester.driver.find_element_by_id('com.nice.main:id/img_return').click()
                except:
                    print "try to tap close button failed"
                self.tester.stop_screen_record(u'story检查非音乐滤镜拍摄的故事')
            else:
                self.tester.stop_screen_record(u'story检查非音乐滤镜拍摄的故事')
                self.tester.back_to_feed()

            # 清理我发布的故事
            self.tester.clear_pub_story()
            self.tester.back_to_feed()

    def test_004_story_pub_image(self):
        """
        检查音乐滤镜拍照，发布
        """
        # 进入story拍摄页面
        self.tester.swipe_right()
        time.sleep(3)

        if self.tester.is_element_exist('com.nice.main:id/record_btn',3)==False:
            self.tester.screenshot(u'设备不支持发story')
            self.tester.press_keycode(4)
        else:
            #点击展开镜头滤镜
            self.tester.find_element_by_id_and_tap('com.nice.main:id/lens_enter')
            time.sleep(15)

            # 找到第一个镜头滤镜点击
            self.tester.find_element_by_xpath_and_tap(
                '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[5]')
            time.sleep(2)
            #找到音乐滤镜EDM 点击
            self.tester.find_element_by_xpath_and_tap(
                '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[7]')
            time.sleep(4)

            # 点击拍摄照片
            self.tester.find_element_by_id_and_tap('com.nice.main:id/record_btn')

            # 等待照片处理完
            self.tester.wait_element('com.nice.main:id/story_draw')

            # story编辑结果
            self.tester.screenshot(u'storystory音乐滤镜图片编辑结果')

            # 点击下一步进入发布预览页
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_edit_complete')
            time.sleep(4)

            # 处理第一次进入发布预览页的引导提示
            if self.tester.is_element_exist('com.nice.main:id/story_scene_info_close'):
                self.tester.find_element_by_id_and_tap('com.nice.main:id/story_scene_info_close')

            # 发布story
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_post_btn')

            # 点击feed
            self.tester.wait_element('com.nice.main:id/btnTabSubscription')

            # Feed页 发布结果
            self.tester.screenshot(u'storystory音乐滤镜图片发布完成')

            # 等待上传故事
            time.sleep(5)

            # 进入我的story查看
            if self.tester.is_element_exist(u'我的故事'):
                self.tester.find_element_by_xpath_and_tap(
                    '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[2]')
            else:
                self.tester.screenshot(u'story未找到我的故事')
                return

            self.tester.start_screen_record(u'story检查音乐滤镜拍摄的故事')

            if self.tester.is_element_exist(u'点击屏幕两侧切换照片', timeout=5):
                self.tester.tap_screen_center()

            # 等待播放完毕返回feed
            if self.tester.is_element_exist('com.nice.main:id/btnTabSubscription', timeout=100):
                self.tester.stop_screen_record(u'story检查音乐滤镜拍摄的故事')
            elif self.tester.is_element_exist('com.nice.main:id/img_return'):
                try:
                    self.tester.driver.find_element_by_id('com.nice.main:id/img_return').click()
                except:
                    print "try to tap close button failed"
                self.tester.stop_screen_record(u'story检查音乐滤镜拍摄的故事')
            else:
                self.tester.stop_screen_record(u'story检查音乐滤镜拍摄的故事')
                self.tester.back_to_feed()

            # 清理我发布的故事
            self.tester.clear_pub_story()
            self.tester.back_to_feed()

    def tearDown(self):
        pass
        # self.tester.back_to_feed()
        # self.tester.clean_mp4_file()

    # 请reset到feed页面
    @classmethod
    def tearDownClass(cls):
        pass
