#!/usr/bin/python
# -*-coding:utf-8 -*-
import os
import sys



import time
from filepath import base
from filepath import basedir
from filepath import headfile_path
from filepath import idafile_path

from filepath import file_name
from filepath import file_path
from filepath import file_result
from filepath import func_address_path
from filepath import sudo_password
from filepath import idapro_dir
from filepath import file_path_c
from filepath import file_kprobes
from filepath import file_coverage_middle
from filepath import basefunc
from filepath import file_makefile
sys.path.append(file_path_c) #adress_of_B 表示文件B的地址
import auto_make



def c_headfile(str):
    file_object = open(str)  
    try:
	    context = file_object.read()
    finally:
        file_object.close()
#print file_context
    return context



def ida_script():#idapython
  if file_name.find("x64")>=0:#check file name
     os.system("wine "+idapro_dir+"64.exe -A -c -S"+base+idafile_path+" "+ file_path + file_name)#binary file path 
     print
  else:
     os.system("wine "+idapro_dir+".exe -A -c -S"+base+idafile_path+" "+file_path + file_name)#binary file path 
  return


#all func address in txt 
#get the dictionary first item address in memory(kernel)
def address_txt(str,path,passwd):
   command="cat /proc/kallsyms |grep -w -E "+str+">"+path
   os.system('echo %s | sudo -S %s' % (passwd, command))
   return 


#ida blocks infomation take into dictionary
#create str to complete the .c file
def c_file_mainbody():
   var_shengming=""
   kp_hook=""
   zhuce_hook=""
   cuowu_tishi=""
   pr_info=""
   exit_hook=""
   pr_info_exit=""
   dict_struct={}
   context=""
   


   blockfenxi=open(file_result,"r")
   for line1 in blockfenxi:#Traverse function
     buffer="  short "
     if line1.find('0x')<0:
        str_han=""
        shu=0
        list1=line1.strip().split(' ')
        str_han=list1[0]#fun name
        shu=list1[1]#num
        address=[]

        for i in range(int(list1[1])):#Traverse blocks
            str_name=list1[0]+str(i)
            str_name=str_name.replace('.','_')
            kp_hook+="  kp_"+str_name+".pre_handler="+str_name+"_handler_pre;\n"
            zhuce_hook+="  ret_"+str_name+" = register_kprobe(&kp_"+str_name+");\n"
            
            #cuowu_tishi+="if(ret_"+str_name+" < 0) {\n  pr_err(\"register_kprobe failed, returned %d\\n\", "+"ret_"+str_name+");\n  return ret_"+str_name+";\n}\n"
            #pr_info+="  pr_info(\"Planted kprobe at %p\\n\", kp_"+str_name+".addr);\n"
            #pr_info_exit+="  pr_info(\"kprobe at %p unregistered\\n\", kp_"+ str_name+".addr);\n"
            

            exit_hook+="  unregister_kprobe(&kp_"+str_name+");\n"
            if(i==int(list1[1])-1):
               buffer+="ret_"+str_name+";\n"
            else :
               buffer+="ret_"+str_name+","
        var_shengming+=buffer
     else:
         address.append(line1.strip())
         str_han=str_han.replace('.','_')
         dict_struct[str_han]=[shu,address]
         continue
   blockfenxi.close()
  
#get the dictionary first item address in memory(kernel)

   fbase=open(basefunc,'r')
   try:
       base_name=fbase.read()
   finally:
       fbase.close()
   command="cat /proc/kallsyms |grep -w "+base_name+">"+func_address_path
   os.system('echo %s | sudo -S %s' % (sudo_password, command))
   file_object = open(func_address_path)  
   try:
       address=file_object.read()	
   finally:
       file_object.close()

   list3=address.split(' ')
   print list3
   base_address=int(list3[0],16)
   print list3[0]
   base_ida_adress=int(dict_struct[base_name][1][0],16)
   base_caclu=base_address-base_ida_adress
   print base_address
   print base_ida_adress
   address_len=len(dict_struct.items()[0][1][1][0])
#create struct
   struct="\nstatic struct kprobe kp_"
   struct_lp="\n= {\n"
   struct_rp=" };\n"
   struct_deal="\nstatic int __kprobes "
   deal_lp="(struct kprobe *p, struct pt_regs *regs){\n"
   pr_biaoji_lp="   printk(KERN_DEBUG\""
   pr_biaoji_rp="\\n\");\n   return 0;\n"
   deal_rp=" };\n"
   deal_buffer=""
   count=0
   fp=open(file_coverage_middle,'w+')
   for key in dict_struct:
       #print dict_struct[key]
       for i in range(int(dict_struct[key][0])):
          #print hex(dict_struct[key][1][i][2:address_len])
           count+=1
           b=base_caclu+int(dict_struct[key][1][i],16)
           print '%s 0x%016x'%(key,b)
           fp.write('%s 0x%016x\n'%(key,b))
           b_str= "{:016x}".format(b)
           context+=struct+key+str(i)+struct_lp+"   .addr=(kprobe_opcode_t *)0x"+b_str+",\n"+struct_rp   #content xiugai
           deal_buffer+=struct_deal+key+str(i)+"_handler_pre"+deal_lp+pr_biaoji_lp+"(make_by_sgd!) <"+key+" "+str(i)+">"+str(count)+pr_biaoji_rp+deal_rp
   fp.close()
   pr_info+="  return 0;\n}\n"
   pr_info_exit+="}\n"
   init_shengming="\nstatic int __init kprobe_init(void){\n"
   exit_shengming="\nstatic void __exit kprobe_exit(void){\n"
   GPL_shengming="module_init(kprobe_init)\nmodule_exit(kprobe_exit)\nMODULE_LICENSE(\"GPL\");"
   
   context+=deal_buffer+init_shengming+var_shengming+kp_hook+zhuce_hook+cuowu_tishi+pr_info+exit_shengming+exit_hook+pr_info_exit+GPL_shengming
   return context


def c_file_create(str,context,cpath):
   create_c=cpath+str[0:str.find('.')]+".c"
   
   file_object = open(create_c,'w+')  
   try:
       file_object.write(context)
   finally:
       file_object.close()
   return str[0:str.find('.')]

def makefile_create(str,name):
    file_object = open(str,'w+')  
    string="ifneq ($(KERNELRELEASE),)\nobj-m :="
    string1=name[0:name.find('.')]+"_kprobes.o"
    string+=string1
    string+="\nelse\nKDIR :=/lib/modules/$(shell uname -r)/build\nall:\n	make -C $(KDIR) M=$(PWD) modules\nclean:\n	rm -f *.ko *.o *.mod.o *.mod.c *.symvers *.order *.cmd *.mk\nendif" 
    try:
       file_object.write(string)
    finally:
       file_object.close() 

if __name__=="__main__":    
    file_context=""
    file_context=c_headfile(headfile_path)
    ida_script()

    file_context+=c_file_mainbody()
    target=c_file_create(file_kprobes,file_context,file_path_c)
    pwd=os.getcwd()
    makefile_create(file_path_c+file_makefile,file_name)
    auto_make.auto_process(sudo_password,file_path_c,file_kprobes)
    print file_kprobes
    os.chdir(pwd)
    print pwd
