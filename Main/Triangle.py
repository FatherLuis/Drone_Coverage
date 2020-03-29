import numpy as np 


########################################
# Class name: Triangle()
# Class Author: Luis E. Vargas Tamayo
# Purpose of the class: Create a Triangle object that contains all the necessary information of a triangle, given three points
# Date: 3/2/2020
# List of changes with dates: none
########################################
class Triangle:

    ##############################################
    # Method Name: __init__
    # Purpose: Class Constructor
    # Parameter: None
    # Method used: None
    # Return Value: None
    # Date:  3/2/2020
    ##############################################
    def __init__(self,A_p,B_p,C_p):
        self.A = np.array(A_p)
        self.B = np.array(B_p)
        self.C = np.array(C_p)

        self.AB_dist = 0
        self.BC_dist = 0
        self.AC_dist = 0
        self.calculate_distance()

        self.A_angle = 0
        self.B_angle = 0
        self.C_angle = 0
        self.find_angles()

        self.centroid = 0
        self.calculate_centroid()

    ##############################################
    # Method Name: find_angles()
    # Purpose: Using the Law of Cosine, It finds the angles of the triangle
    # Parameter: None
    # Method used: None
    # Return Value: None
    # Date:  3/2/2020
    ##############################################
    def find_angles(self):
        
        # ANGLES ARE IN RADIANS
        # THIS IS THE FORMULA FROM LAWS OF COSINE
        self.B_angle = np.arccos( (self.AB_dist**2 + self.BC_dist**2 - self.AC_dist**2) / (2*self.AB_dist*self.BC_dist) )
        self.C_angle = np.arccos( (self.BC_dist**2 + self.AC_dist**2 - self.AB_dist**2) / (2*self.BC_dist*self.AC_dist) )
        self.A_angle = np.arccos( (self.AC_dist**2 + self.AB_dist**2 - self.BC_dist**2) / (2*self.AC_dist*self.AB_dist) )
        

    ##############################################
    # Method Name: calculate_distance()
    # Purpose: Using the Law of Cosine, it finds the lenghts of the sides of the triangle
    # Parameter: None
    # Method used: None
    # Return Value: None
    # Date:  3/2/2020
    ##############################################
    def calculate_distance(self):

        def euler_distance(p1,p2):
            return np.sqrt( (p2[1]-p1[1])**2 +(p2[0]-p1[0])**2)
        
        self.AB_dist = euler_distance(self.A, self.B)
        self.BC_dist = euler_distance(self.B, self.C)
        self.AC_dist = euler_distance(self.A, self.C)

    ##############################################
    # Method Name: calculate_centroid()
    # Purpose: Find the centroid of the triangle
    # Parameter: None
    # Method used: None
    # Return Value: tuple (x,y)
    # Date:  3/2/2020
    ##############################################
    def calculate_centroid(self):
        #x = (self.A[0] + self.B[0] + self.C[0])  / 3.0
        #y = (self.A[1] + self.B[1] + self.C[1])  / 3.0

        self.centroid =  ( self.A + self.B + self.C ) / 3.0

    ##############################################
    # Method Name: calculate_area()
    # Purpose: Calculate the Area of a Triangle using 0.5BH
    # Parameter: None
    # Method used: None
    # Return Value: Float
    # Date:  3/2/2020
    ##############################################
    def calculate_area(self):
        return ((self.B[1] - self.A[1]) * (self.C[0] - self.A[0] )) / 0.5

    ##############################################
    # Method Name: get_all_points()
    # Purpose: return a list of points ( the verteces of the triangle)
    # Parameter: None
    # Method used: None
    # Return Value: list of tuples (x,y)
    # Date:  3/2/2020
    ##############################################
    def get_all_points(self):
        return self.A,self.B,self.C

    ##############################################
    # Method Name: set_A()
    # Purpose: Set a new vertex A and recalculate the sides of the triangle
    # Parameter: None
    # Method used: None
    # Return Value: None
    # Date:  3/2/2020
    ##############################################
    def set_A(self,new_a):
        self.A = new_a
        self.calculate_distance()
        self.calculate_centroid()

    ##############################################
    # Method Name: set_B()
    # Purpose: Set a new vertex B and recalculate the sides of the triangle
    # Parameter: None
    # Method used: None
    # Return Value: None
    # Date:  3/2/2020
    ##############################################
    def set_B(self,new_b):
        self.B = new_b
        self.calculate_distance()
        self.calculate_centroid()

    ##############################################
    # Method Name: set_C()
    # Purpose: Set a new vertex C and recalculate the sides of the triangle
    # Parameter: None
    # Method used: None
    # Return Value: None
    # Date:  3/2/2020
    ##############################################
    def set_C(self,new_c):
        self.C = new_c
        self.calculate_distance()
        self.calculate_centroid()

    ##############################################
    # Method Name: copy()
    # Purpose: return a copy of the object
    # Parameter: None
    # Method used: None
    # Return Value: Triangle object
    # Date:  3/2/2020
    ##############################################
    def copy(self):
        return Triangle(self.A,self.B,self.C)

    ##############################################
    # Method Name: __str__()
    # Purpose: overrides the default print() method used on this object. When print() is used, information of the triangle is printed
    # Parameter: None
    # Method used: None
    # Return Value: None
    # Date:  3/2/2020
    ##############################################
    def __str__(self):
        str_points = "Points: {},{},{}".format(self.A,self.B,self.C)
        str_angles = "Angles: {},{},{}".format(self.A_angle,self.B_angle,self.C_angle)
        str_sides = "Sides: {},{},{}".format(self.AB_dist,self.BC_dist,self.AC_dist)

        return "{}\n{}\n{}\n".format(str_points,str_angles,str_sides)

