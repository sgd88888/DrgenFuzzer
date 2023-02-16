#!/usr/bin/python
# -*-coding:utf-8 -*-
#IDA Python有三个库，其中提供一些API来提供一些功能
import idaapi
import idautils
import idc
#其他头文件
import binascii
import os
from filepath import idafile_path
from filepath import file_result
from filepath import total_num
from filepath import basefunc
f= open(file_result,"w+")
idaapi.autoWait()#ida结束
f1=open(total_num,"w+")#blocks total num
f2=open(basefunc,"w+")#first not sub_ function
count=0
index=0
for func in idautils.Functions():#遍历每个函数
    functionObject = idaapi.get_func(func)#返回函数开始地址
    
    try:
        if (functionObject == None):
            print("This is not a function! Exiting!")
            os._exit(0)
            #return -1
    except:
        print("Looks like this is a function. Continuing...")
    seg=SegName(func)
    if seg=="extern" or seg==".init.text" or seg ==".exit.text":
        continue
    str=idaapi.get_func_name(func)
    if index==0 and str.find('sub_')<0:   #first not sub_ function
        index=1
        f2.write(str)
    # Now let's get its flowchart.
    flowChart = idaapi.FlowChart(functionObject,flags = idaapi.FC_PREDS)
    f.write("%s %d\n" %(idaapi.get_func_name(func), flowChart.size))

    
    count+=flowChart.size
    for block in flowChart:
        f.write('0x%016X\n'%(block.startEA))
    try:
        if (flowChart == None):
            print("Could not build a flow chart! Exiting!")
            #return -1
            os._exit(0)
    except:
        print("Exception occurred when trying to find the flowchart! Exiting!")
        os._exit(0)
   

f1.write("%d"%count)
f.close()
f1.close()
f2.close()
idc.Exit(0)















     #return -1
    #for block in flowChart
     #   print %x %(hex(func))
    # Print out info about the number of basic blocks
    # found in the current function. Comment this out
    # if you are not interested in seeing this in the output.





#f_blocks = idaapi.FlowChart(idaapi.get_func(ea), flags=idaapi.FC_PREDS)  #获取start_ea所在函数的所有基本块，可以通过遍历f_blocks中的基本块得到每个基本快的信息
#idaapi.FlowChart(idaapi.get_func(ea), flags=idaapi.FC_PREDS).size #获取函数基本快数量 
