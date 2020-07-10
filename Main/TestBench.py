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
                'Intrinsic_Inefficiency',
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
           'Intrinsic_Inefficiency':'float64',
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
n_trials = 25



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
                                'Intrinsic_Inefficiency':lst[2],
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
                                'Intrinsic_Inefficiency':0,
                                'isSuccessful': 0},
                              ignore_index = True)
    
    
                  
                print(traceback.format_exc())


df['cs_DIV_area'] = df['numChargingStation']/ df['Shape_Area']                                                                                            
df['dist_DIV_area'] = df['Total_Distance_Travel'] / df['Shape_Area']                                                                                                 
df['CS_Efficiency'] = 1.0 / ( (3.0*np.sqrt(2.0)/2.0)* (df['CS_Radius']**2) * df['cs_DIV_area'] )


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

select_col = ['Shape',
              'N_Gon',
              'Shape_Area',
              'CS_Radius',
              'numCandidates']

summary_df = df[criteria].groupby(select_col,as_index = False).agg({'numChargingStation':['mean', 'std'],
                                                                'Total_Time': ['mean', 'std'],
                                                                'Total_Distance_Travel': ['mean', 'std'],
                                                                'cs_DIV_area': ['mean', 'std'],
                                                                'dist_DIV_area': ['mean', 'std'],
                                                                'CS_Efficiency':['mean', 'std'],
                                                                'Intrinsic_Inefficiency':['mean', 'std'],
                                                                'isSuccessful': ['sum']}).round(2)
    
                                                                  
new_col_names = ['nCS_mean',
                 'nCS_std',
                 'TotalTime_mean',
                 'TotalTime_std',
                 'TotalDistanceTravel_mean',
                 'TotalDistanceTravel_std',
                 'csDIVarea_mean',
                 'csDIVarea_std',
                 'distDIVarea_mean',
                 'distDIVarea_std',
                 'CS_Efficiency_mean',
                 'CS_Efficiency_std',
                 'Intrinsic_Inefficiency_mean',
                 'Intrinsic_Inefficiency_std',
                 'Total_Success']                                                                
                                                                  
summary_df.columns = select_col + new_col_names  
summary_df.reset_index()  


filename = '{}_{}.csv'.format('TestDataSummary_ByConfig_nTrial',n_trials)

file_path = os.path.join(directory, filename)

if not os.path.isdir(directory):
    os.mkdir(directory)

summary_df.to_csv(file_path)

# # #######################################
# # ### SAVE SUMMARY STATS BY AREA & CS RADIUS
# # ### PANDA DATAFRAME AS CSV FILE 
# # #######################################           


select_col2 = ['Shape_Area',
              'CS_Radius',
              'numCandidates']

areaCSRadius_df = df[criteria].groupby(select_col2,as_index = False).agg({'numChargingStation':['mean', 'std'],
                                                                'Total_Time': ['mean', 'std'],
                                                                'Total_Distance_Travel': ['mean', 'std'],
                                                                'cs_DIV_area': ['mean', 'std'],
                                                                'dist_DIV_area': ['mean', 'std'],
                                                                'CS_Efficiency':['mean', 'std'],
                                                                'Intrinsic_Inefficiency':['mean', 'std'],
                                                                'isSuccessful': ['sum']}).round(2)


new_col_names = ['nCS_mean',
                 'nCS_std',
                 'TotalTime_mean',
                 'TotalTime_std',
                 'TotalDistanceTravel_mean',
                 'TotalDistanceTravel_std',
                 'csDIVarea_mean',
                 'csDIVarea_std',
                 'distDIVarea_mean',
                 'distDIVarea_std',
                 'CS_Efficiency_mean',
                 'CS_Efficiency_std',
                 'Intrinsic_Inefficiency_mean',
                 'Intrinsic_Inefficiency_std',
                 'Total_Success']                                                                 
                                                                  
areaCSRadius_df.columns = select_col2 + new_col_names  
areaCSRadius_df.reset_index()                                                                                                                                                                                


filename = '{}.csv'.format('TestDataSummary_ByAreaCSRadius')

file_path = os.path.join(directory, filename)

if not os.path.isdir(directory):
    os.mkdir(directory)

areaCSRadius_df.to_csv(file_path)




# # #######################################
# # ### CREATE FIGURES TO REPRESENT THE DATA 
# # #######################################    



fig1 , ( (ax1,ax2,ax3) , (ax4,ax5,ax6) , (ax7,ax8,ax9) ) = plt.subplots(3,3)
fig1.set_size_inches(19.20, 10.80)

mark = 0
curAx1 = 0
curAx2 = 0


ax1.get_shared_y_axes().join(ax1,ax2,ax3)
ax4.get_shared_y_axes().join(ax4,ax5,ax6)
ax7.get_shared_y_axes().join(ax7,ax8,ax9)

shape_names = pd.unique(summary_df['Shape'])
shape_areas = pd.unique(summary_df['Shape_Area'])

for name in shape_names:
    for area in shape_areas:

    

    
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
            curAx3 = ax7
        elif( area == 50):
            curAx1 = ax2   
            curAx2 = ax5
            curAx3 = ax8
        elif( area == 100):
            curAx1 = ax3     
            curAx2 = ax6
            curAx3 = ax9
            
        
        crit1 = summary_df['Shape'] == name 
        crit2 = summary_df['Shape_Area'] == area      
        
        x = summary_df[crit1 & crit2]['CS_Radius']
        
        y1 = summary_df[crit1 & crit2]['csDIVarea_mean']
        y1_err = summary_df[crit1 & crit2]['csDIVarea_std'] 
        
        y2 = summary_df[crit1 & crit2]['CS_Efficiency_mean']
        y2_err = summary_df[crit1 & crit2]['CS_Efficiency_std'] 
        
        
        y3 = summary_df[crit1 & crit2]['distDIVarea_mean'] / 20.0
        y3_err = summary_df[crit1 & crit2]['distDIVarea_std']  / 20.0
        
        y4 = summary_df[crit1 & crit2]['Intrinsic_Inefficiency_mean']
        
        
        curAx1.scatter( x, y1 , marker = mark , label = name, c = color)
        curAx1.errorbar(x, y1, yerr = y1_err , fmt = 'none', ecolor = color)
        
        
        curAx2.scatter( x, y2 , marker = mark , label = name, c = color)
        curAx2.errorbar(x, y2, yerr = y2_err , fmt = 'none', ecolor = color)
        
        
        curAx3.scatter( x, y3 , marker = mark , label = name, c = color)
        curAx3.errorbar(x, y3, yerr = y3_err , fmt = 'none', ecolor = color)
        
        curAx3.plot( x, y4 , linestyle = '-' , label = '{} Intrinsic Inefficiency'.format(name), c = color)





ax1.set_title('Field with $25 km^{2}$ area')
ax1.set_ylabel('Mean nCS / Area')
ax1.set_xlabel('CS coverage radius')
ax1.legend(prop={'size': 6})

ax2.set_title('Field with $50 km^{2}$ area')
ax2.set_ylabel('Mean nCS / Area')
ax2.set_xlabel('CS coverage radius')
ax2.legend(prop={'size': 6})

ax3.set_title('Field with $100 km^{2}$ area')
ax3.set_ylabel('Mean nCS / Area')
ax3.set_xlabel('CS coverage radius')
ax3.legend(prop={'size': 6})




ax4.set_title('Field with $25 km^{2}$ area')
ax4.set_ylabel('Mean CS Efficiency')
ax4.set_xlabel('CS coverage radius')
ax4.legend(prop={'size': 6})

ax5.set_title('Field with $50 km^{2}$ area')
ax5.set_ylabel('Mean CS Efficiency')
ax5.set_xlabel('CS coverage radius')
ax5.legend(prop={'size': 6})

ax6.set_title('Field with $100 km^{2}$ area')
ax6.set_ylabel('Mean CS Efficiency')
ax6.set_xlabel('CS coverage radius')
ax6.legend(prop={'size': 6})






ax7.set_title('Field with $25 km^{2}$ area')
ax7.set_ylabel('Travel distance ratio')
ax7.set_xlabel('CS coverage radius')
ax7.legend(prop={'size': 6})

ax8.set_title('Field with $50 km^{2}$ area')
ax8.set_ylabel('Travel distance ratio')
ax8.set_xlabel('CS coverage radius')
ax8.legend(prop={'size': 6})

ax9.set_title('Field with $100 km^{2}$ area')
ax9.set_ylabel('Travel distance ratio')
ax9.set_xlabel('CS coverage radius')
ax9.legend(prop={'size': 6})


plt.subplots_adjust(left=0.2, wspace =0.3, hspace = 0.5)


imType = ['.png','.eps','.svg']

for im in imType:
    
    filename= '{}{}'.format('TestDataSummary_plot',im)
    
    file_path = os.path.join(directory, filename)
    
    if not os.path.isdir(directory):
        os.mkdir(directory)
    
    plt.savefig(file_path)






















