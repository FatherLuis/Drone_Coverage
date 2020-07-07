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

from Field import Field




# ns: Number of possible charging station positions
# rad: coverage radius
# solMax: Maximum number of solutions
# start: Starting point for tour (point of origin) 
# nx: Number of cells on the x-axis
# ny: Number of cells on the y-axis
def linear_program(binMatrix, xmin,xmax,ymin,ymax,nx, ny , ns ,step, rad, droneRange, solMax, start):

    #plt.pcolor(binMatrix)
    #plt.show()

    

    # converts numerical values in an array to boolean/logicals'''
    logicalFn = lambda y: np.asarray(list(map(lambda x: bool(x), y))) 
    
    

    rad2 = rad**2

    #To the edges
    power = 0.5 #Penalty for large distances
    solMx = np.array([])


    inclVec = binMatrix.flatten().astype(bool)

    xVec = np.repeat( np.arange(xmin,xmax,step), ny )[inclVec]
    yVec = np.tile(np.arange(ymin,ymax,step), nx )[inclVec]
   

    np_tot = np.sum(inclVec) # Number of points in region




    # Locate charging stations
    locs0 = r.sample(range(np_tot),ns) #k Random locations for charging station
    locs = np.array([xVec[locs0], yVec[locs0]])

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


    fmin = 1E20 # Set large value as initial solution 

    
    #Minimize cx
    # subject to Ax >= b
    # A negative is placed in the parameter because ilp only does Ax <= B
    
    for ii in range(solMax):
        fmin0 = 1*fmin
        status, solNew = ilp(c, 
                             -1*iMx, 
                             -1*b, 
                             matrix(1., (0,ns) ),
                             matrix(1., (0,1) ), 
                             I = set(), 
                             B = set(range(ns)))
        
        if not(status == 'optimal') or round(fmin) > round(fmin0):
            break
        else:
            
            fmin = dotu(c, solNew)
            
            # ADDITIONAL CONTRAINS
            iMx = matrix([iMx, -1*solNew.ctrans()]) #[iMx ; -1*solNew'] #Add to LP matrix
            # ADDED NEW BOUND 
            b = matrix([b, -1*fmin+1])    # Constraint constant

            if ii == 0:
                solMx = solNew.ctrans()
            else:
                solMx = np.vstack((solMx, solNew.ctrans())) # Add to matrix of solutions

    # lP relaxation is primal infeasible       
    #print("****************************************************************************")     
    #print("Status:", status)
    #print("solMx:", solMx)
    #print("****************************************************************************")


    # CHECK IF THE NUMPY ARRAY IS NOT EMPRY
    if solMx.size == 0:

        raise('Solution Not Found')


    #Minimize points' distance to charging stations

    distStat = np.zeros(solMx.shape[0])
    startConjT = np.array(np.matrix(start).H) #start.conj().transpose()#conjugate transpose of start
    for ii in range(solMx.shape[0]): 
        
        minDistVec = 1E50 * np.ones(len(xVec))
        
        csLocs = locs[:, logicalFn(solMx[ii,:])] #select charging stations for current solution
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
        distStat[ii] = max((len(minDistVec) - nVec) / ( droneRange - minDistVec));
        #distStat[ii] = min(distStat[ii],distStat[ii - (ii > 0)])


    bestVal,bestIx = min(distStat), np.argmin(distStat) #Choose best solution
    #iBest = bestIx[0];

    #select charging station locs. for best solution
    csLocs = locs[:, np.asarray(list(map(lambda x: bool(x), solMx[bestIx,:] ))) ] 
    csLocs = np.append(startConjT,csLocs, axis = 1) #add starting point

    # print(csLocs)
    return csLocs,bestVal


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
    vertices = [voronoi_lst[0][1]]
    
    # CREATE AN ARRAY OF SIZE 1 X nCS FILLED WITH EMPTY ARRAYS
    # WE'LL BE APPENDING THE ENTRY/EXIT POINTS FOR EACH VORONOI CELL
    start_end_lst = [ []  for i in range(nCS)]
    
    
    # FIND THE INTERSECTION BETWEEN THE FIRST VORONOI 
    # AND LAST VORONOI IN THE TOUR
    set1 = set(voronoi_lst[coor[-1]][0])
    set2 = set(voronoi_lst[coor[-2]][0])
    previous = set1.intersection(set2)  
    
    
    for i in range(nTour-1):
        
        # GET THE INTERSECTED POINTS BETWEEN VORONOI CELLS
        set1 = set(voronoi_lst[coor[i]][0])
        set2 = set(voronoi_lst[coor[i+1]][0])
        interPts = set1.intersection(set2)
        
        
        # INDICATE IF YOU HAVE TRAVELED TO A VERTEX
        flag  = 0
        # ITERATE THROUGH THE PREVIOUS INTERSECTED VERTICES
        # SO THAT YOU DONT USE THEM
        for prev in previous:
            
            # INDICATE IF A VERTEX HAS BEEN FOUND
            if flag == 0:
            
                # ITERATE THROUGH THE INTERSECTED POINTS
                for p in interPts:
        
                    # DONT USE VERTICES THAT IS SHARED WITH ANOTHER VORONOI
                    if not( np.array_equal(prev, p)):
                        
                        # MAKE SURE YOU DID NOT ALREADY ADD THESE POINTS INTO THE EXIT/ENTRY ARRAY
                        # OR THE VERTICES ARRAY
                        if not(p in start_end_lst[coor[i]]) and not(p in start_end_lst[coor[i+1]]):
                            
                            # STORE THE INTERSECTED VERTEX INTO THE ENTRY'EXIT ARRAY
                            start_end_lst[coor[i]].append(p)
                            start_end_lst[coor[i+1]].append(p)
                            
                            # ADD THE INTERSECTED VERTEX INTO THE VERTICES LIST
                            vertices.append(p)
                            vertices.append(voronoi_lst[coor[i+1]][1])
                            
                            # STORE THE INTERSECTED POINTS FOR NEXT VORONOI INTERSECTIOSN
                            previous = interPts
                            
                            # INDICATE THAT YOU HAVE FOUND A VERTEX
                            flag = 1
                            break 
            
            
            
    
    print('------------ locs --------------')
    locsTmp = np.array( [ [x[0] for x in csLocs ] , [y[1] for y in csLocs ]  ] )
    print(locsTmp)
    print('')
    
    
    return start_end_lst, coor, vertices
    




if __name__ == '__main__':

    # IF THIS FILE IS RUN, THE FOLLOWING CODE WILL BE READ


    ns = 50
    rad = 60
    solMax = 5
    start = np.array([20, 20])

    ng = np.array([200,200]) #number of cells on each side of grid
    ng_tot = ng[0] * ng[1]
    ns = 50 # Number of possible charging station positions
    rad = 60 #coverage radius
    solMax = 5 #Maximum number of solutions
    start = np.array([20, 20]) #Starting point for tour (point of origin)

    #Determine region to be covered 
    ##NEEDS TO BE POLYGONAL
    gMeans = np.array([[50, 50, 150, 150], [50, 150, 50, 150]]) #Means of Gaussian used to determine regions
    gStd = np.array([[30, 30, 30, 30], [30, 30, 30, 30]]) #Std's of Guassions used to determine region
    theta_g = 0.4 #Threshold to decide inclusion in region

    #x and y coordinates of grid
    xVecGrid = np.floor(np.arange(ng_tot)/ ng[0]) + 1 #Integer values for x and y


    yVecGrid = (np.arange(ng_tot) % ng[0]) + 1

    inclVec = 0 * xVecGrid

    #Find points in region
    for ii in range(gMeans.shape[1]):
        inclVec = inclVec + np.exp(-(xVecGrid - gMeans[0,ii])**2/(2*gStd[0,ii]**2)-(yVecGrid - gMeans[1,ii])**2/(2*gStd[1,ii]**2))
        
    inclVec = inclVec > theta_g
    inclMx = np.reshape(inclVec, ng) # Matrix for inclusion in region (used in plotting)

    plt.pcolor(inclMx)
    plt.show()

    CS,bestVal = linear_program(inclMx,0,200,0,200,200,200,ns,1,rad,8, solMax,start)

    print(CS)
    print(bestVal)
    

