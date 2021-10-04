# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 18:20:46 2021

@author: Usuario
"""

#Script to create the map of the pandemicSim

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle
pi = np.pi

##########
###InitialParameters
##########
NCLUSTERS = 5   #Number of total clusters per type
NHOUSES = 5     #Number of houses in each cluster
NMEETINGS = 3  #Number of meetings in each cluster

MAPSIZE = 500
RADIO = 10

houseCenters = np.array([]).reshape(0,2)
meetingCenters = np.array([]).reshape(0,2)
polygonCenters = np.array([]).reshape(0,2)
##########
###Funtions
##########

#Returns the center of a cluster that does not colide with other obstacules
def getClusterPosition(polyRadio):
    
    distance = polyRadio+2*RADIO
    checkingPos = True
    
    #To check infite loop
    correct = True
    protection = 0
    
    while (checkingPos):
        
        center = MAPSIZE*np.random.rand(2)
        
        # Is the whole cluster inside the map?
        if center[0]>distance and center[1]>distance and (center[1]+distance)<MAPSIZE and (center[0]+distance)<MAPSIZE:
            
            # Does it overlap any previous circles?
            for pc in polygonCenters:
                d=np.sqrt((center[0]-pc[0])**2 + (center[1]-pc[1])**2)
                
                if d < (distance*2): #If they colide stop counting and restart
                    checkingPos = True 
                    break
                else:
                     checkingPos = False # If not, continue
               
                    
            #if it is the first center continue        
            if len(polygonCenters) == 0 :
                 checkingPos = False 
                    
        # Are we stuck? check infinite loop
        protection+=1
        if (protection > 1000):
          correct = False
          break
    
    return center, correct

#Returns the centers of the buildings in one cluster
def getBuildingsInCluster(polyRadio,Nbuildings,center):
    polygon = RegularPolygon((center[0],center[1]), Nbuildings,radius=polyRadio)
    verts = polygon.get_path().vertices
    trans = polygon.get_patch_transform()
    points = trans.transform(verts)
    points = points[:-1]
  
    return points


##########
###LOGIC
##########

##HOUSES
#Calculate the distance between the circles of the cluster
angle = 2*pi/NHOUSES 
polygonRadio = RADIO/(np.sin(angle/2))

#For each cluster it creates a polygon of NHOUSES  vertices and get the position of that verts to get the position of the circles
for cluster in range(NCLUSTERS):
    
    center, correct = getClusterPosition(polygonRadio)
    
    if (correct): # if there is not errors when cheking
        polygonCenters=np.vstack([polygonCenters,center])
        tempCenters = getBuildingsInCluster(polygonRadio,NHOUSES,center)
        houseCenters=np.vstack([houseCenters,tempCenters])
        

#MEETINGS
#Calculate the distance between the circles of the cluster
angle = 2*pi/NMEETINGS 
polygonRadio = RADIO/(np.sin(angle/2))

#For each cluster it creates a polygon of NMEETINGS  vertices and get the position of that verts to get the position of the circles
for cluster in range(NCLUSTERS):
    
    center, correct = getClusterPosition(polygonRadio)
    
    if (correct): # if there is not errors when cheking
        polygonCenters=np.vstack([polygonCenters,center])
        tempCenters = getBuildingsInCluster(polygonRadio,NMEETINGS,center)
        meetingCenters=np.vstack([meetingCenters,tempCenters])
        
        
##########
###PLOTING
##########

patchesHouses = [] 
patchesMeeting = [] 

for p in houseCenters:
    circle = Circle((p[0], p[1]), radius = RADIO)
    patchesHouses.append(circle)
    
for p in meetingCenters:
    circle = Circle((p[0], p[1]), radius = RADIO)
    patchesMeeting.append(circle)
    
fig, ax =plt.subplots()
plt.title('Map')
ph = PatchCollection(patchesHouses, alpha=0.4, color = 'green') #alpha=transparency
pm = PatchCollection(patchesMeeting, alpha=0.4, color = 'red') #alpha=transparency

ax.add_collection(ph)
ax.add_collection(pm)

plt.axis([0,MAPSIZE,0,MAPSIZE])
plt.draw()

##########
###SAVING
##########
    