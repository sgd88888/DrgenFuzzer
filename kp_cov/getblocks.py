#!/usr/bin/python
# -*-coding:utf-8 -*-
#IDA Python有三个库，其中提供一些API来提供一些功能
import idaapi
import idautils
import idc
#其他头文件
import binascii
import os
idaapi.autoWait()#ida结束
for func in idautils.Functions():#遍历每个函数
    functionObject = idaapi.get_func(func)#返回函数开始地址
    try:
        if (functionObject == None):
            print("This is not a function! Exiting!")
            os._exit(0)
            #return -1
    except:
        print("Looks like this is a function. Continuing...")

    flowChart = idaapi.FlowChart(functionObject,flags = idaapi.FC_PREDS)
    for block in flowChart:
        print('0x%016X'%(block.startEA))
    try:
        if (flowChart == None):
            print("Could not build a flow chart! Exiting!")
            #return -1
            os._exit(0)
    except:
        print("Exception occurred when trying to find the flowchart! Exiting!")
        os._exit(0)
    print "%s has %d basic blocks!" %(idaapi.get_func_name(func), flowChart.size)
    print 