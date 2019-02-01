#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 09:44:14 2019

@author: MacBook
"""
import warnings
warnings.filterwarnings('ignore')
import md5
import random
"""
def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

try:
    import requests
except:    
    install_and_import('requests')
"""
import requests

def get_english(chinese):
    m = md5.new()
    salt = random.randint(0,100)
    q = chinese
    id = '20190201000261397'
    str1 = id + q + str(salt) + '3dMpDG89j4D87KLLLCtm'
    m.update(str1)
    sign = m.hexdigest()
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate?from=zh&q={q}&to=en&appid={id}&salt={salt}&sign={sign}'.format(q=q,id=id,salt=salt,sign=sign)
    r = requests.get(url)
    data = r.json()
    trans_result_list = data['trans_result']
    output = ""
    if len(trans_result_list) > 0:
        output = trans_result_list[0]['dst']
    return output
