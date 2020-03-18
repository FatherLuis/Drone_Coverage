
from Triangle import Triangle
from Drone import Drone
from Drone_Path import Drone_Path
from Draw import Draw
from Transformation import Transformation 

import numpy as np 


### INITIALIZE ###

rad = 2
mxDist = 250 # MUST BE ABLE TO REACH A VERTEX AND RETURN TO CHARGING STATION

# Given Triangle 
a = np.array( (0,0) ) # CHARGING STATION
b = np.array( (0,100) ) # LONGEST SIDE
c = np.array( (60,80) ) # OTHER SIDE


# a = np.array( (-40,-40) ) # CHARGING STATION
# b = np.array( (-80,-100) ) # Side
# c = np.array( (-100,-60)  ) # SIDE


orin_shape = Triangle(a,b,c)


### LINEAR TRANSFORMATIONS ###

transform =  Transformation()
trans_points = transform.transform_triangle_prime(a,b,c)

trans_shape =  Triangle(*trans_points)


### ALGORITHM ###

drone = Drone(radius=rad, max_distance = mxDist)

DP = Drone_Path(trans_shape , drone)
path = DP.algorithm()

print(drone)

### DRAW PLOTS ###
Canvas = Draw()

Canvas.boundary(orin_shape.get_all_points())
trans_path = transform.transform_path(path)
Canvas.path(trans_path)

Canvas.show_plot()






