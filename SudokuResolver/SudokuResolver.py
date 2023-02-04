# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 16:30:05 2023

@author:  xaju5
"""

import numpy as np

#Parameters
solution = np.zeros((9,9))
unsolved = np.zeros((9,9))
option = None

#FUNCTIONS
def fillArray(array):
    
    for r in range(9):
        print("Insert "+str(r)+"row: ")
        row = input()
        c = 0
        for value in row:
            array[r,c] = value
            c +=1
            
def printArray(array):
    print(array)


#MAIN
while option != "0":
    print("What do you want to do? \n0-Exit \n1-insert unsolved array \n2-Insert solution \n3-print unsolved \n4-print solution \n5-save arrays \nChoose one:")
    option = input()
    if option == "0":
        print("exit")
        break
    if option == "1":
        fillArray(unsolved)
    if option == "2":
        fillArray(solution)
    if option == "3":
        printArray(unsolved)
    if option == "4":
        printArray(solution)
    if option == "5":
        print("TODO")
   
    
