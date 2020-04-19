#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:04:16 2020

@author: Shauna-Resilient
"""

import random as r
import numpy as np
import cvxopt
from cvxopt import matrix, spmatrix, sparse
from cvxopt.glpk import ilp
from cvxopt.blas import dotu
import numpy.random as rnd


##############################################################################################
 #HELPER FUNCTIONS

def logicalFn(y):
    '''converts numerical values in an array to boolean/logicals'''
    return np.asarray(list(map(lambda x: bool(x), y))) 


def Not(Mx):
    '''Returns logical not'''
    
    result = Mx
    if Mx.ndim > 1:
        for i in range(np.size(result, 0)):
            result[i, :] = list(map(lambda x: not(x), result[i, :]))
    elif Mx.ndim == 1:
        result = list(map(lambda x: not(x), Mx))
    return result           
##############################################################################################



##############################################################################################
#ARGUMENTS TO TEST tourFn
##############################################################################################

start = np.array([20, 20]) #Starting point for tour (point of origin)
ns = 50

#a = [20,20]

#k = 1* solMx# [rnd.choice(a, ns)*1.0, rnd.choice(a, ns), rnd.choice(a, ns), rnd.choice(a, ns), rnd.choice(a, ns)]
csMx = np.array([[0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
   
ii = 1

locs = np.array([[160,96,50,183,55,64,61,169,144,91,34,154,55,84,55,48,46,179,114,35,164,72,110,174,30,19,141,122,123,42,68,44,60,88,173,81,62,102,78,52,128,124,50,155,83,82,120,51,172,50], [73,169,139,70,66,22,103,60,14,164,35,34,174,43,181,31,57,125,65,23,181,183,35,164,60,147,62,24,88,157,146,162,163,154,29,37,179,167,41,71,45,170,184,126,82,65,73,77,41,31]])

rad = 60 #coverage radius

##############################################################################################


def tourFn(start,csMx,ii,locs,rad):
    
    ns = csMx.shape[1]#size(csMx,2);
    locsTmp = locs[:,logicalFn(csMx[ii,range(ns)])] #select charging stations for current solution
    ncs = locsTmp.shape[1] #size(locsTmp,2)
    locsTmp = np.concatenate(([[start[0]],[start[1]]],locsTmp), axis = 1) #add starting point
    
    #Create link matrix with acceptable distances
    # compute all distances
    xTmp = np.ones((ncs+1,1))*locsTmp[0, range(ncs+1)] # Create x matrix
    yTmp = np.ones((ncs+1,1))*locsTmp[1,range(ncs+1)] #Create y matrix
    dMxTmp = np.sqrt((xTmp - xTmp.conj().transpose()) **2 + (yTmp - yTmp.conj().transpose())**2) # Mx of mutual dists
    dMxTmp = dMxTmp - dMxTmp * (dMxTmp >= 2*rad) # possible edges
    

    # Check whether any singletons that are connected to only 1 site
    # Store singletons (nodes with only one way to get there)
    singLvec = (np.sum(dMxTmp>0,0) == 1)  #Stations that can only be reached by 1
    singLmx = locsTmp[:, singLvec]
    
    # print("singLvec: ", singLvec)
    
    dMxSingleTmp = np.array([[0]])
    
    if sum(singLvec >= 1):
        dMxSingleTmp = dMxTmp[np.ix_(logicalFn(singLvec),logicalFn(Not(singLvec)))] # connect single with other CS
        dMxTmp = dMxTmp[np.ix_(logicalFn(Not(singLvec)),logicalFn(Not(singLvec)))]# Remaining edge vector
    
    ncsTmp = ncs + 1 - sum(singLvec) #remaining charging stations
    
    # print("ncs: ", ncs)
    
    # Create variables from finite entries of reduced matrix
    edgeTmp = np.array([[], []]) # All edges
    cVec = [] #Edge distances
    for jj in range (ncsTmp-1):
        for kk in range(jj, ncsTmp):
            if dMxTmp[jj,kk] > 0:
                idx = np.array([[jj],[kk]])
                edgeTmp = np.append(edgeTmp, idx, axis = 1)
                cVec.append((dMxTmp[jj,kk]))

    nEdge = len(cVec) #Number of edges (variables)
    
    # Set up TSP (variables are connections, nodes are constraints)
    TSPmx = np.zeros((ncsTmp,nEdge)) # LP matrix
    for jj in range(nEdge):  #Populate LP matrix
        TSPmx[(edgeTmp[0,jj]).astype(int),jj] = 1  #Two nodes per edge
        TSPmx[(edgeTmp[1,jj]).astype(int),jj] = 1
        
    TSPmx = matrix(np.array(TSPmx, dtype = float))
    bTmp = matrix(2*np.ones((ncsTmp,1), dtype = float)) #Two edges per node
    cVec = matrix(np.array(cVec, dtype = float))
    
    flag = 0
    A_ineq = spmatrix(0.0, [0], [0], (1,nEdge), tc = 'd')
    b_ineq = matrix(np.zeros((1,1), dtype = float), tc = 'd')
    
    fmin = 1E20 # Set large value as initial solution ##INCLUDE OR NOT?
    
    while flag == 0: #Flag denotes cycle has been achieved
        global xNew
        #Solve linear program
        status, xNew = ilp(cVec, A_ineq, b_ineq, TSPmx, bTmp, I = set(), B = set(range(nEdge)))
        
        if status == 'optimal':
            fmin = dotu(cVec, xNew)
        
        if status != 'optimal': # If no solution is found
            # print("Solution not found!\n\n")
            fmin = 1E100 # Mark this as impossible
            flag = 1 # Exit
        
        else:
            # Check connectivity
            # build a vector of edges connected to node 1
            edgeSoln = edgeTmp[:,logicalFn(xNew)].astype(int) # Edges in solution
            cycNodes = np.zeros(ncsTmp) # Nodes in cycle
            thisNode = 0 #start with base node
            cycNodes[0] = thisNode # starting node
            cycEdges = np.zeros((1, nEdge)) #edges in cycle
            flag = 1
            
            for jj in range(ncsTmp-1):
                tmp = np.where(edgeSoln == thisNode)  # Find current node in list of edges
                edgeIx = tmp[1][0]
                cycEdges[0][edgeIx] = -1  # Mark this edge as part of the solution  ###ISSUE CHECK
                thisNode = edgeSoln[1 - tmp[0][0], edgeIx] # Next node in tour ###ISSUE CHECK
                edgeSoln[:,edgeIx] = -1 # Zero out edge so that it's not found again
                
                # print("****************************************************************************\n")
                if thisNode == cycNodes[1]: # Finished cycle
                    flag = 0
                    break
            
            if flag == 0: #Didn't complete cycle
                A_ineq = sparse([A_ineq, matrix(cycEdges, tc = 'd')])  #Enlarge LP matrix
                b_ineq = matrix(sparse([b_ineq, matrix([-1.0+sum(cycEdges[0])])]), tc = 'd') # Enlarge constant ###ISSUE CHECK
            
    
    if status == 'optimal':
        
        rows = np.arange(edgeTmp.shape[0])[:, np.newaxis] #get all rows of edgeTmp w/ new axes
        edgeMx = edgeTmp[rows,logicalFn(xNew)] # Edges from which cycle is drawn
        tourDist = fmin + 2*sum(sum(dMxSingleTmp)) # Distance for solution
        
        # print("****************************************************************************\n")
        # print("xNew:\n", xNew.trans())
        # print("****************************************************************************\n")
        
        return singLmx, dMxSingleTmp, edgeMx, tourDist
        
           
  
    
    
    
# print(tourFn(start,csMx,ii,locs,rad))

t = tourFn(start,csMx,ii,locs,rad)