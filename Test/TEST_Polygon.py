from Triangle import Triangle
from Drone import Drone
from Drone_Path import Drone_Path
from Draw import Draw
from Transformation import Transformation 
from Field import Field
from Utilities import dist

import numpy as np 


#################### INITIALS ####################
field = Field()
Canvas = Draw()


### INITIALIZE DRONE PROPERTIES ###

rad = 1
mxDist = 200 # MUST BE ABLE TO REACH A VERTEX AND RETURN TO CHARGING STATION
drone = Drone(radius=rad, max_distance = mxDist)


#################### SPLIT POLYGONS INTO A LIST OF TRIANGLES ####################
# EACH CHARGING STATION HAS A POLYGON FIELD, WHICH WILL BE SPLIT INTO TRIANGLES, 
# WHERE THE CHARGING STATION IS A VERTEX AND THE BOUNDARIES ARE THE OTHER VERTICES

vononili_poly1 = [ [ (45,15), (30,25), (30,50), (45,60), (60,50), (60,30)   ] , ( 45,40 ) ]

#################### FIND PATH FOR A GIVEN TRIANGLE ####################

path_lst = []

triangle_lst = field.create_triangle(poly = vononili_poly1[0] , vertex = vononili_poly1[1] )

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
    

print(drone)



#################### DRAW PLOTS ####################
# DRAW THE PATH THE DRONE TOOK
# LOOP THROUGH ALL THE PATHS AND DRAW THEM ON THE PLOT

# DRAW SHAPE BOUNDARY
Canvas.boundary(vononili_poly1[0])

for path in path_lst:
    # DRAW PATH 
    Canvas.path(path)


# SHOW PLOT
Canvas.show_plot()
