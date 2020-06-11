import numpy as np

########################################
# Class name: Draw()
# Class Author: Luis E. Vargas Tamayo
# Purpose of the class: Create an object that has Drone attributes that affect the path algorithm
# Date: 3/2/2020
# List of changes with dates: none
########################################
class Drone:

    ##############################################
    # Method Name: __init__
    # Purpose: Class Constructor
    # Parameter: None
    # Method used: None
    # Return Value: None
    # Date:  3/2/2020
    ##############################################
    def __init__(self,radius=1, max_distance = 10000):
        self.radius= radius
        self.MAX_DISTANCE = max_distance
        self.total_distance_travel = 0

        self.curMax_distance = max_distance 
        self.curPoint = np.array( (0,0) )

    ##############################################
    # Method Name: calculate_area
    # Purpose: Calculate the area covered by the dron (pi*r^2)
    # Parameter: None
    # Method used: None
    # Return Value: None
    # Date:  3/2/2020
    # 3/27/2020 : METHOD NO LONGER BEING USED
    ##############################################
    def calculate_area(self):
        return np.pi * self.radius ** 2



    def copy(self):
        
        drone = Drone(self.radius,self.MAX_DISTANCE)
        drone.total_distance_travel = self.total_distance_travel
        drone.curMax_distance = self.curMax_distance
        drone.curPoint = self.curPoint
        
        return drone
        
        

    ##############################################
    # Method Name: __str__()
    # Purpose: overrides the default print() method used on this object. When print() is used, information of the drone info is printed
    # Parameter: None
    # Method used: None
    # Return Value: None
    # Date:  3/16/2020
    ##############################################
    def __str__(self):
        str_DR = "Drone Radius: {}".format(self.radius)
        str_MD = "Max Distance to Travel: {}".format(self.MAX_DISTANCE)
        str_TDT = "Total Distance Travel: {}".format(self.total_distance_travel)

        return "{}\n{}\n{}\n".format(str_DR,str_MD,str_TDT) 




