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
PINFECTION=0.005  #Probability to infect someone
PDEAD=0.001      #Probability to die when infected
SPREAD=4        #Distance needed for infection
THEAL=50        #Time needed for healing

#Map parameters
loadData = False
FICHNAME = "pandemic-map.npz"
if (loadData):
    with np.load(FICHNAME) as a:
        houseCenters=a['a']
        meetingCenters=a['b']
        RADIO=a['c']
        MAPSIZE=a['d']
else:
    NCLUSTERS = 10
    NHOUSES = 9
    NMEETINGS = 4
    houseCenters, meetingCenters, RADIO, MAPSIZE = pmm.createMap(NCLUSTERS, NHOUSES, NMEETINGS, giveReturn=True)
    
TMAX=10000                                  #Max iterations of the simulation
TSTATIC=50                                  #Time expended in Meetings
TTRANSIT=95                                 #Time expended in Transit
FAMILYMEMBER = 5                            #Relation of how many member live in each house
NUMINDV= len(houseCenters) * FAMILYMEMBER   #Number of individuals on the map
SPEED=5                                     #Speed of movement of individuals
ITEPLOT=True                                #Boolean to plot the iterative movement

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
positionHome = np.array([]).reshape(0,2)
for hc in houseCenters:
    for f in range(FAMILYMEMBER):
        positionHome = np.vstack([positionHome,hc])

positionMeeting = np.array([]).reshape(0,2)
for mc in meetingCenters:
    for f in range(NUMINDV//len(meetingCenters)):
        positionMeeting = np.vstack([positionMeeting,mc])
while(len(positionMeeting) < len(positionHome)):
    indicator = np.random.randint(0,len(meetingCenters))
    positionMeeting = np.vstack([positionMeeting,meetingCenters[indicator]])
np.random.shuffle(positionMeeting)    
    

positionHealthy = np.copy(positionHome) 
positionInfected = np.ones((NUMINDV,2)) * INFECTPOINT
positionImmune = np.ones((NUMINDV,2)) * IMMUNEPOINT 
#destination = np.copy(positionMeeting) 

#set first infected
indicator= np.random.randint(0,NUMINDV)
status[indicator] = 1
positionInfected[indicator] = positionHealthy[indicator]
positionHealthy[indicator] = HEALTHYPOINT 
#==========================
#Definitions of functions
#==========================  
#High level functions
def transitOfIndividuals():
    """Moves individuals through the map"""
    for tt in range(TTRANSIT):      #Transit time
        for indID in range(NUMINDV):
            stepForward(indID,positionHealthy,0)
            stepForward(indID,positionInfected,1)
            stepForward(indID,positionImmune,2)
            infect(indID)
                
        iterativeMovement(fig, sch, scinf, scim)
        
def staticIndividuals():
    """Calculate the behavior of individuals """
    for th in range(TSTATIC):         
        for indID in range(NUMINDV):
            staticInfection(indID)  
        iterativeMovement(fig, sch, scinf, scim)
     
def changeIndividualHealth():
    """If necesary change the health status of the individuals"""  
    for indID in range(NUMINDV):
        heal(indID)
        calculateDeath(indID)
        
#Low level functions        
def stepForward(indID,position,num):
    """Individuals moves one step foward""" 
    if status[indID] == num:
        
        #Check if the indiviual has arrived to the destination. If it does, dont do nothing
        distToDest = np.sqrt((position[indID,0]-destination[indID,0])**2 + (position[indID,1] - destination[indID,1])**2)
        if distToDest >= SPEED:                  
            angle = np.arctan2((destination[indID,1]-position[indID,1]),(destination[indID,0]-position[indID,0]))
            nextStep = np.array([SPEED*np.cos(angle), SPEED*np.sin(angle)])
            position[indID] += nextStep

                    
def infect(indID):
    """If close enough when traveling, they can infect""" 
    if status[indID] == 1: 
        for j in range(NUMINDV):
            if indID != j and status[j] == 0:          
                #Calculate the distance with the other ones
                sideA = positionInfected[indID,0] - positionHealthy [j,0]
                sideB = positionInfected[indID,1] - positionHealthy [j,1]
                distance = np.sqrt(sideA**2 + sideB**2)
                
                if distance <= SPREAD:
                    if np.random.rand() <= PINFECTION:
                        status[j] = 1
                        positionInfected[j] = positionHealthy[j]
                        positionHealthy[j] = HEALTHYPOINT

def staticInfection(indID):
    """If they are inside the same building, they can be infected"""
    if status[indID] == 1:
        for j in range(NUMINDV):
            tempboolean = destination[indID] == destination[j]
            if indID != j and status[j] == 0 and tempboolean.all(): 
                if np.random.rand() <= PINFECTION:
                        status[j] = 1
                        positionInfected[j] = positionHealthy[j]
                        positionHealthy[j] = HEALTHYPOINT


def heal(indID):
    """After a period of time they heal"""
    if status[indID] == 1 and timeInfected[indID] > THEAL: 
        status[indID] = 2
        positionImmune[indID] = positionInfected[indID]
        positionInfected[indID] = INFECTPOINT
    else:
        timeInfected[indID] += 1

                           
def calculateDeath(indID):
    """calculate if a individual should die """
    if status[indID] == 1:
        if np.random.rand() <= PDEAD:
            status[indID] = 3
            positionHealthy[indID] = HEALTHYPOINT 
            positionInfected[indID] = INFECTPOINT
            positionImmune[indID] = IMMUNEPOINT 

#Iterative Plot funtions
def iterativeMovement(fig, sch, scinf, scim):
    """If ITEPLOT enable, move the individuals of the plot"""
    if ITEPLOT:
        sch.set_offsets(np.c_[positionHealthy[:,0],positionHealthy[:,1]])
        scinf.set_offsets(np.c_[positionInfected[:,0],positionInfected[:,1]])
        scim.set_offsets(np.c_[positionImmune[:,0],positionImmune[:,1]])
        fig.canvas.draw_idle()
        plt.pause(0.1)

def setUpIterativeMovement():
    """If ITEPLOT enable, initial configuration of the movements of the individuals"""
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
        
        return fig, sch, scinf, scim
    else:
        return 0,0,0,0
  
       
#==========================
#Execution
#==========================
fig, sch, scinf, scim = setUpIterativeMovement()

#MAIN
for t in range(TMAX): 
    
    if t%2 == 0:
        destination = np.copy(positionMeeting) 
        print("In Home")
    else:
        destination = np.copy(positionHome) 
        print("In Meeting")
        
    staticIndividuals()
    
    #stop loop if there is no more infected
    if np.count_nonzero(status == 1) == 0:
        break
        
    print("Traveling")
    transitOfIndividuals()
    
    changeIndividualHealth()
    
    #stop loop if there is no more infected
    if np.count_nonzero(status == 1) == 0:
        break

#Print data    
print("Healthy: " + str(np.count_nonzero(status == 0)))
print("Infected: " + str(np.count_nonzero(status == 1)))
print("Immune: " + str(np.count_nonzero(status == 2)))
print("Death: " + str(np.count_nonzero(status == 3)))
print("Time: " + str((t+1)/2) + " days")

