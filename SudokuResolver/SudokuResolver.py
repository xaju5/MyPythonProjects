# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 16:30:05 2023

@author:  xaju5
"""

import numpy as np

#==========
#PARAMETERS
#==========
UNKNOW_NUMBER = 0 #The number is avaliable to use
USED_NUMBER = 1 #The number has been used in the same row or colum

solution = np.zeros((9,9)).astype(int)
sudoku = np.zeros((9,9)).astype(int)
solvingarray = np.zeros((10,9,9)).astype(int)

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
    It Fills the array with the input of the user

    Parameters
    ----------
    array : TYPE
        The array that will be filled.

    Returns
    -------
    None.

    """
    
    for r in range(9):
        print(f'\nInsert {r} row (write 0 for unknow values): ')
        row = input()
        c = 0
        for value in row:
            array[r,c] = value
            c +=1
            
def unpack(iterable):
    """
    It takes the items and yields them one by one. 

    Parameters
    ----------
    iterable : 9x9 array
        The array to unpack.

    Yields
    ------
    generator object
        All number stored into the array. Tt stores the values of the array into one direction

    """
    for item in iterable:
        yield from item
        
            
            
def printArray(array):
    """
    It Prints the array formated as a sudoku
    
    Parameters
    ----------
    array : 9x9 array
        array to print.

    Returns
    -------
    None.

    """
    outline = \
    """\
    +-----------------------+
    | {} {} {} | {} {} {} | {} {} {} |
    | {} {} {} | {} {} {} | {} {} {} |
    | {} {} {} | {} {} {} | {} {} {} |
    +-----------------------+
    | {} {} {} | {} {} {} | {} {} {} |
    | {} {} {} | {} {} {} | {} {} {} |
    | {} {} {} | {} {} {} | {} {} {} |
    +-----------------------+
    | {} {} {} | {} {} {} | {} {} {} |
    | {} {} {} | {} {} {} | {} {} {} |
    | {} {} {} | {} {} {} | {} {} {} |
    +-----------------------+
    """ 
    print(outline.format(*unpack(array))) #unpack() stores the values of the array into one direction so it is necesary to obtain its *value
          

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
def createSolvingArray():
    global solvingarray
    solvingarray[0,:,:] = sudoku.copy() #Copy the sudoku to the solving array

def markUsedNumbers():
    """
    It marks the rows, colums and squares if the number is used and, therefore, it cannot be used in that position.

    Returns
    -------
    None.

    """
    global solvingarray
    numrow = 0
    for row in solvingarray[0,:,:]: 
        numcolum = 0 
        for value in row:
            if value != UNKNOW_NUMBER: #If one value asigned, deny it in all its row and columns
                solvingarray[1:,numrow,numcolum] = USED_NUMBER #mark all for this number
                solvingarray[int(value),numrow,:] = USED_NUMBER #mark row as used
                solvingarray[int(value),:,numcolum] = USED_NUMBER #mark colum as used
                
                squarerow = int(numrow/3) #the offset of the squares
                squarecolum = int(numcolum/3)
                for r in range(3):
                    for c in range(3):
                        posr = (3*squarerow) + r
                        posc = (3*squarecolum) + c
                        solvingarray[int(value), posr, posc] = USED_NUMBER #mark the square as used                
#                if numrow== 8:
#                    print("Value: "+str(value)+" square: ["+str(squarerow)+str(squarecolum)+"] pos: ["+str(posr)+str(posc)+"]")
            numcolum += 1
        numrow += 1   
#    print(solvingarray)
 
def checkNewValues():
    """
    Check every row in the x axis. If there is only one zero, the position of the zero is the final value of that row.

    Returns
    -------
    None.

    """
    global solvingarray
    for y_index in range(9): #The total number of colums is 9
        for z_index in range(9): 
            row = solvingarray[1:,y_index,z_index] 
            position = np.where(row==0)
            if np.size(position) == 1:
#                print(position)
                solvingarray[0,y_index,z_index] = position[0] + 1 #+1 because the first is the value of the array and not one posible solution.
                
def checklonelyNumbers():
    """
    Check if in the colum of each value of x in solvingarray(x,y,z) has only one zero. If it does, mark the value of x as the response of that position (y,z)

    Returns
    -------
    None.

    """
    global solvingarray
    for x_index in range(1,10): #all posible values are between 1-10's 2Dmatrix
        for z_index in range(9):  #The total number of colums is 9
#            print(x_index,z_index)
            row = solvingarray[x_index,:,z_index]
            position = np.where(row==0)
            if np.size(position) == 1:
                solvingarray[0,position[0] + 1,z_index] = x_index  #+1 because the first is the value of the array and not one posible solution.
    
                   
def resolveSudoku():
    createSolvingArray()
    for i in range(2):
        print(i," iteration completed")
        markUsedNumbers()
        checkNewValues()
        checklonelyNumbers()
    
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
          
   
    
