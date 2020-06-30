import numpy as np
import cvxopt
from cvxopt import matrix, spmatrix, sparse
from cvxopt.glpk import ilp
from cvxopt.blas import dotu
import numpy.random as rnd






######################################
# CODE BELOW REFLECTS SHAUNNA WORK
######################################

##############################################################################################
 #HELPER FUNCTIONS

def logicalFn(y):
    '''converts numerical values in an array to boolean/logicals'''
    return np.asarray(list(map(lambda x: bool(x), y))) 

##############################################################################################

def finalPath(start, pathArr, singLvec, aMx):

        
    result = []
    path = np.array(pathArr)


    # THERE ARE THREE CASES:
    # CASE I: THERE ARE NO SINGLETONS
    # CASE II: ALL THE VERTICES ARE SINGLETONS
    # CASE III: SOME ARE SINGLETONS
    
    
    nCS = len(singLvec)
    
    ###########################################  
    # CASE I : THERE ARE NO SINGLETONS
    ###########################################  
    if np.sum(singLvec) == 0:
        
        result = path
        
    ###########################################    
    # CASE II: ALL VERTICES ARE SINGLETONS
    ###########################################  
    elif np.sum(singLvec) == nCS:
        
        idx = 0
        result.append(idx)
        singLvec[idx] = 0
        
        
        ###########################################  
        # GO THROUGH EACH ROW, AND FIND THE NEXT VERTICES
        # START ON ROW 0, THEN HOP AROUND ROWS UNTIL YOU REACH THE LAST VERTEX
        ###########################################  
        for k in range(nCS-1):
    
            # SELECT CURRENT ROW
            row = aMx[idx,:]
            # FIND THE INDEX OF THE NEXT VERTICES
            idx = np.where(row == 1)[0][0]
            # ADD THE INDEX TO THE RESULT
            result.append(idx)
            
            # ZERO OUT THE CONNECTIONS TO THIS VERTICES
            aMx[:,np.logical_not(singLvec)] = 0
            aMx[np.logical_not(singLvec),:] = 0
            
            # SET THE INDEx FALSE 
            singLvec[idx] = 0
        
        ###########################################  
        # NEED TO RETURN THE WAY I CAME IN
        ###########################################  
            
        # CREATE A REVERSE LIST
        reverse_lst = [elem for elem in reversed(result[:-1])]
        # ADD THE REVERSE LIST TO THE RESULT LIST
        result.extend(reverse_lst)

    ###########################################  
    # CASE III: THERE IS A PATH AND THERE ARE SINGLETONS
    ###########################################  
    else:

        
        
        # CONSTRUCT A SINGLETON MATRIX
        sMx = np.copy(aMx)
        sMx[np.ix_(np.logical_not(singLvec),np.logical_not(singLvec))] = 0
        
        
        
        # GIVE THE CORRECT INDECES FOR THE PATH
        path = np.arange(nCS)[np.logical_not(np.array(singLvec))][path]
        
        result = np.copy(path)
        
        for k in path:
            
            i = k 
            chain = np.array([])
            
            row = sMx[i,:]
            
            # CHECK FOR LABELED SINGLETONS
            while( not( sum(row) == 0 ) ):
                
                
                idx = np.where(row == 1)[0][0]

                chain = np.append(chain,idx)
                
                sMx[i,:] = 0
                sMx[:,i] = 0
                
                i = idx
                row = sMx[i,:]
                
                # IF THERE ARE NO MORE SINGLETONS
                if( sum(row) == 0 ):
                    
                    # PATH HAS TWO CASES:
                    # CASE I: THE FIRST ELEM IS ALSO AT THE END OF THE PATH
                    # CASE II: THE OTHER ELEMS ONLY APPEAR ONCE
                    # THUS, WE'LL TREAT THEM DIFFERENT
                    
                    
                    p_idx = np.where(result == k)[0]
                    
                    # CASE I:THE FIRST ELEM IS ALSO AT THE END OF THE PATH
                    if (len(p_idx) == 2):
                        
                        # USING THE FIRST MATCH
                        # WE'LL ATTACH THE SINGLETONS TO THE LEFT
                        # IN REVERSE
                        
                        
                        result = np.insert( result , p_idx[0] ,chain[::-1] )
                    
                        # GET THE SECOND APPERANCE 
                        p_idx = np.where(result == k)[0]
                        result = np.insert( result , p_idx[-1] +1 ,chain )
                        
                    else:
                        
                        # CONTRUCT THE ARRAY THAT WE'LL BE INSERTING
                        
                        

                        arr = np.append(chain,np.append(np.flipud(chain[:-1]),k))
                        
                        result = np.insert( result , p_idx[0] + 1 , arr)

                        
                        
                    

    print(result)

    # [0 , ....... , 0]
    return result    






# argument for my matrix
def tourFn(startP, locsTmp, adjMatrix):
    
    
    ncs = locsTmp.shape[1] #size(locsTmp,2)
    
    print(locsTmp)

    ##############################################
    #### CREATE A ADJACENT DISTANCE MATRIX 
    ##############################################
    
    xTmp = np.ones((ncs,1))*locsTmp[0, range(ncs)] # Create x matrix
    yTmp = np.ones((ncs,1))*locsTmp[1,range(ncs)] #Create y matrix
    dMxTmp = np.sqrt((xTmp - xTmp.conj().transpose()) **2 + (yTmp - yTmp.conj().transpose())**2) # Mx of mutual dists
    #dMxTmp = dMxTmp - dMxTmp * (dMxTmp >= 2*rad) # possible edges
    dMxTmp = dMxTmp * adjMatrix  # dMxTmp = dMxTmp * (my matrix) # replace 127
    
    aMx = np.copy(adjMatrix)
    
    ##############################################
    #### ELIMINATE SINGLETON PATHS FROM THE dMxTmp
    ##############################################
    
    # Check whether any singletons that are connected to only 1 site
    # Store singletons (nodes with only one way to get there)    
    singLvec = (np.sum(adjMatrix, axis = 0) == 1)
    singvecTemp = np.copy(singLvec) 
    
    
    while sum(singvecTemp) > 0:
        
        # ZERO OUT THE SINGLETONS ON THE MATRIX
        adjMatrix[:,singLvec] = 0
        adjMatrix[singLvec,:] = 0
    
        
        singLvec = np.logical_or(singLvec,singvecTemp)
        
        singvecTemp = (np.sum(adjMatrix, axis = 0) == 1)

        
        
    # WE TAKE OFF THE SINGLETONS FROM THE MATRIX
    dMxTmp = dMxTmp[np.ix_(np.logical_not(singLvec),np.logical_not(singLvec))]
        
        
        
        
    ##############################################    
    #### Create a Edge Array that presents the relationship between nodes
    #### CREATE A cVec ARRAY THAT CONTAINS THE DISTANCES OF THE EDGES IN THE EDGE_ARRAY
    ##############################################
       
    
    ncsTmp = ncs - sum(singLvec) #remaining charging stations
    
    # IF THERE IS ATLEAST ONE NON-SINGLETON
    if ncsTmp > 0:
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
            
            xNew = np.where(xNew)[0] # Change xNew to vector of indices
            # build a vector of edges connected to node 1
            edgeSoln = edgeTmp[:,xNew].astype(int) # Edges in solution
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
                cycEdges[0][xNew[edgeIx]] = 1  # Mark this edge as part of the solution  ###ISSUE CHECK
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
            tourDist = 0
            
            #print("\nsingLmx: \n", singLmx)
            #print("dMxSingleTmp: ", dMxSingleTmp)
            
            ## PUTS PATH INDECES TOGETHER USING THE START POINT, EDGES PATH, AND THE SINGLETONS
            fPath = finalPath(startP.reshape(-1,1), path, singLvec,aMx)#
            
            #print("****************************************************************************\n")
            #print("xNew:\n", xNew) #xNew.trans()
            #print("****************************************************************************\n")
            
            return locsTmp, fPath, tourDist
    
    else:
        
        fPath = finalPath(startP.reshape(-1,1), [0], singLvec, aMx)
        
        return locsTmp, fPath, 0
        
        
        
           
  
    
if __name__ == '__main__':  
    
    #################################
    # ARGUMENTS TO TEST tourFn
    #################################
    
    startP = np.array([0, 0]) #Starting point for tour (point of origin)
    
    # locs = np.array([[0.,2.,2.,6.,5.],
    #                 [0.,2.,6.,2.,5.]])
    
    
    # ABCDE
    # adjMatrix = np.array([[0,1,0,0,0],
    #                       [1,0,1,1,1],
    #                       [0,1,0,0,1],
    #                       [0,1,0,0,1],
    #                       [0,1,1,1,0]])
    
  
    
    # adjMatrix = np.array([[0. ,1. ,1. ,0.],
    #  [1. ,0. ,1. ,0.],
    #  [1. ,1. ,0. ,1.],
    #  [0. ,0. ,1. ,0.]])
    
    # locs = np.array([[0.   ,0.8  ,4.44 ,8.34],
    #                 [0.   ,3.5  ,2.42 ,2.66]])
    #[0, 2, 3, 2, 3, 0]   
    
    # adjMatrix = np.array([[0. ,0. ,0. ,1.],
    #                      [0. ,0. ,1. ,1.],
    #                      [0. ,1. ,0. ,1.],
    #                      [1. ,1. ,1. ,0.]])
    
    # locs = np.array([[0.   ,7.32 ,7.48 ,2.46],
    #                  [0.   ,3.64 ,1.68 ,2.68]])
    # #[0, 2, 3, 0, 3, 0]
    
    
    
#    adjMatrix = np.array([[0. ,0. ,1. ,1.],
#                          [0. ,0. ,0. ,1.],
#                          [1. ,0. ,0. ,1.],
#                          [1. ,1. ,1. ,0.]])
#    
#    locs = np.array([[0.   ,9.44 ,2.08 ,5.76],
#                     [0.   ,2.1  ,3.24 ,2.62]])
    
    
    
    
    
    # THESE PARAMETERS ARE CAUSING TROUBLES
    #-------------Charging Stations-------------------
    #(0.0, 0.0)
    #(2.38, 2.42)
    #(4.94, 2.58)
    #(8.100000000000001, 2.66)
                             
    # locs = np.array( [[0.0, 2.38, 4.94 ,8.10] , [0.0 , 2.42 , 2.58 , 2.66]] )
    #------------- ADJ Matrix ----------------
    
    # adjMatrix = np.array( [[0., 1., 0., 0.],
    #                       [1., 0., 1., 0.],
    #                       [0., 1., 0., 1.],
    #                       [0., 0., 1., 0.]] )  
    
    
    
    
    
    
    
    # adjMatrix = np.array([[0., 1., 0., 1.],
    #                      [1., 0.,1., 1.],
    #                      [0., 1., 0.,0.],
    #                      [1., 1.,0.,0.]])

    # locs = np.array([[0.   ,4.48 ,8.2  ,2.38],
    #                  [0.   ,2.56 ,2.84 ,3.16]])
    #[0, 1, 1, 2, 3]
    
    
    # adjMatrix = np.array([[0. ,0. ,1. ,1.],
    #              [0. ,0. ,0. ,1.],
    #              [1. ,0. ,0. ,1.],
    #              [1. ,1. ,1. ,0.]])
    
    # locs = np.array([[0.   ,7.94 ,1.72 ,5.2 ],
    #                  [0.   ,2.18 ,4.26 ,2.62]])   
    
    #[0, 1, 3, 2, 3, 0]




    # adjMatrix = np.array([[0. ,1. ,1. ,0.],
    #                       [1. ,0. ,1. ,1.],
    #                       [1. ,1. ,0. ,0.],
    #                       [0. ,1. ,0. ,0.]])
    
    # locs = np.array([[0.   ,4.18 ,1.52 ,8.86],
    #                   [0.   ,2.5  ,3.96 ,2.6 ]])
    #[0, 3, 1, 1, 2, 0])


    # adjMatrix = np.array([[0. ,0. ,1. ,1.],
    #                       [0. ,0. ,1. ,0.],
    #                       [1. ,1. ,0. ,1.],
    #                       [1. ,0. ,1. ,0.]])
    
    # locs = np.array([[0.   ,9.12 ,4.92 ,1.72],
    #                   [0.   ,2.02 ,2.98 ,3.44]])


    # [0, 2, 3, 1, 2, 0]
    
    
    #################
    #TOUR Lin Eq
    
    

    # adjMatrix = np.array([[0. ,0. ,0. ,1. ,0. ,1.],
    #                       [0. ,0. ,1. ,1. ,1. ,0.],
    #                       [0. ,1. ,0. ,0. ,1. ,0.],
    #                       [1. ,1. ,0. ,0. ,1. ,1.],
    #                       [0. ,1. ,1. ,1. ,0. ,1.],
    #                       [1. ,0. ,0. ,1. ,1. ,0.]])
    
    # locs = np.array([[0.   ,8.02 ,8.36 ,3.6  ,5.54 ,1.8 ],
    #                  [0.   ,1.   ,3.94 ,0.16 ,3.92 ,3.32]])    
    
    
    
    
    
    ### CHAINED ENTRY SINGLETONS
    
    # adjMatrix = np.array([ [0,1,0,0,0],
    #                        [1,0,1,0,0],
    #                        [0,1,0,1,1],
    #                        [0,0,1,0,1],
    #                        [0,0,1,1,0]])
    
    # locs = np.array([[0,1,2,3,3],
    #                  [0,0,0,1,-1]])
    
    ### CHAINED COMPLEX SINGLETONS
    
    
    adjMatrix = np.array([[0,1,0,0,0,0,0,0],
                          [1,0,1,0,0,0,0,0],
                          [0,1,0,1,0,1,0,0],
                          [0,0,1,0,1,1,0,0],
                          [0,0,0,1,0,0,0,0],
                          [0,0,1,1,0,0,1,0],
                          [0,0,0,0,0,1,0,1],
                          [0,0,0,0,0,0,1,0]])
    
    locs = np.array([[0,1,2,3,4,3,4,5],
                     [0,0,0,1,2,-1,-2,-3]])
    
    
    
    ##################################
    
    locsTmp, fPath, tourDist = tourFn(startP, locs, adjMatrix)
    
    print('\n')
    print(locsTmp)
    print('')
    print(fPath)
    print('')
    print(tourDist)

