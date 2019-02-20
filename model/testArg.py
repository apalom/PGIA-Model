# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 09:50:40 2019

@author: Alex
"""

import sys

print('Function Name: ', sys.argv[0])

a = int(sys.argv[1])
b = int(sys.argv[2])

print(a + b)

#
#import argparse, sys
#
#parser=argparse.ArgumentParser()
#
#parser.add_argument('--bar', help='Do the bar option')
#parser.add_argument('--foo', help='Foo the program')
#
#args=parser.parse_args()
#
#print args
#print sys
