import math 

class Drone:

    def __init__(self,radius=1, max_distance = 10000):
        self.radius= radius
        self.max_distance = max_distance
        self.curMax_distance = max_distance 
        self.total_distance_travel = 0
        self.curPoint = (0,0)


    def calculate_area(self):
        return math.pi * self.radius ** 2

    







