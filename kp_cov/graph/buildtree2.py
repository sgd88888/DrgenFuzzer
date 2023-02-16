# -*- coding: utf-8 -*-
import networkx as nx
from pprint import pprint as pt
import matplotlib.pyplot as plt
class TreeNode(object):
    '''
    树的节点
    '''
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent=[]
        self.depth=0
        self.is_visit=0
        self.visit_num=0
        #self.depth=depth  #与根的距离

    def setdepth(self,depth):
        self.depth=depth

class MultiTree(object):
    '''
    树的操作：
    增、删、改、查
    '''
    def __init__(self, tree_root_name='root'):
        self.count = 0
        self.tree = TreeNode(tree_root_name)#root
        self.search_result_parent = []
        self.search_result_children = []
        self.allnode=[]
        self.name=tree_root_name
    
    
    def treeinit(self, num):#增加节点
        self.count=num
        for i in range(num):
            t=TreeNode(str(i))
            self.allnode.append(t)
            #root_children = self.tree.children  
           # root_children.append(t)    #更新root的children
           # self.tree.children = root_children
            #print('Add node:%s sucessfully!' % t.name)
        #print self.allnode[18].name           
        #print self.allnode
    def add(self,node,parent=None):
        anum=int(node.name)
        
        if parent==None:           
            root_parent=self.allnode[anum].parent
            root_parent.append(self.tree)           
            self.allnode[anum].parent=root_parent           
            root_children = self.tree.children             
            root_children.append(node)    #更新root的children
            self.tree.children = root_children
            
        else:
            bnum=int(parent.name)                
            parent_list=self.allnode[anum].parent
            parent_list.append(parent)
            self.allnode[anum].parent=parent_list
            children_list =self.allnode[bnum].children
            children_list.append(node)
            self.allnode[bnum].children = children_list
            #for item in self.allnode[bnum].children:
               # print item.name
    def visit(self,node):
        '''
        检索出节点，更改其是否访问过的变量

        '''        
        self.allnode[int(node.name)].is_visit=1        
        self.allnode[int(node.name)].visit_num+=1
        #print self.allnode[int(node.name)].visit_num
    def show(self):
        for i in range(self.count):
            print self.allnode[i].name
            str2=""
            for parent in self.allnode[i].parent:
                str2+=parent.name+','
            for child in self.allnode[i].children:
                str2+=child.name+','
            print "["+str2+"]"
    def search_children(self, node):
        '''
        检索节点
        打印出其父节点的name以及其下一层所有子节点的name
        '''
        self.search_result_children=[]
        for item in self.allnode[int(node.name)].children:
            self.search_result_children.append(item.name)
        return self.search_result_children
    def search_childtree(self, node):        
        #检索子树
        childtree_node=[]
        G = nx.DiGraph()
        self.to_graph_recursion(self.tree, G)
        ff=self.allnode[int(node.name)].name
        T = nx.dfs_tree(G, source=ff, depth_limit=5)
        retree=[]
        for item in T.nodes:
            if ff==item:
                continue
            else:
                retree.append(int(item))
        return retree
    def show_tree(self):
        '''
        利用networkx转换成图结构，方便结合matplotlib将树画出来
        '''
        G = nx.DiGraph()
        self.to_graph_recursion(self.tree, G)
        #print G.nodes
        nx.draw(G, with_labels=True)
        plt.show()
    def to_graph_recursion(self, tree, G):
        '''
        将节点加入到图中
        '''

        G.add_node(tree.name)
        for child in tree.children:
            G.add_nodes_from([tree.name, child.name])
            G.add_edge(tree.name, child.name)
        for i in range(self.count):
            for item in self.allnode[i].children:
                G.add_nodes_from([self.allnode[i].name, item.name])
                G.add_edge(self.allnode[i].name, item.name)
            



