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
import tourFn as tf

from Field import Field





# Note: Changed code from Script to Method
# (4/23/2020): Changed minCharge from Version 2 to Version 4
# (4/23/2020): Changed TourFn from Version 2 to Version 4

# print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")

# ns: Number of possible charging station positions
# rad: coverage radius
# solMax: Maximum number of solutions
# start: Starting point for tour (point of origin) 
# nx: Number of cells on the x-axis
# ny: Number of cells on the y-axis
def linear_program(binMatrix, xmin,xmax,ymin,ymax,nx, ny , ns ,step, rad ,solMax, start):

    #plt.pcolor(binMatrix)
    #plt.show()


    rad2 = rad**2

    #To the edges
    power = 2 #Penalty for large distances
    solMx = np.array([])

    inclVec = binMatrix.flatten().astype(bool)


    xVec = np.repeat( np.arange(xmin,xmax,step), ny )[inclVec]
    yVec = np.tile(np.arange(ymin,ymax,step), nx )[inclVec]
   

    np_tot = np.sum(inclVec) # Number of points in region





    ######################################
    # CODE AFTER HERE REFLECTS SHAUNNA WORK
    ######################################

    # Locate charging stations
    locs0 = r.sample(range(0, np_tot),ns) #k Random locations for charging station
    locs = np.array([xVec[locs0], yVec[locs0]])

    #Define incidence matrix: coverage area for drone is circular with radius rad
    d2Mx = np.zeros((np_tot,ns))
    # Distance matrix and locations not covered by start
    for ii in range(ns):
        d2Mx[:, ii] =  (locs[0,ii]- xVec)**2 + (locs[1,ii]- yVec)**2 
        
    iMx = d2Mx < rad2# Coverage matrix
    iVec = ((xVec - start[0])**2 + (yVec-start[1])**2) > rad2; # points covered by start
    iMx = iMx[tf.logicalFn(iVec), :] #Logical coverage matrix for remaining points
    d2Mx = d2Mx[tf.logicalFn(iVec), :] #Distance matrix for remaining points
    np_eff = iMx.shape[0]#size(iMx,1) #Number of points not covered by start

    #Set up linear program which finds the minimum number of charging stations required
    c = matrix(np.ones((ns,1), dtype = float)) # objective function
    b = matrix(np.ones((np_eff,1), dtype = float)) #constraint vector
    iMx = matrix(np.array(iMx, dtype = float)) #convert to matrix as reqd by cvxopt


    fmin = 1E20 # Set large value as initial solution 

    for ii in range(solMax):
        fmin0 = 1*fmin
        status, solNew = ilp(c, -1*iMx, -1*b, matrix(1., (0,len(c))),matrix(1., (0,1)), I = set(), B = set(range(len(c))))
        
        if status == 'optimal':
            fmin = dotu(c, solNew)
        else:
            print("Solution not found!\n")
            break
        
        print("****************************************************************************")
        print("solNew:", solNew.trans())
        print("fmin:", fmin)
        
        print("****************************************************************************")        
        print("STATUS:", status,)
        print("****************************************************************************")
        
        print("\n///////////////////////////////////////////////////////////////////////////", "\n")  


        if round(fmin) > round(fmin0):
            break
        else:
            iMx = matrix([iMx, -1*solNew.ctrans()]) #[iMx ; -1*solNew'] #Add to LP matrix
            b = matrix([b, -1*fmin+1])    # Constraint constant
            solMx = np.append(solMx, solNew.ctrans()) # Add to matrix of solutions
            rows = int(len(solMx) / len(solNew))
            solMx = solMx.reshape(rows, ns)
            
    print("****************************************************************************")        
    print("solMx:", solMx)
    print("****************************************************************************")


    if solMx.ndim > 1:
        ncs = sum(solMx[0, range(ns)])#sum(solMx(1,1:ns))

        ['Minimum number of charging stations: ', str(ncs)]
        if ncs == 0:
            print('No solutions') #error. RAISE EXCEPTION HERE??
        

        #Minimize points' distance to charging stations

        distStat = np.zeros(solMx.shape[0])
        for ii in range(solMx.shape[0]): 
            minDistVec = 1E50*np.ones(len(xVec))
            csLocs = locs[:, tf.logicalFn(solMx[ii,:])] #select charging stations for current solution
            startConjT = np.array(np.matrix(start).H) #start.conj().transpose()#conjugate transpose of start
            csLocs = np.append(startConjT,csLocs, axis = 1) #add starting point
            for jj in range(csLocs.shape[1]): # Construct minDistMx and regMx
                #If power is larger, farther points are counted more
                tmpDistVec = ((xVec-csLocs[0,jj])**2 + (yVec-csLocs[1,jj])**2)**power
                minDistVec = np.minimum(minDistVec,tmpDistVec)
            #Save best value so far
            distStat[ii] = sum(minDistVec)
            distStat[ii] = min(distStat[ii],distStat[ii - (ii > 0)])
        

        #plt.figure(3)
        #plt.plot(range(len(distStat)),distStat,'*')
        #plt.title('Distance statistic improvement for trial solutions')
        #plt.xlabel('Solution number')
        #plt.ylabel('Distance statistic')
        
        
        bestVal,bestIx = min(distStat), np.argmin(distStat) #Choose best solution
        #iBest = bestIx[0];

        

        csLocs = locs[:, np.asarray(list(map(lambda x: bool(x), solMx[bestIx,:] ))) ] #select charging station locs. for best solution
        


        startConjT = np.array(np.matrix(start).H)
        csLocs = np.append(startConjT,csLocs, axis = 1) #add starting point





        # print(csLocs)
        return csLocs

    return None


def tour(start,rad,voronoi_lst):

    csLocs = [x[1] for x in voronoi_lst]

    n = len(csLocs)
    mtx = np.zeros( (n,n) )

    for i in range(n):

        vor_set = set(voronoi_lst[i][0])

        for j in range(n):

            vor_set2 = set(voronoi_lst[j][0])

            has_intersection = 1 if len(vor_set.intersection(vor_set2)) > 0 else 0

            mtx[i][j] = has_intersection
            mtx[j][i] = has_intersection

        if( i > (n/2) ):
            break

    


    
    #Get tour information

    locsTmp = np.array( [ [x[0] for x in csLocs ] , [y[1] for y in csLocs ]  ] )

    tour = tf.tourFn(start, locsTmp, rad , mtx)

    if tour is not None:
        [locsTmp, coor, tourDist] = tour

    ordered_voronoiLst = [voronoi_lst[i] for i in coor[:-1]]

    #print([x[1] for x in ordered_voronoiLst])

    return ordered_voronoiLst




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

    CS = linear_program(inclMx,0,200,0,200,200,200,ns,1,rad,solMax,start)

    print(CS)


