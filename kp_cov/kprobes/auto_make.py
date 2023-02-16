#!/usr/bin/python
# -*-coding:utf-8 -*-
import os
def auto_process(passwd,path,target_name):
   #产生的.c要放入文件夹（路径改变） make clean，make，rmmod，insmod
   os.chdir(path)
   command1='dmesg -c'
   os.system('echo %s | sudo -S %s' % (passwd, command1))
   os.system('make clean')
   os.system('make')
   os.system('ls')
   command2="rmmod "+target_name
   os.system('echo %s | sudo -S %s' % (passwd, command2))
   command3="insmod "+target_name
   os.system('echo %s | sudo -S %s' % (passwd, command3))

   return 
