注意：Appium Server端要求单独启动，到时方便做分布式部署
启动方法：运行run_server.py

解决每次都会安装各种APK的问题,

文件: /usr/local/lib/node_modules/appium/node_modules/appium-android-driver/lib/driver.js，注释以下几句代码
await this.adb.uninstallApk(this.opts.appPackage);
await helpers.installApkRemotely(this.adb, this.opts);
await helpers.resetApp(this.adb, this.opts.app, this.opts.appPackage, this.opts.fastReset);
await this.checkPackagePresent();

文件：/usr/local/lib/node_modules/appium/node_modules/appium-android-driver/build/lib/driver.js 注释以下几句代码
return _regeneratorRuntime.awrap(_androidHelpers2['default'].resetApp(this.adb, this.opts.app, this.opts.appPackage, this.opts.fastReset));
return _regeneratorRuntime.awrap(this.adb.uninstallApk(this.opts.appPackage));
return _regeneratorRuntime.awrap(_androidHelpers2['default'].installApkRemotely(this.adb, this.opts));
return _regeneratorRuntime.awrap(this.checkPackagePresent());

文件：/usr/local/lib/node_modules/appium/node_modules/appium-android-driver/lib/android-helpers.js 注释以下几句代码
await adb.install(unicodeIMEPath, false);
await helpers.pushSettingsApp(adb);
await helpers.pushUnlock(adb);

文件 /usr/local/lib/node_modules/appium/node_modules/appium-android-driver/build/lib/android-helpers.js 替换以下几句代码
return _regeneratorRuntime.awrap(helpers.initUnicodeKeyboard(adb)) 替换为return context$1$0.abrupt('return', defaultIME);
return _regeneratorRuntime.awrap(helpers.pushSettingsApp(adb)); 替换为return context$1$0.abrupt('return', defaultIME);
return _regeneratorRuntime.awrap(helpers.pushUnlock(adb)); 替换为return context$1$0.abrupt('return', defaultIME);





