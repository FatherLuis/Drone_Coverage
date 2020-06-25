import numpy as np
import cvxopt
from cvxopt import matrix, spmatrix, sparse
from cvxopt.glpk import ilp
from cvxopt.blas import dotu
import numpy.random as rnd




# Note: 
# (4/23/2020): Changed TourFn from Version 2 to Version 4





######################################
# CODE BELOW REFLECTS SHAUNNA WORK
######################################

##############################################################################################
 #HELPER FUNCTIONS

def logicalFn(y):
    '''converts numerical values in an array to boolean/logicals'''
    return np.asarray(list(map(lambda x: bool(x), y))) 

##############################################################################################

def finalPath(start, pathArr, arr):
    '''Function to return path given start, edges(pathArray) 
        and array indicating where singleton is connected'''
    result = 0
    

    idxArray = np.where(arr[0].astype(int) > 0)[0]

    # CHECK IF SINGLETON ARRAY IS EMPTY
    if idxArray.size == 0:
        result = 1*pathArr
        
    else:
        path = np.asarray(list(map(lambda x: x + 1, pathArr)))
        idx = idxArray[-1]
        loc = np.where(path == idx+1)[0][-1] #gets last of matching indices
        afterIdx = np.append(path[loc:-1][::-1], start[0][0]) #reverse element after index
        res = np.append(start[1][0], path[: (loc + 1)][::-1])
        result = np.append(res, afterIdx)
        
        #print("result: ", result)
        
        if idxArray.size > 1:
            idxArr = idxArray[: -1]
            
            for index in idxArr:
                loc = np.where(result == index+1)[0][-1] #gets last of matching indices
                numBefore = result[loc-1]
                result = np.insert(result, loc+1, numBefore)    
    
    #Ask about case where dMxSingleTmp has more than one elem > 0
    return result    






# argument for my matrix
def tourFn(startP, locsTmp, adjMatrix):
    
    ncs = locsTmp.shape[1] #size(locsTmp,2)
    

    ##############################################
    #### CREATE A ADJACENT DISTANCE MATRIX 
    ##############################################
    
    xTmp = np.ones((ncs,1))*locsTmp[0, range(ncs)] # Create x matrix
    yTmp = np.ones((ncs,1))*locsTmp[1,range(ncs)] #Create y matrix
    dMxTmp = np.sqrt((xTmp - xTmp.conj().transpose()) **2 + (yTmp - yTmp.conj().transpose())**2) # Mx of mutual dists
    #dMxTmp = dMxTmp - dMxTmp * (dMxTmp >= 2*rad) # possible edges
    dMxTmp = dMxTmp * adjMatrix  # dMxTmp = dMxTmp * (my matrix) # replace 127
    
    
    ##############################################
    #### ELIMINATE SINGLETON PATHS FROM THE dMxTmp
    ##############################################
    
    # Check whether any singletons that are connected to only 1 site
    # Store singletons (nodes with only one way to get there)
    singLvec = (np.sum(dMxTmp>0, 0) == 1)  #Stations that can only be reached by 1
    #print("singLvec: ", singLvec, "\n")
    singLmx = locsTmp[:, singLvec] #x,y locations of singletons
    #print("\nsingLmx: ", singLmx, "\n")
    nonSingLMx = locsTmp[:, np.logical_not(singLvec)] #x,y locations of non-singletons
    #print("\nnonSingLMx: \n", nonSingLMx, "\n")
    dMxSingleTmp = np.array([[0]])
    
    
    
    if sum(singLvec >= 1):
        dMxSingleTmp = dMxTmp[np.ix_(logicalFn(singLvec),np.logical_not(singLvec))] # connect single with other CS
        dMxTmp = dMxTmp[np.ix_(np.logical_not(singLvec),np.logical_not(singLvec))]# Remaining edge vector
      
        
    ##############################################    
    #### Create a Edge Array that presents the relationship between nodes
    #### CREATE A cVec ARRAY THAT CONTAINS THE DISTANCES OF THE EDGES IN THE EDGE_ARRAY
    ##############################################
       
    
    ncsTmp = ncs - sum(singLvec) #remaining charging stations
    
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
    
    
    
    ##############################################    
    #### SET UP LINEAR PROGRAM
    ##############################################  
    
    
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
    
    
    
    ##############################################    
    #### THE LINEAR PROGRAM RETURNS THE ACCEPTABLE EDGES TO TRAVEL
    #### AFTERWARDS, THE CODE WILL TRY TO CREATE A CYCLE USING THE ACCEPTABLE EDGES
    ##############################################     
    

    
    while flag == 0: #Flag denotes cycle has been achieved
        global xNew
        #Solve linear program
        status, xNew = ilp(cVec, A_ineq, b_ineq, TSPmx, bTmp, I = set(), B = set(range(nEdge)))
        

        if status != 'optimal': # If no solution is found
            #print("Solution not found!\n\n")
            raise('No Tour Found')
            fmin = 1E100 # Mark this as impossible
            flag = 1 # Exit
        

        fmin = dotu(cVec, xNew)
        
        
        # build a vector of edges connected to node 1
        edgeSoln = edgeTmp[:,logicalFn(xNew)].astype(int) # Edges in solution
        cycNodes = np.zeros(ncsTmp) # Nodes in cycle
        thisNode = 0 #start with base node
        startNode = thisNode
        cycNodes[0] = thisNode # starting node
        cycEdges = np.zeros((1, nEdge)) #edges in cycle
        flag = 1
        path = [thisNode]
        
        #print("\nEdgeSoln: \n", edgeSoln, "\n")
        for jj in range(ncsTmp-1):
            tmp = np.where(edgeSoln == thisNode)  # Find current node in list of edges
            edgeIx = tmp[1][0]
            cycEdges[0][edgeIx] = -1  # Mark this edge as part of the solution  ###ISSUE CHECK
            thisNode = edgeSoln[1 - tmp[0][0], edgeIx] # Next node in tour ###ISSUE CHECK
            path.append(thisNode)
            edgeSoln[:,edgeIx] = -1 # Zero out edge so that it's not found again
            
            # DID THE CYCLE END PREMATURELY?
            if thisNode == cycNodes[0]: # Finished cycle
                flag = 0
                break

        if flag == 0: #Didn't complete cycle
            A_ineq = sparse([A_ineq, matrix(cycEdges, tc = 'd')])  #Enlarge LP matrix
            b_ineq = matrix(sparse([b_ineq, matrix([-1.0+sum(cycEdges[0])])]), tc = 'd') # Enlarge constant ###ISSUE CHECK
        
        path.append(startNode)
        path = np.asarray(path)

    #print("path: ", path)
    
    
           
    if status == 'optimal':
        
        #rows = np.arange(edgeTmp.shape[0])[:, np.newaxis] #get all rows of edgeTmp w/ new axes
        #edgeMx = edgeTmp[rows,logicalFn(xNew)] # Edges from which cycle is drawn
        tourDist = fmin + 2*sum(sum(dMxSingleTmp)) # Distance for solution
        
        #print("\nsingLmx: \n", singLmx)
        #print("dMxSingleTmp: ", dMxSingleTmp)
        
        ## PUTS PATH INDECES TOGETHER USING THE START POINT, EDGES PATH, AND THE SINGLETONS
        fPath = finalPath(startP.reshape(-1,1), path, dMxSingleTmp)#
        
        #print("****************************************************************************\n")
        #print("xNew:\n", xNew) #xNew.trans()
        #print("****************************************************************************\n")
        
        return locsTmp, fPath, tourDist
    
    return None
        
           
  
    
if __name__ == '__main__':  
    
    #################################
    # ARGUMENTS TO TEST tourFn
    #################################
    
    startP = np.array([0, 0]) #Starting point for tour (point of origin)
    
    locs = np.array([[0.,2.,2.,6.,5.],
                    [0.,2.,6.,2.,5.]])
    
    
    # ABCDE
    adjMatrix = np.array([[0,1,0,0,0],
                         [1,0,1,1,1],
                         [0,1,0,0,1],
                         [0,1,0,0,1],
                         [0,1,1,1,0]])
    
    ##################################
    
    locsTmp, fPath, tourDist = tourFn(startP, locs, adjMatrix)
    
    print(locsTmp)
    print('')
    print(fPath)
    print('')
    print(tourDist)

