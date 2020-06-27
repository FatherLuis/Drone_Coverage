
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
import os.path





def run_program(drone, CS_radius , shape ,candidate, showPlot = True):
    
    outpath = './photos/'
    
    
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
    start_point = np.array([0, 0])

    CS = linear_program( binMatrix = matrix, xmin=xmin, xmax=xmax,ymin=ymin,ymax=ymax,nx = nx, ny = ny, step = step,
                        ns = numberStations , rad = half_distance , solMax = max_solutions, start = start_point)




    # #################### SPLIT POLYGONS INTO A LIST OF TRIANGLES ####################
    # # EACH CHARGING STATION HAS A POLYGON FIELD, WHICH WILL BE SPLIT INTO TRIANGLES, 
    # # WHERE THE CHARGING STATION IS A VERTEX AND THE BOUNDARIES ARE THE OTHER VERTICES

    sites = [ (x,y) for x,y in zip( CS[0][:], CS[1][:] ) ]
    
    vononili_lst = field.create_voronoi_polygons(site=sites, boundary=field_boundary)




    ############################################      
    from scipy.spatial import voronoi_plot_2d
    from scipy.spatial import Voronoi
    
    
    ### Create a box to bound
    
    xVal = np.array([x[0] for x in field_boundary])
    yVal = np.array([y[1] for y in field_boundary])
    
    xmin = np.min(xVal) 
    xmax = np.max(xVal) 
    ymin = np.min(yVal) 
    ymax = np.max(yVal) 
    
    diffx = xmax - xmin
    diffy = ymax - ymin
    
    xmin -= 2*diffx
    xmax += 2*diffx 
    ymin -= 2*diffy  
    ymax += 2*diffy  
    

    vor = Voronoi(sites)    
    
    
    # CREATE A FIGURE OBJECT
    fig1 = plt.figure(1)
    
    # CREATE A SUBPLOT IN THE FIGURE 
    ax1 = fig1.add_subplot(111)  
    ax1.set_xlabel('x-axis: kilometers (km)')
    ax1.set_ylabel('y-axis: kilometers (km)')

    
    voronoi_plot_2d(vor, ax1, show_vertices = False)
    dr = Draw(ax1)
    fig1.savefig(os.path.join(outpath,"undefinedVoronoiRegion.png"))


   #######################################
    
        
    
    
    box = [ [xmin,ymin] , [xmin,ymax], [xmax,ymax] , [xmax,ymin] ]

    vor = Voronoi(sites + box)  

    # CREATE A FIGURE OBJECT
    fig2 = plt.figure(2)
    
    # CREATE A SUBPLOT IN THE FIGURE 
    ax2 = fig2.add_subplot(111)
    ax2.set_xlabel('x-axis: kilometers (km)')
    ax2.set_ylabel('y-axis: kilometers (km)')
    voronoi_plot_2d(vor, ax2,show_vertices = False)
    dr = Draw(ax2)
    dr.boundary(field_boundary,lines = 'dotted')
    dr.draw_sites(box,col = 'r',mark = '*')
    fig2.savefig(os.path.join(outpath,"boundedVoronoiRegion.png"))
   
    #######################################





    #######################################
    #######################################
    # CREATE A FIGURE OBJECT
    fig3 = plt.figure(3)
    
    # CREATE A SUBPLOT IN THE FIGURE 
    ax3 = fig3.add_subplot(111)
    ax3.set_xlabel('x-axis: kilometers (km)')
    ax3.set_ylabel('y-axis: kilometers (km)')
    
    draw3 = Draw(ax3)
    draw3.draw_sites(sites)
    draw3.boundary(field_boundary)
    
    for v in vononili_lst:
        draw3.boundary(v[0])
    
    fig3.savefig(os.path.join(outpath,"shapeBoundVoronoiRegion.png"))

    #######################################
    #######################################





   
    # # ordered
    vononili_polys,entryExitLst, vertices = tour(start_point, drone.MAX_DISTANCE , vononili_lst)
    

    #######################################
    #######################################
    # CREATE A FIGURE OBJECT
    fig4 = plt.figure(4)
    
    # CREATE A SUBPLOT IN THE FIGURE 
    ax4 = fig4.add_subplot(111)    
    ax4.set_xlabel('x-axis: kilometers (km)')
    ax4.set_ylabel('y-axis: kilometers (km)')
    
    draw4 = Draw(ax4)
    draw4.draw_sites(sites)
    draw4.boundary(field_boundary)
    
    for v in vononili_polys:
        draw4.boundary(v[0])
        
    draw4.draw_sites_path(vertices)
    
    fig4.savefig(os.path.join(outpath,"regionTour.png"))

    
    
    #######################################
    #######################################



    # #################### FIND PATH FOR A GIVEN TRIANGLE ####################

    path_lst = []
    
    N = len(vononili_polys)
    
    k = 0




    #######################################
    #######################################
    # CREATE A FIGURE OBJECT
    fig5 = plt.figure(5)
    
    # CREATE A SUBPLOT IN THE FIGURE 
    ax5 = fig5.add_subplot(111)    
    ax5.set_xlabel('x-axis: kilometers (km)')
    ax5.set_ylabel('y-axis: kilometers (km)')
    
    draw5 = Draw(ax5)
     
    #######################################
    #######################################
        
    for i,vononili_poly in enumerate(vononili_polys):
        
        #print('\n----- Voronoi ',i,' ------')

        
        # CREATE TRIANGLES FROM THE POLYGON, STORE AS LIST
        triangle_lst = field.create_triangle(poly = vononili_poly[0] , vertex = vononili_poly[1] ,)

        # LOOP THROUGH A LIST OF TRIANGLES, FIND PATH THAT COVERS THE AREA OF EACH

        for j,triangle in enumerate(triangle_lst):  
            
            draw5.boundary(triangle.get_all_points())

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
    
    for vononili_poly in vononili_polys:
        draw5.boundary(vononili_poly[0],col='b',lines='dotted')
    draw5.draw_sites(sites)  
    fig5.savefig(os.path.join(outpath,"triangularRegions.png"))


    if showPlot :
        #################### DRAW PLOTS ####################
        
        
    
        # CREATE A FIGURE OBJECT
        fig6 = plt.figure(6)
        
        # CREATE A SUBPLOT IN THE FIGURE 
        ax6 = fig6.add_subplot(111)
        ax6.set_xlabel('x-axis: kilometers (km)')
        ax6.set_ylabel('y-axis: kilometers (km)')
        
        
        Canvas = Draw(ax6)
    
        # DRAW SHAPE BOUNDARY
        Canvas.boundary(field_boundary)
    
        for vononili_poly in vononili_polys:
            #print(vononili_poly)
            Canvas.boundary(vononili_poly[0],col='b')
            pass
    
        # DRAW THE PATH THE DRONE TOOK
        # LOOP THROUGH ALL THE PATHS AND DRAW THEM ON THE PLOT
        for path in path_lst:
            # DRAW PATH 
            Canvas.path(path)
            pass
    
        Canvas.draw_sites(sites)
        
        fig6.savefig(os.path.join(outpath,"dronePathPentagon.png"))

    
        # SHOW PLOT
        #plt.gca().set_aspect('equal',adjustable='box')
        plt.plot()


    #   'num_Charging_Station','Total_Time','Total_Distance_Travel'

    return len(sites),drone.total_distance_travel





if __name__ == '__main__':

    # IF THIS FILE IS RUN, THE FOLLOWING CODE WILL BE READ
    
    try:
        
        
         ### INITIALIZE DRONE PROPERTIES ###

        drone = Drone(radius=0.025, max_distance = 8)       
    
        #field_boundary =  [ (0,0) , (0,7) , (7,7) , (7,0)]
        #field_boundary = [ (0,0),(2.28,0),(3.88,1.61),(3.88,3.88),(2.28,5.49),(0,5.49),(-1.61,3.88),(-1.61,1.61) ]

        field_boundary =  [ [0,0] , [0,3] , [4,5] , [8,3] , [8,0]]

        
        CS_radius = 2.5
        
    
        lst = run_program(drone, CS_radius , field_boundary, 50 )
        
        print('')
        print('nCS:',lst[0])
        print('Time:',lst[1]/25)
        print('Travel',lst[1])
        
    except:
        
        print(traceback.format_exc())
