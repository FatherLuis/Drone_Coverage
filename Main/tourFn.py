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

def finalPath(pathArr, singLvec, aMx):

        
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
        # GO THROUGH EACH ROW, AND FIND THE NEXT VERTEX
        # START ON ROW 0, THEN HOP AROUND ROWS UNTIL YOU REACH THE LAST VERTEX
        ###########################################  
        for k in range(nCS-1):
    
            # SELECT CURRENT ROW
            row = aMx[idx,:]
            # FIND THE INDEX OF THE NEXT VERTICES
            idx = np.where(row == 1)[0][0]
            # ADD THE INDEX TO THE RESULT
            result.append(idx)
            
            # ZERO OUT THE CONNECTIONS TO THIS VERTEX
            aMx[:,np.logical_not(singLvec)] = 0
            aMx[np.logical_not(singLvec),:] = 0
            
            # SET THE INDEX FALSE 
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
        # ZERO OUT THE NON SINGLETONS 
        sMx[np.ix_(np.logical_not(singLvec),np.logical_not(singLvec))] = 0
        
        
        
        # GIVE THE CORRECT INDECES FOR THE PATH
        path = np.arange(nCS)[np.logical_not(np.array(singLvec))][path]
        
        
        
        ###########################################  
        # ROTATE THE PATH SUCH THAT THE FIRST ELEMENT 
        # IN THE PATH IS RELATED TO THE FIRST CS
        ###########################################  
        # WHY THIS IS NECESSARY: THE CYCLE BEGINS ON 
        # THE FIRST NON-SINGLETON IN 'singLvec'
        # THE FIRST CS MAY NOT BE CONNECTED ON THIS ELEM.
        # THE ALGORITHM BELOW ASSUMES THAT THE FIRST ELEM
        # IN THE CYCLE IS RELATED TO THE FIRST CS
        ############################################
        
        # IS MY FIRST ELEM A SINGLETON?
        if singLvec[0]:
            
            # CONVERT NUMPY ARRAY INTO LIST
            path = path.tolist()

            # COPY THE SINGLETON MATRIX
            sMx2 = np.copy(sMx)       
            
            # START OFF ON THE FIRST ROW (TRAIL MY WAY INTO THE CYCLE)
            idx =  0
            
            # ITERATE UNTIL YOU'RE IN THE CYCLE (PATH)
            while (True):
                
                
                # GET THE ROW
                # (SINCE IT'S WORKING AS A REFERENCE, I NEEDED TO MAKE A COPY)
                row = np.copy(sMx2[idx,:])      
                     
                # ZERO OUT THE CONNECTIONS TOT HIS NODE
                sMx2[idx,:] = 0
                sMx2[:,idx] = 0      
                
                # IDENTIFY WHERE I AM CONNECTED TO
                idx = np.where(row == 1)[0][0]
                    
                # IS THE ELEM THAT IS RELATED TO THE FIRST ELEM IN THE CYCLE?
                if (idx in path):
                    
                    # WE'LL BE RECONSTRUCTING THE CYCLE
                    # DELETE THE LAST ELEMENT IN THE PATH
                    path.pop(-1)
                    
                    # ITERATE UNTIL THE ELEM 'idx' IS THE FIRST ELEMENT IN THE PATH
                    while(not(path[0] == idx)):
                        
                        # REMOVE FIRST ELEMENT
                        # ADD THE REMOVED ELEMENT TO THE END
                        path.append(path.pop(0))
                    
                    # ADD THE 'idx' ELEMENT TO THE END OF THE PATH
                    # THE CYCLE HAS BEEN RECONSTRUCTED
                    path.append(idx)
                    break
                    
                    
                    
                            
        
        
        
        result = np.copy(path)
        
        ###########################################  
        # ITERATE THROUGH EACH ELEM IN PATH AND ATTACH THE SINGLETONS TO THE PATH
        ###########################################  
        for k in path:
            
            # WILL BE USED TO TRAVEL BETWEEN ROWS
            i = k 
            
            # WILL STORE THE SINGLETONS FOUND
            chain = np.array([])
            
            # SELECT THE ROW OF INTEREST
            row = sMx[i,:]
            
            # CHECK FOR LABELED SINGLETONS
            while( not( sum(row) == 0 ) ):
                
                # GET THE INDEX OF THE SINGLETON
                idx = np.where(row == 1)[0][0]

                # ADD THE INDEX TO THE CHAIN
                chain = np.append(chain,idx)
                
                # ZERO OUT THE SINGLETON ON THE MATRIX
                sMx[i,:] = 0
                sMx[:,i] = 0
                
                # IDENTIFY TO WHICH ROW I WILL BE GOING NEXT
                i = idx
                row = sMx[i,:]
                
                
                # CHECK IF THERE ARE SINGLETONS ON THE ROW,
                # IF NOT, THEN ATTACH THE CHAIN TO THE PATH
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
                        # THEN, THE ON THE SECOND APPERANCE
                        # WE'LL ATTACH THE CHAIN TO THE RIGHT
                        
                        
                        ###########################################  
                        # EXAMPLE:
                        #
                        # CHAIN = [3,2,1]
                        # PATH = [ 4,5,6,4]
                        #
                        # FIRST APPERANCE (REVERSE THE CHAIN)
                        # [1,2,3] -> [4,5,6,4]
                        #
                        #
                        # SECOND APPERANCE
                        # [1,2,3,4,5,6,4] <- [3,2,1]
                        ###########################################  
                        
                        # FIRST APPERANCE 
                        result = np.insert( result , p_idx[0] ,chain[::-1] )
                    
                        # GET THE SECOND APPERANCE 
                        p_idx = np.where(result == k)[0]
                        result = np.insert( result , p_idx[-1] +1 ,chain )
                        
                    else:
                        
                        # CONTRUCT THE ARRAY THAT WE'LL BE INSERTING
                        
                        ###########################################  
                        # EXAMPLE:
                        #
                        # CHAIN = [3,2,1]
                        # PATH = [ 4,5,6,4]
                        #
                        # K = 5
                        #
                        # CONSTRUCT ARRAY THAT'LL BE INSERTED
                        # [3,2,1] <- [2,3] <- [K]
                        # [3,2,1,2,3,5]
                        #
                        # INSERT
                        # [4,5] -> [3,2,1,2,3,5] <- [6,4]
                        ###########################################                          

                        arr = np.append(chain,np.append(np.flipud(chain[:-1]),k))
                        
                        result = np.insert( result , p_idx[0] + 1 , arr)

                        
              
                    
    print('------------ TOUR ---------------')
    print(result)
    print('')
    
    

    # [0 , ....... , 0]
    return result    






# argument for my matrix
def tourFn(locsTmp, adjMatrix):
    
    
    ncs = locsTmp.shape[1] #size(locsTmp,2)
    
    print('------------ CS LOCS ---------------')
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
    
    print('------------ ADJ MATRIX ---------------')
    print(aMx)
    print('')  
    
    ##############################################
    #### ELIMINATE SINGLETON FROM THE dMxTmp
    ##############################################
    
    # Check whether any singletons that are connected to only 1 site
    # STA singletons (nodes with only one way to get there)    
    
    # WILL STORE TRUE/FALSE IF NODE IS A SINGLETON
    # CHAINED SINGLETONS WILL ALSO BE STORED HERE AS TRUE/FALSE
    singLvec = (np.sum(adjMatrix, axis = 0) == 1)
    
    # IDENTIFY ALL SINGLETONS AND CHAINED SINGLETONS
    while (True):
        
        
        # ZERO OUT THE SINGLETONS ON THE MATRIX
        adjMatrix[:,singLvec] = 0
        adjMatrix[singLvec,:] = 0 
        
        
        # NEWLY IDENTIFIED SINGLETONS
        has1 = (np.sum(adjMatrix, axis = 0) == 1)
        # PREVIOUSLY IDENTIFIED SINGLETON
        has0 = (np.sum(adjMatrix, axis = 0) == 0)
        # ENSURE singLvec KNOWS WHO ARE SINGLETONS
        singLvec =  np.logical_or(has0, has1)
        
        # DID WE IDENTIFY MORE SINGLETONS?
        # 0: NO
        if sum(has1) == 0:
            break
          
    
    # CREATE A DISTANCE MATRIX WITHOUT THE SINGLETONS
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
                    #cVec.append((dMxTmp[jj,kk]))
                    cVec.append(1)  # Minimize number of edges used
        
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
        
    
        # SCOPE ISSUE
        path = None       
        edgeSoln = None
        edgeLst = None
        cycEdges = None
        
        while True:
            
            
            # FLAG = 0 : THIS IS THE FIRST ITERATION
            # FLAG = 1 : LINEAR PROGRAM HAS EXECUTED SUCCESSFULLY ATLEAST ONCE
            # FLAG = 2 : LINEAR PROGRAM FAILED AFTER ADDITIONAL CONTRAINTS ADDED
            #            WHICH MEANS THERE IS MORE THAN ONCE CYCLE FOUND. 
            
            #Solve linear program
            status, xNew = ilp(cVec, A_ineq, b_ineq, TSPmx, bTmp, I = set(), B = set(range(nEdge)))
            
            
            # LINEAR PROGRAM FAILED ON FIRST TRY 
            if status != 'optimal' and flag == 0:
                
                raise('No Tour Found')

            if status != 'optimal' and flag == 1:
                
                flag = 2
                 
            else:    
                # LINEAR PROGRAM HAS EXECUTED SUCCESSFULLY ATLEAST ONCE
                flag = 1
                       
    
    
            ###############################################
            # RESET VARIABLES TO WORK FOR NEW xNew SOLUTION
            ###############################################
            
            if flag == 1:
                # CAST CVXOPT.MATRIX TO NUMPY ARRAY AS ROW VECTOR
                edgeSoln = np.array(xNew.T).astype(int)[0]   
                            
                # GET A COPY OF THE 'edgeTmp' TO MANIPULATE
                edgeLst = np.copy(edgeTmp).astype(int)
                
                # WILL STORE TRUE/FALSE IF I HAVE TRAVELED TO THAT EDGE
                cycEdges = np.zeros(nEdge)        
        
                # STARTING NODE
                path = [0]
                
                # NUMBER OF EDGES IN SOLUTION
                nsEdges = sum(edgeSoln)
                
                
                
                for k in range(nsEdges):
                
                    
                    # LOCATE WHERE TO GO CURRENT NODE IS
                    possibleEdges = np.where(  np.logical_and( (edgeLst == path[-1]) , (edgeSoln==1) ) )
                    
                    # GET THE INDEX OF THE FIRST POTENTIAL EDGE
                    edgeIx = possibleEdges[1][0]
                    
                    # GET THE EDGE WHERE MY NODE IS
                    curEdge = edgeLst[:,edgeIx]
                    
                    # GET THE NEXT NODE I NEED TO TRAVEL TO
                    nextNode = curEdge[0] if curEdge[1] == path[-1] else curEdge[1]
                    path.append(nextNode)
                    
                    # LET 'cycEdge' KNOW THAT I TRAVELED ON THAT EDGE
                    cycEdges[edgeIx] = 1
                    
                    # MARK THE EDGE SO THAT IT IS NOT FOUND AGAIN
                    edgeLst[:,edgeIx] = -1
                    
                    
                    
                    # DID THE CYCLE END PREMATURELY?
                    if path[0] == path[-1] : 
                        
                        A_ineq = sparse([A_ineq, matrix(np.array([cycEdges]), tc = 'd')])  #Enlarge LP matrix
                        b_ineq = matrix(sparse([b_ineq, matrix([-1.0+sum(cycEdges)])]), tc = 'd') # Enlarge constant
                        
                        break
            
                    
                            
            elif flag == 2 :
                
                cycleLst = [path]
                
                
                
                while( not( np.all(np.equal( (edgeLst[0] == -1 ) , edgeSoln) )) ):    
                    
                    edgeIx= np.where(  np.logical_and( np.logical_not(edgeLst == -1) , edgeSoln ) )[1][0] 
                    
                    curPath = [  edgeLst[:,edgeIx][0] ]
                    
                    
                    nEdgesLeft = sum(cycEdges == 0)
                    
                    for k in range(nEdgesLeft):
                    
                    
                        # LOCATE WHERE TO GO CURRENT NODE IS
                        possibleEdges = np.where(  np.logical_and( (edgeLst == curPath[-1]) , (edgeSoln==1) ) )
                        
                        # GET THE INDEX OF THE FIRST POTENTIAL EDGE
                        edgeIx = possibleEdges[1][0]
                        
                        # GET THE EDGE WHERE MY NODE IS
                        curEdge = edgeLst[:,edgeIx]
                        
                        # GET THE NEXT NODE I NEED TO TRAVEL TO
                        nextNode = curEdge[0] if curEdge[1] == curPath[-1] else curEdge[1]
                        curPath.append(nextNode)
                        
                        # LET 'cycEdge' KNOW THAT I TRAVELED ON THAT EDGE
                        cycEdges[edgeIx] = 1
                        
                        # MARK THE EDGE SO THAT IT IS NOT FOUND AGAIN
                        edgeLst[:,edgeIx] = -1           
                
                    
                        # DID THE CYCLE END?
                        if curPath[0] == curPath[-1]:
                
                            cycleLst.append(curPath)
                            break
                
                
                ###################################################
                # NOW THAT I HAVE THE CYCLES, I NEED TO CONNECT THEM
                ###################################################
                        
                        
                       
                        
            
            
                break
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    
            # if status != 'optimal': # If no solution is found
            #     #print("Solution not found!\n\n")
            #     raise('No Tour Found')
            #     fmin = 1E100 # Mark this as impossible
            #     flag = 1 # Exit
            
    
            # fmin = dotu(cVec, xNew)
            
            # xNew = np.where(xNew)[0] # Change xNew to vector of indices
            # # build a vector of edges connected to node 1
            # edgeSoln = edgeTmp[:,xNew].astype(int) # Edges in solution
            # cycNodes = np.zeros(ncsTmp) # Nodes in cycle
            # thisNode = 0 #start with base node
            # startNode = thisNode
            # cycNodes[0] = thisNode # starting node
            # cycEdges = np.zeros((1, nEdge)) #edges in cycle
            # flag = 1
            # path = [thisNode]
            
            # #print("\nEdgeSoln: \n", edgeSoln, "\n")
            # for jj in range(ncsTmp-1):
            #     tmp = np.where(edgeSoln == thisNode)  # Find current node in list of edges
            #     edgeIx = tmp[1][0]
            #     cycEdges[0][xNew[edgeIx]] = 1  # Mark this edge as part of the solution  ###ISSUE CHECK
            #     thisNode = edgeSoln[1 - tmp[0][0], edgeIx] # Next node in tour ###ISSUE CHECK
            #     path.append(thisNode)
            #     edgeSoln[:,edgeIx] = -1 # Zero out edge so that it's not found again
                
            #     # DID THE CYCLE END PREMATURELY?
            #     if thisNode == cycNodes[0]: # Finished cycle
            #         flag = 0
            #         break
    
            # if flag == 0: #Didn't complete cycle
                
                
                
            #     A_ineq = sparse([A_ineq, matrix(cycEdges, tc = 'd')])  #Enlarge LP matrix
            #     b_ineq = matrix(sparse([b_ineq, matrix([-1.0+sum(cycEdges[0])])]), tc = 'd') # Enlarge constant ###ISSUE CHECK
            
    #         path.append(startNode)
    #         path = np.asarray(path)
    
    #     #print("path: ", path)
        
        
               
    #     if status == 'optimal':
            
    #         ## PUTS PATH INDECES TOGETHER USING THE START POINT, EDGES PATH, AND THE SINGLETONS
    #         fPath = finalPath(path, singLvec,aMx)#

            
    #         return locsTmp, fPath
    
    # else:
        
    #     fPath = finalPath([], singLvec, aMx)
        
    #     return locsTmp, fPath
        
        
        
           
  
    
if __name__ == '__main__':  
    
    #################################
    # ARGUMENTS TO TEST tourFn
    #################################

    
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
    
    # THRON TEST SUBJECT
    # adjMatrix = np.array([[0,1,0,0,0,0,0,0],
    #                       [1,0,1,0,0,0,0,0],
    #                       [0,1,0,1,0,1,0,0],
    #                       [0,0,1,0,1,1,0,0],
    #                       [0,0,0,1,0,0,0,0],
    #                       [0,0,1,1,0,0,1,0],
    #                       [0,0,0,0,0,1,0,1],
    #                       [0,0,0,0,0,0,1,0]])
    
    # locs = np.array([[0,1,2,3,4,3,4,5],
    #                   [0,0,0,1,2,-1,-2,-3]])
    
    
    
    # adjMatrix = np.array([[0,0,0,0,1,0],
    #                       [0,0,1,1,1,0],
    #                       [0,1,0,0,1,1],
    #                       [0,1,0,0,1,0],
    #                       [1,1,1,1,0,1],
    #                       [0,0,1,0,1,0]])
    
    
    # locs = np.array([[0,8.12,7.12,6.78,2.9,2.26],
    #                   [0,4.34,8.4,0.82,3.1,7.7]])
    
    # [1 2 5 4 0 4 3 1]
    
    # adjMatrix = np.array([[0,0,0,0,0,1],
    #                       [0,0,1,0,1,1],
    #                       [0,1,0,0,1,0],
    #                       [0,0,0,0,1,1],
    #                       [0,1,1,1,0,1],
    #                       [1,1,0,1,1,0]])    
    
    # locs = np.array([[0.   ,7.64 ,7.88 ,0.34 ,3.94 ,3.  ],
    #                  [0.   ,2.44 ,7.48 ,6.84 ,7.42 ,1.82]])
    
    # FAILED (07/1/2020)
    #------------ CS LOCS ---------------
    locs = np.array([[ 0.    ,7.06  ,3.78 ,11.06  ,1.04  ,6.92 ,10.78],
                     [ 0.    ,0.26  ,2.1   ,1.46  ,2.56  ,3.04  ,3.96]])
    #------------ ADJ MATRIX ---------------
    adjMatrix = np.array([[0. ,0. ,1. ,0. ,1. ,0. ,0.],
                          [0. ,0. ,1. ,1. ,0. ,1. ,0.],
                          [1. ,1. ,0. ,0. ,1. ,1. ,0.],
                          [0. ,1. ,0. ,0. ,0. ,1. ,1.],
                          [1. ,0. ,1. ,0. ,0. ,0. ,0.],
                          [0. ,1. ,1. ,1. ,0. ,0. ,1.],
                          [0. ,0. ,0. ,1. ,0. ,1. ,0.]])
    
    
    ##################################
    
    locsTmp, fPath = tourFn(locs, adjMatrix)
    
    print('\n')
    print(locsTmp)
    print('')
    print(fPath)

