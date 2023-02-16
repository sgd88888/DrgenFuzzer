# -*- coding: utf-8 -*-
import sys
import random
import string
import math

def number_change(num):
    numdata=random.randint(0,5)
    string_mutator = {
            0: lambda x: x^2,
            1: lambda x: -x,
            2: lambda x: 2*x,
            3: lambda x: x/2,
            4: lambda x: x+1,
            5: lambda x: int(math.sqrt(x)),
        }
    return string_mutator[numdata](num)

if __name__=='__main__':



    print number_change(10)