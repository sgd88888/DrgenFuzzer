# -*- coding: utf-8 -*-
import os
import sys
import json
from buildtree2 import TreeNode,MultiTree 



def countnum():
    fbase=open("num.txt",'r')
    try:
        total_num=fbase.read()
    finally:
        fbase.close()
    
    num=int(total_num)
    return num
    # with open("1.txt", 'r') as fp:

def graph(dc_tree):
    cnt=countnum()
    dc_tree={} 
    index=0
    with open("pred.txt", 'r') as fp:
        lines = fp.readlines()
        i=0
        while(i<cnt):#按各个函数分
            func_name=lines[index].split(' ')[0]
            func_num=int(lines[index].split(' ')[1].strip())
            func_name=func_name.replace('.','_')
            tree=MultiTree(func_name)
            tree.treeinit(func_num)
            j=0
            index=index+1
            #print func_name
            while(j<func_num):#各个函数的基本块
                if(lines[index][0] == 'b'):
                    id=lines[index].split(' ')[1].strip()
                    block_name=lines[index].split(' ')[0].split(':')[1]
                    t=TreeNode(id)
                    #print "id:"+id
                    #tree.add(t)
                    index=index+1
                    #print index
                    if(lines[index][0] != 'b' and lines[index][0] != 'p'):
                        pred_num=int(lines[index].strip())
                        #print pred_num
                        if(pred_num==0):
                            tree.add(t)
                            index=index+1                            
                        else: 
                            index=index+1
                            z=0
                            while(z<pred_num):#按pred
                                if(lines[index][0]=='p'):
                                    cid=lines[index].split(':')[1].strip()
                                    #print id,cid                                       
                                    tree.add(t,TreeNode(cid))
                                index=index+1
                                z=z+1
                        
                j=j+1
            dc_tree.setdefault(func_name,tree)
            i=i+1
    #for item in dc_tree:
        #dc_tree[item].show_tree()
    return dc_tree    


   
   #访问 dc_tree["my_ioctl"].visit(TreeNode(2))


'''#print list_tree[0].search(TreeNode('4'))
    # main()
     #print(list_tree)
    def DumpJson(InPath, OutPath):
    mp = {} 
    with open(InPath, 'r') as fp:
        lines = fp.readlines()
        mp['FunctionName'] = lines[0].split(' ')[0]
        mp['BlockNumber'] = int(lines[0].split(' ')[1].strip())
        mp['Block'] = []
        index = 1
        i = 0
        while(i < mp['BlockNumber']):
            if(lines[index][0] == 'b'):
                block = {}
                block['Address'] = lines[index].split(' ')[0].split(':')[1]
                block['Id'] = int(lines[index].split(' ')[1].strip())
                index += 1
                block['SuccsNumber'] = int(lines[index].strip())
                block['Succs'] = []
                index += 1
                j = 0 
                while(j<block['SuccsNumber']):
                    block['Succs'].append(int(lines[index].split(':')[1].strip()))
                    j += 1
                    index += 1
                mp['Block'].append(block)
                i += 1
        with open(OutPath, 'w') as wp:
            json.dump(mp, wp)
'''
# def main():
#     with open('1.json', 'r') as fp:
#         mp = json.load(fp)
#         tree = Function(mp)
 