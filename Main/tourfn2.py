# -*- coding: utf-8 -*-


import numpy as np
#import cvxopt
from cvxopt import matrix, spmatrix, sparse
from cvxopt.glpk import ilp



from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path





def tourFn(adjMatrix):

    
    def get_path(Pr, i, j):
        path = [j]
        k = j
        while Pr[i, k] != -9999:
            path.append(Pr[i, k])
            k = Pr[i, k]
        return path[::-1]
    
    
    # GET THE NUMBER OF VERTICES
    nCS = adjMatrix.shape[0]
    
    
    
    if nCS == 2:
        
        return np.array([0,1,0])
    
    
    
    graph = csr_matrix(adjMatrix)
    dMtx, predecessors = shortest_path(csgraph=graph, directed=False, return_predecessors=True)

    # Create variables from finite entries of reduced matrix
    edgeTmp = np.array([[], []]) # All edges
    cVec = [] #Edge distances
    
    for jj in range (nCS-1):
        for kk in range(jj+1, nCS):
            
            
            if dMtx[jj,kk] > 0:
                idx = np.array([[jj],[kk]])
                edgeTmp = np.append(edgeTmp, idx, axis = 1)

                cVec.append(dMtx[jj,kk])  # Minimize number of edges used
    
    nEdge = len(cVec) #Number of edges (variables)




    # Set up TSP (variables are connections, nodes are constraints)
    TSPmx = np.zeros((nCS,nEdge)) # LP matrix
    
    for jj in range(nEdge):  #Populate LP matrix
        TSPmx[(edgeTmp[0,jj]).astype(int),jj] = 1  #Two nodes per edge
        TSPmx[(edgeTmp[1,jj]).astype(int),jj] = 1
        
        
    TSPmx = matrix(np.array(TSPmx, dtype = float))
    bTmp = matrix(2*np.ones((nCS,1), dtype = float)) #Two edges per node
    cVec = matrix(np.array(cVec, dtype = float))
    
    A_ineq = spmatrix(0.0, [0], [0], (1,nEdge), tc = 'd')
    b_ineq = matrix(np.zeros((1,1), dtype = float), tc = 'd')
    

    isComplete = False
    
    while not(isComplete):
        
        status, xNew = ilp(cVec, A_ineq, b_ineq, TSPmx, bTmp, I = set(), B = set(range(nEdge)))
    
    
        # LINEAR PROGRAM FAILED
        if status != 'optimal':
            
            print('------------ ADJ MATRIX ---------------')
            print(adjMatrix)
            print('')  
            
            raise('No Tour Found')
        
        
        
        # CAST CVXOPT.MATRIX TO NUMPY ARRAY AS ROW VECTOR
        soln = np.array(xNew.T).astype(bool)[0]   
    
        cVecSoln = np.array(cVec.T)[0].astype(int)
        
        # GET A COPY OF THE 'edgeTmp' TO MANIPULATE
        edgeLst = np.copy(edgeTmp).astype(int)
        
    
        
        # WILL STORE TRUE/FALSE IF I HAVE TRAVELED TO THAT EDGE
        cycEdges = np.zeros(nEdge)        
    
        # STARTING NODE
        path = [0]
        
        # NUMBER OF EDGES IN SOLUTION
        nsEdges = sum(soln)
        

        # STARTING NODE
        path = [0]
        
        
        # ITERATE BY THE NUMBER OF EDGES IN THE SOLUTION
        for k in range(nsEdges):
        
            
            # LOCATE WHERE TO GO CURRENT NODE IS
            possibleEdges = np.where(  np.logical_and( (edgeLst == path[-1]) , (soln==1) ) )
                    
            
            # GET THE INDEX OF THE FIRST POTENTIAL EDGE
            edgeIx = possibleEdges[1][0]
            
            # GET THE EDGE WHERE MY NODE IS
            curEdge = edgeLst[:,edgeIx]
            
    
            ####################################
            ### CHECK THE WEIGHT OF THE EDGE 
            ####################################
            
            if cVecSoln[edgeIx] == 1:
                        
                # GET THE NEXT NODE I NEED TO TRAVEL TO
                nextNode = curEdge[0] if curEdge[1] == path[-1] else curEdge[1]         
                path.append(nextNode)
                
            else:
                
                curNode,nxtNode = (curEdge[1],curEdge[0]) if curEdge[1] == path[-1] else (curEdge[0],curEdge[1]) 
                
                lst = get_path(predecessors,curNode,nxtNode)
            
                path.extend(lst[1:]) 
            
            
            # LET 'cycEdge' KNOW THAT I TRAVELED ON THAT EDGE
            cycEdges[edgeIx] = 1
            
            # MARK THE EDGE SO THAT IT IS NOT FOUND AGAIN
            edgeLst[:,edgeIx] = -1
    
            # DID THE CYCLE END PREMATURELY? (NOT ALL EDGES IN SOLUTION WERE USED)
            if path[0] == path[-1]  and (k < nsEdges -1): 
    
                A_ineq = sparse([A_ineq, matrix(np.array([cycEdges]), tc = 'd')])  #Enlarge LP matrix
                b_ineq = matrix(sparse([b_ineq, matrix([-1.0+sum(cycEdges)])]), tc = 'd') # Enlarge constant
                
                break    
        
            elif k == nsEdges - 1 :
                
                isComplete = True
    

    return path











if __name__ == '__main__':  
    
    pass


    # adjMatrix = np.array([[0,1],
    #                       [1,0]])


    
    
    # adjMatrix = np.array([[0,1,0],
    #                       [1,0,1],
    #                       [0,1,0]])

    # adjMatrix = np.array([[1,1,1],
    #                       [1,1,1],
    #                       [1,1,1]])
    
    # adjMatrix = np.array([[0. ,0. ,1. ,0. ,1. ,0. ,0.],
    #                       [0. ,0. ,1. ,1. ,0. ,1. ,0.],
    #                       [1. ,1. ,0. ,0. ,1. ,1. ,0.],
    #                       [0. ,1. ,0. ,0. ,0. ,1. ,1.],
    #                       [1. ,0. ,1. ,0. ,0. ,0. ,0.],
    #                       [0. ,1. ,1. ,1. ,0. ,0. ,1.],
    #                       [0. ,0. ,0. ,1. ,0. ,1. ,0.]])




    # adjMatrix = np.array([[0,0,0,1,0,1,1,0,0,0],
    #                       [0,0,0,0,0,1,1,0,0,1],
    #                       [0,0,0,0,1,0,0,1,1,0],
    #                       [1,0,0,0,0,0,1,1,1,0],
    #                       [0,0,1,0,0,0,0,1,0,1],
    #                       [1,1,0,0,0,0,1,0,0,0],
    #                       [1,1,0,1,0,1,0,1,0,1],
    #                       [0,0,1,1,1,0,1,0,1,1],
    #                       [0,0,1,1,0,0,0,1,0,0],
    #                       [0,1,0,0,1,0,1,1,0,0]])

    adjMatrix = np.array([[1,0],
                         [0,1]])

    print(tourFn(adjMatrix))




