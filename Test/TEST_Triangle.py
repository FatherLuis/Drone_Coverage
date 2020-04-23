from Triangle import Triangle
from Drone import Drone
from Drone_Path import Drone_Path
from Draw import Draw
from Transformation import Transformation 
from Field import Field

import numpy as np 


#################### INITIALS ####################
field = Field()
Canvas = Draw()


### INITIALIZE DRONE PROPERTIES ###

rad = 1
mxDist = 200 # MUST BE ABLE TO REACH A VERTEX AND RETURN TO CHARGING STATION
drone = Drone(radius=rad, max_distance = mxDist)

#################### FIND PATH FOR A GIVEN TRIANGLE ####################

path_lst = []

triangle_boundary = [ (45,40),(30,27),(30,50)]
triangle = Triangle(*triangle_boundary)

        
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
path_taken = trans_path
               

print(drone)



#################### DRAW PLOTS ####################
# DRAW THE PATH THE DRONE TOOK
# LOOP THROUGH ALL THE PATHS AND DRAW THEM ON THE PLOT

# DRAW SHAPE BOUNDARY
Canvas.boundary(triangle_boundary)

Canvas.path(path_taken)

# SHOW PLOT
Canvas.show_plot()
