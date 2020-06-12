from Triangle import Triangle
from Drone import Drone
import numpy as np 
from Utilities import dist



########################################
# Class name: self.drone_Path()
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
    # Parameter: Triangle Object, self.drone Object
    # Method used: None
    # Return Value: None
    # Date:  3/2/2020
    ##############################################
    def __init__(self,triangle,drone,entry_exit):

        self.triangle = triangle # SAVES THE ORIGINAL TRIANGLE IN WHICH THE ALGORITHM WILL THE FIND THE PATH TO
        self.curTriangle = triangle.copy()
        self.drone = drone
        self.entryExit = np.array(entry_exit)
        
        self.locStart = []
        self.farNode = ''

    ##############################################
    # Method Name: segment_AB
    # Purpose: Contains the computations needed to calculate the next path/prime_vertex from point A to point B
    # Parameter: reverse: dictate if you're going from A to B or B to A
    #            info: determines what the method is returning (path,prime)
    # Method used: None
    # Return Value: two points are returned (x,y)
    # Date:  3/2/2020
    ##############################################
    def segment_AB(self,vertexA = None , vertexB = None ,reverse = False, info = "path"):
        


        if(vertexA is None):

            vertexA = self.curTriangle.A

        if(vertexB is None):

            vertexB = self.curTriangle.B

        ### Calculate path of self.drone ###
        
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
    def segment_BC(self,vertexB = None , vertexC = None , reverse = False, info = "path"):
            
       
        if(vertexB is None):

            vertexB = self.curTriangle.B


        if(vertexC is None):

            vertexC = self.curTriangle.C      
        
        
        ### Calculate path of self.drone ###

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
    def segment_AC(self,vertexA = None , vertexC = None , reverse = False, info = "path"):


        if(vertexA is None):

            vertexA = self.curTriangle.A


        if(vertexC is None):

            vertexC = self.curTriangle.C


            ### Calculate path of self.drone ###
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





    def reserve_path(self):


        for p in self.entryExit:
            
            if self.farNode == 'BC':

                if( np.allclose(p,self.triangle.B)  ):
    
                        pNi, pNf = self.segment_AB(info = 'path')
                        self.elim_edges('AB', pNi, pNf)
    
    
                elif( np.allclose(p,self.triangle.C) ):
    
                        pNi, pNf = self.segment_AC(info = 'path')
                        self.elim_edges('AC', pNi, pNf)
                        
            else:
                
                if( np.allclose(p,self.triangle.A)  ):
    
                        pNi, pNf = self.segment_AC(info = 'path',reverse = True)
                        self.elim_edges('CA', pNi, pNf)
    
                        
                elif( np.allclose(p,self.triangle.B)  ):
    
                        pNi, pNf = self.segment_BC(info = 'path', reverse = True)
                        self.elim_edges('CB', pNi, pNf)
             








    def calculate_path(self,loct=None, pNi = None, pNf = None,req = 'path'):
        
        
        
        
        if loct == 'AB':
            
            return self.segment_AB(reverse = False , info = req)
            
        elif loct == 'BA':
            
            return self.segment_AB(reverse = True , info = req)
            
        elif loct == 'AC':
            
            return self.segment_AC(reverse = False , info = req)
        
        elif loct == 'CA':
            
            return self.segment_AC(reverse = True , info = req)
            
        elif loct == 'BC':
            
            return self.segment_BC(reverse = False , info = req)
            
        elif loct == 'CB':
            
            return self.segment_BC(reverse = True , info = req)
        
        elif loct == 'AA':
            
            #print("Could not Travel to B")
            return None            
        else:
            print('Bad Loc Argument')
            return  None
        
        
        
        
    def elim_edges(self,loct, pNi, pNf):
        
        loc = None
        
        if( loct == 'AB' ):
            
            loc = 'BC' if self.farNode == 'BC' else 'BA'
            
            self.curTriangle.set_A(pNi)
            self.curTriangle.set_B(pNf)
            
            
        elif( loct == 'BA' ):
            
            loc = 'AB'  
            self.curTriangle.set_B(pNi)
            self.curTriangle.set_A(pNf)            
            
        elif( loct == 'AC' ):
            
            loc = 'CB' if self.farNode == 'BC' else 'CB'   
            self.curTriangle.set_A(pNi)
            self.curTriangle.set_C(pNf)            
            
        elif( loct == 'CA' ):
            
            loc = self.locStart if self.farNode == 'BC' else 'AB'  
            self.curTriangle.set_C(pNi)
            self.curTriangle.set_A(pNf)            
            
        elif( loct == 'BC' ):
            
            loc = 'CB' if self.farNode == 'BC' else self.locStart  
            self.curTriangle.set_B(pNi)
            self.curTriangle.set_C(pNf)            
            
        elif( loct == 'CB' ):
            
            loc = 'BC' if self.farNode == 'BC' else 'BA'        
            self.curTriangle.set_C(pNi)
            self.curTriangle.set_B(pNf)        
        else:
            print('elim_edges: Something is wrong')
            
        return loc
        
        
        

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


        return  (self.drone.radius >= dist(centroid,self.curTriangle.A) and 
               self.drone.radius >= dist(centroid,self.curTriangle.B) and 
               self.drone.radius >= dist(centroid,self.curTriangle.C) )




    def inBound(self,loc,pi,pNi,pf,pNf):
     
        A = self.curTriangle.A
        B = self.curTriangle.B
        C = self.curTriangle.C     
        
        endAlg = False
     
        if loc == 'AB':
            

            bound_init = lambda x: (A[0] <= x[0]) and (x[0] <= C[0]) and (A[1] <= x[1]) and (x[1] <= C[1])            
            bound_final = lambda x: (B[0] <= x[0]) and (x[0] <= C[0]) and (C[1] <= x[1]) and (x[1] <= B[1])        
        
           
            if not(bound_init(pi) and bound_init(pNi)):
                
                endAlg = True
                
                delX = 0.5*(C[0]-A[0])
                delY = 0.5*(C[1]-A[1])
                
                pi = np.array([ A[0]+delX , A[1]+delY ])
                
            if not(bound_final(pf) and bound_final(pNf)):
                
                endAlg = True
                
                delX = 0.5*(C[0]-B[0])
                delY = 0.5*(B[1]-C[1])
                
                pf = np.array([ B[0]+delX , B[1]-delY ])               
                
        elif loc == 'BA':
            

            bound_init = lambda x: (B[0] <= x[0]) and (x[0] <= C[0]) and (C[1] <= x[1]) and (x[1] <= B[1])             
            bound_final = lambda x: (A[0] <= x[0]) and (x[0] <= C[0]) and (A[1] <= x[1]) and (x[1] <= C[1])       
        
           
            if not(bound_init(pi) and bound_init(pNi)):
                
                endAlg = True
 
                
                delX = 0.5*(C[0]-B[0])
                delY = 0.5*(B[1]-C[1])
                
                pi = np.array([ B[0]+delX , B[1]-delY ])                                
                
            if not(bound_final(pf) and bound_final(pNf)):
                
                endAlg = True
                
                delX = 0.5*(C[0]-A[0])
                delY = 0.5*(C[1]-A[1])
                
                pf = np.array([ A[0]+delX , A[1]+delY ])              


        elif loc == 'BC':
            

            bound_init = lambda x: (A[1] <= x[1]) and (x[1] <= B[1])            
            bound_final = lambda x: (A[0] <= x[0]) and (x[0] <= C[0]) and (A[1] <= x[1]) and (x[1] <= C[1])        
        
           
            if not(bound_init(pi) and bound_init(pNi)):
                
                endAlg = True

                delY = 0.5*(B[1]-A[1])
                
                pi = np.array([ A[0], A[1]+delY ])
                
            if not(bound_final(pf) and bound_final(pNf)):
                
                endAlg = True
                
                delX = 0.5*(C[0]-A[0])
                delY = 0.5*(C[1]-A[1])
                
                pf = np.array([ A[0]+delX , A[1]+delY ])   
                
                
        elif loc == 'CB':     
            
            bound_init = lambda x: (A[0] <= x[0]) and (x[0] <= C[0]) and (A[1] <= x[1]) and (x[1] <= C[1])
            bound_final = lambda x: (A[1] <= x[1]) and (x[1] <= B[1])
            
            
            if not(bound_init(pi) and bound_init(pNi)):
                
                endAlg = True
                
                delX = 0.5*(C[0]-A[0])
                delY = 0.5*(C[1]-A[1])
                
                pi = np.array([ A[0]+delX , A[1]+delY ])   
                
            
            if not(bound_final(pf) and bound_final(pNf)):
                
                endAlg = True

                delY = 0.5*(B[1]-A[1])
                
                pf = np.array([ A[0], A[1]+delY ])            
            
            
        elif loc == 'AC':     
            
            bound_init = lambda x: (A[1] <= x[1]) and (x[1] <= B[1])
            bound_final = lambda x: (B[0] <= x[0]) and (x[0] <= C[0]) and (C[1] <= x[1]) and (x[1] <= B[1])
            
            
            if not(bound_init(pi) and bound_init(pNi)):
                
                endAlg = True

                delY = 0.5*(B[1]-A[1])
                
                pi = np.array([ A[0] , A[1]+delY ])   
                
            
            if not(bound_final(pf) and bound_final(pNf)):
                
                endAlg = True

                delX = 0.5*(C[0]-B[0])
                delY = 0.5*(B[1]-C[1])
                
                pf = np.array([ B[0]+delX, B[1]-delY ])             
            
            
        elif loc == 'CA':             
            
            bound_init = lambda x: (B[0] <= x[0]) and (x[0] <= C[0]) and (C[1] <= x[1]) and (x[1] <= B[1])
            bound_final = lambda x: (A[1] <= x[1]) and (x[1] <= B[1])
            
            
            if not(bound_init(pi) and bound_init(pNi)):
                
                endAlg = True

                delX = 0.5*(C[0]-B[0])
                delY = 0.5*(B[1]-C[1])
                
                pi = np.array([ B[0]+delX, B[1]-delY ])               
            
            
            if not(bound_final(pf) and bound_final(pNf)):
                
                endAlg = True

                delY = 0.5*(B[1]-A[1])
                
                pf = np.array([ A[0] , A[1]+delY ])            


        return endAlg, pi, pf

    ##############################################
    # Method Name: algorithm()
    # Purpose: creates the path needed to cover a triangle, given the limitations of the self.drone
    # Parameter: None
    # Method used: dist() , isCoverable()
    # Return Value: Float
    # Date:  3/2/2020
    #        3/27/2020: Redid Code for easier understanding and opmimal code
    ##############################################  
    def algorithm(self,chargingStation):

        loc = None

        # CS: CHARGING STATION
        CS = None
        
        
        if chargingStation == 'A':
            
            CS = self.triangle.A
            
            loc = 'AB' if(self.triangle.AB_dist > self.triangle.AC_dist) else 'AC'
            
            self.locStart = loc
            self.farNode = 'BC'
            
        elif chargingStation == 'C':        
        
            CS = self.triangle.C
            loc = 'CB' if(self.triangle.BC_dist > self.triangle.AC_dist) else 'CA'
            
            self.locStart = loc
            self.farNode = 'AB'
            
        else:
            print('Wrong CS Char')
        
        
        self.drone.curPoint = CS
        
        # Store paths
        path = [self.drone.curPoint] 
        
        
        
        ## 5/12/2020 Reserve Paths
        self.reserve_path()
        
        
        total_distance_travel_copy = self.drone.total_distance_travel

        path1 = self.next_step(CS,loc)
        
        
        if(len(path1)==0 or path1 is None):
            self.drone.total_distance_travel = total_distance_travel_copy
            return self.drone,[]
        
        return self.drone,path+path1 










    ##############################################
    # Method Name: algorithm()
    # Purpose: creates the path needed to cover a triangle, given the limitations of the self.drone
    # Parameter: None
    # Method used: dist() , isCoverable()
    # Return Value: Float
    # Date:  3/2/2020
    #        3/27/2020: Redid Code for easier understanding and opmimal code
    ##############################################  
    def next_step(self,CS,loc):

        req_dist_travel = 0

        # should be a list or None
        futurePath = []
        
        # Store paths
        path = []


        pi = None
        pf = None
        pNi = None
        pNf = None
          
            
        if all(self.drone.curPoint == CS):
            # charge
            self.drone.curMax_distance = self.drone.MAX_DISTANCE
            
            loc = self.locStart
                    
        
        # Check if I can cover 
        if(self.isCoverable()):
            
            # self.drone INITIAL PATH POINT
            pi = self.curTriangle.centroid
            # self.drone FINAL PATH POINT
            pf = CS
                
            # DISTANCE FROM CURRENT POSITION TO self.drone INITIAL PATH POINT
            dist_curPos_pi = dist(self.drone.curPoint , pi)

            # DISTANCE FROM self.drone INITIAL PATH POINT TO self.drone FINAL PATH POINT(CHARGING STATION)
            dist_pi_pf = dist(pi,pf)                
            

            # ADD ALL THE DISTANCES TOGETHER
            req_dist_travel = dist_curPos_pi + dist_pi_pf 
            
            
            
            

            if(self.drone.curMax_distance >= req_dist_travel): 
                
                self.drone.curMax_distance -= req_dist_travel
                
                # ADD self.drone INITIAL PATH POINT TO THE PATH LIST
                path.append(pi)
                # ADD self.drone FINAL PATH POINT TO THE PATH LIST
                path.append(pf)                
                # ADD CHARGING STATION POINT TO THE PATH LIST
        
                self.drone.total_distance_travel += req_dist_travel
                self.drone.curPoint = CS
                return path


        # Try going to the next Location
        try:
            
            pi,pf = self.calculate_path(loct = loc, req = 'path')
            
            pNi, pNf = self.calculate_path(loct = loc, req = 'prime')
            
            endAlg, pi, pf = self.inBound(loc,pi,pNi,pf,pNf)

            
            # DISTANCE FROM CURRENT POSITION TO self.drone INITIAL PATH POINT
            dist_curPos_pi = dist(self.drone.curPoint , pi)
            # DISTANCE FROM self.drone INITIAL PATH POINT TO self.drone FINAL PATH POINT
            dist_pi_pf = dist(pi,pf)  


            if not(endAlg):
                
                req_dist_travel = dist_curPos_pi + dist_pi_pf
                
                
                if(self.drone.curMax_distance >= req_dist_travel):    
        
                    # ADD self.drone INITIAL PATH POINT TO THE PATH LIST
                    path.append(pi)
                    # ADD self.drone FINAL PATH POINT TO THE PATH LIST
                    path.append(pf)
                    # ADD THE DISTANCE TRAVELED TO THE self.drone TOTAL_DISTANCE_TRAVEL
                    self.drone.total_distance_travel += req_dist_travel
                    
                    
    
                    
                    self.drone.curMax_distance -= req_dist_travel
                    self.drone.curPoint = pf   
                    
    
    
                    loc = self.elim_edges(loc, pNi, pNf)      
                    
                
                    drone_copy = self.drone.copy()          
                    curTriangle_copy = self.curTriangle.copy()
                
                
                    futurePath = self.next_step(CS,loc)
                                  
                    if len(futurePath) == 0 :
                        self.drone = drone_copy
                        self.curTriangle = curTriangle_copy
            else:
                
                dist_pf_CS = dist(pf,CS)
 
                req_dist_travel = dist_curPos_pi + dist_pi_pf + dist_pf_CS
                
                
                if(self.drone.curMax_distance >= req_dist_travel):    
        
                    # ADD self.drone INITIAL PATH POINT TO THE PATH LIST
                    path.append(pi)
                    # ADD self.drone FINAL PATH POINT TO THE PATH LIST
                    path.append(pf)           
                    # ADD CHARGING STATION POINT TO THE PATH LIST
                    path.append(CS)
                    # ADD THE DISTANCE TRAVELED TO THE self.drone TOTAL_DISTANCE_TRAVEL
                    self.drone.total_distance_travel += req_dist_travel
                    
                
                    self.drone.curMax_distance -= req_dist_travel
                    self.drone.curPoint = CS  
                    #print('Alg End Reach OOB')
                    return path

        except:
            print('Return None')
            
            return []
        
    

    
        if len(futurePath) == 0 :
     
            # Try to Return to CS
            
            
            loc = loc[0]+'A' if self.farNode == 'BC' else loc[0]+'C'
            

            try:         
                
                pi,pf = self.calculate_path(loct = loc, req = 'path')
            
                pNi, pNf = self.calculate_path(loct = loc, req = 'prime')   
                
                
                endAlg, pi, pf = self.inBound(loc,pi,pNi,pf,pNf)
                
                
                # DISTANCE FROM CURRENT POSITION TO self.drone INITIAL PATH POINT
                dist_curPos_pi = dist(self.drone.curPoint , pi)
                # DISTANCE FROM self.drone INITIAL PATH POINT TO self.drone FINAL PATH POINT
                dist_pi_pf = dist(pi,pf)  
                # DISTANCE FROM self.drone FINAL PATH POINT TO CHARGING STATION
                dist_pf_CS = dist(pf,CS)

                req_dist_travel = dist_curPos_pi + dist_pi_pf + dist_pf_CS
                
    

                if(self.drone.curMax_distance >= req_dist_travel):    
                    
                    
                        
                    loc = self.elim_edges(loc, pNi, pNf)
    
                    
                    # ADD self.drone INITIAL PATH POINT TO THE PATH LIST
                    path.append(pi)
                    # ADD self.drone FINAL PATH POINT TO THE PATH LIST
                    path.append(pf)                
                    # ADD CHARGING STATION POINT TO THE PATH LIST
                    path.append(CS)
                    # ADD THE DISTANCE TRAVELED TO THE self.drone TOTAL_DISTANCE_TRAVEL
                    self.drone.total_distance_travel += req_dist_travel
                    self.drone.curMax_distance -= req_dist_travel
                    self.drone.curPoint = CS 
                    
                    if not(endAlg):
                        return path+self.next_step(CS,loc)
                    else:
                        print('Alg End: No more Travels')
                        return path

               
            except:
                #print('Could Not Return to CS')
                return []




                
            else:
                #print("Can't Go Back Home")
                return []
    
        return path+futurePath

                
                





if __name__ == '__main__':

    from Draw import Draw
    
    canvas = Draw()

    rad = 0.5
    mxDist = 1000 # MUST BE ABLE TO REACH A VERTEX AND RETURN TO CHARGING STATION 250
    drone = Drone(radius=rad, max_distance = mxDist)    
    
    
    entryExit = [ (0,0) , (0,30)]
    
    pp= [ (0., 0.),(0, 30),(10, 7)]
    
    #pp = [ (0,0), (0,33) , (30,20) ]   
    
    triangle = Triangle(*pp)
    
    #print('\n',triangle)
    
    curCS = 'C'
    
    DP = Drone_Path(triangle,drone,entryExit)  
    
   
    drone, path = DP.algorithm(curCS)

    print(drone)
    


    canvas.boundary(pp)

    canvas.path(path)

    canvas.show_plot()









