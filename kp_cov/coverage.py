# -*- coding: UTF-8 -*-
import os
from filepath import file_coverage_middle
from filepath import file_coverage
from filepath import sudo_password
from filepath import total_num
from filepath import file_name
from dominate.tags import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def cmd_name(dict_struct):
   all_func_name="\""
   func_count=0
   for key in dict_struct:
       if(func_count==0):
          all_func_name+=key
       else:
          all_func_name+="|"+key
       func_count+=1
   all_func_name+="\""
   return all_func_name


def cmd(str,path,passwd):
   command="dmesg |grep -w -E "+str+">"+path
   print command
   os.system('echo %s | sudo -S %s' % (passwd, command))
   return 

def deal(file1,file2,file3,filename):
    
    dc={}
    list0=[]
    file_object0=open(file1,"r")#Analyze intermediate file placement set
    for line in file_object0:
        list1=line.strip().split(' ')
        name=list1[0]
        dc.setdefault(name,[]).append(0)
    file_object0.close()
    print dc
    cmd(cmd_name(dc),file2,sudo_password)
    
    file_object1=open(file2,"r")#Analyze coverage file log
    for line in file_object1:
        if (line.find('<') != -1):
		list1=line[line.find('<'):-1].strip().split(' ')
		funname=list1[0][1:]
		#print funname
		list2=list1[1].split('>')
		num=int(list2[0],10)
		#print num
		dc[funname][num]=1
    #print dc   
    file_object1.close()
    
    count=0
    dc1={}
    #print "Function Coverage"
    for key in dc:
        l=len(dc[key])
        index=0
        for i in range(l):
            if dc[key][i]==1:
                count+=1
                index+=1
        dc1[key]=float(index)/l
        dc1[key]="{:.2f}".format(dc1[key])
        #print '%s %s'%(key,dc1[key])  

    file_object2=open(file3,"r")
    try:
	    context = file_object2.read()
    finally:
        file_object2.close()  
    total=int(context,10)
    result=float(count)/total
    
    #visualization(dc1,filename,result)
    create_html(dc1,file_name,result)
    return result




#def visualization(dc,filename,num):
    #plt.rcParams['font.sans-serif']=['Youyuan'] 
 #   plt.rcParams['font.size']=20
  #  plt.figure(figsize=(15,8), dpi=80)#创建一个画布，也可以不使用
 #   x=[]
 #   for key in dc:
 #       x.append(dc[key])   
  #  x.append(num) 
#    y=[]
 #   for key in dc:
 #       y.append(key)
  #  y.append('total')
   # p1 = plt.bar(x=0, bottom=y, height=0.4, width=x, orientation="horizontal")
   # plt.xlabel('Coverage Percentage')
   # str=filename+" coverage of different functions"
   # plt.title(str)
   # for a, b in zip(x, y):#显示数字图标 ha表示位置
    #   plt.text(a+0.2, b, '%04.2f' % a, ha='left', va='bottom', fontsize=20)
    #plt.show()
def create_html(dc,name,result):
    h = html()
    with h.add(body()).add(div(id='content')):
        str=name+'驱动程序的函数覆盖率'
        h1(str)
        with table(border="1",cellspacing="0",style="border-collapse:collapse").add(tbody()):
            # 生成报表头部
            with tr(align="center",bgcolor="#0080FF",style="color:white"):
                td(rowspan="2").add('函数名')
                td(colspan="4").add('覆盖率')
            l = tr(align="center",bgcolor="#0080FF",style="color:white")
            


            l = tr(align="center") 
            with l:
                td('总覆盖率')
                td(result)
            for key in dc:
                l = tr(align="center")
                with l:
                    td(key)                    
                    td(dc[key])
                    

    with open('result.html','w+') as f:
        f.write(h.render())



if __name__ =="__main__":
    total=deal(file_coverage_middle,file_coverage,total_num,file_name)
    print 'Total Coverage %.2f'%(total) 
