#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 05:56:51 2019

@author: MacBook
"""

import get_userinfo
import file_processor
from output_color import bcolors
import warnings
warnings.filterwarnings('ignore')

if __name__ == '__main__':
    
    success,user_email,password,kindle_mail,config_lang,modified = get_userinfo.get_info()
    if success:
        result = file_processor.get_upload_file_list_and_run(user_email,password,kindle_mail,config_lang)
        if config_lang == 'cn':
            if result:
                print bcolors.OKGREEN + '推送成功' + bcolors.ENDC
                file_processor.move_uploaded_files(config_lang)
            else:
                print bcolors.FAIL + '推送未完成' + bcolors.ENDC
        else:
            if result:
                print bcolors.OKGREEN +'Files are successfully pushed'+ bcolors.ENDC
                file_processor.move_uploaded_files(config_lang)
            else:
                print bcolors.FAIL +'Push failed'+ bcolors.ENDC
    else:
        if config_lang == 'cn':
            print bcolors.WARNING +'由于配置无效，推送未开始'+ bcolors.ENDC
        else:
            if not modified:
                print bcolors.WARNING+'由于配置无效，推送未开始\nPush hasn\'t started yet because of the invalid config file.'+ bcolors.ENDC
            else:
                print bcolors.WARNING+'Push hasn\'t started yet because of the invalid config file.'+ bcolors.ENDC
                
