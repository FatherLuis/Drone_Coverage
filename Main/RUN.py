
from Triangle import Triangle
from Drone import Drone
from Drone_Path import Drone_Path
from Draw import Draw
from Transformation import Transformation 
from Field import Field
from Utilities import dist
from minCharge_LUIS import linear_program,tour
from Travel import traveling

import numpy as np 


#################### INITIALS ####################
field = Field()
Canvas = Draw()


### INITIALIZE DRONE PROPERTIES ###

rad = 0.5
mxDist = 80   # MUST BE ABLE TO REACH A VERTEX AND RETURN TO CHARGING STATION
drone = Drone(radius=rad, max_distance = mxDist)



#################### FIELD MATRIX ####################
# CREATE A BINARY MATRIX THAT REPRESENTS A FIELD 

field_boundary =  [  (0,0) , (0,60) , (60,60), (60,0) ]

step = 0.7

matrix, xmin, xmax, ymin, ymax, nx, ny = field.create_matrix_field(poly = field_boundary ,step = step)


#################### LOCATING CHARGING STATIONS ####################
# USE LINEAR PROGRAMMING TO OPTIMIZE THE LOCATION OF THE CHARGING STATIONS IN A FIELD

half_distance  = np.floor(drone.MAX_DISTANCE / 2.0 ) * 0.6
numberStations = 50
max_solutions = 5
start_point = np.array([0, 0])

CS = linear_program( binMatrix = matrix, xmin=xmin, xmax=xmax,ymin=ymin,ymax=ymax,nx = nx, ny = ny, step = step,
                     ns = numberStations , rad = half_distance , solMax = max_solutions, start = start_point)



#################### SPLIT POLYGONS INTO A LIST OF TRIANGLES ####################
# EACH CHARGING STATION HAS A POLYGON FIELD, WHICH WILL BE SPLIT INTO TRIANGLES, 
# WHERE THE CHARGING STATION IS A VERTEX AND THE BOUNDARIES ARE THE OTHER VERTICES

sites = [ (x,y) for x,y in zip( CS[0][:], CS[1][:] ) ]

vononili_lst = field.create_voronoi_polygons(site=sites, boundary=field_boundary)

# ordered
vononili_polys = tour(start_point,rad , vononili_lst)

vertices , entryExitLst = traveling(vononili_polys)



#################### FIND PATH FOR A GIVEN TRIANGLE ####################

path_lst = []
site_path = []
N = len(vononili_polys)
i = 0

for vononili_poly in vononili_polys:

    print('--------------------')
    
    # CREATE TRIANGLES FROM THE POLYGON, STORE AS LIST
    triangle_lst = field.create_triangle(poly = vononili_poly[0] , vertex = vononili_poly[1] ,)

    # LOOP THROUGH A LIST OF TRIANGLES, FIND PATH THAT COVERS THE AREA OF EACH

    print(vononili_poly[1])
    print(entryExitLst[i])
    for triangle in triangle_lst:    

    

        ### LINEAR TRANSFORMATIONS ###
        transform =  Transformation()
        trans_triangle, entryExit = transform.transform_triangle(triangle,entryExitLst[i])


        print(triangle)
        print('')
        print(trans_triangle)

        ### ALGORITHM ###

        DP = Drone_Path(trans_triangle , drone , entryExit)
        path = DP.algorithm(transform.BC_switch)
        trans_path = transform.transform_path(path) # TRANSFORM PATH TO FIT ORIGINAL SHAPE

        # SET DRONE POSITION TO [0,0]
        drone.curPoint = np.array([0,0])
        # RESET CURMAX DISTANCE TO DRONE MAX DISTANCE
        drone.curMax_distance = drone.MAX_DISTANCE

        # ADD PATH TAKEN TO THE PATH LIST 
        path_lst.append(trans_path)

        Canvas.boundary(triangle.get_all_points())

    # HERE, WE WILL ADD THE DISTANCE FROM ONE CHARGING STATION TO ANOTHER

    
    if( i < N-1):

        if(i == 0):
            a = vononili_polys[i][1]
        else:
            a = site_path[-1]
            
        b = vertices[i]
        c = vononili_polys[i+1][1]


        site_path.append(b)
        site_path.append(c)

        drone.total_distance_travel += dist(a,b) + dist(b,c)

    else:

        a = site_path[-1]
        b = vertices[i]
        c = vononili_polys[0][1]

        site_path.append(b)
        site_path.append(c)

        drone.total_distance_travel += dist(a,b) + dist(b,c)        


        
        
    i+= 1

print('------------- Drone -------------')
print(drone)
print('---------------------------------')



#################### DRAW PLOTS ####################
# DRAW THE PATH THE DRONE TOOK
# LOOP THROUGH ALL THE PATHS AND DRAW THEM ON THE PLOT

# DRAW SHAPE BOUNDARY
Canvas.boundary(field_boundary)

for vononili_poly in vononili_polys:
    #print(vononili_poly)
    Canvas.boundary(vononili_poly[0],col='b')
    pass


for path in path_lst:
    # DRAW PATH 
    Canvas.path(path)
    pass

Canvas.draw_sites(sites)



Canvas.draw_sites_path(site_path)

# SHOW PLOT
Canvas.show_plot()






