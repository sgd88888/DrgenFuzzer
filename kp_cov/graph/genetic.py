#!/usr/bin/python
# -*-coding:utf-8 -*-
import os
import sys
import time
from graph import countnum,graph
from buildtree2 import TreeNode,MultiTree
import copy
import math
import json

from filepath_gen import basedir
from filepath_gen import idafile_path
from filepath_gen import idapro_dir
from filepath_gen import file_name
from filepath_gen import file_path
from filepath_gen import cov_addresspath
from filepath_gen import file_coverage
from filepath_gen import sudo_password
from Mutators import Mutators
from Mutators import _byteify
from Mutators import isarray
from Mutators import lengtharray
from Mutators import chararray
from Mutators import Sample
def ida_script():#idapython
   if file_name.find("x64")>=0:#check file name
     os.system("wine "+idapro_dir+"64.exe -A -c -S"+basedir+idafile_path+" "+ file_path + file_name)#binary file path 
     print "wine "+idapro_dir+"64.exe -A -c -S"+basedir+idafile_path+" "+ file_path + file_name
   else:
     os.system("wine "+idapro_dir+".exe -A -c -S"+basedir+idafile_path+" "+file_path + file_name)#binary file path 
   return
def node_vis_init(path):#得到包含函数节点的名字和基本块块号，从零开始的计数字典，字典一一对应     。一个参数file
    dc={}
    list0=[]
    file_object0=open(path,"r")#Analyze intermediate file placement set
    for line in file_object0:
        list1=line.strip().split(' ')
        name=list1[0]
        dc.setdefault(name,[]).append(0)
    file_object0.close()
    #print dc
    return dc
 #{'my_release': [0], 'my_read': [0], 'my_write': [0], 
    # 'my_ioctl_cold': [0], 'my_open_cold': [0, 0], 'my_open': [0, 0, 0, 0], 'my_ioctl': [0, 0, 0, 0, 0, 0, 0, 0, 0]}
def node_visit(dc,file):#统计一次覆盖 
    file_object1=open(file,"r")#Analyze coverage file log
    for line in file_object1:
        if (line.find("BUG")!= -1):
           print "find!!!!!!"
           sys.exit(0)
           
        if (line.find('<') != -1):
		   list1=line[line.find('<'):-1].strip().split(' ')
		   funname=list1[0][1:]
		#print funname
		   list2=list1[1].split('>')
		   num=int(list2[0],10)
        if dc[funname][num] == 0:
            dc[funname][num]=1
    #print dc
    file_object1.close() 
#已有的现在的基本块访问情况vis；访问次数：希望节点序列H；后继节点序列S；
#本次测试覆盖节点序列V: 
# for each node in V:
    #  if node not in VIS:
          #    flag = True
      #UPDATEVIS(node, VIS) #更新访问次数    
def fiteness(v,vis,vis_num,dc_tree,h,s,x):#计算适应度   先以整个基本块作为测试单位
    flag = False
    for item in v:
      for j in range(len(v[item])):
        node=v[item][j]
        #print item,j,node,vis[item][j]
        if node==1:
            if vis[item][j]==0:
                flag = True
                vis[item][j]=1
            vis_num[item][j]+=1
            dc_tree[item].visit(TreeNode(str(j)))                      
        else:
            continue
    #print "flag:",flag            
    if flag:
        updatehopeseq(v,dc_tree,h)
        updatesuccseq(v,dc_tree,h,s)
    sum=0
    for it in h:
        for node in h[it]:
           sum=sum+calffitness(it,node,vis_num,s)
    
    p=float(sum*exp_math(x))
    print "fitness",p
    return p


def exp_math(x):
    mm=float(x-1000)/100
    fx=1/float(1+math.exp(mm))
    return fx

def calffitness(it,node,vis_num,s):
    fit=s[it][node]/float(vis_num[it][node])
    #print "fit:",fit
    return fit

def updatesuccseq(v,dc_tree,h,s):#求后继节点数量
    for item in h:
        s.setdefault(item,{})
    for item in h:
        if len(h[item])==0:
            continue
        else:
            for j in h[item]:
                mm=dc_tree[item].search_childtree(TreeNode(str(j)))
                #print mm
                count=0
                for ff in mm:
                    if v[item][ff]==0:
                        count+=1
                    else:
                        continue
                #print count
                s[item][j]=count#统计后继节点数量
    '''for item in s:
        print s[item]
        for mm in s[item].keys():
           print s[item][mm]
    '''


def updatehopeseq(v,dc_tree,h):
    for name in v:
        h.setdefault(name,[])

    for item in v:
      for j in range(len(v[item])):
        node=v[item][j]
        if node==1:#覆盖的才可能成为希望节点
            mm=dc_tree[item].search_children(TreeNode(str(j)))#子节点存在且没被访问
            #print mm
            if mm == []:
                continue
            for ff in mm:#访问其子节点
                if v[item][int(ff)]==0:
                     h[item].append(j)
                else:
                    continue
    #for item in h:
        #print item,h[item]

'''       
def choose(filelist):
    N=len(filelist)
    sum_fit=0
    fitlist=[]
    for item in filelist:
        sum_fit+=item.fitness
def select(pop, fitness):    # nature selection wrt pop's fitness
    idx = np.random.choice(np.arange(POP_SIZE), size=POP_SIZE, replace=True,
                        p=(fitness)/(fitness.sum()) )
    return pop[idx]
'''
#计算适应度和



if __name__=="__main__": 
    #ida_script()#得到各个基本块和其前驱关系，以及前驱数量
    dc_tree={}
    dc_tree=graph(dc_tree)#建立驱动中各个函数里的基本块图关系
    with open('i2c.json', 'r') as jsonFile:
            weatherData = json.load(jsonFile,object_hook=_byteify)
    filelist=[]    
    vis_num={}#记录访问次数
    vis={}
 
    m=Mutators(weatherData)
    vis_num=node_vis_init(cov_addresspath)#访问次数初始化  
    vis=node_vis_init(cov_addresspath)
    
    h={}
    s={}
    filelist=m.gen_sample1('cmd2')
    
    for item in filelist:
        logcmd1="dmesg -C"#日志方式可能要改，超过环形buffer的话，命令输出的记录内容会少    v字典置0
        os.system('echo %s | sudo -S %s' % (sudo_password, logcmd1))
        m.fuzztest(item)#只能一个一个文件的测
        m.exe_test(item)
        logcmd2="dmesg > "+file_coverage
        os.system('echo %s | sudo -S %s' % (sudo_password, logcmd2))
        v={}
        print item.name
        v=node_vis_init(cov_addresspath)
        node_visit(v,file_coverage)#一次统计
        ret=fiteness(v,vis,vis_num,dc_tree,h,s,item.test_num)
        item.fit(ret)
        print "fitness",item.fitness
    m.select_mutator(filelist)    
   
    
    while True:
        for item in filelist:
            logcmd1="dmesg -C"#日志方式可能要改，超过环形buffer的话，命令输出的记录内容会少    v字典置0
            os.system('echo %s | sudo -S %s' % (sudo_password, logcmd1))
            m.fuzztest(item)#只能一个一个文件的测
            m.exe_test(item)
            logcmd2="dmesg > "+file_coverage
            os.system('echo %s | sudo -S %s' % (sudo_password, logcmd2))
            v={}
            print item.name
            v=node_vis_init(cov_addresspath)
            node_visit(v,file_coverage)#一次统计
            ret=fiteness(v,vis,vis_num,dc_tree,h,s,item.test_num)
            item.fit(ret)
            print item.fitness
        m.select_mutator(filelist)    
    
    
    for item in filelist:
        print item.name,item.test_num
    #print sys.minsize
    
    

    

    

  
    #Data=json.loads(weatherData)
    #print(type(weatherData))



