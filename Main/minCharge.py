# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 20:46:52 2020

@author: SK
"""

from cvxopt import matrix 

from cvxopt.glpk import ilp
from cvxopt.blas import dotu
import numpy as np
import matplotlib.pyplot as plt
import random as r
import tourfn2 as tf

import Field as field



# ns: Number of possible charging station positions
# rad: coverage radius

# start: Starting point for tour (point of origin) 
# nx: Number of cells on the x-axis
# ny: Number of cells on the y-axis
def linear_program(maskVec, xVec, yVec, ns, rad, droneRange, start, customCandidate_coor):

    '''
    Parameters:
        maskVec: logical array that state what xValue is in the field
        xVec: a x-valued mesh vector
        yVec: a y-valued mesh vector
        ns: Number of generated CS candidate locations
        rad: Farthest distance drone can travel and return to charging station
        droneRange: Half the max distance drone can travel before recharge
        start: (x,y) coordinate of the first CS
        customCandidate_coor: a x,y array of charging station location
    '''
    
    

    # converts numerical values in an array to boolean/logicals'''
    logicalFn = lambda y: np.asarray(list(map(lambda x: bool(x), y))) 
    
    

    

    #To the edges
    power = 0.5 #Penalty for large distances
    solMx = np.array([])


    #inclVec = binMatrix.flatten().astype(bool)
    #xVec = np.repeat( np.arange(xmin,xmax,step), ny )[inclVec]
    #yVec = np.tile(np.arange(ymin,ymax,step), nx )[inclVec]
    
    
    xVec = xVec[maskVec]
    yVec = yVec[maskVec]
    
    np_tot = np.sum(maskVec) # Number of points in region
   
    if len(customCandidate_coor) > 0:
        
        locs = customCandidate_coor
        genCandidate = locs[:]

    else:
        
        
        # Locate charging stations
        locs0 = r.sample(range(np_tot),ns) #k Random locations for charging station
        locs = np.array([xVec[locs0], yVec[locs0]])
        genCandidate = locs[:]
        
    



    flag = 0
    solMx = [ [] , [] ]
    while not(flag == -1):
       
        # flag = -1 : STOP THE LOOP
        # flag = 0  : FIRST LOOP
        # flag = 1  : A SOLUTION WAS PREVIOUSLY FOUND
        
        rad2 = rad**2
    
        #Define incidence matrix: coverage area for drone is circular with radius rad
        d2Mx = np.zeros((np_tot,ns))
        
        # Distance matrix and locations not covered by start
        # DISTANCE MATRIX THAT EACH SITE MAY REACH
        for ii in range(ns):
            d2Mx[:, ii] =  (locs[0,ii]- xVec)**2 + (locs[1,ii]- yVec)**2 
            
        # SELECT LOCATIONS THAT ARE LESS THAN THE MAX TRAVEL DISTANCE
        iMx = d2Mx < rad2 # LOGICAL Coverage matrix
        # LOCATE THE AREA WHERE THE FIRST CHARGING STATION CANNOT REACHES
        iVec = ((xVec - start[0])**2 + (yVec-start[1])**2) > rad2; # points not covered by start
        # SELECT THE AREAS THAT ARE NOT COVERED BY THE FIRST CHARGING STATION ( GIVES A BOOLEAN MATRIX)
        iMx = iMx[logicalFn(iVec), :] #Logical coverage matrix for remaining points
        # SELECT THE AREAS THAT ARE NOT COVERED BY THE FIRST CHARGING STATION ( GIVES A DISTANCE MATRIX)
        d2Mx = d2Mx[logicalFn(iVec), :] #Distance matrix for remaining points
        np_eff = iMx.shape[0]#size(iMx,1) #Number of points not covered by start
    
        #Set up linear program which finds the minimum number of charging stations required
        c = matrix(np.ones((ns,1), dtype = float)) # objective function
        b = matrix(np.ones((np_eff,1), dtype = float)) #constraint vector
        iMx = matrix(np.array(iMx, dtype = float)) #convert to matrix as reqd by cvxopt
    
    

        #Minimize cx
        # subject to Ax >= b
        # A negative is placed in the parameter because ilp only does Ax <= B
        
        status, solNew = ilp(c, 
                             -1*iMx, 
                             -1*b, 
                             matrix(1., (0,ns) ),
                             matrix(1., (0,1) ), 
                             I = set(), 
                             B = set(range(ns)))
        
        if not(status == 'optimal'):
             
            if flag == 0:
                raise('Charging Station Locations Not Found')
                
            if flag == 1:
                
                flag = -1 
        
        

        if flag == 0:   
            
            solMx[0] = solNew.ctrans()  
            rad = rad - 0.1
            
            flag = 1
            
        elif flag == 1:
            
            newSoln = solNew.ctrans()  
            
            if sum(solMx[0]) < sum(newSoln):
                
                flag = -1
                solMx[1] = newSoln
                
            else:
                solMx[0] = newSoln
                rad = rad - 0.1
                
            
 
    
    
    distStat = np.zeros(2)
    startConjT = np.array(np.matrix(start).H) #start.conj().transpose()#conjugate transpose of start
    
    CS_Locs_lst = []
    bestVal_lst = []
    

    for ii in range(2): 
        
        if len(solMx[ii]) == 0 :
            break
        
        minDistVec = 1E50 * np.ones(len(xVec))
        
        
        csLocs = locs[:, logicalFn(solMx[ii])] #select charging stations for current solution
        csLocs = np.append(startConjT, csLocs, axis = 1) #add starting point
        

        # Construct minDistMx and regMx
        for jj in range(csLocs.shape[1]): 
            
            #If power is larger, farther points are counted more
            tmpDistVec = ((xVec-csLocs[0,jj])**2 + (yVec-csLocs[1,jj])**2)**power
            # minDistVec gives value of r
            minDistVec = np.minimum(minDistVec,tmpDistVec)
            
            
        # Compute the best-case distance for this example
        nVec = np.arange(1,len(minDistVec)+1); # Value of n for each r
        minDistVec = np.sort(minDistVec)
        
        #Save best value so far
        distStat[ii] = max((len(minDistVec) - nVec) / ( droneRange - minDistVec))
        distStat[ii] = distStat[ii] * droneRange / len(minDistVec)


        CS_Locs_lst.append(csLocs)
        bestVal_lst.append(distStat[ii])




    return CS_Locs_lst, bestVal_lst, genCandidate





def tour(voronoi_lst):
    
    
    # GET THE CS LOCATIONS FROM THE VORONOI LIST
    csLocs = [x[1] for x in voronoi_lst]

    # GET THE NUMBER OF CS
    nCS = len(csLocs)
    
    # CREATE A ZERO MATRIX OF SIZE nCS x nCS
    mtx = np.zeros( (nCS,nCS) )

    # CREATE A ADJ MATRIX BASED ON THE RELATION BETWEEN VORONOI CELLS
    for i in range(nCS):

        vor_set = set(voronoi_lst[i][0])

        for j in range(i,nCS):
            
            if not( i == j ):

                vor_set2 = set(voronoi_lst[j][0])
    
                has_intersection = 1 if len(vor_set.intersection(vor_set2)) > 0 else 0
    
                mtx[i][j] = has_intersection
                mtx[j][i] = has_intersection




    ################################
    # 'Tour' requires:
    # ADJ MATRIX  
    ################################

    tour = tf.tourFn(mtx)


    if tour is  None:
        raise('Empty Tour')
      
    # coor : CONTAINS THE INDECES OF THE TOUR BETWEEN CS
    coor = tour
    
    
    
    ##################################################################
    # CONSTRUCT AN ARRAY OF POINTS, WHERE YOU GO FROM ONE CS TO A VERTEX TO A CS
    # CONSTRUCT A LIST OF ENTRY & EXIT VERTICES FOR EACH VORONOI CELL
    ##################################################################
    
    # GET THE NUMBER OF CS WE'LL BE TRAVELING TO
    nTour =len(coor)
    
    # THE FIRST POINT IS WERE WE START
    vertices = []
    
    # CREATE AN ARRAY OF SIZE 1 X nCS FILLED WITH EMPTY ARRAYS
    # WE'LL BE APPENDING THE ENTRY/EXIT POINTS FOR EACH VORONOI CELL
    start_end_lst = [ []  for i in range(nCS)]
    
   
    
    
    
    
    vertices.append(voronoi_lst[coor[0]][1]) 
    
    for i in range(nTour-1):

        # GET THE INTERSECTED POINTS BETWEEN VORONOI CELLS
        set1 = set(voronoi_lst[coor[i]][0])
        set2 = set(voronoi_lst[coor[i+1]][0])
        p1,p2 = set1.intersection(set2)      
    
    
        isUsedP1 = p1 in start_end_lst[coor[i]] or p1 in start_end_lst[coor[i+1]] 
        isUsedP2 = p2 in start_end_lst[coor[i]] or p2 in start_end_lst[coor[i+1]]
    
        chosenP = None
        
        # IF NEITHER HAVE BEEN USED
        if not(isUsedP1) and not(isUsedP2):
            
            
            if p1[0] > p2[0]:
                chosenP = p1
            else:
                chosenP = p2
                
        else:
            
            chosenP =  p1 if not(isUsedP1) else p2
        
    

        # STORE THE INTERSECTED VERTEX INTO THE ENTRY'EXIT ARRAY
        start_end_lst[coor[i]].append(chosenP)
        start_end_lst[coor[i+1]].append(chosenP)
        
        # ADD THE INTERSECTED VERTEX INTO THE VERTICES LIST
        vertices.append(chosenP)
        vertices.append(voronoi_lst[coor[i+1]][1]) 

  
    
    
    


    
    print('------------ locs --------------')
    locsTmp = np.array( [ [x[0] for x in csLocs ] , [y[1] for y in csLocs ]  ] )
    print(locsTmp)
    print('')
    
    
    return start_end_lst, coor, vertices
    




# if __name__ == '__main__':
    
#     OUTDATED
    
#     # IF THIS FILE IS RUN, THE FOLLOWING CODE WILL BE READ


#     ns = 50
#     rad = 60
#     solMax = 5
#     start = np.array([20, 20])

#     ng = np.array([200,200]) #number of cells on each side of grid
#     ng_tot = ng[0] * ng[1]
#     ns = 50 # Number of possible charging station positions
#     rad = 60 #coverage radius
#     solMax = 5 #Maximum number of solutions
#     start = np.array([20, 20]) #Starting point for tour (point of origin)

#     #Determine region to be covered 
#     ##NEEDS TO BE POLYGONAL
#     gMeans = np.array([[50, 50, 150, 150], [50, 150, 50, 150]]) #Means of Gaussian used to determine regions
#     gStd = np.array([[30, 30, 30, 30], [30, 30, 30, 30]]) #Std's of Guassions used to determine region
#     theta_g = 0.4 #Threshold to decide inclusion in region

#     #x and y coordinates of grid
#     xVecGrid = np.floor(np.arange(ng_tot)/ ng[0]) + 1 #Integer values for x and y


#     yVecGrid = (np.arange(ng_tot) % ng[0]) + 1

#     inclVec = 0 * xVecGrid

#     #Find points in region
#     for ii in range(gMeans.shape[1]):
#         inclVec = inclVec + np.exp(-(xVecGrid - gMeans[0,ii])**2/(2*gStd[0,ii]**2)-(yVecGrid - gMeans[1,ii])**2/(2*gStd[1,ii]**2))
        
#     inclVec = inclVec > theta_g
#     inclMx = np.reshape(inclVec, ng) # Matrix for inclusion in region (used in plotting)

#     plt.pcolor(inclMx)
#     plt.show()

#     CS,bestVal = linear_program(inclMx,0,200,0,200,200,200,ns,1,rad,8, solMax,start)

#     print(CS)
#     print(bestVal)
    

