# -*- coding: utf-8 -*-

from Drone import Drone

class ChargingPad():
    
    
    def __init__(self, voltage):
        
        self.voltage = voltage
        
        
    def charge_drone(self,drone ):
        
        # CALCULATE TIME FLYING
        
        distance_travel = (drone.MAX_DISTANCE - drone.curMax_distance )
        
        time_flying = distance_travel / drone.velocity 
        
        # CALCULATE TIME CHARGING
        # figure out calculations later
        time_charging = 0
        
        
        drone.total_time += time_flying + time_charging
        
        drone.curMax_distance = drone.MAX_DISTANCE
        
        
        