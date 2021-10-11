# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 22:44:03 2021

@author: xaju5
"""
import numpy as np
import matplotlib.pyplot as plt
import PandemicMapMaker as pmm
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle

#==========================
#Initial parameters
#==========================
#Pandemic parameters
PINFECTION=0.3  #Probability to infect someone
PDEAD=0.01      #Probability to die when infected
SPREAD=20        #Distance needed for infection
THEAL=50        #Time needed for healing

#Map parameters
LoadData = False
FICHNAME = "pandemic-map.npz"
if (LoadData):
    with np.load(FICHNAME) as a:
        houseCenters=a['a']
        meetingCenters=a['b']
        RADIO=a['c']
        MAPSIZE=a['d']
else:
    houseCenters, meetingCenters, RADIO, MAPSIZE = pmm.createMap(save=True, plot=False, giveReturn=True)
    
TMAX=300        #Max iterations of the simulation
NUMINDV=100     #Number of individuals on the map
SPEED=10        #Speed of movement of individuals
ITEPLOT=True   #Boolean to plot the iterative movement

#Point to send the diferent indiviuals when their status changes.
HEALTHYPOINT = -20
INFECTPOINT = -30
IMMUNEPOINT = -40

#==========================
#Initialize variables
#==========================
#variables of individuals
status = np.zeros(NUMINDV)          #0=normal 1=infected 2=immune 3=dead
timeInfected = np.zeros(NUMINDV)    

#position divided in types for make the plot easy
positionHealhy = MAPSIZE * np.random.rand(NUMINDV,2)
positionInfected = np.ones((NUMINDV,2)) * INFECTPOINT
positionImmune = np.ones((NUMINDV,2)) * IMMUNEPOINT 

destination = MAPSIZE * np.random.rand(NUMINDV,2)

#set first infected
indicator= np.random.randint(0,NUMINDV)
status[indicator] = 1
positionInfected[indicator] = positionHealhy[indicator]
positionHealhy[indicator] = HEALTHYPOINT 
#==========================
#Definitions of functions
#==========================    
def stepForward(position,num):
    """Individuals moves one step foward""" 
    if status[i] == num:
        angle = np.arctan2((destination[i,1]-position[i,1]),(destination[i,0]-position[i,0]))
        nextStep = np.array([SPEED*np.cos(angle), SPEED*np.sin(angle)])
        position[i] += nextStep
        
        #Check if the indiviual has arrived to the destination. If it does, make a new destination
        distToDest = np.sqrt((position[i,0]-destination[i,0])**2 + (position[i,1] - destination[i,1])**2)
        if distToDest <= SPEED:
            destination[i] = MAPSIZE * np.random.rand(2)
        
def infect():
    """If close enough, they can infect""" 
    if status[i] == 1: 
        timeInfected[i] += 1
        
        for j in range(NUMINDV):
            if i != j and status[j] == 0:          
                #Calculate the distance with the other ones
                sideA = positionInfected[i,0] - positionHealhy [j,0]
                sideB = positionInfected[i,1] - positionHealhy [j,1]
                distance = np.sqrt(sideA**2 + sideB**2)
                
                if distance <= SPREAD:
                    if np.random.rand() <= PINFECTION:
                        status[j] = 1
                        positionInfected[j] = positionHealhy[j]
                        positionHealhy[j] = HEALTHYPOINT

def heal():
    """After a period of time they heal"""
    if status[i] == 1 and timeInfected[i] > THEAL: 
        status[i] = 2
        positionImmune[i] = positionInfected[i]
        positionInfected[i] = INFECTPOINT

                           
def calculateDeath():
    """calculate if a individual should die """
    if status[i] == 1:
        if np.random.rand() <= PDEAD:
            status[i] = 3
            positionHealhy[i] = HEALTHYPOINT 
            positionInfected[i] = INFECTPOINT
            positionImmune[i] = IMMUNEPOINT 
         
 
#==========================
#Execution
#==========================
#Iterative plot
if ITEPLOT:
    fig, ax = plt.subplots(1)
    
    patchesHouses = [] 
    patchesMeeting = [] 
    
    for p in houseCenters:
        circle = Circle((p[0], p[1]), radius = RADIO)
        patchesHouses.append(circle)
        
    for p in meetingCenters:
        circle = Circle((p[0], p[1]), radius = RADIO)
        patchesMeeting.append(circle)
    
    ph = PatchCollection(patchesHouses, alpha=0.4, color = 'green') #alpha=transparency
    pm = PatchCollection(patchesMeeting, alpha=0.4, color = 'red') #alpha=transparency
    
    ax.add_collection(ph)
    ax.add_collection(pm)
    
    
    xh, yh = [],[]
    xinf, yinf = [],[]
    xim, yim = [],[]
    sch = ax.scatter(xh,yh,s=10,c='red') #x&y=data position, s=size points, c=color
    scinf = ax.scatter(xinf, yinf,s=10,c='blue') #x&y=data position, s=size points, c=color
    scim = ax.scatter(xim, yim,s=10,c='green') #x&y=data position, s=size points, c=color
    plt.axis([0,MAPSIZE,0,MAPSIZE])
    plt.draw()

#main
for t in range(TMAX): 
    for i in range(NUMINDV):
        stepForward(positionHealhy,0)
        stepForward(positionInfected,1)
        stepForward(positionImmune,2)
        infect()
        heal()
        calculateDeath()
    
    #Represent movement of individuals  
    if ITEPLOT:
        sch.set_offsets(np.c_[positionHealhy[:,0],positionHealhy[:,1]])
        scinf.set_offsets(np.c_[positionInfected[:,0],positionInfected[:,1]])
        scim.set_offsets(np.c_[positionImmune[:,0],positionImmune[:,1]])
        fig.canvas.draw_idle()
        plt.pause(0.2)
    
    #stop loop if there is no more infected
    if np.count_nonzero(status == 1) == 0:
        break

#Print data    
print("Healthy: " + str(np.count_nonzero(status == 0)))
print("Infected: " + str(np.count_nonzero(status == 1)))
print("Immune: " + str(np.count_nonzero(status == 2)))
print("Death: " + str(np.count_nonzero(status == 3)))
print("Time: " + str(t))

