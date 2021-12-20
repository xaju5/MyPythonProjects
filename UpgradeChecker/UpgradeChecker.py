# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 17:46:58 2021

@author: xaju5
"""

import pandas as pd

filename_Original = "NuevosCambiosRaw.txt"
filename_Filtered = "CambiosAAA.txt"
teamName = "AAA"
#TODO: Change to dataframe
upgradeData = pd.Series(index=["Tech","Network","Location","Version"])


#Step 1: Read data
file = open(filename_Original,"r")
rawData = file.read()
file.close()

#Step2: Filter unecesary information
rawLines = rawData.splitlines()
teamLines = []
for line in rawLines:
    if line.find(teamName) > 0:
        teamLines.append(line + '\n')

file = open(filename_Filtered,"w")
file.write(''.join(teamLines))
file.close()

#Step3: Data processing
for line in teamLines: #TODO
    print(line.split("-"))
    print('\n')