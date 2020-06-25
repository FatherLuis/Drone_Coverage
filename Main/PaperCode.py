# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt



def voronoiRegionCreation():
    
    from scipy.spatial import Voronoi, voronoi_plot_2d
    
    from Field import Field

    
    ###################################
    ## UNDEFINED VORONOI REGIONS
    ###################################
    
#    points = np.array([[0, 0], [2, 0], [1, 2], [1, 1]])
#    
#    vor = Voronoi(points) 
#
#    voronoi_plot_2d(vor)
#    
#    
#    plt.xlim( - 3 , 5)
#    plt.ylim( - 2 , 4)
#    
#    plt.savefig('photos\\undefinedVoronoiRegion.png')
    
    ###################################
    ## BOUNDED VORONOI REGIONS
    ###################################
    
#    points = np.array([[0, 0], [2, 0], [1, 2], [1, 1] , [-5,-5], [-5,5], [5,5], [5,-5]])
#    
#    vor = Voronoi(points) 
#
#    voronoi_plot_2d(vor)
#      
#    plt.xlim( - 7 , 7)
#    plt.ylim( - 7 , 9)
#    
#    plt.savefig('photos\\boundedVoronoiRegion.png')    
    
    
    ###################################
    ## BOUNDED VORONOI REGIONS W/ Shape
    ###################################    
    
#    points = np.array([[0, 0], [2, 0], [1, 2], [1, 1] , [-5,-5], [-5,5], [5,5], [5,-5]])
#    
#    vor = Voronoi(points) 
#
#    voronoi_plot_2d(vor)
#    
#    
#    
#    shape = [ [-1,-1] , [3,-1] , [3,2] , [1,4] , [-1,2]]
#    
#    # GET THE SIZE OF THE LIST
#    N = len(shape)
#    
#    col = 'k'
#    # ITERATE THROUGH THE LIST OF POINTS
#    for i in range(N):
#
#        # SELECT i ELEMENT FROM THE LIST
#        x1 = shape[i][0]
#        y1 = shape[i][1]
#
#        # IF THIS IS THE LAST ELEMENT IN THE LIST
#        if( i == N-1):
#            
#            # DRAW A LINE FROM THE LAST ELEMENT TO THE FIRST ELEMENT 
#            plt.plot( (shape[0][0] ,  x1) , (shape[0][1] ,y1) ,color= col)
#
#
#        else:
#            # SELECT i+1 ELEMENT FROM THE LIST
#            x2 = shape[i+1][0]
#            y2 = shape[i+1][1]              
#
#            # DRAW A LINE FROM i ELEMENT TO i+1 ELEMENT
#            plt.plot( (x1,x2) , (y1,y2) ,color=col)      
#    
#      
#    plt.xlim( - 7 , 7)
#    plt.ylim( - 7 , 9)
#    
#    plt.savefig('photos\\boundedVoronoiRegionWithShape.png')     
    
    
    
    
    ###################################
    ## BOUNDED VORONOI REGIONS IN SHAPE
    ###################################

#    field = Field()
#    
#    site = [ [0, 0], [2, 0], [1, 2], [1, 1] ]
#    shape = [ [-1,-1] , [3,-1] , [3,2] , [1,4] , [-1,2]]
#    
#    lstvor = field.create_voronoi_polygons(site, shape)
#    
#    vor_only_lst = [lst[0] for lst in lstvor]
#    
#    for p in site:
#        
#        plt.plot(p[0],p[1],'ro')
#        
#    # GET THE SIZE OF THE LIST
#    N = len(shape)
#    
#    col = 'k'
#    # ITERATE THROUGH THE LIST OF POINTS
#    for i in range(N):
#
#        # SELECT i ELEMENT FROM THE LIST
#        x1 = shape[i][0]
#        y1 = shape[i][1]
#
#        # IF THIS IS THE LAST ELEMENT IN THE LIST
#        if( i == N-1):
#            
#            # DRAW A LINE FROM THE LAST ELEMENT TO THE FIRST ELEMENT 
#            plt.plot( (shape[0][0] ,  x1) , (shape[0][1] ,y1) ,color= col)
#
#
#        else:
#            # SELECT i+1 ELEMENT FROM THE LIST
#            x2 = shape[i+1][0]
#            y2 = shape[i+1][1]              
#
#            # DRAW A LINE FROM i ELEMENT TO i+1 ELEMENT
#            plt.plot( (x1,x2) , (y1,y2) ,color=col)    
#
#
#    for vor in vor_only_lst:
#        
#        # GET THE SIZE OF THE LIST
#        N = len(vor)
#        
#        col = 'k'
#        # ITERATE THROUGH THE LIST OF POINTS
#        for i in range(N):
#    
#            # SELECT i ELEMENT FROM THE LIST
#            x1 = vor[i][0]
#            y1 = vor[i][1]
#    
#            # IF THIS IS THE LAST ELEMENT IN THE LIST
#            if( i == N-1):
#                
#                # DRAW A LINE FROM THE LAST ELEMENT TO THE FIRST ELEMENT 
#                plt.plot( (vor[0][0] ,  x1) , (vor[0][1] ,y1) ,color= col)
#    
#    
#            else:
#                # SELECT i+1 ELEMENT FROM THE LIST
#                x2 = vor[i+1][0]
#                y2 = vor[i+1][1]              
#    
#                # DRAW A LINE FROM i ELEMENT TO i+1 ELEMENT
#                plt.plot( (x1,x2) , (y1,y2) ,color=col)         
#
#    plt.savefig('photos\\shapeBoundVoronoiRegion.png')



def field_paths():


    from Draw import Draw
    from Drone import Drone
    from Triangle import Triangle
    from ChargingPad import ChargingPad
    from Drone_Path2 import Drone_Path
    from Transformation2 import Transformation
    from Field import Field
    from minCharge_LUIS import tour
 
    
    ###################################
    ## Triangle Drone Passage
    ###################################

#    drone = Drone(radius= 0.025, max_distance = 8, velocity = 25)    
#    
#    # Initialize Charging Pad
#    volt = 25
#    cPad = ChargingPad(volt)    
#    
#    entryExit = [ (0,1.43495) , (0,2.98667)]
#    
#    # It is assumed that the first point is the CS
#    pp =  [ (0,0), (0,3) , (2,2) ]  
#    
#    triangle = Triangle(*pp)
#    
#    transform = Transformation()
#    
#    curCS,transTriangle, primeEntryExit= transform.transform_triangle(triangle,entryExit)
#    
#    #print('\n',triangle)
#    
#    #curCS = 'C'
#    
#    DP = Drone_Path(transTriangle,drone,cPad,primeEntryExit)  
#
#    drone, path = DP.algorithm(curCS)
#    
#    path_pts = transform.transform_path(path)
#
#
#    # GET THE SIZE OF THE LIST
#    N = len(pp)
#    col = 'k'
#    
#    
#    plt.plot(0,0,'ro')
#
#    # ITERATE THROUGH THE LIST OF POINTS
#    for i in range(N):
#
#        # SELECT i ELEMENT FROM THE LIST
#        x1 = pp[i][0]
#        y1 = pp[i][1]
#
#        # IF THIS IS THE LAST ELEMENT IN THE LIST
#        if( i == N-1):
#            
#            # DRAW A LINE FROM THE LAST ELEMENT TO THE FIRST ELEMENT 
#            plt.plot( (pp[0][0] ,  x1) , (pp[0][1] ,y1) ,color= col)
#
#        else:
#            # SELECT i+1 ELEMENT FROM THE LIST
#            x2 = pp[i+1][0]
#            y2 = pp[i+1][1]              
#
#            # DRAW A LINE FROM i ELEMENT TO i+1 ELEMENT
#            plt.plot( (x1,x2) , (y1,y2) ,color=col)
#
#
#
#    # CREATE A TUPLE WITH THREE RANDOM NUMBERS ( USED FOR RGM COLORING)
#    colors = np.random.rand(3,)
#    
#    # ITERATE THROUGH THE LIST OF POINTS
#    for i in range( len(path_pts) - 1 ):
#
#        # SELECT i ELEMENT FROM THE LIST
#        x1 = path_pts[i][0]
#        y1 = path_pts[i][1]
#
#        # SELECT i+1 ELEMENT FROM THE LIST
#        x2 = path_pts[i+1][0]
#        y2 = path_pts[i+1][1]  
#
#        # IF i ELEMENT IS IN THE ORIGIN, CHANGE COLORS
#        # THIS HELPS IDENTIFY NEW PATHS FROM THE DRONE PROJECT
#        if ( (x1==path_pts[0][0] and y1==path_pts[0][1])):
#           
#            # CREATE A TUPLE WITH THREE RANDOM NUMBERS ( USED FOR RGM COLORING)
#            colors = np.random.rand(3,)
#      
#        # DRAW A LINE FROM i ELEMENT TO i+1 ELEMENT
#        plt.plot( (x1,x2) , (y1,y2) , c = colors , linewidth = 1, alpha = 0.7 )
#
#
#    plt.savefig('photos\\dronePathTriangle.png')
    
    
#    field = Field()
#    
#
#    drone = Drone(radius= 0.025, max_distance = 8, velocity = 25) 
#     
#    
#    # Initialize Charging Pad
#    volt = 25
#    cPad = ChargingPad(volt)
#
#    ### SHAPE ###
#    # Square
#    pentagon = [ [-1,-1] , [3,-1] , [3,2] , [1,4] , [-1,2]]
#    
#    start_point = np.array([0,0])
#
#    sites = [ [0, 0], [2, 0], [1, 2], [1, 1] ]
#
#    vononili_lst = field.create_voronoi_polygons(site=sites, boundary=pentagon)
#    
#    # ordered
#    vononili_polys,entryExitLst, vertices = tour(start_point, drone.MAX_DISTANCE , vononili_lst)
#
#    #################### FIND PATH FOR A GIVEN TRIANGLE ####################
#
#    path_lst = []
#
#    for i,vononili_poly in enumerate(vononili_polys):
#        
#        #print('\n----- Voronoi ',i,' ------')
#
#        
#        # CREATE TRIANGLES FROM THE POLYGON, STORE AS LIST
#        triangle_lst = field.create_triangle(poly = vononili_poly[0] , vertex = vononili_poly[1] ,)
#
#        # LOOP THROUGH A LIST OF TRIANGLES, FIND PATH THAT COVERS THE AREA OF EACH
#
#        for triangle in triangle_lst:    
#
#            #print('\n--- Triangle ', k, ' ---')
#
#            ### LINEAR TRANSFORMATIONS ###
#            transform =  Transformation()
#            curCS, trans_triangle, entryExit = transform.transform_triangle(triangle,entryExitLst[i])
#
#
#            ### ALGORITHM ###
#
#            DP = Drone_Path(trans_triangle , drone , cPad ,entryExit)
#            
#            drone,path = DP.algorithm(curCS)
#
#            trans_path = transform.transform_path(path) # TRANSFORM PATH TO FIT ORIGINAL SHAPE
#
#
#            # ADD PATH TAKEN TO THE PATH LIST 
#            path_lst.append(trans_path)
#            #Canvas.boundary(triangle.get_all_points())
#
#            # SET DRONE POSITION TO [0,0]
#            drone.curPoint = np.array([0,0])         
#            cPad.charge_drone(drone)
#
#
    
    
    
    
    
    
    ###################################
    ## Pentagon Drone Passage
    ###################################    
    
    
    
    
#
#    for p in sites:
#        
#        plt.plot(p[0],p[1],'ro')
#
#    col = 'k'
#    ## DRAW SHAPE
#    N = len(pentagon)
#    # ITERATE THROUGH THE LIST OF POINTS
#    for i in range(N):
#
#        # SELECT i ELEMENT FROM THE LIST
#        x1 = pentagon[i][0]
#        y1 = pentagon[i][1]
#
#        # IF THIS IS THE LAST ELEMENT IN THE LIST
#        if( i == N-1):
#            
#            # DRAW A LINE FROM THE LAST ELEMENT TO THE FIRST ELEMENT 
#            plt.plot( (pentagon[0][0] ,  x1) , (pentagon[0][1] ,y1) ,color= col)
#
#        else:
#            # SELECT i+1 ELEMENT FROM THE LIST
#            x2 = pentagon[i+1][0]
#            y2 = pentagon[i+1][1]              
#
#            # DRAW A LINE FROM i ELEMENT TO i+1 ELEMENT
#            plt.plot( (x1,x2) , (y1,y2) ,color=col)
#
#    # DRAW Path
#    
#    for path_pts in path_lst:
#        # CREATE A TUPLE WITH THREE RANDOM NUMBERS ( USED FOR RGM COLORING)
#        colors = np.random.rand(3,)
#        
#        # ITERATE THROUGH THE LIST OF POINTS
#        for i in range( len(path_pts) - 1 ):
#    
#            # SELECT i ELEMENT FROM THE LIST
#            x1 = path_pts[i][0]
#            y1 = path_pts[i][1]
#    
#            # SELECT i+1 ELEMENT FROM THE LIST
#            x2 = path_pts[i+1][0]
#            y2 = path_pts[i+1][1]  
#    
#            # IF i ELEMENT IS IN THE ORIGIN, CHANGE COLORS
#            # THIS HELPS IDENTIFY NEW PATHS FROM THE DRONE PROJECT
#            if ( (x1==path_pts[0][0] and y1==path_pts[0][1])):
#               
#                # CREATE A TUPLE WITH THREE RANDOM NUMBERS ( USED FOR RGM COLORING)
#                colors = np.random.rand(3,)
#          
#            # DRAW A LINE FROM i ELEMENT TO i+1 ELEMENT
#            plt.plot( (x1,x2) , (y1,y2) , c = colors , linewidth = 1, alpha = 0.7 )
#
#    plt.gca().set_aspect('equal',adjustable='box')
#
#
#    plt.savefig('photos\\dronePathPentagon.png')



































#voronoiRegionCreation()
    
field_paths()