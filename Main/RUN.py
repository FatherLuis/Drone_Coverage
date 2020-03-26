
from Triangle import Triangle
from Drone import Drone
from Drone_Path import Drone_Path
from Draw import Draw
from Transformation import Transformation 
from Field import Field

import numpy as np 



########## FIELD MATRIX ##########
# CREATE A BINARY MATRIX THAT REPRESENTS A FIELD 

field_boundary = [ (0,2), (4,2), (4,6),(8,6),(8,2),(12,2),(12,10),(0,10)  ]

field = Field( field_boundary )

matrix = field.create_matrix_field(pixel = 200)





########## LOCATING CHARGING STATIONS ##########
# USE LINEAR PROGRAMMING TO OPTIMIZE THE LOCATION OF THE CHARGING STATIONS IN A FIELD







########## SPLIT POLYGONS INTO A LIST OF TRIANGLES ##########
# EACH CHARGING STATION HAS A POLYGON FIELD, WHICH WILL BE SPLIT INTO TRIANGLES, 
# WHERE THE CHARGING STATION IS A VERTEX AND THE BOUNDARIES ARE THE OTHER VERTICES






########## INITIALIZE DRONE PROPERTIES ##########

rad = 2
mxDist = 250 # MUST BE ABLE TO REACH A VERTEX AND RETURN TO CHARGING STATION
drone = Drone(radius=rad, max_distance = mxDist)


########## FIND PATH FOR A GIVEN TRIANGLE ##########
# LOOP THROUGH A LIST OF TRIANGLES, FIND PATH THAT COVERS THE AREA

# Given Triangle 
a = np.array( (0,0) ) # CHARGING STATION
b = np.array( (0,100) ) # LONGEST SIDE
c = np.array( (60,80) ) # OTHER SIDE


orin_shape = Triangle(a,b,c)

### LINEAR TRANSFORMATIONS ###

transform =  Transformation()
trans_points = transform.transform_triangle_prime(a,b,c)

trans_shape =  Triangle(*trans_points)


### ALGORITHM ###

DP = Drone_Path(trans_shape , drone)
path = DP.algorithm()
trans_path = transform.transform_path(path) # TRANSFORM PATH TO FIT ORIGINAL SHAPE

# HAVE AN ARRAY WITH TUPLES, SUCH THAT (TRIANGLE, PATH), CONTINUE LOOPING
# OR HAVE AN ARRAY WITH PATHS, CONTINUE LOOPING


########## DRAW PLOTS ##########
# DRAW THE PATH THE DRONE TOOK
# LOOP THROUGH ALL THE PATHS AND DRAW THEM ON THE PLOT


Canvas = Draw()

# DRAW SHAPE BOUNDARY
Canvas.boundary(orin_shape.get_all_points())

# DRAW PATH 
Canvas.path(trans_path)

# SHOW PLOT
Canvas.show_plot()






