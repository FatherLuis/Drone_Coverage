import pandas as pd
import numpy as np
from Drone import Drone
from shapely import geometry 
from datetime import datetime
from RUN import run_program
import traceback
import os.path
import matplotlib.pyplot as plt

#####################################
# CREATE PANDA DATAFRAME
#####################################



column_names = ['Shape',
                'N_Gon',
                'Shape_Area',
                'CS_Radius',
                'numCandidates',
                'numChargingStation',
                'Total_Time',
                'Total_Distance_Travel',
                'isSuccessful']





df = pd.DataFrame(columns = column_names)


df = df.astype({'Shape':'string',
           'N_Gon': 'int64',
           'Shape_Area': 'int64',
           'CS_Radius':'float64',
           'numCandidates':'int64',
           'numChargingStation': 'int64',
           'Total_Time':'float64',
           'Total_Distance_Travel':'float64',
           'isSuccessful': 'int64'})










#####################################
### INITIALIZE DRONE PROPERTIES 
#####################################


rad = 0.025
mxDist = 8
velocity = 25
 
start = np.array([0, 0])


#####################################
### Charging Station Properties 
#####################################

# Charging Station Coverage distance
CS_radius = [2.0,2.5,3.0,3.5,4.0]



#####################################
### SHAPE 
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


fields = [square1,
          square2,
          square3,
            rect1,
            rect2,
            rect3,
            oct1,
            oct2,
            oct3]


names = [squareName,
         squareName,
         squareName,
            rectName,
            rectName,
            rectName,
            octName,
            octName,
            octName]



# HOW MANY TIMES DO YOU WANT TO RUN EACH CONFIGURATION
n_trials = 1



# START TEST BENCH
for name,field in zip(names,fields):

    curShape = geometry.Polygon(field)
    
    
    # FOR EVERY SQ, THERE IS 1 CANDIDATE
    shape_area = round(curShape.area)
    cand = shape_area 
       
    for mdv in CS_radius:
        
        drone = Drone(radius=rad, max_distance = mxDist)  
        
        i = 0
        while( i < n_trials):
            try:
                
                # lst is ['num_Charging_Station','Total_Distance_Travel']
                lst = run_program( drone = drone,
                                  CS_radius = mdv, 
                                  shape = field,
                                  candidate = cand,
                                  sp = start,
                                  showPlot = False)
                
                
                # CALCULATE TOTAL TIME BASED ON DRONE
                # VELOCITY AND THEO. CHARGING TIME
                tot_time = 3*(lst[1] / velocity)
                
                
        
                df = df.append({'Shape': name,
                                'N_Gon': len(field),
                                'Shape_Area': shape_area ,
                                'CS_Radius': mdv,
                                'numCandidates': cand,
                                'numChargingStation':lst[0],
                                'Total_Time': tot_time,
                                'Total_Distance_Travel': lst[1],
                                'isSuccessful': 1},
                              ignore_index = True)
    
                i+= 1
    
            except:
    
                df = df.append({'Shape': name,
                                'N_Gon': len(field),
                                'Shape_Area':curShape.area,
                                'CS_Radius': mdv,
                                'numCandidates':cand,
                                'numChargingStation':0,
                                'Total_Time': 0,
                                'Total_Distance_Travel': 0,
                                'isSuccessful': 0},
                              ignore_index = True)
    
    
                  
                print(traceback.format_exc())


df['cs_DIV_area'] = df['numChargingStation']/ df['Shape_Area']                                                                                            
df['dist_DIV_area'] = df['Total_Distance_Travel'] / df['Shape_Area']                                                                                                 



#####################################
### SAVE RAW PANDA DATAFRAME AS CSV FILE 
#####################################
                
now = datetime.now() # current date and time
date_time = now.strftime("%m_%d_%Y__%H_%M_%S")
directory = './data/{}'.format(date_time)



filename = '{}_{}.csv'.format('TestData_nTrial',n_trials)

file_path = os.path.join(directory, filename)

if not os.path.isdir(directory):
    os.mkdir(directory)

df.to_csv(file_path)



#######################################
### SAVE SUMMARY STATS BY CONFIGURATION
### PANDA DATAFRAME AS CSV FILE 
#######################################

criteria = df['isSuccessful'] > 0
summary_df = df[criteria].groupby(['Shape',
                         'N_Gon',
                         'Shape_Area',
                         'CS_Radius',
                         'numCandidates'],as_index = False).agg({'numChargingStation':['mean', 'std'],
                                                                'Total_Time': ['mean', 'std'],
                                                                'Total_Distance_Travel': ['mean', 'std'],
                                                                'cs_DIV_area': ['mean', 'std'],
                                                                'dist_DIV_area': ['mean', 'std'],
                                                                'isSuccessful': ['sum']}).round(2)




filename = '{}_{}.csv'.format('TestDataSummary_ByConfig_nTrial',n_trials)

file_path = os.path.join(directory, filename)

if not os.path.isdir(directory):
    os.mkdir(directory)

summary_df.to_csv(file_path)

# #######################################
# ### SAVE SUMMARY STATS BY AREA & CS RADIUS
# ### PANDA DATAFRAME AS CSV FILE 
# #######################################           


col = ['Shape_Area',
        'CS_Radius',
        'numCandidates',
        'numChargingStation',
        'Total_Time',
        'Total_Distance_Travel',
        'cs_DIV_area',
        'dist_DIV_area',
        'isSuccessful']

areaCSRadius_df = df[criteria][col].groupby(['Shape_Area',
                                    'CS_Radius',
                                    'numCandidates'],as_index = False).agg({'numChargingStation':['mean', 'std'],
                                                          'Total_Time': ['mean', 'std'],
                                                          'Total_Distance_Travel': ['mean', 'std'],                                         
                                                          'dist_DIV_area': ['mean', 'std'],
                                                          'cs_DIV_area': ['mean', 'std'],
                                                          'isSuccessful': ['sum']}).round(2)  

                                                                                                                                                                                                 


filename = '{}.csv'.format('TestDataSummary_ByAreaCSRadius')

file_path = os.path.join(directory, filename)

if not os.path.isdir(directory):
    os.mkdir(directory)

areaCSRadius_df.to_csv(file_path)




# # #######################################
# # ### CREATE FIGURES TO REPRESENT THE DATA 
# # #######################################    



fig1 , ( (ax1,ax2,ax3) , (ax4,ax5,ax6) ) = plt.subplots(2,3)
fig1.set_size_inches(19.20, 10.80)

mark = 0
curAx1 = 0
curAx2 = 0



for index, row in summary_df.iterrows():
    

    
    name = row['Shape'].to_numpy()[0]
    area = row['Shape_Area'].to_numpy()[0]
    
    if(name == 'Square'):
        mark = '*'
        color = 'k'
        
    elif(name == 'Rectangle'):
        mark = 'o'   
        color = 'b'
    elif name == 'Octagon':
        mark = 'v'
        color = 'r'
           
    if( area== 25):
        curAx1 = ax1
        curAx2 = ax4
    elif( area == 50):
        curAx1 = ax2   
        curAx2 = ax5
    elif( area == 100):
        curAx1 = ax3     
        curAx2 = ax6
        
    
    curAx1.scatter( row['CS_Radius'], row['cs_DIV_area']['mean'],marker = mark , c = color)
    curAx2.scatter( row['CS_Radius'], row['dist_DIV_area']['mean'], marker = mark , c = color)



ax1.set_title('Field with $25km^{2}$ area')
ax1.set_ylabel('Mean nCS / Area')
ax1.set_xlabel('CS coverage radius')

ax2.set_title('Field with $50km^{2}$ area')
ax2.set_ylabel('Mean nCS / Area')
ax2.set_xlabel('CS coverage radius')

ax3.set_title('Field with $100km^{2}$ area')
ax3.set_ylabel('Mean nCS / Area')
ax3.set_xlabel('CS coverage radius')


ax4.set_title('Field with $25km^{2}$ area')
ax4.set_ylabel('mean travel distance / Area')
ax4.set_xlabel('CS coverage radius')

ax5.set_title('Field with $50km^{2}$ area')
ax5.set_ylabel('mean travel distance / Area')
ax5.set_xlabel('CS coverage radius')

ax6.set_title('Field with $100km^{2}$ area')
ax6.set_ylabel('mean travel distance / Area')
ax6.set_xlabel('CS coverage radius')


plt.subplots_adjust(left=0.125 , wspace =0.7, hspace = 0.7)


imType = ['.png','.eps','.svg']

for im in imType:
    
    filename= '{}{}'.format('TestDataSummary_plot',im)
    
    file_path = os.path.join(directory, filename)
    
    if not os.path.isdir(directory):
        os.mkdir(directory)
    
    plt.savefig(file_path)






















