from Triangle import Triangle
from Drone import Drone
from Drone_Path import Drone_Path
from Draw import Draw
from Transformation import Transformation 
from Field import Field
from Utilities import dist
from Travel import traveling
from minCharge_LUIS import linear_program,tour

import numpy as np 


#################### INITIALS ####################
field = Field()
Canvas = Draw()


### INITIALIZE DRONE PROPERTIES ###

rad = 0.25
mxDist = 100 # MUST BE ABLE TO REACH A VERTEX AND RETURN TO CHARGING STATION
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
        trans_triangle, entryExit = transform.transform_triangle(triangle,entryExitLst[i])


        ### ALGORITHM ###

        DP = Drone_Path(trans_triangle , drone , entryExit)
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
    Canvas.path(path)
    pass

Canvas.draw_sites_path(site_path)

Canvas.draw_sites(sites)

# SHOW PLOT
Canvas.show_plot()