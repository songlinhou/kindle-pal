#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText

msg_from='307977586@qq.com'
passwd='rockwilliams5156'                                   
msg_to='rock307977586@gmail.com'                                  
                            
subject="python 测试"
content="qq发送的邮件"
msg = MIMEText(content)
msg['Subject'] = subject
msg['From'] = msg_from
msg['To'] = msg_to
try:
    s = smtplib.SMTP_SSL("smtp.qq.com",465)
    s.login(msg_from, passwd)
    s.sendmail(msg_from, msg_to, msg.as_string())
    print "Success"
except s.SMTPException,e:
    print "Error",e
finally:
    s.quit()
