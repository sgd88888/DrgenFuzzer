import re
import random
import string
import os
import string
supported_types = ['a', 'n', 's']
count_types = []



def charmutator(charaim,index):
    a=ord(charaim)#ASCII码
    b=index#字符位置
    num=a+b
    
    randnum = rand()%62;                    #随机数生成函数
    = str_array[randnum];          #从字符数组中取值




                    
'''    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";  
pun=[i for i in string.punctuation]
#num_set=[chr(i) for i in range(48,58)]
#char_high=[chr(i) for i in range(65,91)]
#char_set=[chr(i) for i in range(97,123)]
char=[chr(i) for i in range(97,123)]
total_set=char#num_set+char_high+char_set
value="".join(random.sample(total_set,bits))
return value 
'''
def fuzzyfy(types, length):

    # check type and length parameters for validity
    try:
        int(length)
    except Exception:
        return None

    if types == '' or types == "":
        return None

    elif length < 1:
        return None


    # build fuzzy string
    fuzzystr = str("")
    for i in range(0, length):
        fuzzystr += str(_type_to_char(random.choice(types)))

    # check fuzzy string for expected legth
    if len(fuzzystr) == length:
        return fuzzystr
    else:
        return None


def _type_to_char(type):
    # returns character for a given type
    if type == "a":
        return(random.choice(string.ascii_lowercase + string.ascii_uppercase))
    elif type == "n":
        return(random.choice(string.digits))
    elif type == "s":
        return(random.choice(string.punctuation))
    else:
        return str("")


def test():
    
    print(fuzzyfy('ans', 2))
    
   

    print(fuzzyfy('ans', 11))



if __name__ == '__main__':
    pun=[i for i in string.punctuation]
    num_set=[chr(i) for i in range(48,58)]
    print(num_set)