 
from Triangle import Triangle
from Drone import Drone
from Drone_Path2 import Drone_Path
from Draw import Draw
from Transformation2 import Transformation 
import Field as field
from minCharge import linear_program,tour
import matplotlib.pyplot as plt


import numpy as np 

import traceback



class Program():
    
    
    
    def __init__(self, field_boundary, meshStep, direction = 'cw'):
        
        self.fieldBoundary = field_boundary
        self.meshStep = meshStep
        self.fieldDirection = direction 
        
        self.fieldMaskInfo = field.create_matrix_field(poly = field_boundary ,
                                                       step = meshStep, 
                                                       direction = direction)
        
        self.customCandidates = []
        

    def clear_customCandidates(self):
         self.customCandidates = []
        


    def __csLocations(self ,drone ,start_point ,CS_radius ,nCandidates = 10, keepGenCandidates = False, customCandidate_coor = [] ):
        
        '''
        Parameters:
            
            drone: Drone Object that contains FOV radius and the Max distance it can travel before recharge
            start_point: a 1x2 list that contains the starting CS as (x,y)
            CS_Radius: Farthest distance drone can travel and return to charging station
            nCandidates: number of charging station generated candidates for the field
            customCandidate_coor: a x,y vector of the coordinate location for Charging Stations. nCandidates will be omited. 
        '''

        # FIELD MATRIX 
        # CREATE A BINARY MATRIX THAT REPRESENTS A FIELD 
        maskVector, xVector,yVector, nx, ny = self.fieldMaskInfo
    
    
        #################### LOCATING CHARGING STATIONS ####################
        # USE LINEAR PROGRAMMING TO OPTIMIZE THE LOCATION OF THE CHARGING STATIONS IN A FIELD
    
        droneRange = float(drone.MAX_DISTANCE)/2

    
        CS_SmallBig, bestVal_SmallBig, genCandidates = linear_program( maskVec = maskVector, 
                                                      xVec = xVector , 
                                                      yVec = yVector, 
                                                      ns = nCandidates , 
                                                      rad = CS_radius, 
                                                      droneRange = droneRange, 
                                                      start = start_point,
                                                      customCandidate_coor = customCandidate_coor)
    
    
    
        if keepGenCandidates:
            
            self.customCandidates = genCandidates
    
    
        return CS_SmallBig, bestVal_SmallBig
    
    


    def droneMission(self ,drone ,CS, showPlot = False):
        
        '''
        Parameter: 
            drone: Drone Object that contains FOV radius and the Max distance it can travel before recharge
            CS_SmallBig: 2-element list contains a small list of x,y arrays for the coordinates of the smaller list of CS 
                        and a big list of x,y arrays for the coordinate of the larger list of CS
            bestVal_SmallBig: 2-element list contains the best value for the small list of CS 
                        and the best balue for the largest list of CS

        '''
        
        dist = lambda p1,p2: np.sqrt( (p2[1]-p1[1])**2 +(p2[0]-p1[0])**2)
        

        
        
        #################### SPLIT POLYGONS INTO A LIST OF TRIANGLES ####################
        # EACH CHARGING STATION HAS A POLYGON FIELD, WHICH WILL BE SPLIT INTO TRIANGLES, 
        # WHERE THE CHARGING STATION IS A VERTEX AND THE BOUNDARIES ARE THE OTHER VERTICES
    
        sites = [ (x,y) for x,y in zip( CS[0][:], CS[1][:] ) ]
    
        voronoi_lst = field.create_voronoi_polygons(site= sites, 
                                                    boundary= self.fieldBoundary)
        
        # ordered
        entryExitLst, tourOrder ,vertices = tour(voronoi_lst)
    
    
        
        #################### FIND PATH FOR A GIVEN TRIANGLE ####################
    
        hasTravel = np.zeros(len(sites))
        # STORE LIST OF PATHS 
        path_lst = []
    
        for i,curNode in enumerate(tourOrder[:-1]):
            
            if not(hasTravel[curNode]):
                
                hasTravel[curNode] = 1
                
                curVoronoi = voronoi_lst[curNode]
                entryExit = entryExitLst[curNode]
    
                # CREATE TRIANGLES FROM THE POLYGON, STORE AS LIST
                triangle_lst = field.create_triangle(poly = curVoronoi[0] , vertex = curVoronoi[1])
        
                # LOOP THROUGH A LIST OF TRIANGLES, FIND PATH THAT COVERS THE AREA OF EACH
        
                for triangle in triangle_lst:    
        
                    #print('\n--- Triangle ', k, ' ---')
        
                    ### LINEAR TRANSFORMATIONS ###
                    transform =  Transformation()
                    
                    curCS, trans_triangle, entryExitTransform = transform.transform_triangle(triangle,entryExit)
        
                    ### ALGORITHM ###
        
                    DP = Drone_Path(trans_triangle , drone , entryExitTransform)
                    
                    drone,path = DP.algorithm(curCS)
        
                    trans_path = transform.transform_path(path) # TRANSFORM PATH TO FIT ORIGINAL SHAPE
        
            
        
                    # ADD PATH TAKEN TO THE PATH LIST 
                    path_lst.append(trans_path)
                    #Canvas.boundary(triangle.get_all_points())
        
                    # SET DRONE POSITION TO [0,0]
                    drone.curPoint = np.array([0,0])       
                    drone.curMax_distance = drone.MAX_DISTANCE
    
    
            # MOVE TO THE NEXT CS
                    
            k = 2*i
            curCS = vertices[k]
            nextVert = vertices[k+1]
            nextCS = vertices[k+2]
            
            dist_curCS_nextVert = dist(curCS,nextVert)
            dist_nextVert_nextCS = dist(nextVert,nextCS)
            
            req_dist_travel = dist_curCS_nextVert + dist_nextVert_nextCS
    
    
    
            if(drone.curMax_distance >= req_dist_travel):
                
                drone.total_distance_travel += req_dist_travel
                drone.curMax_distance -= req_dist_travel         
                drone.curMax_distance = drone.MAX_DISTANCE 
                
            else:
                
                raise('Could not Travel to next CS')
        
        
        
        if showPlot :
        
            # CREATE A FIGURE OBJECT
            fig1 = plt.figure(1)
            
            # CREATE A SUBPLOT IN THE FIGURE 
            ax1 = fig1.add_subplot(111)
            
            Canvas = Draw(ax1)
            #################### DRAW PLOTS ####################
            # DRAW THE PATH THE DRONE TOOK
            # LOOP THROUGH ALL THE PATHS AND DRAW THEM ON THE PLOT
        
            # DRAW SHAPE BOUNDARY
            Canvas.boundary(self.fieldBoundary)
        
            for curVoronoi in voronoi_lst:
                #print(vononili_poly)
                Canvas.boundary(curVoronoi[0],col='k')
                pass
        
        
            for path in path_lst:
                #DRAW PATH 
                Canvas.path(path)
                pass
            
            #Canvas.draw_sites_path(vertices)
        
            Canvas.draw_sites(sites)
    
        
            # SHOW PLOT
            plt.show()

       
    
        
        return len(sites),drone.total_distance_travel




    def run(self, drone, sp, CS_radius, nCandidates ,keepGenCandidates = False, customCandidate_coor = [], showPlot = False):


        '''
        Parameters:
            
            drone: Drone Object that contains FOV radius and the Max distance it can travel before recharge
            start_point: a 1x2 list that contains the starting CS as (x,y)
            CS_Radius: Farthest distance drone can travel and return to charging station
            nCandidates: number of charging station generated candidates for the field
            keepGenCandidates: Store the Generated CS candidates for reuse
            customCandidate_coor: a x,y vector of the coordinate location for Charging Stations. nCandidates will be omited. 
        '''
        
        
        
        
        if len(customCandidate_coor) > 0:
            
            CS_SmallBig, bestVal_SmallBig = self.__csLocations(drone,
                                                               sp,
                                                               CS_radius,
                                                               nCandidates, 
                                                               keepGenCandidates, 
                                                               customCandidate_coor)
            
        elif len(self.customCandidates) > 0 :
            
            CS_SmallBig, bestVal_SmallBig = self.__csLocations(drone,
                                                               sp,
                                                               CS_radius,
                                                               nCandidates, 
                                                               keepGenCandidates, 
                                                               self.customCandidates)
        
        else:
            
            CS_SmallBig, bestVal_SmallBig = self.__csLocations(drone,
                                                               sp,
                                                               CS_radius,
                                                               nCandidates, 
                                                               keepGenCandidates, 
                                                               customCandidate_coor)
            
        nCS = 0
        totalDist = 0
        bestVal = 0
            
            
        nSoln = len(CS_SmallBig)
            
        for idx in range(nSoln):
            
            try:
                
                drone.clear()  
                CS = CS_SmallBig[idx]
                bestVal = bestVal_SmallBig[idx]
                
                
                nCS, totalDist = self.droneMission(drone , CS, showPlot)
                
                break
    
            except:        

        
                print(traceback.format_exc())   
                nCS = 0
            
            
        if nCS == 0:
            raise('Program failed with given configurations')
            
            

            
            


        return nCS, totalDist , bestVal





if __name__ == '__main__':

    # IF THIS FILE IS RUN, THE FOLLOWING CODE WILL BE READ
    
    ## INITIALIZE ###
    
    field_bounds = [ (0,0) , (0,4.0825) , (12.2474,4.0825), (12.2474,0)]
    #[ (0,0), (-3.218,3.218), (-3.218,7.7689), (0,10.9869), (4.5509,10.9868), (7.7689,7.7689), (7.7689,3.218), (4.5509,0) ]
    #[ (0,0) , (0,7.0711) , (7.0711,7.0711) , (7.0711,0)] #[ (0,0) , (0,5) , (5,5) , (5,0)]
    meshStep = 0.02
    direction = 'cw'
    
    program = Program(field_bounds, meshStep, direction)
    
    nTrials = 1
    
    CS = [[0,0.56,4.2,11.54,6.14,11,7.48],
          [0,3.94,1.96,4.08,1.78,1.04,1.98]]
    

    
    
    for i in range(nTrials):
        try:
            print('----------- RUN {} ------------'.format(i))
    
            drone = Drone(radius = 0.025, max_distance = 8)
            startPoint = [0,0]
            CS_radius = 2.0
            nCandidates = 100
            
            nCS, travelDist, bestVal =program.run(drone, 
                                                  startPoint, 
                                                  CS_radius, 
                                                  nCandidates , 
                                                  keepGenCandidates =False,
                                                  customCandidate_coor = [], 
                                                  showPlot = True)

            print('')
            print('nCS:',nCS)
            print('Time:',travelDist/25)
            print('Travel',travelDist)
            print('Best value', bestVal)
        
        except:
            
            print(traceback.format_exc())
               
            


    # drone = Drone(radius = 0.025, max_distance = 8)
    # nCS, travelDist = program.droneMission(drone , CS)    
    # print('')
    # print('nCS:',nCS)
    # print('Travel',travelDist)