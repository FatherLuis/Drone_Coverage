
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



#################### FIELD MATRIX ####################
# CREATE A BINARY MATRIX THAT REPRESENTS A FIELD 

field_boundary = [ (60,5), (45,15), (30,25), (30,50), (45,60), (60,70), (80,70), (95,60), (110,50), (110,25), (95,15), (80,5)  ]

#matrix = field.create_matrix_field( step = 0.1, poly = field_boundary )[0]





#################### LOCATING CHARGING STATIONS ####################
# USE LINEAR PROGRAMMING TO OPTIMIZE THE LOCATION OF THE CHARGING STATIONS IN A FIELD








#################### SPLIT POLYGONS INTO A LIST OF TRIANGLES ####################
# EACH CHARGING STATION HAS A POLYGON FIELD, WHICH WILL BE SPLIT INTO TRIANGLES, 
# WHERE THE CHARGING STATION IS A VERTEX AND THE BOUNDARIES ARE THE OTHER VERTICES





vononili_poly1 = [ [ (45,15), (30,25), (30,50), (45,60), (60,50), (60,30)   ] , ( 45,40 ) ]
vononili_poly2 = [ [ (45,60), (60,70), (80,70), (95,60), (80,50), (60,50)  ] ,  ( 70,60 ) ]
vononili_poly3 = [ [ (95,60), (110,50), (110,25), (95,15), (80,30), (80,50)  ] ,( 95,40 ) ]
vononili_poly4 = [ [ (45,15), (60,30), (80,30), (95,15), (80,5), (60,5)  ] ,  ( 70,15 ) ]
vononili_poly5 = [ [ (60,30), (60,50), (80,50), (80,30)  ] ,  ( 70,40 ) ]

vononili_polys = [ vononili_poly1 , vononili_poly2 , vononili_poly3 , vononili_poly4 , vononili_poly5    ]



#################### FIND PATH FOR A GIVEN TRIANGLE ####################

path_lst = []
N = len(vononili_polys)
i = 0
for vononili_poly in vononili_polys:

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


    # HERE, WE WILL ADD THE DISTANCE FROM ONE CHARGING STATION TO ANOTHER
    if(not(i==0)):

        CS_to_CS = [ vononili_polys[i-1][1] ,vononili_polys[i][1] ]
        drone.add_distance(CS_to_CS[0],CS_to_CS[1])
        path_lst.append(CS_to_CS)

        if( i == N-1):
            CS_to_CS = [ vononili_polys[i][1] ,vononili_polys[0][1] ]
            drone.add_distance(CS_to_CS[0],CS_to_CS[1])
            path_lst.append(CS_to_CS)
        
        
    i+= 1

print(drone)



#################### DRAW PLOTS ####################
# DRAW THE PATH THE DRONE TOOK
# LOOP THROUGH ALL THE PATHS AND DRAW THEM ON THE PLOT

# DRAW SHAPE BOUNDARY
Canvas.boundary(field_boundary)

for path in path_lst:
    # DRAW PATH 
    Canvas.path(path)


# SHOW PLOT
Canvas.show_plot()






