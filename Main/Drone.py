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
        self.max_distance = max_distance
        self.curMax_distance = max_distance 
        
        self.total_distance_travel = 0
        self.curPoint = np.array( (0,0) )

    ##############################################
    # Method Name: calculate_area
    # Purpose: Calculate the area covered by the dron (pi*r^2)
    # Parameter: None
    # Method used: None
    # Return Value: None
    # Date:  3/2/2020
    ##############################################
    def calculate_area(self):
        return np.pi * self.radius ** 2

    







