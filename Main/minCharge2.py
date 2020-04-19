# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 20:46:52 2020

@author: SK
"""

from cvxopt import matrix, spmatrix, sparse
from cvxopt.glpk import ilp
from cvxopt.blas import dotu
import numpy as np
import matplotlib.pyplot as plt
import random as r
import tourFn



print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")


ng = np.array([200,200]) #number of cells on each side of grid
ng_tot = ng[0] * ng[1]
ns = 50 # Number of possible charging station positions
rad = 60 #coverage radius
solMax = 5 #Maximum number of solutions
start = np.array([20, 20]) #Starting point for tour (point of origin)
rad2 = rad**2

#To the edges
power = 2 #Penalty for large distances
solMx = np.array([])

#Determine region to be covered 
##NEEDS TO BE POLYGONAL
gMeans = np.array([[50, 50, 150, 150], [50, 150, 50, 150]]) #Means of Gaussian used to determine regions
gStd = np.array([[30, 30, 30, 30], [30, 30, 30, 30]]) #Std's of Guassions used to determine region
theta_g = 0.4 #Threshold to decide inclusion in region

#x and y coordinates of grid
xVecGrid = np.floor(np.arange(ng_tot)/ ng[0]) + 1 #Integer values for x and y
yVecGrid = (np.arange(ng_tot) % ng[0]) + 1

print("*************************** X VEC ***************************************")
print('X Grid')
print(xVecGrid)
print('size:',len(xVecGrid))
# repeats n numbers of x values [11111...22222...3333...]
print("*************************** Y VEC ***************************************")
print('Y Grid')
print(yVecGrid)
print('size:',len(yVecGrid))
# repeats sequence of y values [123...123...123]
print("****************************************************************************")

inclVec = 0 * xVecGrid


#Find points in region
for ii in range(gMeans.shape[1]):
    inclVec = inclVec + np.exp(-(xVecGrid - gMeans[0,ii])**2/(2*gStd[0,ii]**2)-(yVecGrid - gMeans[1,ii])**2/(2*gStd[1,ii]**2))
    
inclVec = inclVec > theta_g
inclMx = np.reshape(inclVec, ng) # Matrix for inclusion in region (used in plotting)
plt.pcolor(inclMx) ###CHECK

#plt.show()


xVec = xVecGrid[inclVec]
yVec = yVecGrid[inclVec]
np_tot = sum(inclVec) # Number of points in region

print("*************************** X VEC ***************************************")
print(xVec)
print("****************************************************************************")
print("*************************** Y VEC ***************************************")
print(yVec)
print("****************************************************************************")

# Locate charging stations
locs0 = r.sample(range(1, np_tot+1),ns) #k Random locations for charging station
locs = np.array([xVec[locs0], yVec[locs0]])

#Define incidence matrix: coverage area for drone is circular with radius rad
d2Mx = np.zeros((np_tot,ns))
# Distance matrix and locations not covered by start
for ii in range(ns):
    d2Mx[:, ii] =  (locs[0,ii]- xVec)**2 + (locs[1,ii]- yVec)**2 

  
iMx = d2Mx < rad2# Coverage matrix
iVec = ((xVec - start[0])**2 + (yVec-start[1])**2) > rad2; # points covered by start

logicalIVec = np.asarray([bool(ii) for ii in iVec])
iMx = iMx[logicalIVec, :] #Logical coverage matrix for remaining points
d2Mx = d2Mx[logicalIVec, :] #Distance matrix for remaining points
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
        csLocs = locs[:, tourFn.logicalFn(solMx[ii,:])] #select charging stations for current solution
        startConjT = np.array(np.matrix(start).H) #start.conj().transpose()#conjugate transpose of start
        csLocs = np.append(startConjT,csLocs, axis = 1) #add starting point
        for jj in range(csLocs.shape[1]): # Construct minDistMx and regMx
            #If power is larger, farther points are counted more
            tmpDistVec = ((xVec-csLocs[0,jj])**2 + (yVec-csLocs[1,jj])**2)**power
            minDistVec = np.minimum(minDistVec,tmpDistVec)
        #Save best value so far
        distStat[ii] = sum(minDistVec)
        distStat[ii] = min(distStat[ii],distStat[ii - (ii > 0)])
    

    plt.figure()
    plt.plot(range(len(distStat)),distStat,'*')
    plt.title('Distance statistic improvement for trial solutions')
    plt.xlabel('Solution number')
    plt.ylabel('Distance statistic')
    
    
    bestVal,bestIx = min(distStat), np.argmin(distStat) #Choose best solution
    #iBest = bestIx[0];
    csLocs = locs[:,tourFn.logicalFn(solMx[bestIx,:])] #select charging station locs. for best solution
    startConjT = np.array(np.matrix(start).H)
    csLocs = np.append(startConjT,csLocs, axis = 1) #add starting point
    

    print(csLocs)
    









    #Display voronoi regions
    # Create distance matrix for each location, find minimum, and index.
    minDistMx = 1E50*np.ones(ng) # Set large initial value
    regMx = np.zeros(ng) # regions
    
    xMx = xVecGrid.reshape(ng[0],ng[1]) #Vector of x coords
    yMx = yVecGrid.reshape(ng[0],ng[1]) #Vector of y coords



    for ii in range(csLocs.shape[1]): #Construct minDistMx and regMx
        tmpDistMx = np.sqrt( (xMx-csLocs[0,ii])**2 + (yMx-csLocs[1,ii])**2 )
        minDistMx = np.minimum(minDistMx,tmpDistMx)
        tmpLogMx = (tmpDistMx == minDistMx)
        regMx[tmpLogMx] = ii


    minDistMx[tourFn.Not(inclMx)] = 'nan'
            
    
    

#    #Get tour information
#    [singLmx,dMxSingle,edgeMx,tourDist] = tourFn(start, solMx, bestIx, locs, rad)
#    
#    plt.figure(1)
#    # plot edges plt.colorbar()
#    plt.pcolormesh(minDistMx, shading = 'gouraud')
#    #shading('interp')
#    
#    
#    for ii in range(edgeMx.shape[1]):
#       pt1 = csLocs[:,edgeMx[0,ii]]
#       pt2 = csLocs[:,edgeMx[1,ii]]
#       plt.plot([pt1[0],pt2[0]],[pt1[1],pt2[1]],'k--')
#    
#    for ii in range(singLmx.shape[1]): 
#        pt1 = singLmx[:,ii]
#        pt2 = locs[:,tourFn.logicalFn(dMxSingle[ii, :])]
#        plt.plot([pt1(1),pt2(1)],[pt1(2),pt2(2)],'k--')
#
#    #title('Distance to nearest charging station')
#    plt.figure(2)
#    regMx[tourFn.Not(inclMx)] = 'nan'
#    plt.pcolormesh(minDistMx, shading = 'gouraud') #colorbar() #hold on
#    
#
#    for ii in range(edgeMx.shape[1]): 
#       pt1 = csLocs[:, edgeMx[0,ii]]
#       pt2 = csLocs[:, edgeMx[1,ii]]
#       plt.plot([pt1[0],pt2[0]],[pt1[1],pt2[1]],'k--')
#    
#    for ii in range(singLmx.shape[1]): 
#        pt1 = singLmx[:,ii]
#        pt2 = locs[:,tourFn.logicalFn(dMxSingle[ii, : ])]
#        plt.plot([pt1[0],pt2[0]],[pt1[1],pt2[1]],'k--')
#    
#    #title('Regions covered by different charging stations')
#    
#    plt.figure(4)
#    dists = minDistMx.reshape(1, minDistMx.shape[0] * minDistMx.shape[1])
#    
#    plt.hist(dists, [range(0.5, rad + 0.5, 0.2)], density=True,
#                        facecolor='green', alpha=0.75,
#                        label="")
#    plt.title('Histogram of grid point distances')
    
    
    
#    histogram(dists,0.5:rad+0.5)
    
#    plt.hist(dists, bins = 10, density=True,
#                        facecolor='green', alpha=0.75,
#                        label="")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
print("****************************************************************************")  

#Get tour information
#[singLmx,dMxSingle,edgeMx,tourDist] = tourFn(start,solMx,iBest,locs,rad)

#plt.figure(1)
#plt.pcolor(minDistMx)
#shading('interp')
## plot edges
#plt.colorbar()
#hold on
#for ii = 1:size(edgeMx,2)
#   pt1 = csLocs(:,edgeMx(1,ii));
#   pt2 = csLocs(:,edgeMx(2,ii));
#   plot([pt1(1),pt2(1)],[pt1(2),pt2(2)],'k--')
#end
#for ii = 1:size(singLmx,2)
#    pt1 = singLmx(:,ii);
#    pt2 = locs(1:2,logical(dMxSingle(ii,1:end)));
#    plot([pt1(1),pt2(1)],[pt1(2),pt2(2)],'k--')
#end
#title('Distance to nearest charging station')
#figure(2)
#regMx(not(inclMx)) = NaN;
#pcolor(regMx)
#shading('interp')
#colorbar()
#hold on
#for ii = 1:size(edgeMx,2)
#   pt1 = csLocs(:,edgeMx(1,ii));
#   pt2 = csLocs(:,edgeMx(2,ii));
#   plot([pt1(1),pt2(1)],[pt1(2),pt2(2)],'k--')
#end
#for ii = 1:size(singLmx,2)
#    pt1 = singLmx(:,ii);
#    pt2 = locs(1:2,logical(dMxSingle(ii,1:end)));
#    plot([pt1(1),pt2(1)],[pt1(2),pt2(2)],'k--')
#end
#title('Regions covered by different charging stations')
#
#figure(4)
#dists = reshape(minDistMx,1,size(minDistMx,1)*size(minDistMx,2));
#histogram(dists,0.5:rad+0.5)
#title('Histogram of grid point distances')