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


    def segment_AB(self, reverse = False):
        
        ### Calculate path of Drone ###
        
        #x-y coor from the A vertex
        xi = self.curTriangle.A[0] +  self.drone.radius
        yi = self.curTriangle.A[1] + (self.drone.radius / math.tan(self.curTriangle.A_angle))

        # x-y coor from the B vertex
        xf = self.curTriangle.B[0] + self.drone.radius
        yf = self.curTriangle.B[1] - (self.drone.radius / math.tan(self.curTriangle.B_angle))
        

        if ( self.canTravel( (xi,yi) , (xf,yf) ) ):

            ### Calculate A and B primes ###

            #x-y coor from the A vertex
            Ax = self.curTriangle.A[0] + 2*self.drone.radius
            Ay = self.curTriangle.A[1] + (2*self.drone.radius / math.tan(self.curTriangle.A_angle))

            #x-y coor from the B vertex
            Bx = self.curTriangle.B[0] + 2*self.drone.radius
            By = self.curTriangle.B[1] - (2*self.drone.radius / math.tan(self.curTriangle.B_angle))

            ### Add the information ####

            if (reverse):
                self.path.append((xf,yf))
                self.path.append((xi,yi))
                
            else:

                self.path.append((xi,yi))
                self.path.append((xf,yf))

            self.drone.curPoint = self.path[-1]
            self.curTriangle.set_A((Ax,Ay))
            self.curTriangle.set_B((Bx,By))

            return True 
        
        return False 


    def segment_BC(self, reverse = False):
        ### Calculate path of Drone ###
        
        #x-y coor from the B vertex
        xi = self.curTriangle.B[0]
        yi = self.curTriangle.B[1] - (self.drone.radius / math.sin(self.curTriangle.B_angle))

        # x-y coor from the C vertex
        #xf = self.curTriangle.A[0] + (self.curTriangle.AC_dist - (self.drone.radius / math.sin(self.curTriangle.C_angle)) ) * math.cos(90-self.curTriangle.A_angle)
        #yf = self.curTriangle.A[1] + (self.curTriangle.AC_dist - (self.drone.radius / math.sin(self.curTriangle.C_angle)) ) * math.sin(90-self.curTriangle.A_angle)
        xf = self.curTriangle.C[0] - (math.sin(self.curTriangle.A_angle) / math.sin(self.curTriangle.C_angle )) * self.drone.radius
        yf = self.curTriangle.C[1] - (math.cos(self.curTriangle.A_angle) / math.sin(self.curTriangle.C_angle )) * self.drone.radius  


        if ( self.canTravel( (xi,yi) , (xf,yf) ) ):
            ### Calculate B and C primes ###

            #x-y coor from the B vertex
            Bx = self.curTriangle.B[0]
            By = self.curTriangle.B[1] - (2*self.drone.radius / math.sin(self.curTriangle.B_angle))

            # x-y coor from the C vertex
            #Cx = self.curTriangle.A[0] + (self.curTriangle.AC_dist - (2*self.drone.radius / math.sin(self.curTriangle.C_angle)) ) * math.cos(90-self.curTriangle.A_angle)
            #Cy = self.curTriangle.A[1] +(self.curTriangle.AC_dist - (2*self.drone.radius / math.sin(self.curTriangle.C_angle)) ) * math.sin(90-self.curTriangle.A_angle)
            Cx = self.curTriangle.C[0] - (math.sin(self.curTriangle.A_angle) / math.sin(self.curTriangle.C_angle )) * 2*self.drone.radius
            Cy = self.curTriangle.C[1] - (math.cos(self.curTriangle.A_angle) / math.sin(self.curTriangle.C_angle )) * 2*self.drone.radius

            ### Add the information ####

            if (reverse):
                self.path.append((xf,yf))
                self.path.append((xi,yi))

            else:
                self.path.append((xi,yi))
                self.path.append((xf,yf))

            self.drone.curPoint = self.path[-1]
            self.curTriangle.set_B((Bx,By))
            self.curTriangle.set_C((Cx,Cy))
            return True

        return False 

        
    def segment_CA(self, reverse = False):

        ### Calculate path of Drone ###
        
        #x-y coor from the C vertex
        xi = self.curTriangle.B[0] + (self.curTriangle.BC_dist - (self.drone.radius / math.sin(self.curTriangle.C_angle)) ) * math.sin(self.curTriangle.B_angle)
        yi = self.curTriangle.B[1] - (self.curTriangle.BC_dist - (self.drone.radius / math.sin(self.curTriangle.C_angle)) ) * math.cos(self.curTriangle.B_angle)

        # x-y coor from the A vertex
        xf = self.curTriangle.A[0]
        yf = self.curTriangle.A[1] + (self.drone.radius / math.sin(self.curTriangle.A_angle))
        
        if ( self.canTravel( (xi,yi) , (xf,yf) ) ):
            ### Calculate A and C primes ###

            #x-y coor from the C vertex
            Cx = self.curTriangle.B[0] + (self.curTriangle.BC_dist - (2*self.drone.radius / math.sin(self.curTriangle.C_angle)) ) * math.sin(self.curTriangle.B_angle)
            Cy = self.curTriangle.B[1] - (self.curTriangle.BC_dist - (2*self.drone.radius / math.sin(self.curTriangle.C_angle)) ) * math.cos(self.curTriangle.B_angle)

            # x-y coor from the A vertex
            Ax = self.curTriangle.A[0]
            Ay = self.curTriangle.A[1] + (2*self.drone.radius / math.sin(self.curTriangle.A_angle))

            ### Add the information ####
            
            if (reverse):
            # For now, i'll add the paths, but this will be moved later

                self.path.append((xf,yf))
                self.path.append((xi,yi))
 
            else:
                self.path.append((xi,yi))
                self.path.append((xf,yf))               

            self.drone.curPoint = self.path[-1]
            self.curTriangle.set_C((Cx,Cy))
            self.curTriangle.set_A((Ax,Ay))   

            return True

        return False              


    def canTravel(self,p1,p2):
        def dist(p1,p2):
            return math.sqrt( (p2[1]-p1[1])**2 +(p2[0]-p1[0])**2)

        # TOTAL DISTANCE FROM CURPOINT TO INITPOINT TO FINAL POINT
        dist_curPoint_finalPoint = dist(self.drone.curPoint, p1) + dist(p1,p2)

        if( self.drone.curMax_distance - 2*dist_curPoint_finalPoint  >= 0):
            
            self.drone.curMax_distance = self.drone.curMax_distance - dist_curPoint_finalPoint
            return True 
        
        return False 

    # algorithm is still kinda funky
    # some revisions will be made later
    def algorithm(self):

        seq = [0,1,2] # represents A,B,C
        index = 0 # HELPS DETERMINE WHICH POINT I AM IN

        # FOR NOW, USE AN ITERATION LOOP, SINCE I DONT HAVE A TERMINATOR AT THE MOMENT
        for i in range(15):

            # DETERMINE WHERE I WANT TO GO
            if (index == 0 or index == 1):

                # CREATE A TUPLE TO REPRESENT THE POINTS LABELS
                # FROM WHERE I AM STARTING AND ENDING
                next_location = ( seq[index], seq[index+1] )

            elif(index == 2):

                # CREATE A TUPLE TO REPRESENT THE POINTS LABELS
                # FROM WHERE I AM STARTING AND ENDING
                next_location = ( seq[index], seq[index - 1] )

            # CALCULATE THE INITIAL POINT AND FINAL POINT 

            if( next_location == (0,1) ):

                keepRunning = self.segment_AB( reverse= False)

                index = index+1 if keepRunning else 0

            elif( next_location == (1,2) ):

                keepRunning = self.segment_BC( reverse = False)
                index = index+1 if keepRunning else 0

            elif( next_location == (2,1) ):
                
                keepRunning = self.segment_BC( reverse = True )
                index = index-1 if keepRunning else 0


            if (keepRunning):

                continue

            else: # THIS SECTION IS INCOMPLETE, WILL LOOK AT LATER

                # DETERMINE WHERE I NEED TO GO
                if (index == 1):

                    # CREATE A TUPLE TO REPRESENT THE POINTS LABELS
                    # FROM WHERE I AM STARTING AND ENDING
                    next_location = ( seq[index], seq[0] )

                elif(index == 2):

                    # CREATE A TUPLE TO REPRESENT THE POINTS LABELS
                    # FROM WHERE I AM STARTING AND ENDING
                    next_location = ( seq[index], seq[0] )               

                if( next_location == (1,0) ):
                    self.segment_AB( reverse= True)
                elif( next_location == (2,0) ):
                    self.segment_CA( reverse = True)

    def print_path(self):

        for path in self.path:
            print(path)






























