# -*- coding: utf-8 -*-
import os

def stopAppium():
    r = os.popen("ps -ef | grep appium")
    info = r.readlines()
    for line in info:  # 按行遍历
        eachline = line.split()
        appium_pid = eachline[1]
        action = os.popen("kill " + appium_pid)
        print("kill" + appium_pid)

def kill_server(port):
    cmd = "lsof -i:%s|awk 'NR==2{print $2}'" % port
    pid = os.popen(cmd).read()
    cmd = "kill -9 %s" % pid
    os.popen(cmd).read()

stopAppium()
kill_server(8886)

