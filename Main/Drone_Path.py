import Triangle
import Drone
import math 

#######################
# GIVEN ASSUMPTIONS:
# 'A' IS THE CHARGING STATION AND IS LOCATED AT THE ORIGIN 
# 'B' IS THE LONGEST DISTANCE AND IS LOCATED ON THE Y-AXIS, X=0
# 'C' IS THE SHORTEST DISTANCE AND IS IN THE FIRST QUADRANT 
# All Angles are acute
#######################
class Drone_Path():


    def __init__(self,triangle,drone):

        self.triangle = triangle
        self.drone = drone
        self.curTriangle = Triangle.Triangle(*triangle.get_all_points()) 
        self.path = [(0,0)]


    def segment_AB(self):
        
        ### Calculate path of Drone ###
        
        #x-y coor from the A vertex
        xi = self.drone.radius
        yi = self.curTriangle.A[1] + (self.drone.radius / math.tan(self.curTriangle.B_angle))

        # x-y coor from the B vertex
        xf = self.drone.radius
        yf = self.curTriangle.B[1] - (self.drone.radius / math.tan(self.curTriangle.B_angle))
        
        ### Calculate A and B primes ###

        #x-y coor from the A vertex
        Ax = self.drone.radius
        Ay = self.curTriangle.A[1] + (2*self.drone.radius / math.tan(self.curTriangle.B_angle))

        #x-y coor from the B vertex
        Bx = self.drone.radius
        By = self.curTriangle.B[1] - (2*self.drone.radius / math.tan(self.curTriangle.B_angle))

        ### Add the information ####

        # For now, i'll add the paths, but this will be moved later
        self.path.append((xi,yi))
        self.path.append((xf,yf))

        self.curTriangle.set_A((2*xi,Ay))
        self.curTriangle.set_B((2*xi,By))


    def segment_BC(self):
        ### Calculate path of Drone ###
        
        #x-y coor from the B vertex
        xi = self.curTriangle.B[0]
        yi = self.curTriangle.B[1] - (self.drone.radius / math.tan(self.curTriangle.B_angle))

        # x-y coor from the C vertex
        xf = (self.curTriangle.BC_dist - (self.drone.radius / math.tan(self.curTriangle.C_angle)) ) * math.cos(90-self.curTriangle.A_angle)
        yf = (self.curTriangle.BC_dist - (self.drone.radius / math.tan(self.curTriangle.C_angle)) ) * math.sin(90-self.curTriangle.A_angle)
        
        ### Calculate B and C primes ###

        #x-y coor from the B vertex
        Bx = self.curTriangle.B[0]
        By = self.curTriangle.B[1] - (2*self.drone.radius / math.tan(self.curTriangle.B_angle))

        # x-y coor from the C vertex
        Cx = (self.curTriangle.BC_dist - (2*self.drone.radius / math.tan(self.curTriangle.C_angle)) ) * math.cos(90-self.curTriangle.A_angle)
        Cy = (self.curTriangle.BC_dist - (2*self.drone.radius / math.tan(self.curTriangle.C_angle)) ) * math.sin(90-self.curTriangle.A_angle)

        ### Add the information ####

        # For now, i'll add the paths, but this will be moved later
        self.path.append((xi,yi))
        self.path.append((xf,yf))

        self.curTriangle.set_B((Bx,By))
        self.curTriangle.set_C((Cx,Cy))
        

    def segment_AC(self):

        ### Calculate path of Drone ###
        
        #x-y coor from the C vertex
        xi = self.curTriangle.B[0] + (self.curTriangle.BC_dist - (self.drone.radius / math.sin(self.curTriangle.C_angle)) ) * math.sin(self.curTriangle.B_angle)
        yi = self.curTriangle.B[1] - (self.curTriangle.BC_dist - (self.drone.radius / math.sin(self.curTriangle.C_angle)) ) * math.cos(self.curTriangle.B_angle)

        # x-y coor from the A vertex
        xf = self.curTriangle.A[0]
        yf = self.curTriangle.A[1] + (self.drone.radius / math.sin(self.curTriangle.A_angle))
        
        ### Calculate A and C primes ###

        #x-y coor from the C vertex
        Cx = self.curTriangle.B[0] + (self.curTriangle.BC_dist - (2*self.drone.radius / math.sin(self.curTriangle.C_angle)) ) * math.sin(self.curTriangle.B_angle)
        Cy = self.curTriangle.B[1] - (self.curTriangle.BC_dist - (2*self.drone.radius / math.sin(self.curTriangle.C_angle)) ) * math.cos(self.curTriangle.B_angle)

        # x-y coor from the A vertex
        Ax = self.curTriangle.A[0]
        Ay = self.curTriangle.A[1] + (2*self.drone.radius / math.sin(self.curTriangle.A_angle))

        ### Add the information ####

        # For now, i'll add the paths, but this will be moved later
        self.path.append((xi,yi))
        self.path.append((xf,yf))

        self.curTriangle.set_C((Cx,Cy))
        self.curTriangle.set_A((Ax,Ay))       






#a=(0,0)
#b=(0,10)
#c=(5,5)

#shape = Triangle.Triangle(a,b,c)
#drone = Drone.Drone(radius=1)

#path = Drone_Path(shape,drone)
#path.segment_AB()
#path.segment_BC()
#path.segment_AC()

#print(path.path)
#print(path.curTriangle)























