from Triangle import Triangle
from Drone import Drone
import numpy as np 



########################################
# Class name: Drone_Path()
# Class Author: Luis E. Vargas Tamayo
# Purpose of the class: Helps set up the enviroment to create a path that covers the area of a triangle
# Date: 3/2/2020
# List of changes with dates: none
########################################
class Drone_Path():

    ##############################################
    # Method Name: __init__
    # Purpose: Class Constructor
    # Parameter: Triangle Object, Drone Object
    # Method used: None
    # Return Value: None
    # Date:  3/2/2020
    ##############################################
    def __init__(self, triangle, drone):

        self.triangle = triangle # SAVES THE ORIGINAL TRIANGLE IN WHICH THE ALGORITHM WILL THE FIND THE PATH TO
        self.drone = drone # SAVE THE DRONE
        self.curTriangle = triangle.copy() # CREATES A COPY OF THE TRIANGLE AND WILL BE EDITED THROUGHOUT THE CODE

    ##############################################
    # Method Name: segment_AB
    # Purpose: Contains the computations needed to calculate the next path/prime_vertex from point A to point B
    # Parameter: reverse: dictate if you're going from A to B or B to A
    #            info: determines what the method is returning (path,prime)
    # Method used: None
    # Return Value: two points are returned (x,y)
    # Date:  3/2/2020
    ##############################################
    def segment_AB(self,reverse = False, info = "path"):
        
        ### Calculate path of Drone ###
        
        if (info == "path"):
            #x-y coor from the A vertex
            Axr = self.curTriangle.A[0] +  self.drone.radius
            Ayr = self.curTriangle.A[1] + (self.drone.radius / np.tan(self.curTriangle.A_angle))

            # x-y coor from the B vertex
            Bxr = self.curTriangle.B[0] + self.drone.radius
            Byr = self.curTriangle.B[1] - (self.drone.radius / np.tan(self.curTriangle.B_angle))

            if(reverse):
                return np.array((Bxr,Byr)),np.array((Axr,Ayr))
            else:
                return np.array((Axr,Ayr)),np.array((Bxr,Byr))

        elif(info == "prime"):
            ### Calculate A and B primes ###

            #x-y coor from the A vertex
            Ax = self.curTriangle.A[0] + 2*self.drone.radius
            Ay = self.curTriangle.A[1] + (2*self.drone.radius / np.tan(self.curTriangle.A_angle))

            #x-y coor from the B vertex
            Bx = self.curTriangle.B[0] + 2*self.drone.radius
            By = self.curTriangle.B[1] - (2*self.drone.radius / np.tan(self.curTriangle.B_angle))
            
            if(reverse):
                return np.array((Bx,By)),np.array((Ax,Ay))
            else:
                return np.array((Ax,Ay)),np.array((Bx,By))

    ##############################################
    # Method Name: segment_BC
    # Purpose: Contains the computations needed to calculate the next path/prime_vertex from point B to point C
    # Parameter: reverse: dictate if you're going from B to C or C to B
    #            info: determines what the method is returning (path,prime)
    # Method used: None
    # Return Value: two points are returned (x,y)
    # Date:  3/2/2020
    ##############################################
    def segment_BC(self, reverse = False, info = "path"):
        ### Calculate path of Drone ###

        if (info == "path"):      
            #x-y coor from the B vertex
            Bxr = self.curTriangle.B[0]
            Byr = self.curTriangle.B[1] - (self.drone.radius / np.sin(self.curTriangle.B_angle))

            # x-y coor from the C vertex
            Cxr = self.curTriangle.C[0] - (np.sin(self.curTriangle.A_angle) / np.sin(self.curTriangle.C_angle )) * self.drone.radius
            Cyr = self.curTriangle.C[1] - (np.cos(self.curTriangle.A_angle) / np.sin(self.curTriangle.C_angle )) * self.drone.radius  

            if(reverse):
                return np.array((Cxr,Cyr)),np.array((Bxr,Byr))
            else:
                return np.array((Bxr,Byr)),np.array((Cxr,Cyr))

        elif(info == "prime"):
            ### Calculate B and C primes ###

            #x-y coor from the B vertex
            Bx = self.curTriangle.B[0]
            By = self.curTriangle.B[1] - (2*self.drone.radius / np.sin(self.curTriangle.B_angle))

            # x-y coor from the C vertex
            Cx = self.curTriangle.C[0] - (np.sin(self.curTriangle.A_angle) / np.sin(self.curTriangle.C_angle )) * 2*self.drone.radius
            Cy = self.curTriangle.C[1] - (np.cos(self.curTriangle.A_angle) / np.sin(self.curTriangle.C_angle )) * 2*self.drone.radius

            if(reverse):
                return np.array((Cx,Cy)),np.array((Bx,By))
            else:
                return np.array((Bx,By)),np.array((Cx,Cy))

    ##############################################
    # Method Name: segment_AC
    # Purpose: Contains the computations needed to calculate the next path/prime_vertex from point A to point C
    # Parameter: reverse: dictate if you're going from A to C or C to A
    #            info: determines what the method is returning (path,prime)
    # Method used: None
    # Return Value: two points are returned (x,y)
    # Date:  3/2/2020
    ##############################################        
    def segment_AC(self, reverse = False, info = "path"):

            ### Calculate path of Drone ###
        if (info == "path"):     
            #x-y coor from the C vertex
            #Cxr = self.curTriangle.C[0] - (np.sin(self.curTriangle.A_angle) / np.sin(self.curTriangle.C_angle )) * self.drone.radius
            #Cyr = self.curTriangle.C[1] - (np.cos(self.curTriangle.A_angle) / np.sin(self.curTriangle.C_angle )) * self.drone.radius 
            Cxr = self.curTriangle.C[0] - (self.drone.radius / np.sin(self.curTriangle.C_angle)) * np.sin(self.curTriangle.B_angle)
            Cyr = self.curTriangle.C[1] + (self.drone.radius / np.sin(self.curTriangle.C_angle)) * np.cos(self.curTriangle.B_angle)

            # x-y coor from the A vertex
            Axr = self.curTriangle.A[0] 
            Ayr = self.curTriangle.A[1] + (self.drone.radius / np.sin(self.curTriangle.A_angle))

            if(reverse):
                return np.array((Cxr,Cyr)),np.array((Axr,Ayr))
            else:
                return np.array((Axr,Ayr)),np.array((Cxr,Cyr))

        elif(info == "prime"):
            ### Calculate A and C primes ###

            #x-y coor from the C vertex
            Cx = self.curTriangle.C[0] - (2*self.drone.radius / np.sin(self.curTriangle.C_angle))* np.sin(self.curTriangle.B_angle)
            Cy = self.curTriangle.C[1] + (2*self.drone.radius / np.sin(self.curTriangle.C_angle))* np.cos(self.curTriangle.B_angle)

            # x-y coor from the A vertex
            Ax = self.curTriangle.A[0] 
            Ay = self.curTriangle.A[1] + (2*self.drone.radius / np.sin(self.curTriangle.A_angle))

            if(reverse):
                return np.array((Cx,Cy)),np.array((Ax,Ay))
            else:
                return np.array((Ax,Ay)),np.array((Cx,Cy)) 


    ##############################################
    # THE CODE BELOW IS USED FOR THE ALGORITHM
    # SOME OF THE METHODS ARE FAULTY AND COULD USE SOME EDITING (3/12/2020)
    # ALGORITHM WORKS AS LONG AS THE DRONE CAN REACH A VERTEX AND COME BACK
    ##############################################


    ##############################################
    # Method Name: canTravel()
    # Purpose: Check if the drone is able to travel to the next point
    # Parameter: tuples (x,y)
    # Method used: dist(),is_in_region() 
    # Return Value: boolean
    # Date:  3/2/2020
    ##############################################  
    def canTravel(self,p1,p2):

        # CALCULATE EUCLEDIAN DISTANCE BETWEEN TWO POINTS
        def dist(p1,p2):
            return np.sqrt( (p2[1]-p1[1])**2 +(p2[0]-p1[0])**2)

        # CHECK IF THE POINT IS IN THE REGION OF THE TRIANGLE
        # SOME TOLERANCE IS ADDED FOR ROUND OFF ERRORS
        def is_in_region(p):

            # THERE SHOULD BE A BETTER WAY TO DO THIS, BUT THIS WORKS FOR NOW (3/12/2020)

            tolerance = 0.0000000001

            # CHECK THAT THE X IS IN BETWEEN AX AND CX
            # CHECK THAT THE Y IS IN BETWEEN AY AND BY
            t1 = self.curTriangle.A[0] - tolerance <= p[0] and p[0] <= self.curTriangle.C[0] + tolerance
            t2 = self.curTriangle.A[1] - tolerance <= p[1] and p[1] <= self.curTriangle.B[1] + tolerance

            return (t1 and t2)

        # CHECK THAT THE POINTS ARE IN THE REGION OF THE TRIANGLE
        if ( is_in_region(p1) and is_in_region(p2)):

            # FIND THE DISTANCE FROM THE CURRENT POINT TO P1 PLUS THE DISTANCE FROM P1 TO P2
            # RECALL THAT P1 IS WHERE I AM GOING TO TRAVEL AND P2 IS WHERE I AM ENDING AT
            dist_curPoint_finalPoint = dist(self.drone.curPoint, p1) + dist(p1,p2)

            # FIND THE DISTANCE FROM P2 TO THE VERTEX A
            # REASON: I WANT TO MAKE SURE THE DRONE CAN RETURN BACK TO PRIME A FROM P2
            dist_p2_A = dist(p2,self.curTriangle.A)

            # FIND THE DISTANCE FROM PRIME A TO THE CHARGING STATION
            dist_chargeStation_A = dist(self.triangle.A, self.curTriangle.A)

            # IF I AM ABLE TO TRAVEL TO P2 AND BE ABLE TO GO BACK TO THE CHARGING STATION
            # THEN I WILL GO TO P2, OTHERWISE, I CANT TRAVEL
            if ( self.drone.curMax_distance - dist_curPoint_finalPoint - dist_p2_A - dist_chargeStation_A >= 0 ):
                
                # SUBTRACT THE DISTANCE THE DRONE WILL TRAVEL FROM ITS CURMAX_DISTANCE
                self.drone.curMax_distance = self.drone.curMax_distance - dist_curPoint_finalPoint

                return True

        return False
            

    ##############################################
    # Method Name: algorithm()
    # Purpose: creates the path needed to cover a triangle, given the limitations of the drone
    # Parameter: None
    # Method used: reachable()
    # Return Value: list of tuples (x,y)
    # Date:  3/2/2020
    ##############################################  
    def algorithm(self):
            
        # CHECKS IF THE DRONE IS ABLE TO REACH VERTEX B AND C AND BE ABLE TO COME BACK TO THE CHARGING STATION
        def reachable():

            # REASON FOR 2.4 : THE 2 IS BECAUSE OF THE DISTANCE TO AND BACK FROM THE GIVEN VERTEX TO A
            #                  THE 0.4 IS BECAUSE WE DONT DIRECTLY GO STRAIGHT TO THE GIVEN VERTEX
            #                  SINCE WE MAKE SMALL ADJUSTMENTS IN THE CODE.
            return self.drone.max_distance > 2.4*self.triangle.AB_dist and self.drone.max_distance > 2.4*self.triangle.AC_dist 

        # IN THE ALGORITHM, WE'LL GO FROM 0,1,2,1,2,.... BACK TO 0 DEPENDING ON THE SITUATION
        seq = [0,1,2] # represents A,B,C
        index = 0 # HELPS DETERMINE WHICH POINT THE DRONE IS IN

        # SET THE POSITION OF THE DRONE TO BE AT THE CHARGING STATION
        self.drone.curPoint = self.curTriangle.A

        # ADD THIS POSITION TO THE PATH LIST
        path = [ np.array(self.curTriangle.A) ] 

        # CHECK IF THE DRONE HAS THE REQUIRE MAX DISTANCE TO BE ABLE TO MAKE THE ALGORITHM WORK
        if ( reachable() ):

            # KEEP LOOPING UNTIL THE PATH IS COMPLETE
            while True:

                # CHECK IF THE DRONE AREA COVERAGE IS BIGGER THAN THE TRIANGLE NEEDED TO COVERED
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

                    # DETERMINE IF THE DRONE IS ABLE TO TRAVEL FROM THE NEXT POINT TO THE FINAL POINT
                    if ( self.canTravel( Ni, Nf ) ):

                        # ADD THE INITIAL PATH AND FINAL PATH POINT
                        path.append(Ni)
                        path.append(Nf)

                        # SET THE POSITION OF THE DRONE
                        self.drone.curPoint = path[-1]


                        # SINCE THE DRONE WAS ABLE TO TRAVEL TO A NEW POINT,
                        # WE MUST UPDATE THE TRIANGLE THAT NEEDS TO BE COVERED
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

                    
                    else: # DRONE WAS NOT ABLE TO TRAVEL, THUS, IT MUST RETURN TO RECHARGE

                        # DETERMINE WHERE I NEED TO GO
                        next_location = ( seq[index], seq[0] )               

                        # DEPENDING ON WHERE THE DRONE IS, DRONE NEEDS TO RETURN TO A'
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

                        # ADD THE PATH THE DRONE WILL TAKE
                        path.append(Ni)
                        path.append(Nf)

                        # ADD THE LOCATION OF THE CHARGING STATION
                        path.append(self.triangle.A)

                        # SET THE LOCATION OF THE DRONE
                        self.drone.curPoint = path[-1]

                        # RESET THE INDEX AND CURMAXDISTANCE SO THE ALGORITHM MAY START UP AGAIN
                        index = 0
                        self.drone.curMax_distance = self.drone.max_distance
                else: # THE DRONE CAN COVERED THE CURRENT TRIANGLE, THUS, WE'LL FIND THE CENTROID AND THEN GO BACK TO THE CHARGING STATION
                    # FIND THE TRIANGLE CENTROID POINT
                    tri_centroid = self.curTriangle.calculate_centroid()

                    # ADD THE PATH THE DRONE WILL TAKE 
                    path.append(tri_centroid)
                    path.append(self.triangle.A)

                    # END THE ALGORITHM SINCE WE COVERED THE AREA OF THE TRIANGLE 
                    break

        # RETURN A LIST OF TUPLES (X,Y)
        return path 
































