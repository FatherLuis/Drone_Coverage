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


column_names = ['Shape','N_Gon','Shape_Area','CS_Radius','num_Candidates','num_Charging_Station',
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

# SQUARES
squareName = 'Square'
square1 = [ (0,0) , (0,5) , (5,5) , (5,0)]
square2 = [ (0,0) , (0,7.0711) , (7.0711,7.0711) , (7.0711,0)]
square3 = [ (0,0) , (0,10) , (10,10) , (10,0)]



# RECTANGLES
rectName = 'Rectangle'
rect1 = [ (0,0) , (0,2.8868) , (8.6603,2.8868), (8.6603,0) ]
rect2 = [ (0,0) , (0,4.0825) , (12.2474,4.0825), (12.2474,0)]
rect3 = [ (0,0) , (0,5.7735) , (17.3205,5.7735), (17.3205,0)]



# OCTAGONS
octName = 'Octagon'
oct1 = [ (0,0) , (2.2754,0) , (3.8844,1.609) , (3.8844,3.8844) , (2.2754,5.4934) , (0,5.4934) , (-1.609,3.8844), (-1.609,1.609) ]
oct2 = [ (0,0) , (3.218,0) , (5.4934,2.2754) , (5.4934,5.4934) , (3.218,7.7689) , (0,7.7689) , (-2.2754,5.4934) , (-2.2754,2.2754) ]
oct3 = [ (0,0) , (4.5509,0) , (7.7689,3.218) , (7.7689,7.7689) , (4.5509,10.9868) , (0,10.9869) , (-3.218,7.7689) , (-3.218,3.218) ]


fields = [square1,square2,square3,
          rect1,rect2,rect3,
          oct1,oct2,oct3]


names = [squareName,squareName,squareName,
         rectName,rectName,rectName,
         octName,octName,octName]

n_trials = 2




for name,field in zip(names,fields):

    curShape = geometry.Polygon(field)
    
    
    # FOR EVERY SQ, THERE IS 1 CANDIDATE
    shape_area = round(curShape.area)
    cand = shape_area 
       
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
                
        
                df = df.append({'Shape': name,
                                'N_Gon': len(field),
                                'Shape_Area': shape_area ,
                                'CS_Radius': mdv,
                                'num_Candidates':cand,
                                'num_Charging_Station':lst[0],
                                'Total_Time': tot_time,
                                'Total_Distance_Travel': lst[1]},
                              ignore_index = True)
    
            
    
            except:
    
                df = df.append({'Shape': name,
                                'N_Gon': len(field),
                                'Shape_Area':curShape.area,
                                'CS_Radius': mdv,
                                'num_Candidates':cand,
                                'num_Charging_Station':0,
                                'Total_Time': 0,
                                'Total_Distance_Travel': 0},
                              ignore_index = True)
    
    
                  
                print(traceback.format_exc())



#####################################
### SAVE RAW PANDA DATAFRAME AS CSV FILE 
#####################################
now = datetime.now() # current date and time
date_time = now.strftime("%m_%d_%Y__%H_%M_%S")



directory = './data/'

filename = '{}_{}.csv'.format('Test_Data',date_time)

file_path = os.path.join(directory, filename)

if not os.path.isdir(directory):
    os.mkdir(directory)

df.to_csv(file_path)



#######################################
### SAVE SUMMARY STATS 
### PANDA DATAFRAME AS CSV FILE 
#######################################


summary_df = df.groupby(['Shape',
                         'N_Gon',
                         'Shape_Area',
                         'CS_Radius',
                         'num_Candidates']).agg(['mean', 'std']).round(2)


filename = '{}_{}.csv'.format('Test_Data_Summary',date_time)

file_path = os.path.join(directory, filename)

if not os.path.isdir(directory):
    os.mkdir(directory)

summary_df.to_csv(file_path)

                













    


























