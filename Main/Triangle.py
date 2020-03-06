import math

class Triangle:

    def __init__(self,A_p,B_p,C_p):
        self.A = A_p
        self.B = B_p
        self.C = C_p

        self.AB_dist = 0
        self.BC_dist = 0
        self.AC_dist = 0
        self.calculate_distance()

        self.A_angle,self.B_angle,self.C_angle = self.find_angles(self.A,self.B,self.C)


    def find_angles(self,A,B,C):
        
        # ANGLES ARE IN RADIANS
        # THIS IS THE FORMULA FROM LAWS OF COSINE
        B_theta = math.acos( (self.AB_dist**2 + self.BC_dist**2 - self.AC_dist**2) / (2*self.AB_dist*self.BC_dist) )
        C_theta = math.acos( (self.BC_dist**2 + self.AC_dist**2 - self.AB_dist**2) / (2*self.BC_dist*self.AC_dist) )
        A_theta = math.acos( (self.AC_dist**2 + self.AB_dist**2 - self.BC_dist**2) / (2*self.AC_dist*self.AB_dist) )
        
        return A_theta,B_theta,C_theta
        
    def calculate_distance(self):

        def euler_distance(p1,p2):
            return math.sqrt( (p2[1]-p1[1])**2 +(p2[0]-p1[0])**2)
        
        self.AB_dist = euler_distance(self.A, self.B)
        self.BC_dist = euler_distance(self.B, self.C)
        self.AC_dist = euler_distance(self.A, self.C)
            
               

    def get_all_points(self):
        return self.A,self.B,self.C

    def set_A(self,new_a):
        self.A = new_a
        self.calculate_distance()

    def set_B(self,new_b):
        self.B = new_b
        self.calculate_distance()

    def set_C(self,new_c):
        self.C = new_c
        self.calculate_distance()



    def __str__(self):
        str_points = "Points: {},{},{}".format(self.A,self.B,self.C)
        str_angles = "Angles: {},{},{}".format(self.A_angle,self.B_angle,self.C_angle)
        str_sides = "Sides: {},{},{}".format(self.AB_dist,self.BC_dist,self.AC_dist)

        return "{}\n{}\n{}\n".format(str_points,str_angles,str_sides)

