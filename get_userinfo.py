#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 05:01:52 2019

@author: MacBook
"""

import os

CONFIG_NAME = 'config.txt'
user_email = ''
password = ''
kindle_mail = ''
config_lang = 'cn' # or 'en'
from output_color import bcolors

def create_config_file():
    with open(CONFIG_NAME,'w') as f:
        readme_cn = "下面的内容包含(1)中文和(2)英文配置，请选择其中一项填写即可。\n\n注意：在使用本工具之前，请先确认qq邮箱地址在您的亚马逊账号发件人认可列表中，否则将无法实现推送。\n请登录 www.mazon.cn/myk 确认认可列表和您的Kindle邮箱。"
        readme_en = "\nConfigurations in (1)Chinese and (2)English are available below. You only need to choose one to fill.\n\nNotice: Before using this tool, please confirm your QQ email address is included in the addressor whitelist of your amazon account. Or you cannot receive the pushed content in your device.\n\nPlease sign in www.mazon.cn/myk and confirm your addressor whitelist and Kindle email address. "
        space = '\n\n\n'
        cn_explanation = "(1)中文配置\n请在下方替换你的推送信息：\n"
        cn_content = "可以用于推送的QQ邮件地址=xxxxxx@qq.com\nQQ邮件的登录密码=123123\nKindle邮箱=123123@kindle.cn"
        en_explanation = "(2)Configuration in English\nPlease replace the following information using yours：\n"
        en_content = "Your QQ Email Address for Book Push=xxxxxx@qq.com\nEmail Password=123123\nKindle Email Address=123123@kindle.cn"
        last = "配置完成后即可使用。\n\n\nYou can use this program right after configuration."
        contents = [readme_cn,readme_en,space,cn_explanation,cn_content,space,en_explanation,en_content,space,last]
        f.writelines(contents)

def parse_config_file():
    global config_lang
    global user_email
    global password
    global kindle_mail
    
    with open(CONFIG_NAME,'r') as f:
        contents = f.readlines()
    for line in contents:
        line = line.strip()
        
        if config_lang == 'cn' or config_lang == '':
            if line.startswith('可以用于推送的QQ邮件地址'):
                ans = line.split('=')[1]
                ans = ans.strip()
                if ans != 'xxxxxx@qq.com' and ans != '':
                    # user use configuration in Chinese
                    config_lang = 'cn'
                    user_email = ans
                else:
                    config_lang = 'en'
            if line.startswith('QQ邮件的登录密码'):
                ans = line.split('=')[1]
                ans = ans.strip()
                if ans == '':
                    return False,'邮箱密码不能为空'
                else:
                    password = ans
            if line.startswith('Kindle邮箱'):
                ans = line.split('=')[1]
                ans = ans.strip()
                if ans == '':
                    return False,'Kindle邮箱不能为空'
                else:
                    kindle_mail = ans
                    return True,'成功获取用户信息'
        elif config_lang == 'en':
            if line.startswith('Your QQ Email Address for Book Push'):
                ans = line.split('=')[1]
                ans = ans.strip()
                if ans != 'xxxxxx@qq.com' and ans != '':
                    # user use configuration in Chinese
                    config_lang = 'en'
                    user_email = ans
                else:
                    return False,'You must provide your QQ email address\nQQ邮箱密码不能为空'
            if line.startswith('Email Password'):
                ans = line.split('=')[1]
                ans = ans.strip()
                if ans == '':
                    return False,'email password cannot be empty\n'
                else:
                    password = ans
            if line.startswith('Kindle Email Address'):
                ans = line.split('=')[1]
                ans = ans.strip()
                if ans == '':
                    return False,'Kindle email address cannot be empty'
                else:
                    kindle_mail = ans
                    return True,'success'
    return False,'config.txt is ruined. config.txt 文件已被损坏'
        
                

def get_info():
    global config_lang
    global user_email
    global password
    global kindle_mail
    
    modified = True
    if not os.path.exists(CONFIG_NAME):
        create_config_file()
        print bcolors.BOLD + 'config.txt 已生成，请打开填写必要信息' + bcolors.ENDC
        print bcolors.BOLD + 'config.txt is generated. Please fill in the required fields.' + bcolors.ENDC
        return False,user_email,password,kindle_mail,config_lang,modified
    else:
        success,info = parse_config_file()
        if not success:
            print info
            if config_lang == 'cn':
                if info == 'config.txt is ruined. config.txt 文件已被损坏':
                    print bcolors.FAIL+ '由于配置文件损坏，配置文件已被初始化，请重新设置'+bcolors.ENDC
                    os.remove(CONFIG_NAME)
                    create_config_file()
            elif config_lang == 'en':
                if info == 'config.txt is ruined. config.txt 文件已被损坏':
                    print bcolors.FAIL + 'We will now recover the config.txt file. Please open config.txt and try again.' + bcolors.ENDC
                    os.remove(CONFIG_NAME)
                    create_config_file()
                if info == 'You must provide your QQ email address\nQQ邮箱密码不能为空':
                    modified = False
            return False,user_email,password,kindle_mail,config_lang,modified
        else:
            if config_lang == 'cn':
                print '------------\n\033[94m当前推送设置：\033[0m\n从\033[1m{}\033[0m推送至\033[1m{}\033[0m\n------------'.format(user_email,kindle_mail)
            else:
                print '------------\n\033[94mCurrent push setting:\033[0m\nfrom \033[1m{}\033[0m to \033[1m{}\033[0m\n------------'.format(user_email,kindle_mail)
            #print 'success',user_email,password,kindle_mail,config_lang
            return True,user_email,password,kindle_mail,config_lang,modified
    