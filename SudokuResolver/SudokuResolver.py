# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 16:30:05 2023

@author:  xaju5
"""

import numpy as np

#==========
#PARAMETERS
#==========

solution = np.zeros((9,9))
sudoku = np.zeros((9,9))
option = None
filename='arrays.npz'

#==============
#MENU FUNCTIONS
#==============
def printMenu():
    print("\nWhat do you want to do?"+
          "\n0-Exit"+
          "\n1-Insert sudoku"+
          "\n2-Insert solution"+
          "\n3-Print sudoku"+
          "\n4-Print solution"+
          "\n5-Solve sudoku"+
          "\n"+
          "\n6-Load arrays"+
          "\n7-Save arrays")
    
def fillArray(array):
    """
    Fills the array with the input of the user

    Parameters
    ----------
    array : TYPE
        The array that will be filled.

    Returns
    -------
    None.

    """
    
    for r in range(9):
        print("\nInsert "+str(r)+"row (write 0 for unknow values): ")
        row = input()
        c = 0
        for value in row:
            array[r,c] = value
            c +=1
            
def printArray(array):
    """
    Print the array divided by lines, for easier reading

    Parameters
    ----------
    array : TYPE
        array to print.

    Returns
    -------
    None.

    """
    print("\n")
    numrow = 0
    for row in array:
        #Checks if is needed to print a horizontal line
        if numrow % 3 == 0 and numrow != 0:
            print("--- --- ---")
        numrow += 1
        
        numcolum = 0
        for colum in row:
            #checks if it is needed to print a vertical line
            if numcolum % 3 == 0 and numcolum != 0:
                print("|",end='')
            numcolum += 1
            
            #actual array[r,c] is printed:
            print(int(colum),end='')
        print("\n")
            
def loadArray():
    ans = input("\nAre you sure that you want to LOAD the file?(y/n):")
    if ans == 'y':
        with np.load(filename) as file:
            global sudoku, solution
            sudoku = file['a']
            solution = file['b']
        print("\n>>Arrays loaded")
    else:
        print("\nOperation aborted")

def saveArray():
    ans = input("\nAre you sure that you want to OVERWRITE the file?(y/n):")
    if ans == 'y':
        np.savez(filename,a=sudoku,b=solution)
        print("\n>>Arrays saved")
    else:
        print("\nOperation aborted")
 
#===================
#ALGORITHM FUNCTIONS
#===================
def resolveSudoku():
    print("TODO")
 
#=============
#MAIN fUNCTION
#=============
while option != "0":
    printMenu()
    option = input("Choose one:")
    if option == "0":
        print("\n>>EXIT")
    elif option == "1":
        fillArray(sudoku)
    elif option == "2":
        fillArray(solution)
    elif option == "3":
        printArray(sudoku)
    elif option == "4":
        printArray(solution)
    elif option == "5":
        resolveSudoku()
    elif option == "6":
        loadArray()
        
    elif option == "7":
        saveArray()
    else:
        print("\n>>Wrong value!!")
          
   
    
