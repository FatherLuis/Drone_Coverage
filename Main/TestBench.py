import pandas as pd
import numpy as np
from Drone import Drone
from shapely import geometry 
from datetime import datetime
from RUN import run_program
import traceback
import os.path

#####################################
# CREATE PANDA DATAFRAME
#####################################


column_names = ['N_Gon','Shape_Area','CS_Radius','num_Candidates','num_Charging_Station',
                'Total_Time','Total_Distance_Travel']


df = pd.DataFrame(columns = column_names)


#####################################
### INITIALIZE DRONE PROPERTIES ###
#####################################


rad = 0.025
mxDist = 8
velocity = 25
 
start = np.array([0, 0])

#####################################
### Charging Station Properties ###
#####################################

# Max Charging Station distance
CS_radius = [2.5,3.5]



#####################################
### SHAPE ###
#####################################

# Rectangle
square1 = [ (0,0) , (0,5) , (5,5) , (5,0)]
square2 = [ (0,0) , (0,5) , (10,5) , (10,0)]
square3 = [ (0,0) , (0,10) , (10,10) , (10,0)]


# Octagon
oct1 = [ (0,0),(2.28,0),(3.88,1.61),(3.88,3.88),(2.28,5.49),(0,5.49),(-1.61,3.88),(-1.61,1.61) ]
oct2 = [ (0,0), (3.22,0), (5.49,2.28), (5.49,5.49), (3.22,7.77), (0,7.77), (-2.28,5.49), (-2.28,2.28)  ]
oct3 = [ (0,0), (4.55,0), (7.77,3.22), (7.77,7.77), (4.55,10.99), (0,10.99), (-3.22,7.77), (-3.22,3.22)  ]


fields = [square1,square2,square3,oct1,oct2,oct3]

n_trials = 1




for field in fields:

    curShape = geometry.Polygon(field)
    
    # FOR EVERY SQ, THERE IS 1 CANDIDATE
    cand = int(np.ceil(curShape.area))
       
    for mdv in CS_radius:
        
        drone = Drone(radius=rad, max_distance = mxDist)  
        
        for i in range(n_trials):
            try:
                
                # lst is ['num_Charging_Station','Total_Distance_Travel']
                lst = run_program( drone = drone,
                                  CS_radius = mdv, 
                                  shape = field,
                                  candidate = cand,
                                  sp = start,
                                  showPlot = False)
                
                
                tot_time = 3*(lst[1] / velocity)
                
        
                df = df.append({'N_Gon': len(field),
                                'Shape_Area':curShape.area,
                                'CS_Radius': mdv,
                                'num_Candidates':cand,
                                'num_Charging_Station':lst[0],
                                'Total_Time': tot_time,
                                'Total_Distance_Travel': lst[1]},
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



#####################################
### SAVE PANDA DATAFRAME AS CSV FILE 
#####################################


now = datetime.now() # current date and time
date_time = now.strftime("%m_%d_%Y___%H_%M_%S")


directory = './data/'
filename = '{}_{}.csv'.format('Test_Data',date_time)

file_path = os.path.join(directory, filename)

if not os.path.isdir(directory):
    os.mkdir(directory)

df.to_csv(file_path)










    


























