
from Triangle import Triangle
from Drone import Drone
from Drone_Path import Drone_Path
from Draw import Draw
from Transformation import Transformation 
from Field import Field
from Utilities import dist
from minCharge2_LUIS import linear_program

import numpy as np 


#################### INITIALS ####################
field = Field()
Canvas = Draw()


### INITIALIZE DRONE PROPERTIES ###

rad = 1
mxDist = 50 # MUST BE ABLE TO REACH A VERTEX AND RETURN TO CHARGING STATION
drone = Drone(radius=rad, max_distance = mxDist)



#################### FIELD MATRIX ####################
# CREATE A BINARY MATRIX THAT REPRESENTS A FIELD 

field_boundary =  [  (30,25), (30,50),(60,70), (80,70),(110,50), (110,25),  (80,5)  ]
matrix, xmin,xmax,ymin,ymax,nx, ny = field.create_matrix_field(poly = field_boundary ,step=1)


#################### LOCATING CHARGING STATIONS ####################
# USE LINEAR PROGRAMMING TO OPTIMIZE THE LOCATION OF THE CHARGING STATIONS IN A FIELD

half_distance  = np.floor(drone.MAX_DISTANCE / 2.0 )
numberStations = 50
max_solutions = 5
start_point = np.array([50, 50])

CS = linear_program( binMatrix = matrix, xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax,nx = nx, ny = ny, 
                     ns = numberStations , rad = half_distance , solMax = max_solutions, start = start_point)

print(CS)
#################### SPLIT POLYGONS INTO A LIST OF TRIANGLES ####################
# EACH CHARGING STATION HAS A POLYGON FIELD, WHICH WILL BE SPLIT INTO TRIANGLES, 
# WHERE THE CHARGING STATION IS A VERTEX AND THE BOUNDARIES ARE THE OTHER VERTICES

sites = [ (x,y) for x,y in zip( CS[0][:], CS[1][:] ) ]

vononili_polys = field.create_voronoi_polygons(site=sites, boundary=field_boundary)

#################### FIND PATH FOR A GIVEN TRIANGLE ####################

path_lst = []
N = len(vononili_polys)
i = 0

for vononili_poly in vononili_polys:

    print(vononili_poly[0])
    print(vononili_poly[1])

    # CREATE TRIANGLES FROM THE POLYGON, STORE AS LIST
    triangle_lst = field.create_triangle(poly = vononili_poly[0] , vertex = vononili_poly[1] )

    # LOOP THROUGH A LIST OF TRIANGLES, FIND PATH THAT COVERS THE AREA OF EACH
    for triangle in triangle_lst:       

        ### LINEAR TRANSFORMATIONS ###
        transform =  Transformation()
        trans_triangle = transform.transform_triangle(triangle)

        ### ALGORITHM ###

        DP = Drone_Path(trans_triangle , drone)
        path = DP.algorithm()
        trans_path = transform.transform_path(path) # TRANSFORM PATH TO FIT ORIGINAL SHAPE

        # SET DRONE POSITION TO [0,0]
        drone.curPoint = np.array([0,0])
        # RESET CURMAX DISTANCE TO DRONE MAX DISTANCE
        drone.curMax_distance = drone.MAX_DISTANCE

        # ADD PATH TAKEN TO THE PATH LIST 
        path_lst.append(trans_path)



        #Canvas.boundary(triangle.get_all_points())


    # HERE, WE WILL ADD THE DISTANCE FROM ONE CHARGING STATION TO ANOTHER
    if(not(i==0)):

        CS_to_CS = [ vononili_polys[i-1][1] ,vononili_polys[i][1] ]
        drone.total_distance_travel += dist(CS_to_CS[0],CS_to_CS[1])
        #path_lst.append(CS_to_CS)

        if( i == N-1):
            CS_to_CS = [ vononili_polys[i][1] ,vononili_polys[0][1] ]
            drone.total_distance_travel += dist(CS_to_CS[0],CS_to_CS[1])
            #path_lst.append(CS_to_CS)
        
        
    i+= 1

print(drone)



#################### DRAW PLOTS ####################
# DRAW THE PATH THE DRONE TOOK
# LOOP THROUGH ALL THE PATHS AND DRAW THEM ON THE PLOT

# DRAW SHAPE BOUNDARY
Canvas.boundary(field_boundary)

for vononili_poly in vononili_polys:
    #print(vononili_poly)
    Canvas.boundary(vononili_poly[0],col='b')
    #pass


for path in path_lst:
    # DRAW PATH 
    #Canvas.path(path)
    pass
    


Canvas.draw_sites(sites)

# SHOW PLOT
Canvas.show_plot()






