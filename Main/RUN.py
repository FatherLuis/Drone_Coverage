
from Triangle import Triangle
from Drone import Drone
from Drone_Path2 import Drone_Path
from Draw import Draw
from Transformation2 import Transformation 
from Field import Field
from minCharge_LUIS import linear_program,tour
import matplotlib.pyplot as plt


import numpy as np 

import traceback


def run_program(drone, CS_radius , shape ,candidate, sp , showPlot = True):
    
    
    #################### INITIALS ####################
    field = Field()
    
    dist = lambda p1,p2: np.sqrt( (p2[1]-p1[1])**2 +(p2[0]-p1[0])**2)

    #################### FIELD MATRIX ####################
    # CREATE A BINARY MATRIX THAT REPRESENTS A FIELD 

    field_boundary =  shape
    #field_boundary =  [  (0,0) , (10,20) , (15,40), (35,45),
    #                     (45,35) , (50,25) , (45,15), (25,5) ]

    step = 0.02

    matrix, xmin, xmax, ymin, ymax, nx, ny = field.create_matrix_field(poly = field_boundary ,step = step)


    #################### LOCATING CHARGING STATIONS ####################
    # USE LINEAR PROGRAMMING TO OPTIMIZE THE LOCATION OF THE CHARGING STATIONS IN A FIELD

    half_distance  = CS_radius
    numberStations = candidate
    max_solutions = 10
    start_point = sp

    CS = linear_program( binMatrix = matrix, xmin=xmin, xmax=xmax,ymin=ymin,ymax=ymax,nx = nx, ny = ny, step = step,
                        ns = numberStations , rad = half_distance , solMax = max_solutions, start = start_point)


    
    

    #################### SPLIT POLYGONS INTO A LIST OF TRIANGLES ####################
    # EACH CHARGING STATION HAS A POLYGON FIELD, WHICH WILL BE SPLIT INTO TRIANGLES, 
    # WHERE THE CHARGING STATION IS A VERTEX AND THE BOUNDARIES ARE THE OTHER VERTICES

    sites = [ (x,y) for x,y in zip( CS[0][:], CS[1][:] ) ]

    vononili_lst = field.create_voronoi_polygons(site=sites, boundary=field_boundary)
    
    # ordered
    vononili_polys,entryExitLst, vertices = tour(start_point, drone.MAX_DISTANCE , vononili_lst)

    #################### FIND PATH FOR A GIVEN TRIANGLE ####################

    path_lst = []
    
    N = len(vononili_polys)
    
    k = 0

    for i,vononili_poly in enumerate(vononili_polys):
        
        #print('\n----- Voronoi ',i,' ------')

        
        # CREATE TRIANGLES FROM THE POLYGON, STORE AS LIST
        triangle_lst = field.create_triangle(poly = vononili_poly[0] , vertex = vononili_poly[1] ,)

        # LOOP THROUGH A LIST OF TRIANGLES, FIND PATH THAT COVERS THE AREA OF EACH

        for triangle in triangle_lst:    

            #print('\n--- Triangle ', k, ' ---')

            ### LINEAR TRANSFORMATIONS ###
            transform =  Transformation()
            
            curCS, trans_triangle, entryExit = transform.transform_triangle(triangle,entryExitLst[i])

            ### ALGORITHM ###

            DP = Drone_Path(trans_triangle , drone , entryExit)
            
            drone,path = DP.algorithm(curCS)

            trans_path = transform.transform_path(path) # TRANSFORM PATH TO FIT ORIGINAL SHAPE


            # ADD PATH TAKEN TO THE PATH LIST 
            path_lst.append(trans_path)
            #Canvas.boundary(triangle.get_all_points())

            # SET DRONE POSITION TO [0,0]
            drone.curPoint = np.array([0,0])       
            drone.curMax_distance = drone.MAX_DISTANCE
            

        # HERE, WE WILL ADD THE DISTANCE FROM ONE CHARGING STATION TO ANOTHER
        
        
        
        if i == N-1:         
            nVert = len(vertices)
        else:
            nVert = k + 2
            
        while(k < nVert-1):
            
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

                
                k += 2   
                
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
        Canvas.boundary(field_boundary)
    
        for vononili_poly in vononili_polys:
            #print(vononili_poly)
            #Canvas.boundary(vononili_poly[0],col='b')
            pass
    
    
        for path in path_lst:
            # DRAW PATH 
            Canvas.path(path)
            pass
    
        Canvas.draw_sites(sites)

    
        # SHOW PLOT
        plt.show()


    #   'num_Charging_Station','Total_Time','Total_Distance_Travel'

    return len(sites),drone.total_distance_travel





if __name__ == '__main__':

    # IF THIS FILE IS RUN, THE FOLLOWING CODE WILL BE READ
    
    try:
        
        
         ### INITIALIZE DRONE PROPERTIES ###

        drone = Drone(radius=0.025, max_distance = 8)       
    
        #field_boundary =  [ (0,0) , (0,7) , (7,7) , (7,0)]
        #field_boundary = [ (0,0),(2.28,0),(3.88,1.61),(3.88,3.88),(2.28,5.49),(0,5.49),(-1.61,3.88),(-1.61,1.61) ]

        field_boundary = [ (0,0) , (0,5) , (5,5) , (5,0)]

        
        CS_radius = 2.5
        
    
        lst = run_program(drone, CS_radius , field_boundary, 50, np.array([0, 0]) )
        
        print('')
        print('nCS:',lst[0])
        print('Time:',lst[1]/25)
        print('Travel',lst[1])
        
    except:
        
        print(traceback.format_exc())
