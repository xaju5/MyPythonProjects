# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 17:46:58 2021

@author: xaju5
"""

import pandas as pd

filename_Original = "NuevosCambiosRaw.txt"
filename_Filtered = "CambiosAAA.txt"
teamName = "AAA"
upgradeDF = pd.DataFrame(columns=["Network","New Version"])



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
    if(line.find("pgrade") >= 0):
        splitedLine = line.split(" - ")
        techName = splitedLine[1].split(" ")[0]
        networkName = splitedLine[1].split(" ")[1]
       
        if(len(splitedLine[2]) == 1):
            location = splitedLine[2]
        elif(splitedLine[2].split(" ")[0] == "Ramal"):
            location = splitedLine[2].split(" ")[0] + " " + splitedLine[2].split(" ")[1]
        else:
            print(splitedLine[2])
            location = splitedLine[2].split(" ")[1]        
         
        upgradeTextPos = line.find("pgrade a")    
        if(upgradeTextPos >= 0):
            upgradeText = line.split("pgrade a ")
            versionName = upgradeText[1].split(" ")[0]
            versionName = versionName[:-1]
        else:
            upgradeTextPos = line.find("pgrade v")    
            if(upgradeTextPos >= 0):
                upgradeText = line.split("pgrade v")
                versionName = upgradeText[1].split(" ")[0]
       
        upgradeDF.loc[techName + " " + location] =[networkName,versionName]

#Step 4: Representation
print("Number of total changes: " + str(len(rawLines)))        
print("Number of team changes: " + str(len(teamLines)))
upgradeDF = upgradeDF.sort_index()
print("Results: ")
print(upgradeDF)