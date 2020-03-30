from Triangle import Triangle
from Drone import Drone
import numpy as np 



########################################
# Class name: Drone_Path()
# Class Author: Luis E. Vargas Tamayo
# Purpose of the class: Helps set up the enviroment to create a path that covers the area of a triangle
# Date: 3/2/2020
# List of changes with dates: 
# 3/27/2020: added two parameters to the segments. This way, if i have a prime vertex and i want the prime prime vertex, its possible to calculate; same goes for path
#            redid the algorithm for a much cleaner loop and optimal
#            deleted two methods and replaced it with isCoverable()
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
    def segment_AB(self, vertexA = None , vertexB = None ,reverse = False, info = "path"):
        


        if(vertexA is None):

            vertexA = self.curTriangle.A

        if(vertexB is None):

            vertexB = self.curTriangle.B

        ### Calculate path of Drone ###
        
        if (info == "path"):
            #x-y coor from the A vertex
            Axr = vertexA[0] +  self.drone.radius
            Ayr = vertexA[1] + (self.drone.radius / np.tan(self.curTriangle.A_angle))

            # x-y coor from the B vertex
            Bxr = vertexB[0] + self.drone.radius
            Byr = vertexB[1] - (self.drone.radius / np.tan(self.curTriangle.B_angle))

            if(reverse):
                return np.array((Bxr,Byr)),np.array((Axr,Ayr))
            else:
                return np.array((Axr,Ayr)),np.array((Bxr,Byr))

        elif(info == "prime"):
            ### Calculate A and B primes ###

            #x-y coor from the A vertex
            Ax = vertexA[0] + 2*self.drone.radius
            Ay = vertexA[1] + (2*self.drone.radius / np.tan(self.curTriangle.A_angle))

            #x-y coor from the B vertex
            Bx = vertexB[0] + 2*self.drone.radius
            By = vertexB[1] - (2*self.drone.radius / np.tan(self.curTriangle.B_angle))
            
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
    def segment_BC(self, vertexB = None , vertexC = None , reverse = False, info = "path"):
            
       
        if(vertexB is None):

            vertexB = self.curTriangle.B


        if(vertexC is None):

            vertexC = self.curTriangle.C      
        
        
        ### Calculate path of Drone ###

        if (info == "path"):      
            #x-y coor from the B vertex
            Bxr = vertexB[0]
            Byr = vertexB[1] - (self.drone.radius / np.sin(self.curTriangle.B_angle))

            # x-y coor from the C vertex
            Cxr = vertexC[0] - (np.sin(self.curTriangle.A_angle) / np.sin(self.curTriangle.C_angle )) * self.drone.radius
            Cyr = vertexC[1] - (np.cos(self.curTriangle.A_angle) / np.sin(self.curTriangle.C_angle )) * self.drone.radius  

            if(reverse):
                return np.array((Cxr,Cyr)),np.array((Bxr,Byr))
            else:
                return np.array((Bxr,Byr)),np.array((Cxr,Cyr))

        elif(info == "prime"):
            ### Calculate B and C primes ###

            #x-y coor from the B vertex
            Bx = vertexB[0]
            By = vertexB[1] - (2*self.drone.radius / np.sin(self.curTriangle.B_angle))

            # x-y coor from the C vertex
            Cx = vertexC[0] - (np.sin(self.curTriangle.A_angle) / np.sin(self.curTriangle.C_angle )) * 2*self.drone.radius
            Cy = vertexC[1] - (np.cos(self.curTriangle.A_angle) / np.sin(self.curTriangle.C_angle )) * 2*self.drone.radius

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
    def segment_AC(self, vertexA = None , vertexC = None , reverse = False, info = "path"):


        if(vertexA is None):

            vertexA = self.curTriangle.A


        if(vertexC is None):

            vertexC = self.curTriangle.C


            ### Calculate path of Drone ###
        if (info == "path"):     
            #x-y coor from the C vertex
            #Cxr = self.curTriangle.C[0] - (np.sin(self.curTriangle.A_angle) / np.sin(self.curTriangle.C_angle )) * self.drone.radius
            #Cyr = self.curTriangle.C[1] - (np.cos(self.curTriangle.A_angle) / np.sin(self.curTriangle.C_angle )) * self.drone.radius 
            Cxr = vertexC[0] - (self.drone.radius / np.sin(self.curTriangle.C_angle)) * np.sin(self.curTriangle.B_angle)
            Cyr = vertexC[1] + (self.drone.radius / np.sin(self.curTriangle.C_angle)) * np.cos(self.curTriangle.B_angle)

            # x-y coor from the A vertex
            Axr = vertexA[0] 
            Ayr = vertexA[1] + (self.drone.radius / np.sin(self.curTriangle.A_angle))

            if(reverse):
                return np.array((Cxr,Cyr)),np.array((Axr,Ayr))
            else:
                return np.array((Axr,Ayr)),np.array((Cxr,Cyr))

        elif(info == "prime"):
            ### Calculate A and C primes ###

            #x-y coor from the C vertex
            Cx = vertexC[0] - (2*self.drone.radius / np.sin(self.curTriangle.C_angle))* np.sin(self.curTriangle.B_angle)
            Cy = vertexC[1] + (2*self.drone.radius / np.sin(self.curTriangle.C_angle))* np.cos(self.curTriangle.B_angle)

            # x-y coor from the A vertex
            Ax = vertexA[0] 
            Ay = vertexA[1] + (2*self.drone.radius / np.sin(self.curTriangle.A_angle))

            if(reverse):
                return np.array((Cx,Cy)),np.array((Ax,Ay))
            else:
                return np.array((Ax,Ay)),np.array((Cx,Cy)) 




    ##############################################
    # Method Name: dist()
    # Purpose: Calculate eucledian distance between two points
    # Parameter: two tuples-like objects (x,y)
    # Method used: None
    # Return Value: Float
    # Date:  3/2/2020
    ##############################################  
    def dist(self,p1,p2):
        return np.sqrt( (p2[1]-p1[1])**2 +(p2[0]-p1[0])**2)


    ##############################################
    # Method Name: isCoverable()
    # Purpose: checks if a circle can cover a triangle
    # Parameter: None
    # Method used: None
    # Return Value: Boolean
    # Date:  3/27/2020
    ##############################################  
    def isCoverable(self):

        centroid = self.curTriangle.centroid


        return  (self.drone.radius >= self.dist(centroid,self.curTriangle.A) and 
               self.drone.radius >= self.dist(centroid,self.curTriangle.B) and 
               self.drone.radius >= self.dist(centroid,self.curTriangle.C) )



    def validate(Dp,Np,vertex,side_length):

        if( self.dist(Dp,vertex) > side_length ):

            Dp = vertex
            Np = vertex

        elif( self.dist(Np,vertex) > side_length ):

            Np = pi

        return Dp,Np



            



    ##############################################
    # Method Name: dist()
    # Purpose: creates the path needed to cover a triangle, given the limitations of the drone
    # Parameter: None
    # Method used: dist() , isCoverable()
    # Return Value: Float
    # Date:  3/2/2020
    #        3/27/2020: Redid Code for easier understanding and opmimal code
    ##############################################  
    def algorithm(self):

        # Store paths
        path = [self.drone.curPoint]

        # CREATE A SET OF LOCATIONS
        # 0 Charging station
        # 1 vertex A
        # 2 vertex B
        # 3 Vertex C
        loc = [0,1,2,3]

        # CS: CHARGING STATION
        CS = self.triangle.A
        
        # INDEX LOCATION
        loc_i = 1
        
        
        # LOOKING AT A FUTURE PATH
        start_end = [0,0]
        

        # LOOP WILL CONTINUE UNTIL IT BREAKS BY:
        # PATH IS FOUND TO COVER TRIANGLE
        # DRONE CANT TRAVEL FAR, SO NO PATH IS MADE
        while( True ):



            # DETERMINE WHERE DRONE IS AND WHERE IT IS GOING
            
            # CURRENT VERTEX
            start_end[0] = loc_i

            # DETERMINE WHAT MY NEXT VERTEX IS 
            if(loc_i == 3):
                loc_i = loc_i - 1
                
            else:
                loc_i = loc_i + 1 
            
            # NEXT VERTEX
            start_end[1] = loc_i

            # pi: INITIAL DRONE PATH POINT
            # pf: FINAL DRONE PATH POINT
            pi = None
            pf = None

            # pNi: NEW CURRENT PRIME POINT
            # pNf: NEW FINAL PRIME POINT
            pNi = None
            pNf = None 
        
            # CHECK IF THE CIRCLE CAN COVER THE TRIANGLE
            if( self.isCoverable() ):

                # DRONE INITIAL PATH POINT
                pi = self.curTriangle.centroid
                # DRONE FINAL PATH POINT
                pf = CS
                

                # DISTANCE FROM CURRENT POSITION TO DRONE INITIAL PATH POINT
                dist_curPos_pi = self.dist(self.drone.curPoint , pi)

                # DISTANCE FROM DRONE INITIAL PATH POINT TO DRONE FINAL PATH POINT(CHARGING STATION)
                dist_pi_pf = self.dist(pi,pf)  

                # ADD ALL THE DISTANCES TOGETHER
                req_dist_travel = dist_curPos_pi + dist_pi_pf

                # CHECK IF ITS POSSIBLE TO MAKE THE TRIP TO THE CENTROID, THEN TO THE CHARGING STATION
                if(self.drone.curMax_distance >= req_dist_travel):    

                    # ADD DRONE INITIAL PATH POINT TO THE PATH LIST
                    path.append(pi)
                    # ADD DRONE FINAL PATH POINT TO THE PATH LIST
                    path.append(pf)
                    # ADD THE DISTANCE TRAVELED TO THE DRONE TOTAL_DISTANCE_TRAVEL
                    self.drone.total_distance_travel += dist_curPos_pi + dist_pi_pf
                    break
           
            # IF DRONE IS IN A, THEN WE MUST GO FROM A TO B   
            if(start_end == [1,2]):
                
                # GET THE DRONE INITIAL PATH POINT AND DRONE FINAL PATH POINT
                pi,pf = self.segment_AB(reverse = False , info = "path")
                # GET A PRIME AND B PRIME POINTS
                pNi,pNf = self.segment_AB(reverse = False , info = "prime")
                # GET THE DRONE PRIME INITIAL PATH POINT AND DRONE PRIME PATH POINT
                ppi,ppf = self.segment_AB( vertexA = pNi , vertexB = pNf , reverse = True , info = "path")

            # IF DRONE IS IN B, THEN WE MUST GO FROM B TO C
            elif(start_end == [2,3]):

                # GET THE DRONE INITIAL PATH POINT AND DRONE FINAL PATH POINT
                pi,pf = self.segment_BC(reverse = False , info = "path")
                # GET B PRIME AND C PRIME POINTS
                pNi,pNf = self.segment_BC(reverse = False , info = "prime")  
                # GET THE DRONE PRIME INITIAL PATH POINT AND DRONE PRIME PATH POINT
                ppi,ppf = self.segment_AC( vertexC = pNf , reverse = True , info = "path")         

            # IF DRONE IS IN B, THEN WE MUST GO FROM C TO B
            elif(start_end == [3,2]):

                # GET THE DRONE INITIAL PATH POINT AND DRONE FINAL PATH POINT
                pi,pf = self.segment_BC(reverse = True , info = "path")
                # GET C PRIME AND B PRIME POINTS
                pNi,pNf = self.segment_BC(reverse = True , info = "prime")     
                # GET THE DRONE PRIME INITIAL PATH POINT AND DRONE PRIME PATH POINT
                ppi,ppf = self.segment_AB( vertexB = pNf , reverse = True , info = "path")         



            # DISTANCE FROM CURRENT POSITION TO DRONE INITIAL PATH POINT
            dist_curPos_pi = self.dist(self.drone.curPoint , pi)
            # DISTANCE FROM DRONE INITIAL PATH POINT TO DRONE FINAL PATH POINT
            dist_pi_pf = self.dist(pi,pf)  

            # DISTANCE FROM THE DRONE FINAL PATH POINT TO THE DRONE PRIME INITIAL POINT
            dist_pf_ppi = self.dist(pf,ppi)   
            # DISTANCE FORM THE DRONE PRIME INITIAL POINT TO THE DRONE PRIME FINAL POINT
            dist_ppi_ppf = self.dist(ppi,ppf)
            # DISTANCE FROM THE DRONE PRIME FINAL POINT TO THE CHARGING STATION
            dist_ppf_CS = self.dist( pNf, CS)


            # CALCULATE THE REQUIRE DISTANCE TO TRAVEL 
            req_dist_travel = dist_curPos_pi + dist_pi_pf + dist_pf_ppi + dist_ppi_ppf + dist_ppf_CS

            # CHECK IF ITS POSSIBLE TO TRAVEL
            if(self.drone.curMax_distance >= req_dist_travel):

                # IF DRONE TRAVELS FROM A TO B
                if(start_end == [1,2]):
                    # SET THE NEW VERTICES FROM THE PRIMES
                    self.curTriangle.set_A(pNi) 
                    self.curTriangle.set_B(pNf)

                # IF DRONE TRAVELS FROM B TO C
                elif(start_end == [2,3]):
                    # SET THE NEW VERTICES FROM THE PRIMES    
                    self.curTriangle.set_B(pNi) 
                    self.curTriangle.set_C(pNf)
                # IF DRONE TRAVELS FROM C TO B
                elif(start_end == [3,2]):
                    # SET THE NEW VERTICES FROM THE PRIMES
                    self.curTriangle.set_C(pNi) 
                    self.curTriangle.set_B(pNf)

                # ADD DRONE INITIAL PATH POINT TO THE PATH LIST
                path.append(pi)
                # ADD DRONE FINAL PATH POINT TO THE PATH LIST
                path.append(pf)
                # SET DRONE POSITION TO THE DRONE FINAL PATH POINT
                self.drone.curPoint = pf

                
                # SUBSTRACT THE DISTANCE TRAVELED FROM THE CURMAX_DISTANCE
                self.drone.curMax_distance -= dist_curPos_pi + dist_pi_pf
                # ADD THE DISTANCE TRAVELED TO THE DRONE TOTAL_DISTANCE_TRAVEL
                self.drone.total_distance_travel += dist_curPos_pi + dist_pi_pf

            # SINCE DRONE CANNOT TRAVEL, THEN IT MUST RETURN TO CHARGING STATION
            else:

                # IF I AM ON VERTEX A AND I CANNOT TRAVEL, THEN TERMINATE ALGORITHM
                # REASON: THE ONLY TIME THE DRONE IS IN THIS POINT IS WHEN COMING FROM THE CHARGING STATION
                if(start_end == [1,2]):
                    return path
                    #return None

                # IF DRONE IS IN B, THEN WE MUST GO FROM B TO A
                if(start_end == [2,3]):
                    # GET THE DRONE INITIAL PATH POINT AND DRONE FINAL PATH POINT
                    pi,pf = self.segment_AB(reverse = True , info = "path")
                    
                    pNi,pNf = self.segment_AB(reverse = True , info = "prime")         

                    self.curTriangle.set_A(pNf) 
                    self.curTriangle.set_B(pNi)
                
                # IF DRONE IS IN C, THEN WE MUST GO FROM C TO A
                elif(start_end == [3,2]):
                    # GET THE DRONE INITIAL PATH POINT AND DRONE FINAL PATH POINT
                    pi,pf = self.segment_AC(reverse = True , info = "path")
                    # GET C PRIME AND B PRIME POINTS
                    pNi,pNf = self.segment_AC(reverse = True , info = "prime")     

                    # SET THE NEW VERTICES FROM THE PRIMES
                    self.curTriangle.set_A(pNf) 
                    self.curTriangle.set_C(pNi)                      

                # DISTANCE FROM CURRENT POSITION TO DRONE INITIAL PATH POINT
                dist_curPos_pi = self.dist(self.drone.curPoint , pi)
                # DISTANCE FROM DRONE INITIAL PATH POINT TO DRONE FINAL PATH POINT
                dist_pi_pf = self.dist(pi,pf)  
                # DISTANCE FROM DRONE FINAL PATH POINT TO CHARGING STATION
                dist_pf_CS = self.dist(pf,CS)

                # ADD DRONE INITIAL PATH POINT TO THE PATH LIST
                path.append(pi)
                # ADD DRONE FINAL PATH POINT TO THE PATH LIST
                path.append(pf)
                # ADD CHARGING STATION POINT TO THE PATH LIST
                path.append(CS)

                # SET DRONE POSITION TO THE DRONE FINAL PATH POINT
                self.drone.curPoint = CS
                # RESET THE INDEX BACK TO 1
                loc_i = 1

                # RESET THE CURMAX_DISTANCE TO THE DRONE MAX DISTANCE
                self.drone.curMax_distance = self.drone.MAX_DISTANCE
                # ADD THE DISTANCE TRAVELED TO THE DRONE TOTAL_DISTANCE_TRAVEL
                self.drone.total_distance_travel += dist_curPos_pi + dist_pi_pf + dist_pf_CS


        return path


























