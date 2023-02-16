# -*- coding: utf-8 -*-

#输入：基本块访问情况vis；希望节点序列H；后继节点序列S；
#本次测试覆盖节点序列V
def analyze():
    file_object1=open(file2,"r")#Analyze coverage file log
    for line in file_object1:
        if (line.find('<') != -1):
		list1=line[line.find('<'):-1].strip().split(' ')
		funname=list1[0][1:]
		#print funname
		list2=list1[1].split('>')
		num=int(list2[0],10)
		#print num
		dc[funname][num-1]=1
    #print dc   
    file_object1.close()


def fitness_p(vis):
    flag = False
    
    
    '''
    for each node in V:
        UPDATEVIS(node, VIS) #更新访问次数
        if node not in VIS:
          flag = True
    if flag:
      UPDATEHOPESEQ(V, H) #更新希望节点序列
      UPDATESUCCSEQ(V, S) #更新后继节点序列
    sum = 0
    for each node in H:
        sum = sum + CALCFITNESS(node, VIS, S)
    P = sum * F(x) #F(x)调整函数，x为样本测试次数
    return P
    '''

if __name__ =="__main__":
    total=deal(file_coverage_middle,file_coverage,total_num,file_name)
    print 'Total Coverage %.2f'%(total) 



