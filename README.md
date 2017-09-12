appium_pyton_android
继承并封装了appium，Android移动端自动化测试框架。
支持多设备并发运行testcase，直接错误log及截图功能，html输出测试报告等。

简单介绍下用法：

1、运行前请添加测试包、设备信息到config.yaml中
NiceAPK: /Users/xxxxx/xxx.apk    # 测试包的路径

Devices:
 - deviceid: 5HUC9S6599999999    # 设备识别adb devices的值
   devicename: OPPO_R9M    # 设备的名称，用于区分
   serverport: 4723    # -p Appium的主要端口，设备之间不能重复
   bootstrapport: 4823    # -bp Appium bootstrap端口，设备之间不能重复
   platformname: Android    # desired_caps
   platformversion: 5.1    # desired_caps
   server: 127.0.0.1     # 地址

2、测试用例，testcase目录下保留了两条参考用例，其中一条是真实用例测试com.nice.main
   
3、连接好所有的设备后运行run_server_appium，启动appium server

4、待appium server启动完毕，运行run_server_http

5、选择需要运行的类型：自动化测试或者monkey测试

*如有任何建议欢迎邮件 h080294@163.com










# appium_python_android
