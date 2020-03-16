import numpy as np
import math 

########################################
# Class name: Transformation
# Class Author: Luis E. Vargas Tamayo
# Purpose of the class: Create a class that will perform linear transformations on Triangles and points
# Date: 3/13/2020
# List of changes with dates: none
########################################
class Transformation:

    ##############################################
    # Method Name: __init__
    # Purpose: Class Constructor
    # Parameter: None
    # Method used: None
    # Return Value: None
    # Date:  3/13/2020
    ##############################################
    def __init__(self):

        self.matrix = None 
        self.transition = None 
        self.negX = False 

    ##############################################
    # Method Name: transform_triangle_prime
    # Purpose: Transform any given triangle to the given assumption described inside the method
    # Parameter: Three points (x,y) form
    # Method used: None
    # Return Value: Three points (x,y) based on the assumption described
    # Date:  3/13/2020
    ##############################################
    def transform_triangle_prime(self,A,B,C):
        # GIVEN ASSUMPTIONS:
        # 'A prime' IS THE CHARGING STATION AND IS LOCATED AT THE ORIGIN 
        # 'B prime' IS THE LONGEST DISTANCE AND IS LOCATED ON THE Y-AXIS, X=0
        # 'C prime' IS THE OTHER VERTEX  
        # TRIANGLE IS IN THE FIRST QUADRANT 
        
        # GET THE EUCLEDIAN DISTANCE FROM TWO POINTS
        def dist(p1,p2):
            return math.sqrt( (p2[1]-p1[1])**2 +(p2[0]-p1[0])**2)

        # PERFORM A LINEAR TRANSFORMATION WITH A GIVEN MATRIX
        def linear_trans(P):
            return np.dot(self.matrix , np.transpose(P))
        
        # A WILL BE MY TRANSITION... SINCE I WANT A TO BE IN THE ORIGIN
        self.transition = A

        # GET THE DISTANCE OF A-B AND A-C
        # THIS WILL HELP DETERMINE WHICH ON IS FARTHER
        dist_AB = dist(A,B) 
        dist_AC = dist(A,C)

        # IF AB IS FARTHER THAN AC
        if (  dist_AB >= dist_AC  ):

            # B WILL MOVE TO ( 0, dist(A,B) )
            # THESE ARE THE TRANSFORMATION ELEMENTS NEEDED FOR THE MATRIX
            sin = ( B[0] - A[0] ) / dist_AB
            cos = ( B[1] - A[1] ) / dist_AB

        else:

            # C WILL MOVE TO ( 0, dist(A,B) )
            # THESE ARE THE TRANSFORMATION ELEMENTS NEEDED FOR THE MATRIX
            sin = ( C[0] - A[0] ) / dist_AC
            cos = ( C[1] - A[1] ) / dist_AC

        # CREATE A TRANSFORMATION MATRIX
        # WILL BE USED IN THE LINEAR TRANSFORMATION METHOD
        self.matrix = np.array( [ [ cos , -sin ] , [ sin , cos] ] )

        # GET THE TRANSFORMED POINTS
        A_prime = linear_trans(A-A) 
        B_prime = linear_trans(B-A)
        C_prime = linear_trans(C-A)


        # WE WANT TO REASSURE THAT THE TRIANGLE WILL END IN THE FIRST QUADRAINT
        # SINCE WE KNOW THAT A WILL END IN THE ORIGIN AND THAT B/C WILL END
        # ON THE Y-AXIS, THEN HE HAVE TO ASSURE THAT B/C END IN THE FIRST QUADRANT
        if( B_prime[0] < -0.001 ):
            # WE APPLIED A NEGATIVE ON THE X 
            self.negX = True
            B_prime[0] = -B_prime[0]

        elif( C_prime[0] < -0.001 ):
            # WE APPLIED A NEGATIVE ON THE X 
            self.negX = True
            C_prime[0] = -C_prime[0] 

        # RETURN THE TRANSFORMED POINTS
        return A_prime,B_prime,C_prime


    ##############################################
    # Method Name: transform_triangle_prime
    # Purpose: Detransform points to their original position ( given the transformation matrix, transition, and negative x)
    # Parameter: A list of points (x,y)
    # Method used: linear_trans() , found inside this method
    # Return Value: Three points (x,y) based on the assumption described
    # Date:  3/13/2020
    ##############################################
    def transform_path(self,path_points):
        
        # CREATE A LINEAR TRANSFORMATION THAT MOVES A GIVEN POINT TO A NEW POSITION
        def linear_trans(P):
            # FOR ROTATION TRANSFORMATIONS, THE INVERSE OF THE MATRIX PLUS ANY TRANSLATION
            # IS THE KEY TO UNDO THE TRANSFORMATION
            return np.dot(np.transpose(self.matrix) , np.transpose(P)) + self.transition

        # EMPTY LIST TO FILL WITH TRANSFORMED POINTS
        new_path = []

        # ITERATE THROUGH THE LIST OF POINTS
        for p in path_points:

            # CHECK IF WE HAD ADDED A NEGATIVE TO THE X IN THE TRANSFORMATION
            if(self.negX):
                # MULTIPLY X BY A NEGATIVE
                p[0] = -p[0]

            # ADD TO THE LIST THE TRANSFORM POINT
            new_path.append(linear_trans(p))

        # RETURN A LIST OF TRANSFORMED POINTS
        return new_path






        








