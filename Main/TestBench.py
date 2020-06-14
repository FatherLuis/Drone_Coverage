import pandas as pd
import numpy as np
from Drone import Drone
from shapely import geometry 
from datetime import datetime
from RUN import run_program
from ChargingPad import ChargingPad
import traceback


# Create a Panda Dataframe 

column_names = ['N_Gon','Shape_Area','CS_Radius','num_Candidates','num_Charging_Station',
                'Total_Time','Total_Distance_Travel']


df = pd.DataFrame(columns = column_names)


 ### INITIALIZE DRONE PROPERTIES ###

rad = 0.025
mxDist = 8
velocity = 25
 

# Initialize Charging Pad
volt = 25
cPad = ChargingPad(volt)

### Charging Station Properties

# Max Charging Station distance
CS_radius = [2.5] #,3.5]


### SHAPE ###
# Square
square1 = [ (0,0) , (0,7) , (7,7) , (7,0)]
#square2 = [ (0,0) , (0,10) , (10,10) , (10,0)]
#poly3 = [ (0,0) , (0,200) , (100,300) , (200,200) , (200,0)]

fields = [square1]
candidates = [25]


n_trials = 50
for i in range(n_trials):
    for cand,field in zip(candidates,fields):
    
        
        drone = Drone(radius=rad, max_distance = mxDist, velocity = velocity)  
        curShape = geometry.Polygon(field)
        
        
        for mdv in CS_radius:
            
            try:

                lst = run_program( drone = drone,
                                  cPad = cPad,
                                  CS_radius = mdv, 
                                  shape = field,
                                  candidate = cand,
                                  showPlot = False)
                
                # lst is ['num_Charging_Station','Total_Time','Total_Distance_Travel']
                
        
                df = df.append({'N_Gon': len(field),
                                'Shape_Area':curShape.area,
                                'CS_Radius': mdv,
                                'num_Candidates':cand,
                                'num_Charging_Station':lst[0],
                                'Total_Time': lst[1],
                                'Total_Distance_Travel': lst[2]},
                              ignore_index = True)
    
            
    
            except:
    
                df = df.append({'N_Gon': len(field),
                                'Shape_Area':curShape.area,
                                'CS_Radius': mdv,
                                'num_Candidates':cand,
                                'num_Charging_Station':0,
                                'Total_Time': 0,
                                'Total_Distance_Travel': 0},
                              ignore_index = True)
    
    
                  
                print(traceback.format_exc())
    


now = datetime.now() # current date and time
date_time = now.strftime("%m_%d_%Y___%H_%M_%S")

df.to_csv('data\{}_{}.csv'.format('Test_Data',date_time))
    


























