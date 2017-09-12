#!/usr/bin/env python
#coding: utf-8

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from model.Tester import *
from email.header import Header
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def run():
    sender = 'xxx@163.com'    #发送方
    receiver = ['xxx@163.com']  #接收方

    # 发送的邮箱服务地址
    smtp = smtplib.SMTP_SSL("smtp.exmail.qq.com", port=465)
    username = 'xxx@163.com'
    password = 'xxxxxx'

    #邮件对象
    msgRoot = MIMEMultipart('related')
    msgRoot['From'] = _format_addr(u'autotest<%s>' % sender)
    for x in receiver:
        msgRoot['to'] = _format_addr(u'<%s>' % x)
    msgRoot['Subject'] = '[Monkey]%s' % get_format_currenttime()

    #构造附件，即邮件正文
    for listdir in Tester.lis:
        att = MIMEText(open('%s' % listdir, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="%s"' % listdir
        msgRoot.attach(att)

    smtp.connect('smtp.exmail.qq.com')
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msgRoot.as_string())
    smtp.quit()

if __name__ == '__main__':
    run()