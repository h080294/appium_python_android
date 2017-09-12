#!/bin/bash
# 用于获取手机登陆的验证码，这里只是示例，相关地址已经隐去

#手机号
MOBILE=$1

#token
TOKEN='xxxxxxxxxxxxxxxxxxxxxx'

CODE=`curl -s "http://xxxxxx?token=$TOKEN&mobile=$MOBILE" | awk -F ',' '{print $9;}' | awk -F ':' '{print $3;}' | awk -F '}' '{print $1;}'`

echo $CODE

