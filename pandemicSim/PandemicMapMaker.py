# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 18:20:46 2021

@author: xaju5
"""

#Script to create the map of the pandemicSim

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle
PI = np.pi

FICHNAME = "pandemic-map.npz"

#=============================================================================
#   Funtions
#=============================================================================

#The main function to create the map
def createMap(ncluster=5, nhouses=6, nmeeting=3, mapsize=500, radio=10, offset=0.3, save=True, plot=False, giveReturn=False):
    
    global NCLUSTERS, NHOUSES, NMEETINGS, MAPSIZE, RADIO, OFFSET
    
    NCLUSTERS = ncluster     #Number of total clusters per type
    NHOUSES = nhouses        #Number of houses in each cluster
    NMEETINGS = nmeeting     #Number of meetings in each cluster
    MAPSIZE = mapsize
    RADIO = radio            #size of buildings
    OFFSET = offset          #offset distance between same cluster buildings
    
    houseCenters = np.array([]).reshape(0,2)
    meetingCenters = np.array([]).reshape(0,2)
    polygonCenters = np.array([]).reshape(0,2)
    
    # HOUSES
    houseCenters, polygonCenters = __createClusterOfBuildings(NHOUSES, polygonCenters)
          
    # MEETINGS
    meetingCenters, polygonCenters = __createClusterOfBuildings(NMEETINGS, polygonCenters)
    
    if(save):
        np.savez(FICHNAME,a=houseCenters,b=meetingCenters,c=RADIO,d=MAPSIZE)    
        
    if(plot):
        plotMap(houseCenters, meetingCenters, RADIO, MAPSIZE)
        
    if (giveReturn):
        return houseCenters, meetingCenters, RADIO, MAPSIZE
    else:
        return

#Returns the buildings of a cluster
def __createClusterOfBuildings(nbuildings, polygonCenters):
    buildingPosition = np.array([]).reshape(0,2)
    
    angle = 2*PI/nbuildings 
    polygonRadio = RADIO/(np.sin(angle/2)) + OFFSET * RADIO #distance form the center of the cluster to the position of the buildings
      
    #For each cluster it creates a polygon of "nbuildings" vertices and get the position of that verts to get the position of the buildings
    for cluster in range(NCLUSTERS):
        
        center, correct = __getClusterPosition(polygonRadio, polygonCenters)
        
        if (correct): # if there is not errors when cheking
            polygonCenters = np.vstack([polygonCenters,center])   #store the centers of all clusters
            tempCenters = __getBuildingsInCluster(polygonRadio,nbuildings,center,polygonCenters)
            buildingPosition=np.vstack([buildingPosition,tempCenters])
            
    return buildingPosition, polygonCenters

#Returns the center of a cluster that does not colide with other obstacules
def __getClusterPosition(polygonRadio, polygonCenters):
    
    distance = polygonRadio + 2 * RADIO   #distance from the center to the end of the cluster
    checkingPos = True
    
    #To check infite loop
    correct = True
    protection = 0
    
    while (checkingPos):
        
        center = MAPSIZE * np.random.rand(2)
        
        # Is the whole cluster inside the map?
        if center[0]>distance and center[1]>distance and (center[1]+distance)<MAPSIZE and (center[0]+distance)<MAPSIZE:
            
            # Does it overlap any previous circles?
            for pc in polygonCenters:
                d = np.sqrt((center[0]-pc[0])**2 + (center[1]-pc[1])**2)
                
                if d < (distance * 2): #If they colide stop counting and restart
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

#Returns the position of the buildings in one cluster
def __getBuildingsInCluster(polygonRadio,nbuildings,center, polygonCenters):
    
    polygon = RegularPolygon((center[0],center[1]), nbuildings,radius=polygonRadio)
    verts = polygon.get_path().vertices
    trans = polygon.get_patch_transform()
    points = trans.transform(verts)
    points = points[:-1]
  
    return points

#A function to plot the map
def plotMap(houseCenters=None, meetingCenters= None, radio = None, mapsize = None, loadData=False):
    
    if (loadData):
        with np.load(FICHNAME) as a:
            houseCenters=a['a']
            meetingCenters=a['b']
            radio=a['c']
            mapsize=a['d']
    
    patchesHouses = [] 
    patchesMeeting = [] 
    
    for p in houseCenters:
        circle = Circle((p[0], p[1]), radius = radio)
        patchesHouses.append(circle)
        
    for p in meetingCenters:
        circle = Circle((p[0], p[1]), radius = radio)
        patchesMeeting.append(circle)
        
    fig, ax =plt.subplots()
    plt.title('Map')
    ph = PatchCollection(patchesHouses, alpha=0.4, color = 'green') #alpha=transparency
    pm = PatchCollection(patchesMeeting, alpha=0.4, color = 'red')  #alpha=transparency
    
    ax.add_collection(ph)
    ax.add_collection(pm)
    
    plt.axis([0,mapsize,0,mapsize])
    plt.draw()
    
    return
