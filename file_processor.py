#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 04:45:51 2019

@author: MacBook
"""

import os
import shutil
from sync_files import send_attachment_mail
from output_color import bcolors
import operator
import baidu_translator

TOSEND = 'TOSEND'
SENT = 'SENT'
upload_list = []
kindle_supported_exts = ['.azw3','.azw','.txt','.pdf','.mobi','.prc']


def check_contain_chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def split_word(word):
    cn_str = ''
    en_str = ''
    for ch in word.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            cn_str += ch
        else:
            en_str += ch
    return cn_str,en_str
    

def change_chosen_file_name(chosen_map,config_lang):
    names = chosen_map.keys()
    name_change = {}
    flag = True
    for name in names:
        if check_contain_chinese(name):
            # I have to replace it using english
            if flag:
                if config_lang == 'cn':
                    print bcolors.BOLD + '发现非英文文件名。由于非英文文件名目前不能支持，将进行英文转换。' + bcolors.ENDC
                else:
                    print bcolors.BOLD + 'Non-english characters which are not supported found in file names. A English translation of file names will start.' + bcolors.ENDC
                flag = False
            basename,ext = os.path.splitext(name)
            new_name = baidu_translator.get_english(basename) + ext
            name_change[name] = new_name
            if config_lang == 'cn':
                print '重命名:\033[93m{}\033[0m -> \033[1m{}\033[0m'.format(name,new_name)
            else:
                print 'Rename:\033[93m{}\033[0m -> \033[1m{}\033[0m'.format(name,new_name)
        else:
            name_change[name] = name
    return name_change
            
            
            
            




def pdf_included(file_list):
    for filename in file_list:
        basename,ext = os.path.splitext(filename)
        if ext.lower() == '.pdf':
            return True
    return False

def total_size():
    file_size_map = {}
    chosen_file_map = {}
    left_out_map = {}
    for filename in upload_list:
        filesize = os.path.getsize(filename)/(1024*1024.0)
        file_size_map[os.path.basename(filename)] = filesize
    
    sorted_size = sorted(file_size_map.items(), key=operator.itemgetter(1))
    overall_size = 0
    for (filename,size) in sorted_size:
        overall_size += size
        if overall_size < 50:
            chosen_file_map[filename] = size
        else:
            left_out_map[filename] = size
    exceed = (len(left_out_map.keys()) > 0)
    chosen_all_file_size = sum(chosen_file_map.values())
    left_out_all_size = sum(left_out_map.values())
    return exceed,chosen_file_map,left_out_map,chosen_all_file_size,left_out_all_size

def get_upload_file_list_and_run(user_email,password,kindle_mail,config_lang):
    
    if not os.path.exists(TOSEND):
        os.makedirs(TOSEND)
    if not os.path.exists(SENT):
        os.makedirs(SENT)
    
    
    for filename in os.listdir(TOSEND):
        if os.path.isfile(os.path.join(TOSEND,filename)):
            basename,ext = os.path.splitext(filename)
            if basename.startswith('.'):
                continue
            if ext.lower() in kindle_supported_exts:
                # we can upload this file
                file_path = os.path.join(TOSEND,filename)
                filesize = os.path.getsize(file_path)/(1024*1024.0)
                if filesize < 50: # for stable issues
                    upload_list.append(file_path)
                else:
                    print '['+bcolors.FAIL+'x'+bcolors.ENDC+']'+filename+'\t'+bcolors.FAIL + "(>=50MB)" + bcolors.ENDC
                #print '[+]',filename
            else:
                print '['+bcolors.FAIL+'x'+bcolors.ENDC+']',filename
    
    if len(upload_list) == 0:
        if config_lang == 'cn':
            if len(os.listdir(TOSEND)) == 0:
                print bcolors.BOLD + '请在\033[4m{}\033[0m文件夹中放入需要推送的文件'.format(TOSEND) + bcolors.ENDC
            else:
                print bcolors.FAIL + '未能在{}文件夹中发现符合推送格式的文件'.format(TOSEND) + bcolors.ENDC
        else:
            if len(os.listdir(TOSEND)) == 0:
                print bcolors.BOLD + 'Please put the files you want to push in the {} folder'.format(TOSEND) + + bcolors.ENDC
            else:
                print bcolors.FAIL + 'No file in folder {} satisfies the file format for push.'.format(TOSEND) + bcolors.ENDC
        return False
    
    exceed,chosen_file_map,left_out_map,chosen_size,left_size = total_size()
    if config_lang == 'cn':
        if exceed:
            print bcolors.WARNING+ '由于总大小超出了50MB，超出的文件将不会推送' + bcolors.ENDC
    else:
        if exceed:
            print bcolors.WARNING+ 'The overall size of files exceeds 50MB, some large files are omitted in push' + bcolors.ENDC
    if config_lang == 'cn':
        print bcolors.HEADER+ '--------\n以下文件将会被推送' + bcolors.ENDC + bcolors.BOLD + "\t(" + str(round(chosen_size,2)) + "MB)" + bcolors.ENDC
    else:
        print bcolors.HEADER+'--------\nThese files are going to be pushed' + bcolors.ENDC+ bcolors.BOLD + "\t(" + str(round(chosen_size,2)) + "MB)" + bcolors.ENDC
    for id,filename in enumerate(chosen_file_map.keys()):
        print "\033[1m({id})\033[0m \033[94m{filename}\033[0m\t({size}MB)".format(id=id+1,filename=os.path.basename(filename),size=round(chosen_file_map[filename],2))
    if exceed:
        if config_lang == 'cn':
            print bcolors.FAIL+ '--------\n以下文件将不被推送' + bcolors.ENDC + bcolors.BOLD + "\t(" + str(round(left_size,2)) + "MB)" + bcolors.ENDC
        else:
            print bcolors.FAIL+ '--------\nThese files will not be pushed' + bcolors.ENDC + bcolors.BOLD + "\t(" + str(round(left_size,2)) + "MB)" + bcolors.ENDC
    
    for id,filename in enumerate(left_out_map.keys()):
        print "\033[91m({id})\033[0m \033[94m{filename}\033[0m\t({size}MB)".format(id=id+1,filename=os.path.basename(filename),size=round(left_out_map[filename],2))    
        
    
    if config_lang == 'cn':
        proceed_request = bcolors.BOLD + '继续吗？输入yes或者no.(不输入默认yes)' + bcolors.ENDC
    else:
        proceed_request = bcolors.BOLD + 'Proceed?[yes]/no' + bcolors.ENDC
    user_input = raw_input(proceed_request)
    user_input = user_input.lower().strip()
    
    if user_input == 'no' or user_input == 'n':
        if config_lang == 'cn':
            print bcolors.WARNING + '操作已被用户取消' + bcolors.ENDC
        else:
            print bcolors.WARNING +'Operation cancelled.' + bcolors.ENDC
        return False
    else:
        
        #http://xtk.azurewebsites.net/BingDictService.aspx?Word=welcome
        safe_names_map = change_chosen_file_name(chosen_file_map,config_lang)
        
        need_pdf_convert = False
        if pdf_included(chosen_file_map.keys()):
            if config_lang == 'cn':
                convert_query = bcolors.BOLD+'是否将pdf文件转换为Kindle阅读适配格式？输入yes或者no.(不输入默认no)' + bcolors.ENDC
            else:
                convert_query = bcolors.BOLD+'Do you need to optimize your pdf files for better reading experience in Kindle?yes/[no]' + bcolors.ENDC
            need_convert = raw_input(convert_query)
            need_convert = need_convert.lower().strip()
            if need_convert == 'yes' or need_convert == 'y':
                need_pdf_convert = True
        #send_attachment_mail(sender, pwd, receiver, mail_title, mail_content, filenames)
        sender = user_email.split('@')[0]
        if config_lang == 'cn':
            mail_title = '来自{}的推送'.format(user_email)
            mail_content = '推送的内容见附件'
        else:
            mail_title = 'Push From {}'.format(user_email)
            mail_content = 'Please see the attachment list'
        if need_pdf_convert:
            mail_title = 'Convert'
        final_upload_list = [os.path.join(TOSEND,filename) for filename in chosen_file_map.keys()]
        #print 'safe_names=',safe_names_map
        send_attachment_mail(sender,password,kindle_mail,mail_title,mail_content,final_upload_list,config_lang,safe_names_map)
        return True
    
def move_uploaded_files(config_lang):
    for filename in upload_list:
        basename = os.path.basename(filename)
        try:
            shutil.move(filename,os.path.join(SENT,basename))
        except:
            if config_lang == 'cn':
                print '\033[93m未能将文件{}移入{}文件夹\033[0m'.format(basename,SENT)
            else:
                print '\033[93mFailed to move file {} to {} folder\033[0m'.format(basename,SENT)