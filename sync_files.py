#!/usr/bin/python
# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from smtplib import SMTP_SSL
from email.header import Header
from output_color import bcolors
import time
import os

def send_attachment_mail(sender_qq, pwd, receiver, title, content, filelist,config_lang,safe_names_map=None):
    try:
        # qq邮箱smtp服务器
        host_server = 'smtp.qq.com'
        sender_qq_email = sender_qq + '@qq.com'
        # SSL登录
        smtp = SMTP_SSL(host_server)
        smtp.login(sender_qq, pwd)

        msg = MIMEMultipart()

        msg['Subject'] = Header(title, 'utf-8')
        msg['From'] = sender_qq_email
        msg['To'] = receiver
        # 文本
        text = MIMEText(content, 'plain', 'utf-8')
        msg.attach(text)
        # 附件
        for file in filelist:
            attachment = MIMEApplication(open(file, 'rb').read())
            basename = os.path.basename(file)
            if safe_names_map:
                basename = safe_names_map[basename]
            attachment.add_header('Content-Disposition', 'Attachment', filename=basename)
            msg.attach(attachment)
        
        if config_lang == 'cn':
            print bcolors.OKBLUE + '正在推送中...文件多或者大时等待时间较长，请不要退出' + bcolors.ENDC
        else:
            print bcolors.OKBLUE + 'Files are being pushed now. Please wait patiently.' + bcolors.ENDC
        time_start = time.time()
        smtp.sendmail(sender_qq_email, receiver, msg.as_string())
        time_end = time.time()
        
        if config_lang == 'cn':
            print '操作耗时{}秒'.format(time_end-time_start)
        else:
            print 'Time used:{} secs'.format(time_end - time_start)

    except smtp.SMTPException,e:
        if config_lang == 'cn':
            print bcolors.FAIL + '发生错误，错误内容为:'+str(e) + bcolors.ENDC
        else:
            print bcolors.FAIL + 'Error found:'+str(e) + bcolors.ENDC
    finally:
        smtp.quit()
        



#send_attachment_mail(sender, pwd, receiver, mail_title, mail_content, filenames)

