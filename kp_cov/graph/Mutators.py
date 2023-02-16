# -*- coding: utf-8 -*-
import random
import string
import re
import struct
import math
import sys
import json
import os
import collections
from fcntl import ioctl 
from head import headfile
import urllib
from filepath_gen import sudo_password
import numpy as np
import re


if sys.version_info >= (3, 0):
    long = int
    unicode = str
def _byteify(data, ignore_dicts = False):
    if isinstance(data, str):
        return data
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.items() # changed to .items() for python 2.7/3
        }
    # python 3 compatible duck-typing
    # if this is a unicode string, return its string representation
    if str(type(data)) == "<type 'unicode'>":
        return data.encode('utf-8')
    # if it's anything else, return it in its original form
    return data
def isarray(str1):
    left=str1.find('[')
    right=str1.find(']')
    #print "left:",left
    #print "right:",right
    if left<0 or right<0:
        return False
    flag=True
    for item in str1[left+1:right]:
        if (item>='0') and (item<='9'):
            flag=True
            continue
        else:
            flag=False
            break
    return flag
def lengtharray(str1):
    left=str1.find('[')
    right=str1.find(']')
    leng=int(str1[left+1:right])
    return leng
def chararray(str1):
    left=str1.find('[')
    right=str1.find(']')
    leng=str1[left:right+1]
    return leng
def ten_to_two(n,x):
    #n为待转换的十进制数，x为机制，取值为2-16
    print n
    a=[0,1,2,3,4,5,6,7,8,9,'A','b','C','D','E','F']
    b=[]
    while True:
        s=n//x#商
        y=n%x#余数
        b=b+[y]
        if s==0:
            break
        n=s
    b.reverse()
    print b
    return b
    


class Sample(object):
    def __init__(self, name,keys,id,mm):
        self.name = name
        self.test_num=0
        self.keys=keys
        self.id=id
        self.fitness=float(0)
        self.type=mm
    def visit(self):
        self.test_num+=1
    def clear(self):
        self.test_num=0
    def fit(self,num):
        self.fitness=num   

class Mutators(object):
    def __init__(self,dict):
        self.dev=dict['dev']
        self.cmd=dict['cmd']
        self.arg=dict['arg']
        self.signal=0#是否进行测试的信号
        self.gen_file=[]#模糊测试生成的文件名
        self.fitness={}#样本适应度保存
        self.typearg=["unsigned short int","short","int","unsigned int","long","unsigned long","long long","unsigned long long"]
        self.typearg_char=["unsigned char","char"]
        self.type_struct_pointer=["struct pointer"]
        self.typepointer=["unsigned char*"]
        self.random_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"#string.printable[:-5]
        self.key=""
        self.shortint_mutator = {
            0: lambda x: x**2,
            1: lambda x: -x,
            2: lambda x: 2*x,
            3: lambda x: x/2,
            4: lambda x: x+1,
            5: lambda x: int(math.sqrt(abs(x))),
            6: lambda x: random.randint(-32768,32767),
        }        
        self.unsignedshortint_mutator = {
            0: lambda x: x**2,
            1: lambda x: -x,
            2: lambda x: 2*x,
            3: lambda x: x%1000,
            4: lambda x: x+1,
            5: lambda x: int(math.sqrt(abs(x))),
            6: lambda x: random.randint(0,65535),
        }
        self.int_mutator = {
            0: lambda x: x**2,
            1: lambda x: -x,
            2: lambda x: 2*x,
            3: lambda x: x/2,
            4: lambda x: x+1,
            5: lambda x: int(math.sqrt(abs(x))),
            6: lambda x: random.randint(-2147483647, 2147483647),
        }
        self.unsignedint_mutator = {
            0: lambda x: x**2,
            1: lambda x: -x,
            2: lambda x: 2*x,
            3: lambda x: x%20,
            4: lambda x: x+1,
            5: lambda x: int(math.sqrt(abs(x))),
            6: lambda x: random.randint(0, 4294967295),
        }
        self.long_mutator = {
            0: lambda x: x^2,
            1: lambda x: -x,
            2: lambda x: 2*x,
            3: lambda x: x/2,
            4: lambda x: x+1,
            5: lambda x: int(math.sqrt(abs(x))),
            6: lambda x: np.random.randint(-9223372036854775808,9223372036854775808,dtype=np.int64),
        }
        self.unsignedlong_mutator = {
            0: lambda x: x**2,
            1: lambda x: -x,
            2: lambda x: 2*x,
            3: lambda x: x/2,
            4: lambda x: x+1,
            5: lambda x: int(math.sqrt(abs(x))),
            6: lambda x: np.random.randint(0,18446744073709551616,dtype=np.uint64),
        }
        self.longlong_mutator = {
            0: lambda x: x**2,
            1: lambda x: -x,
            2: lambda x: 2*x,
            3: lambda x: x/2,
            4: lambda x: x+1,
            5: lambda x: int(math.sqrt(abs(x))),
            6: lambda x: np.random.randint(-9223372036854775808,9223372036854775808,dtype=np.int64),
        }
        self.unsignedlonglong_mutator = {
            0: lambda x: x**2,
            1: lambda x: -x,
            2: lambda x: 2*x,
            3: lambda x: x/2,
            4: lambda x: x+1,
            5: lambda x: int(math.sqrt(abs(x))),
            6: lambda x: np.random.randint(0,18446744073709551616,dtype=np.uint64),
        }
        self.mutator = {
            "short":self.shortint_mutator,
            "unsigned short int":self.unsignedshortint_mutator,           
            "int": self.int_mutator,
            "unsigned int":self.unsignedint_mutator,
            "long":self.long_mutator,
            "unsigned long":self.unsignedlong_mutator,
            "long long":self.longlong_mutator,
            "unsigned long long":self.unsignedlonglong_mutator,
        }
    def random_string_generator(self,max_size):
        return ''.join(random.choice(self.random_chars) for x in range(random.randint(0, max_size)))
    def charmutator(self,charaim,index):
        #print charaim
        a=ord(charaim)#ASCII码
        b=index#字符位置
        num=a+b
        
        randnum = (self.mutator["int"][random.randint(0,5)](num))%62;                    #随机数生成函数
        c= self.random_chars[randnum];          #从字符数组中取值
        return c 


    def fuzzing(self,keys):#json中cmd得有序号才行
        opencmd="int fd;\nfd=open(\""+self.dev+"\", O_RDWR);\nif (fd < 0) {\nprintf(\"Couldn't reopen "+self.dev+"\");\n}"
        print opencmd
        type=''
        count=0
        print keys
        for item in self.cmd:            
            if self.cmd[item]['name']==keys:
               type=self.cmd[item]['value']
               print type
               countstr=item
               count=self.cmd[item]['id']
               break
            else:
                continue    
                 
        print countstr  
        argindex="arg"+str(count)
        print argindex  
        mm=str(self.arg[argindex]['type'])
        #print self.arg[argindex]

           
        if mm in self.typearg:
            #print typearg.index(mm)
            gendata=self.mutator[mm][6](1)
            genstr=mm+" a="+str(gendata)+";\n"+"ioctl(fd,"+keys+",a);\nreturn 0;\n"  
            print genstr
            
            basestr="{\n\"dev\"=\""+self.dev+"\","+"\n"+"\"cmd\"=\""+str(self.cmd[countstr]['value']) +"\",\n"
            typestr="\"type\":\""+mm+"\",\n"
            gendata_json="\"value\":\""+str(gendata)+"\"\n}"
            print basestr+typestr+gendata_json

    def gen_sample1(self,keys):#生成样本json，json中cmd得有序号才行
        self.key=keys
        filegenpath="/home/test/Desktop/kp_cov/graph/input/"+keys
        if not os.path.exists(filegenpath):
             os.mkdir(filegenpath)        
        type=''
        count=0
        print self.cmd
        for item in self.cmd:            
            if item==keys:
               type=self.cmd[item]
               print type
               countstr=item
               
               count=item[(item.find('d')+1):]
               print count
               break
            else:
                continue    
        argindex="arg"+str(count)                 
        mm=self.arg[argindex]['type']
        
        dic = collections.OrderedDict()
        dic['dev']=self.dev
        dic['cmd']=self.cmd[countstr]
        for i in range(20):
            t=Sample(filegenpath+"/"+str(i)+".json",keys,i,mm)
            fd=open(filegenpath+"/"+str(i)+".json",'w')
            if mm in self.typearg:
                gendata=self.mutator[mm][6](1)           
                dic['type']=mm
                dic['value']=gendata
                #print dic
        #print self.arg[argindex]
            elif mm=="struct":
                #print "struct"
                elements=self.arg[argindex]['element']
                #print elements
                listele=[]
                listele_name=[]
                listele_val=[]
                
                for item in elements:
                    #print item
                    listele.append(item['data_type'])
                    listele_name.append(item['name'])
                    listele_val.append(str(self.structdata(item,item['name'],item['data_type'])))
                    
                #print listele
                #print listele_val
                dic['type']=listele
                dic['name']=listele_name
                dic['value']=listele_val
            json.dump(dic,fd,indent=4)

            self.gen_file.append(t)
        for item in self.gen_file:
            print item.name
        return self.gen_file
    def datagen(self,item,name,datatype,index,length,data):
        if datatype in self.typearg:#["unsigned short int","short","int","unsigned int","long","unsigned long","long long","unsigned long long"]
            if index==1:
                #print "sss"
                genlen=random.randint(0,length)
                data+="{"
                for i in range(genlen):
                    if i==genlen-1:
                        data+=str(self.mutator[datatype][6](1))
                    else:
                        data+=str(self.mutator[datatype][6](1))+","
                data+="}"
            elif index==0:
                data=self.mutator[datatype][6](1)
        elif datatype in self.typearg_char:#["unsigned char,char"]
            if index==1:
                data=self.random_string_generator(random.randint(0,length))
            elif index==0:                              
                randnum = (self.mutator["int"][6](1))%62;                    #随机数生成函数
                data= self.random_chars[randnum]; 
                if data=='\'' or data=='\"' or data=='\\':
                   data='\\'+data
        elif datatype in self.type_struct_pointer:
            print item['element']
            data+="{"
            for i in range(len(item['element'])):
                if i==len(item['element'])-1:
                   data+=str(self.structdata(item['element'][i],item['element'][i]['name'],item['element'][i]['data_type']))
                else:
                   data+=str(self.structdata(item['element'][i],item['element'][i]['name'],item['element'][i]['data_type']))+","
                
            data+="}"
        elif datatype in self.typepointer:
            '''
            num=random.randint(-1,0)
            if num==0:
               data=hex(self.mutator["int"][6](1))
            else:
               data="NULL"
            '''
            data="NULL"
        return data    


    def structdata(self,item,name,datatype):        
        index=isarray(name)
        #print "index:",index
        length=0
        data=""
        if index==1: #是数组求长度
           length=lengtharray(name)
           #print "len:",length
        if item['value']=="any":
            data=self.datagen(item,name,datatype,index,length,data)
        else:
            data=str(item['value'])
        #print data
        return data




    def structdata_mutator(self,name,data1,datatype,dataindex):
        index=isarray(name)
        #print "index:",index
        length=0
        data=""
        if index==1: #是数组求长度
           length=lengtharray(name)
           #print "len:",length
        if datatype in self.typearg:#["unsigned short int","short","int"]
            if index==1:
                #print "structmutator",data1
                genlen=random.randint(0,length)
                data1len=data1.count(',')  
                str0=""
                str0=data1[1:-1]
                if data1len==0 and len(str0)==0:#求长度
                   data1len=0   
                elif data1len==0 and len(str0)!=0:
                   data1len=1
                else:
                    data1len+=1
                print "data1len",data1len
              

                list0=[]
                list0=str0.split(',')
                print list0
 #data+="{"     
                #print str0
                #print list0
                list1=[]
                if genlen>=data1len and data1len>0:
                    for item in list0:
                        if datatype=="int":
                            list1.append(str(self.mutator[datatype][random.randint(0,5)](int(item))))
                        elif datatype=="short":
                            print item
                            list1.append(str(self.mutator[datatype][random.randint(0,5)](np.short(item))))
                        elif datatype=="unsigned short int":
                            list1.append(str(self.mutator[datatype][random.randint(0,5)](int(item))))
                        elif datatype=="unsigned int":
                            list1.append(str(self.mutator[datatype][random.randint(0,5)](int(item))))
                        elif datatype=="long":
                            list1.append(str(self.mutator[datatype][random.randint(0,5)](np.int_(item))))
                        elif datatype=="unsigned long":
                            list1.append(str(self.mutator[datatype][random.randint(0,5)](np.uint(item))))
                        elif datatype=="long long":
                            list1.append(str(self.mutator[datatype][random.randint(0,5)](np.longlong(item))))
                        elif datatype=="unsigned long long":
                            list1.append(str(self.mutator[datatype][random.randint(0,5)](np.ulonglong(item))))
                    ranlen=genlen-data1len
                    for i in range(ranlen):
                        list1.append(str(self.mutator[datatype][random.randint(0,5)](1)))                        
                    
                    data= data+"{"
                    for i in range(len(list1)):
                        if i==len(list1)-1:
                            data+=list1[i]
                        else:
                            data+=list1[i]+","
                    data+="}"
                else:
                    for i in range(genlen):
                        if datatype=="int":
                            list1.append(str(self.mutator[datatype][random.randint(0,5)](int(list0[i]))))
                        elif datatype=="short":
                            list1.append(str(self.mutator[datatype][random.randint(0,5)](np.short(list0[i]))))
                        elif datatype=="unsigned short int":
                            list1.append(str(self.mutator[datatype][random.randint(0,5)](int(list0[i]))))
                        elif datatype=="unsigned int":
                            list1.append(str(self.mutator[datatype][random.randint(0,5)](int(list0[i]))))
                        elif datatype=="long":
                            list1.append(str(self.mutator[datatype][random.randint(0,5)](np.int_(list0[i]))))
                        elif datatype=="unsigned long":
                            list1.append(str(self.mutator[datatype][random.randint(0,5)](np.uint(list0[i]))))
                        elif datatype=="long long":
                            list1.append(str(self.mutator[datatype][random.randint(0,5)](np.longlong(list0[i]))))
                        elif datatype=="unsigned long long":
                            list1.append(str(self.mutator[datatype][random.randint(0,5)](np.ulonglong(list0[i]))))
                    data+="{"
                    for i in range(len(list1)):
                        if i==len(list1)-1:
                            data+=list1[i]
                        else:
                            data+=list1[i]+","
                    data+="}"    
                   
            elif index==0:#按不同类型变异
                if datatype=="int":
                   data=self.mutator[datatype][random.randint(0,5)](int(data1))
                elif datatype=="short":
                   data=self.mutator[datatype][random.randint(0,5)](np.short(data1))
                elif datatype=="unsigned short int":
                   data=self.mutator[datatype][random.randint(0,5)](int(data1))
                elif datatype=="unsigned int":
                   data=self.mutator[datatype][random.randint(0,5)](int(data1))
                elif datatype=="long":
                   data=self.mutator[datatype][random.randint(0,5)](np.int_(data1))
                elif datatype=="unsigned long":
                   data=self.mutator[datatype][random.randint(0,5)](np.uint(data1))
                elif datatype=="long long":
                   data=self.mutator[datatype][random.randint(0,5)](np.longlong(data1))
                elif datatype=="unsigned long long":
                   data=self.mutator[datatype][random.randint(0,5)](np.ulonglong(data1))                     
        elif datatype in self.typearg_char:#["unsigned char,char"]
            if index==1:
                #print data1
                datalen=len(data1)
                genlen=random.randint(0,length)
                if genlen>=datalen:
                    for i in range(len(data1)):
                        data+=self.charmutator(data1[i],i)
                    data+=self.random_string_generator(genlen-datalen)
                else:
                    for i in range(genlen):
                        data+=self.charmutator(data1[i],i)

            elif index==0:
                #print data1              
                data+=self.charmutator(str(data1),random.randint(0,62))
        elif datatype in self.type_struct_pointer:
            for item in self.cmd:            
                if item==self.key:
                   type=self.cmd[item]
                   print type
                   countstr=item
               
                   count=item[(item.find('d')+1):]
                   print count
                   break
                else:
                   continue    
            argindex="arg"+str(count)                 
            mm=self.arg[argindex]['type']
            ele=self.arg[argindex]['element'][dataindex]['element']
            data1len=data1.count(',')  
            str0=""
            str0=data1[1:-1]
            if data1len==0 and len(str0)==0:#求长度
                data1len=0   
            elif data1len==0 and len(str0)!=0:
                data1len=1
            else:
                data1len+=1
            list0=[]
            list0=str0.split(',')
            print "data1len",data1len
            data+="{"
            print ele               
            for item in range(len(ele)):
                if item==len(ele)-1:
                    if ele[item]['value']=="any":
                       data+=str(self.structdata_mutator(name,list0[item],ele[item]['data_type'],dataindex))
                    else:
                       data+=str(list0[item])
                else:
                    if ele[item]['value']=="any":
                       data+=str(self.structdata_mutator(name,list0[item],ele[item]['data_type'],dataindex))+","
                    else:
                       data+=str(list0[item])+","
            data+="}"    
        elif datatype in self.typepointer:
            data=data1        
            
        #print data
        return data

    def fuzztest(self,node):#根据样本json，生成测试程序
        file=node.name#输入文件名
        keys=node.keys

        count=0
        for item in self.cmd:            
            if item==keys:
               count=item[(item.find('d')+1):]
               break
            else:
                continue    
        argindex="arg"+str(count)  
        filegenpath="/home/test/Desktop/kp_cov/graph/fuzztest/"+keys
        if not os.path.exists(filegenpath):
             os.mkdir(filegenpath) 
        with open(file, 'r') as jsonFile:
          Data=json.load(jsonFile,object_hook=_byteify)
        opencmd=headfile+"int main(int argc, char *argv[]){\nint fd;\nfd=open(\""+Data['dev']+"\", O_RDWR);\nif (fd < 0) {\nprintf(\"Couldn't reopen "+Data['dev']+"\");\n}\n"
        if type(Data['type'])==list:
            str1="\ntypedef struct {\n"
            count=1
            str_struct=""
            for i in range(len(Data['type'])):
                if Data['type'][i] in self.type_struct_pointer:
                    str_struct+="struct data"+str(i)+"{\n"
                    elements=self.arg[argindex]['element'][i]['element']
                    
                    for item in range(len(elements)):
                        str_struct+=elements[item]['data_type']+" a"+str(item)+";\n"
                    str_struct+="};"    
            for item in range(len(Data['type'])):
                mm=Data['type'][item]
                name=Data['name'][item]
                #print name
                if (mm in self.typearg_char) and isarray(name):
                    str1+=mm+" a"+str(item)+chararray(name)+";\n"
                elif (mm in self.typearg) and isarray(name):
                    str1+=mm+" a"+str(item)+chararray(name)+";\n"
                elif mm in self.type_struct_pointer:
                    str1+="struct data"+str(item)+"* a"+str(item)+chararray(name)+";\n"
                else:
                    str1+=mm+" a"+str(item)+";\n"
                count+=1
            str2=str1+"} data;\ndata A;\n"           
            cou=1
            for i in range(len(Data['value'])):
                name=Data['name'][i]
                val=Data['value'][i]

                if (Data['type'][i] in self.typearg_char) and isarray(name):#["unsigned char","char"]   
                    #str2+= "A.a"+str(cou)+"=\""+val+"\";\n"
                        str2+="A.a"+str(i)+"="+"\""+val+"\";\n"
                elif (Data['type'][i] in self.typearg_char) and not isarray(name):
                        str2+="A.a"+str(i)+"="+"\'"+val+"\';\n"
                elif (Data['type'][i] in self.typearg) and isarray(name):
                        str2+="A.a"+str(i)+"="+val+";\n"
                elif Data['type'][i] in self.type_struct_pointer:
                    str2+="A.a"+str(i)+"="+"(struct data"+str(i)+" *)malloc(sizeof(A.a"+str(i)+"));\n"
                    ele=self.arg[argindex]['element'][i]['element']
                    print ele 
                    #(s1.a1[0]).a1=8193;
                    data1len=val.count(',')  
                    str0=""
                    str0=val[1:-1]
                    if data1len==0 and len(str0)==0:#求长度
                       data1len=0   
                    elif data1len==0 and len(str0)!=0:
                       data1len=1
                    else:
                       data1len+=1
                    list0=[]
                    list0=str0.split(',')
                    print "data1len",data1len               
                    for item in range(len(ele)):

                        str2+="(A.a"+str(i)+"[0]).a"+str(item)+"="+str(list0[item])+";\n"
                else:
                    if Data['type'][i]=="unsigned long long":
                        val=val+"uLL"
                    str2+="A.a"+str(i)+"="+val+";\n"

                cou+=1
            #print str2    
            genstr=str_struct+str2+"\n"+"int ret;\nret=ioctl(fd,"+str(Data['cmd'])+",&A);\nprintf(\"ret=%d\\n\",ret);\nreturn 0;\n}" 
        else:
            genstr=Data['type']+" a="+str(Data['value'])+";\n"+"int ret;\nret=ioctl(fd,"+str(Data['cmd'])+",a);\nprintf(\"ret=%d\\n\",ret);\nreturn 0;\n}" 
        
        genstr=opencmd+genstr
        #print genstr
        fileName=filegenpath+'/'+str(node.id)+'.c'
        with open(fileName,'w')as file:
            file.write(genstr)
    def exe_test(self,node):
        file=node.name#输入文件名

        keys=node.keys
        #print node.keys
        filegenpath="/home/test/Desktop/kp_cov/graph/fuzztest/"+keys
        fileName=filegenpath+'/'+str(node.id)+'.c'
        command="gcc "+fileName+" -o "+filegenpath+"/"+str(node.id)+".exe -m64"
        os.system(command)
        command1=filegenpath+"/"+str(node.id)+".exe"
        os.system('echo %s | sudo -S %s' % (sudo_password, command1))
        node.visit()
    def number_change(self,num):
        numdata=random.randint(0,5)

        return int_mutator[numdata](num)
    def sum(self,list0):
        total=0
        list1=[]
        for i in range(len(list0)):
            total+=list0[i]
            list1.append(list0[i])
        return total,list1
    
    #计算适应度斐波纳挈列表，这里是为了求出累积的适应度
    def cumsum(self,fitness1):
        for i in range(len(fitness1)-2,-1,-1):
            # range(start,stop,[step])
            # 倒计数
            total=0
            j=0
            while(j<=i):
                total+=fitness1[j]
                j+=1
            #这里是为了将适应度划分成区间
            fitness1[i]=total
        fitness1[len(fitness1)-1]+=fitness1[len(fitness1)-2]

    def selection(self,list1):
        new_fitness=[]
        #单个公式暂存器
        N=len(list1)
        sumtotal,sum_fitness=self.sum(list1)
        #将所有的适应度求和
        print sum_fitness
        print sumtotal
        #mm=np.cumsum(sum_fitness)
        self.cumsum(sum_fitness)        
        print sum_fitness
        #print mm
        result=random.uniform(0,sumtotal-1)
        print "result:",result
        index=0

        for i in range(len(sum_fitness)-1):
            #print i
            if i==0:
                if result>=0 and result<=sum_fitness[i]-1:
                    index=i
                    break
            elif i>0:
                if result>=sum_fitness[i] and result<=sum_fitness[i+1]-1:
                    index=i
                    break
        print "index:",index
        return index
    

    def sample_mutator(self,filelist,choose,disusechoose):
        file=filelist[choose].name
        file1=filelist[disusechoose].name
        with open(file, 'r') as jsonFile:
           Data=json.load(jsonFile,object_hook=_byteify)
        #if type(Data['type'])==list:
          #  print 1
        #else:#非结构体的变异  这里变异的文件还需要考虑再次保存的位置
        mm=Data['type']
        
        gendata=self.mutator[mm][random.randint(0,5)](Data['value'])
        print Data['value']
        print gendata
        Data['value']=gendata
        fd=open(file1,'w')
        json.dump(Data,fd,indent=4)
    def sample_mutator_struct(self,filelist,choose,choose1,disusechoose):
        file=filelist[choose].name
        file1=filelist[choose1].name
        file2=filelist[disusechoose].name
        with open(file, 'r') as jsonFile:
           Data=json.load(jsonFile,object_hook=_byteify)
        with open(file1, 'r') as jsonFile:
           Data2=json.load(jsonFile,object_hook=_byteify)
        length=len(Data['type'])
        print length
        cou=random.randint(0,np.power(2,length)-1)
        weishu=[]
        weishu=ten_to_two(cou,2)
        print weishu
        weishu.reverse()
        print weishu
        print Data['value']
        print Data2['value']
        for i in range(len(weishu)):
            if weishu[i]==1:
                buff=Data['value'][i]
                buff2=Data2['value'][i]
                Data['value'][i]=buff2
                Data2['value'][i]=buff
            else:
                continue
        print Data['value']
        print Data2['value']
        ismuta=random.randint(0,100)
        if ismuta<=10:
            for i in range(len(Data['value'])):

                str1=Data['name'][i]
                str2=Data['value'][i]
                Data['value'][i]=str(self.structdata_mutator(str1,str2,Data['type'][i],i))
                
            for i in range(len(Data2['value'])):
                
                str1=Data2['name'][i]
                str2=Data2['value'][i]
                Data2['value'][i]=str(self.structdata_mutator(str1,str2,Data2['type'][i],i))
        print Data['value']
        print Data2['value']
        fd=open(file,'w')
        json.dump(Data,fd,indent=4)
        filelist[choose].clear()        
        fd1=open(file1,'w')
        json.dump(Data2,fd1,indent=4)
        filelist[choose1].clear()
                #Data2['value'][i]=self.arg[argindex]['element'][i]['name']+":"+str(self.structdata(item['name'],item['data_type'])
        #if type(Data['type'])==list:
          #  print 1
        #else:#非结构体的变异  这里变异的文件还需要考虑再次保存的位置
    '''    
        mm=Data['type']
        
        gendata=self.mutator[mm][random.randint(0,5)](Data['value'])
        print Data['value']
        print gendata
        Data['value']=gendata
        
        
        fd=open(file1,'w')
        json.dump(Data,fd,indent=4)
    '''


    def disuseprobability(self,list0,total):
  
        list1=[]
        length=len(list0)
        print list0
        sum=0
        for i in list0:
            a=float(total-i)/total
            b=(length-1)
            p=a/b
            sum+=p
            list1.append(p)
        print sum
        return list1
    def disuse(self,list1):
        
        new_fitness=[]
        new_fitness2=[]
        for i in range(len(list1)):
            new_fitness2.append(i)
        print new_fitness2
        #单个公式暂存器
        N=len(list1)
        sumtotal,sum_fitness=self.sum(list1)
        #将所有的适应度求和
        print sum_fitness
        new_fitness=self.disuseprobability(sum_fitness,sumtotal)
        print new_fitness
        p = np.array(new_fitness)
        #np.random.seed(0)
        index = np.random.choice(new_fitness2, p = p.ravel())
        print "index:",index
        return index
    def select_mutator(self,filelist):          
        list1=[]       
        for i in range(len(filelist)):
            list1.append(filelist[i].fitness)
        if filelist[0].type=="struct":            
            choose=self.selection(list1)
            list2=[]
            for i in range(len(list1)):
                 if i!=choose:
                    list2.append(list1[i])
                 else:
                    continue
            choose1=self.selection(list2)
            if choose1>=choose:
                choose1+=1
            print "choose:",choose
            print "choose1",choose1
            disusechoose=self.disuse(list1)
            self.sample_mutator_struct(filelist,choose,choose1,disusechoose)    
        else:
            choose=self.selection(list1)
            disusechoose=self.disuse(list1)
            self.sample_mutator(filelist,choose,disusechoose)
             
        print filelist[0].type 
 

if __name__=='__main__':
    with open('snd.json', 'r') as jsonFile:
          weatherData = json.load(jsonFile,object_hook=_byteify)
    #Data=json.loads(weatherData)
    #print(type(weatherData))

    m=Mutators(weatherData)
    m.printinfo()
    m.gen_sample1('SNDRV_CTL_IOCTL_CARD_INFO')
    m.fuzztest()
    #m.gen_sample('SNDRV_CTL_IOCTL_PVERSION')


'''
    def longlong_num(self,type):
        return random.randint(-32768,32767)    
    def unsigned_char(self,type):
        return random.randint(-32768,32767)    
    def unsignedshortint_num(self,type):
        return random.randint(-32768,32767) 
   def printinfo(self):
        print self.dev
        print self.cmd
        for item in self.cmd:
            print item
        print self.arg
       # "unsigned char","signed char",,"signed int" ,"unsigned int", "long long"

    def gen_sample(self,keys):#生成样本json，json中cmd得有序号才行
        filegenpath="/home/test/Desktop/kp_cov/graph/input/"+keys
        if not os.path.exists(filegenpath):
             os.mkdir(filegenpath)
                
        for i in range(20):
            os.mknod(filegenpath+"/"+str(i)+".json")

        type=''
        count=0
        print keys
        for item in self.cmd:            
            if self.cmd[item]['name']==keys:
               type=self.cmd[item]['value']
               print type
               countstr=item
               count=self.cmd[item]['id']
               break
            else:
                continue    
        argindex="arg"+str(count)                 
        mm=self.arg[argindex]['type']
        #print self.arg[argindex]
        
        if mm in self.typearg:
            gendata=self.mutator[mm][6](1)
            dic = collections.OrderedDict()
            dic['dev']=self.dev
            dic['cmd']=self.cmd[countstr]['value']
            dic['type']=mm
            dic['value']=gendata
            print dic
            json.dump(dic,open('input/configuration.json','w'),indent=4)
            self.gen_file.append('input/configuration.json')
            print self.gen_file
        elif mm=="struct":
            print "struct"
            elements=self.arg[argindex]['element']
            print elements
            listele=[]
            listele_val=[]
            for item in elements:
                print item
                listele.append(item['data_type'])

                listele_val.append(item['name']+":"+str(self.structdata(item['name'],item['data_type'])))
                
            print listele
            print listele_val
            dic = collections.OrderedDict()
            dic['dev']=self.dev
            dic['cmd']=self.cmd[countstr]['value']
            dic['type']=listele
            dic['value']=listele_val
            print dic
            json.dump(dic,open('input/configuration.json','w'),indent=4)
            self.gen_file.append('input/configuration.json')
            #print self.gen_file


'''
'''    #存活的种群
        population_length=pop_len=len(population)
        #求出种群长度
        #根据随机数确定哪几个能存活
    
        for i in range(pop_len):
            ms.append(random.random())
        # 产生种群个数的随机值
        ms.sort()
        # 存活的种群排序
        fitin=0
        newin=0
        new_population=new_pop=population
    
        #轮盘赌方式
        while newin<pop_len:
            if(ms[newin]<new_fitness[fitin]):
                new_pop[newin]=pop[fitin]
                newin+=1
            else:
                fitin+=1
        population=new_pop
'''