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

        self.container = []
        self.container.append(self.curTriangle.copy())


    def segment_AB(self,reverse = False, info = "path"):
        
        ### Calculate path of Drone ###
        
        if (info == "path"):
            #x-y coor from the A vertex
            Axr = self.curTriangle.A[0] +  self.drone.radius
            Ayr = self.curTriangle.A[1] + (self.drone.radius / math.tan(self.curTriangle.A_angle))

            # x-y coor from the B vertex
            Bxr = self.curTriangle.B[0] + self.drone.radius
            Byr = self.curTriangle.B[1] - (self.drone.radius / math.tan(self.curTriangle.B_angle))

            if(reverse):
                return (Bxr,Byr),(Axr,Ayr)
            else:
                return (Axr,Ayr),(Bxr,Byr)

        elif(info == "prime"):
            ### Calculate A and B primes ###

            #x-y coor from the A vertex
            Ax = self.curTriangle.A[0] + 2*self.drone.radius
            Ay = self.curTriangle.A[1] + (2*self.drone.radius / math.tan(self.curTriangle.A_angle))

            #x-y coor from the B vertex
            Bx = self.curTriangle.B[0] + 2*self.drone.radius
            By = self.curTriangle.B[1] - (2*self.drone.radius / math.tan(self.curTriangle.B_angle))
            
            if(reverse):
                return (Bx,By),(Ax,Ay)
            else:
                return (Ax,Ay),(Bx,By)


    def segment_BC(self, reverse = False, info = "path"):
        ### Calculate path of Drone ###

        if (info == "path"):      
            #x-y coor from the B vertex
            Bxr = self.curTriangle.B[0]
            Byr = self.curTriangle.B[1] - (self.drone.radius / math.sin(self.curTriangle.B_angle))

            # x-y coor from the C vertex
            Cxr = self.curTriangle.C[0] - (math.sin(self.curTriangle.A_angle) / math.sin(self.curTriangle.C_angle )) * self.drone.radius
            Cyr = self.curTriangle.C[1] - (math.cos(self.curTriangle.A_angle) / math.sin(self.curTriangle.C_angle )) * self.drone.radius  

            if(reverse):
                return (Cxr,Cyr),(Bxr,Byr)
            else:
                return (Bxr,Byr),(Cxr,Cyr)

        elif(info == "prime"):
            ### Calculate B and C primes ###

            #x-y coor from the B vertex
            Bx = self.curTriangle.B[0]
            By = self.curTriangle.B[1] - (2*self.drone.radius / math.sin(self.curTriangle.B_angle))

            # x-y coor from the C vertex
            Cx = self.curTriangle.C[0] - (math.sin(self.curTriangle.A_angle) / math.sin(self.curTriangle.C_angle )) * 2*self.drone.radius
            Cy = self.curTriangle.C[1] - (math.cos(self.curTriangle.A_angle) / math.sin(self.curTriangle.C_angle )) * 2*self.drone.radius

            if(reverse):
                return (Cx,Cy),(Bx,By)
            else:
                return (Bx,By),(Cx,Cy)

        
    def segment_AC(self, reverse = False, info = "path"):

            ### Calculate path of Drone ###
        if (info == "path"):     
            #x-y coor from the C vertex
            #Cxr = self.curTriangle.C[0] - (math.sin(self.curTriangle.A_angle) / math.sin(self.curTriangle.C_angle )) * self.drone.radius
            #Cyr = self.curTriangle.C[1] - (math.cos(self.curTriangle.A_angle) / math.sin(self.curTriangle.C_angle )) * self.drone.radius 
            Cxr = self.curTriangle.C[0] - (self.drone.radius / math.sin(self.curTriangle.C_angle)) * math.sin(self.curTriangle.B_angle)
            Cyr = self.curTriangle.C[1] + (self.drone.radius / math.sin(self.curTriangle.C_angle)) * math.cos(self.curTriangle.B_angle)

            # x-y coor from the A vertex
            Axr = self.curTriangle.A[0] 
            Ayr = self.curTriangle.A[1] + (self.drone.radius / math.sin(self.curTriangle.A_angle))

            if(reverse):
                return (Cxr,Cyr),(Axr,Ayr)
            else:
                return (Axr,Ayr),(Cxr,Cyr)

        elif(info == "prime"):
            ### Calculate A and C primes ###

            #x-y coor from the C vertex
            #Cx = self.curTriangle.C[0] - (math.sin(self.curTriangle.A_angle) / math.sin(self.curTriangle.C_angle )) * 2 *self.drone.radius
            #Cy = self.curTriangle.C[1] - (math.cos(self.curTriangle.A_angle) / math.sin(self.curTriangle.C_angle )) * 2 *self.drone.radius 

            Cx = self.curTriangle.C[0] - (2*self.drone.radius / math.sin(self.curTriangle.C_angle))* math.sin(self.curTriangle.B_angle)
            Cy = self.curTriangle.C[1] + (2*self.drone.radius / math.sin(self.curTriangle.C_angle))* math.cos(self.curTriangle.B_angle)

            # x-y coor from the A vertex
            Ax = self.curTriangle.A[0] 
            Ay = self.curTriangle.A[1] + (2*self.drone.radius / math.sin(self.curTriangle.A_angle))

            if(reverse):
                return (Cx,Cy),(Ax,Ay)
            else:
                return (Ax,Ay),(Cx,Cy)       

    # Check if point is within the polygon
    def is_in_region(self,p):
        # https://en.wikipedia.org/wiki/Even-odd_rule
        """Determine if the point is in the path."""

        t1 = self.curTriangle.A[0] <= p[0] and p[0] <= self.curTriangle.C[0]
        t2 = self.curTriangle.A[1] <= p[1] and p[1] <= self.curTriangle.B[1]

        return (t1 and t2)



    def canTravel(self,p1,p2):
        def dist(p1,p2):
            return math.sqrt( (p2[1]-p1[1])**2 +(p2[0]-p1[0])**2)

        if ( self.is_in_region(p1) and self.is_in_region(p2)):

            
            dist_curPoint_finalPoint = dist(self.drone.curPoint, p1) + dist(p1,p2)
            dist_p2_A = dist(p2,self.curTriangle.A)
            dist_chargeStation_A = dist(self.triangle.A, self.curTriangle.A)

            if ( self.drone.curMax_distance - dist_curPoint_finalPoint - dist_p2_A - dist_chargeStation_A >= 0 ):

                self.drone.curMax_distance = self.drone.curMax_distance - dist_curPoint_finalPoint 

                return True

        return False
            



    # algorithm is still kinda funky
    # some revisions will be made later
    def algorithm(self, frame = 1):

        seq = [0,1,2] # represents A,B,C
        index = 0 # HELPS DETERMINE WHICH POINT I AM IN

        # FOR NOW, USE AN ITERATION LOOP, SINCE I DONT HAVE A TERMINATOR AT THE MOMENT
        #for i in range(frame):
        while True:
            if(self.drone.calculate_area() <= self.curTriangle.calculate_area() ):
                # DETERMINE WHERE I WANT TO GO       
                # CREATE A TUPLE TO REPRESENT THE POINTS LABELS
                # FROM WHERE I AM STARTING AND ENDING
                if (index == 0 or index == 1):
                    next_location = ( seq[index], seq[index+1] )
                elif(index == 2):
                    next_location = ( seq[index], seq[index - 1] )

                # CALCULATE THE INITIAL PATH POINT AND FINAL PATH POINT 
                if( next_location == (0,1) ):
                    Ni,Nf = self.segment_AB( reverse= False, info = "path" )

                elif( next_location == (1,2) ):
                    Ni,Nf = self.segment_BC( reverse = False, info = "path")

                elif( next_location == (2,1) ):
                    Ni,Nf = self.segment_BC( reverse = True, info = "path" )



                if ( self.canTravel( Ni, Nf ) ):

                    # ADD THE INITIAL PATH AND FINAL PATH POINT
                    self.path.append(Ni)
                    self.path.append(Nf)
                    self.drone.curPoint = self.path[-1]

                    if( next_location == (0,1) ):

                        Ap,Bp = self.segment_AB( reverse= False, info = "prime")
                        self.curTriangle.set_A(Ap)
                        self.curTriangle.set_B(Bp)

                        index += 1

                    elif( next_location == (1,2) ):

                        Bp,Cp =self.segment_BC( reverse = False, info = "prime")
                        self.curTriangle.set_B(Bp)
                        self.curTriangle.set_C(Cp)

                        index += 1

                    elif( next_location == (2,1) ):
                        
                        Cp,Bp =self.segment_BC( reverse = True, info = "prime" )  
                        self.curTriangle.set_B(Bp)
                        self.curTriangle.set_C(Cp)

                        index -= 1     

                    self.container.append(self.curTriangle.copy())                          

                else: # THIS SECTION IS INCOMPLETE, WILL LOOK AT LATER

                    # DETERMINE WHERE I NEED TO GO
                    next_location = ( seq[index], seq[0] )               

                    if( next_location == (1,0) ):
                        Ni,Nf = self.segment_AB( reverse= True, info = "path")
                        Bp,Ap =self.segment_AB( reverse = True, info = "prime" ) 
                        self.curTriangle.set_A(Ap) 
                        self.curTriangle.set_B(Bp)

                    elif( next_location == (2,0) ):
                        Ni,Nf = self.segment_AC( reverse = True, info = "path")
                        Cp,Ap =self.segment_AC( reverse = True, info = "prime" ) 
                        self.curTriangle.set_A(Ap)
                        self.curTriangle.set_C(Cp)

                    self.path.append(Ni)
                    self.path.append(Nf)
                    self.path.append(self.triangle.A)
                    self.drone.curPoint = self.path[-1]
                    self.container.append(self.curTriangle.copy()) 

                    index = 0
                    self.drone.curMax_distance = self.drone.max_distance
            else:
                tri_centroid = self.curTriangle.calculate_centroid()
                self.path.append(tri_centroid)
                self.path.append(self.triangle.A)
                break



    def print_path(self):

        for path in self.path:
            print(path)






























