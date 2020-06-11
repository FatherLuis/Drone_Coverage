import pandas as pd
import numpy as np
from shapely import geometry 
from datetime import datetime
from RUN import run_program


# Create a Panda Dataframe 

column_names = ['N_Gon','Shape_Area','CS_MaxRadius','num_Charging_Station',
                'Total_Time','Total_Distance_Travel']


df = pd.DataFrame(columns = column_names)


#### Drone Properties
#
drone_max_range = 8
drone_cov_rad = 0.05


### Charging Station Properties

# Max Charging Station distance
Max_Dist_Vertex = [2.5,3.5]


### SHAPE ###
# Square
square1 = [ (0,0) , (0,7) , (7,7) , (7,0)]
#square2 = [ (0,0) , (0,200) , (200,200) , (200,0)]
#poly3 = [ (0,0) , (0,200) , (100,300) , (200,200) , (200,0)]

fields = [square1]
candidates = [25]

for cand,field in zip(candidates,fields):
    
    curShape = geometry.Polygon(field)
    
    
    for mdv in  Max_Dist_Vertex:
        
        try:
            lst = run_program(drone_rad = drone_cov_rad , 
                        drone_maxDist = drone_max_range , 
                        max_CS_dist = mdv, 
                        shape = square1,
                        candidate = cand,
                        showPlot = False)
            
            # lst is 'num_Charging_Station','Total_Time','Total_Distance_Travel'
            
            
            
    
            df = df.append({'N_Gon': len(field),
                            'Shape_Area':curShape.area,
                            'CS_MaxRadius': mdv,
                            'num_Charging_Station':lst[0],
                            'Total_Time': lst[1],
                            'Total_Distance_Travel': lst[2]},
                          ignore_index = True)

        

        except:
            print('\n','No Bueno','\n')


now = datetime.now() # current date and time
date_time = now.strftime("%m_%d_%Y___%H_%M_%S")

df.to_csv('data\{}_{}.csv'.format('Test_Data',date_time))
    


























