# -*- coding: utf-8 -*-


from Triangle import Triangle
from Drone import Drone
from DronePath2 import Drone_Path2
from Draw import Draw
from Transformation2 import Transformation 
from Field import Field
from Utilities import dist
from minCharge_LUIS import linear_program,tour
from Travel import traveling

import numpy as np 



def run_program(drone_rad , drone_maxDist , max_CS_dist, shape ,candidate, showPlot = True):
    #################### INITIALS ####################
    field = Field()
    
    
    ### INITIALIZE DRONE PROPERTIES ###
    
    rad = 0.25
    mxDist = 25 # MUST BE ABLE TO REACH A VERTEX AND RETURN TO CHARGING STATION
    drone = Drone(radius=rad, max_distance = mxDist)
    
    #################### SPLIT POLYGONS INTO A LIST OF TRIANGLES ####################
    # EACH CHARGING STATION HAS A POLYGON FIELD, WHICH WILL BE SPLIT INTO TRIANGLES, 
    # WHERE THE CHARGING STATION IS A VERTEX AND THE BOUNDARIES ARE THE OTHER VERTICES
    
    field_boundary = [ (0,0) , (0,20) , (20,20), (20,0)  ]
    
    sites = [( 0,0 ) , ( 5,15 ) , ( 15,15 ) ,  ( 15,5 ) ]
    
    vononili_lst = field.create_voronoi_polygons(site=sites, boundary=field_boundary)
    
    # ordered
    vononili_polys = tour(sites[0],rad , vononili_lst)
    
    vertices , entryExitLst = traveling(vononili_polys)
    
    #################### FIND PATH FOR A GIVEN TRIANGLE ####################
    
    path_lst = []
    site_path = []
    N = len(vononili_polys)
    i = 0

    for vononili_poly in vononili_polys:
        
        # CREATE TRIANGLES FROM THE POLYGON, STORE AS LIST
        triangle_lst = field.create_triangle(poly = vononili_poly[0] , vertex = vononili_poly[1] ,)

        # LOOP THROUGH A LIST OF TRIANGLES, FIND PATH THAT COVERS THE AREA OF EACH

        for triangle in triangle_lst:    

        

            ### LINEAR TRANSFORMATIONS ###
            transform =  Transformation()
            curCS,trans_triangle, entryExit = transform.transform_triangle(triangle,entryExitLst[i])


            ### ALGORITHM ###

            DP = Drone_Path2(trans_triangle , drone , entryExit)
            
            print('CS:  ',curCS)
            
            drone,path = DP.algorithm(curCS)

            #print('path N:',len(path))
            trans_path = transform.transform_path(path) # TRANSFORM PATH TO FIT ORIGINAL SHAPE

            # SET DRONE POSITION TO [0,0]
            drone.curPoint = np.array([0,0])
            # RESET CURMAX DISTANCE TO DRONE MAX DISTANCE
            drone.curMax_distance = drone.MAX_DISTANCE

            # ADD PATH TAKEN TO THE PATH LIST 
            path_lst.append(trans_path)

            #Canvas.boundary(triangle.get_all_points())

        # HERE, WE WILL ADD THE DISTANCE FROM ONE CHARGING STATION TO ANOTHER


    print('------------- Drone -------------')
    print(drone)
    print('---------------------------------')


    if showPlot :
        Canvas = Draw()
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
    
    
    
        #Canvas.draw_sites_path(site_path)
    
        # SHOW PLOT
        Canvas.show_plot()


    #   'num_Charging_Station','Total_Time','Total_Distance_Travel'

    return len(sites), 0 , drone.total_distance_travel





if __name__ == '__main__':

    # IF THIS FILE IS RUN, THE FOLLOWING CODE WILL BE READ

    rad = 0.7
    mxDist = 20

    field_boundary =  [  (0,0) , (0,60) , (60,60), (60,0) ]
    #field_boundary =  [  (0,0) , (10,20) , (15,40), (35,45),
    #                     (45,35) , (50,25) , (45,15), (25,5) ]
    half_distance  = np.floor(mxDist / 2.0 ) * 0.6

    run_program(rad, mxDist, half_distance, field_boundary, 25)
