import pandas as pd
import numpy as np
from Drone import Drone
from shapely import geometry 
from datetime import datetime
import traceback
import os.path
import matplotlib.pyplot as plt
import seaborn as sns

from RUN import Program

import time


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
 




#####################################
### Charging Station Properties 
#####################################


startPoint = [0, 0]

# Charging Station Coverage distance
CS_radius = [2.0,2.5,3.0,3.5,4.0]
step = 0.02


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
oct1 = [ (0,0), (-1.609,1.609),  (-1.609,3.8844),  (0,5.4934), (2.2754,5.4934), (3.8844,3.8844) ,(3.8844,1.609) ,(2.2754,0) ]
oct2 = [ (0,0), (-2.2754,2.2754), (-2.2754,5.4934), (0,7.7689), (3.218,7.7689), (5.4934,5.4934), (5.4934,2.2754), (3.218,0) ]
oct3 = [ (0,0), (-3.218,3.218), (-3.218,7.7689), (0,10.9869), (4.5509,10.9868), (7.7689,7.7689), (7.7689,3.218), (4.5509,0) ]

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
n_trials = 50


t1=time.perf_counter()


      
for name,field in zip(names,fields):
    
    for ii in range(n_trials):
        
        curShape = geometry.Polygon(field)
        
        
        # FOR EVERY SQ, THERE IS 1 CANDIDATE
        shape_area = round(curShape.area)
        cand = shape_area 
        
        
        
        program = Program(field_boundary = field,
                          meshStep = step,
                          direction = 'cw')
    

        for csr in CS_radius:
            
            print('\n\n------------------------------')
            print('{}:{}  CS:{}  Run:{}'.format(name,shape_area,csr,ii))
            print('------------------------------\n\n')
            
            drone = Drone(radius=rad, max_distance = mxDist)  
            
            
            notComplete = True
            
            while( notComplete ):
                
                # CLEARS ANY DATA THAT IT HAD STORED
                drone.clear()
                

                
                try:
                    
    
                    
                    nCS, travelDist, bestVal = program.run(drone, 
                                                            startPoint, 
                                                            csr, 
                                                            cand , 
                                                            keepGenCandidates =True)            
                    
                    
                    
                    
                    # CALCULATE TOTAL TIME BASED ON DRONE
                    # VELOCITY AND THEO. CHARGING TIME
                    tot_time = 3*( travelDist / velocity)
                    
                    
            
                    df = df.append({'Shape': name,
                                    'N_Gon': len(field),
                                    'Shape_Area': shape_area ,
                                    'CS_Radius': csr,
                                    'numCandidates': cand,
                                    'numChargingStation': nCS,
                                    'Total_Time': tot_time,
                                    'Total_Distance_Travel': travelDist,
                                    'Intrinsic_Inefficiency': bestVal,
                                    'isSuccessful': 1},
                                    ignore_index = True)
        
                    notComplete = False
        
                except:
        
                    df = df.append({'Shape': name,
                                    'N_Gon': len(field),
                                    'Shape_Area': shape_area,
                                    'CS_Radius': csr,
                                    'numCandidates':cand,
                                    'numChargingStation':0,
                                    'Total_Time': 0,
                                    'Total_Distance_Travel': 0,
                                    'Intrinsic_Inefficiency':0,
                                    'isSuccessful': 0},
                                  ignore_index = True)
        
        
                      
                    print(traceback.format_exc())
    

t2=time.perf_counter()


print('Execution:',t2-t1)




df['cs_DIV_area'] = df['numChargingStation']/ df['Shape_Area']                                                                                            
df['dist_DIV_area'] = ( df['Total_Distance_Travel'] / df['Shape_Area'] ) / 20.0                                                                                                 
df['CS_Efficiency'] = 1.0 / ( (3.0*np.sqrt(2.0)/2.0)* (df['CS_Radius']**2) * df['cs_DIV_area'] )

df['TheoBestDist'] = ( df['Shape_Area'] / 2*rad ) * df['Intrinsic_Inefficiency']
df['TheoBestTime'] = ( df['TheoBestDist'] / 25.0) * 3 


df['coverage_efficiency'] = 1.0 / df['Intrinsic_Inefficiency']
df['area_DIV_dist'] = 1.0 / df['dist_DIV_area']
df['area_DIV_cs'] = 1.0 / df['cs_DIV_area']


df['mission_efficiency'] = df['area_DIV_dist'] / df['coverage_efficiency']







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



# ######################################
# ## SAVE SUMMARY STATS BY CONFIGURATION
# ## PANDA DATAFRAME AS CSV FILE 
# ######################################

# criteria = df['isSuccessful'] > 0

# select_col = ['Shape',
#               'N_Gon',
#               'Shape_Area',
#               'CS_Radius',
#               'numCandidates']

# summary_df = df[criteria].groupby(select_col,as_index = False).agg({'numChargingStation':['mean', 'std'],
#                                                                 'Total_Time': ['mean', 'std'],
#                                                                 'Total_Distance_Travel': ['mean', 'std'],
#                                                                 'TheoBestDist': ['mean', 'std'], 
#                                                                 'TheoBestTime': ['mean', 'std'], 
#                                                                 'cs_DIV_area': ['mean', 'std'],
#                                                                 'area_DIV_cs': ['mean', 'std'],
#                                                                 'dist_DIV_area': ['mean', 'std'],
#                                                                 'area_DIV_dist': ['mean', 'std'],
#                                                                 'CS_Efficiency':['mean', 'std'],
#                                                                 'Intrinsic_Inefficiency':['mean', 'std'],
#                                                                 'coverage_efficiency':['mean', 'std'],
#                                                                 'mission_efficiency':['mean', 'std'],
#                                                                 'isSuccessful': ['sum']}).round(2)
   
                                                                  
# new_col_names = ['nCS_mean',
#                   'nCS_std',
#                   'TotalTime_mean',
#                   'TotalTime_std',
#                   'TotalDistanceTravel_mean',
#                   'TotalDistanceTravel_std',          
#                   'TheoBestDist_mean',
#                   'TheoBestDist_std',
#                   'TheoBestTime_mean',
#                   'TheoBestTime_std',
#                   'csDIVarea_mean',
#                   'csDIVarea_std',         
#                   'areaDIVcs_mean',
#                   'areaDIVcs_std',
#                   'distDIVarea_mean',
#                   'distDIVarea_std',                  
#                   'areaDIVdist_mean',
#                   'areaDIVdist_std',
#                   'CS_Efficiency_mean',
#                   'CS_Efficiency_std',
#                   'Intrinsic_Inefficiency_mean',
#                   'Intrinsic_Inefficiency_std',
#                   'coverage_efficiency_mean',
#                   'coverage_efficiency_std', 
#                   'mission_efficiency_mean',
#                   'mission_efficiency_std', 
#                   'Total_Success']                                                               
                                                                  
# summary_df.columns = select_col + new_col_names  
# summary_df.reset_index()  


# filename = '{}_{}.csv'.format('TestDataSummary_ByConfig_nTrial',n_trials)

# file_path = os.path.join(directory, filename)

# if not os.path.isdir(directory):
#     os.mkdir(directory)

# summary_df.to_csv(file_path)

# # # #######################################
# # # ### SAVE SUMMARY STATS BY AREA & CS RADIUS
# # # ### PANDA DATAFRAME AS CSV FILE 
# # # #######################################           


# select_col2 = ['Shape_Area',
#               'CS_Radius',
#               'numCandidates']

# areaCSRadius_df = df[criteria].groupby(select_col2,as_index = False).agg({'numChargingStation':['mean', 'std'],
#                                                                 'Total_Time': ['mean', 'std'],
#                                                                 'Total_Distance_Travel': ['mean', 'std'],
#                                                                 'TheoBestDist': ['mean', 'std'], 
#                                                                 'TheoBestTime': ['mean', 'std'], 
#                                                                 'cs_DIV_area': ['mean', 'std'],
#                                                                 'area_DIV_cs': ['mean', 'std'],
#                                                                 'dist_DIV_area': ['mean', 'std'],
#                                                                 'area_DIV_dist': ['mean', 'std'],
#                                                                 'CS_Efficiency':['mean', 'std'],
#                                                                 'Intrinsic_Inefficiency':['mean', 'std'],
#                                                                 'coverage_efficiency':['mean', 'std'],
#                                                                 'mission_efficiency':['mean', 'std'],
#                                                                 'isSuccessful': ['sum']}).round(2)


# new_col_names = ['nCS_mean',
#                   'nCS_std',
#                   'TotalTime_mean',
#                   'TotalTime_std',
#                   'TotalDistanceTravel_mean',
#                   'TotalDistanceTravel_std',          
#                   'TheoBestDist_mean',
#                   'TheoBestDist_std',
#                   'TheoBestTime_mean',
#                   'TheoBestTime_std',
#                   'csDIVarea_mean',
#                   'csDIVarea_std',         
#                   'areaDIVcs_mean',
#                   'areaDIVcs_std',
#                   'distDIVarea_mean',
#                   'distDIVarea_std',                  
#                   'areaDIVdist_mean',
#                   'areaDIVdist_std',
#                   'CS_Efficiency_mean',
#                   'CS_Efficiency_std',
#                   'Intrinsic_Inefficiency_mean',
#                   'Intrinsic_Inefficiency_std',
#                   'coverage_efficiency_mean',
#                   'coverage_efficiency_std',               
#                   'mission_efficiency_mean',
#                   'mission_efficiency_std', 
#                   'Total_Success']                                                                   
   
                                                               
# areaCSRadius_df.columns = select_col2 + new_col_names  
# areaCSRadius_df.reset_index()                                                                                                                                                                                


# filename = '{}.csv'.format('TestDataSummary_ByAreaCSRadius')

# file_path = os.path.join(directory, filename)

# if not os.path.isdir(directory):
#     os.mkdir(directory)

# areaCSRadius_df.to_csv(file_path)




# #######################################
# ### CREATE FIGURES TO REPRESENT THE DATA 
# #######################################    

# ## NOTE: THESE GRAPHS WERE MADE SPECIFICALLY FOR AREAS OF 25,50,100

# df = df[ df['isSuccessful'] > 0 ]



# fig1 , ( (ax1,ax2,ax3) , (ax4,ax5,ax6))  = plt.subplots(2,3)
# fig2 , ( (ax7,ax8,ax9) , (ax10,ax11,ax12))  = plt.subplots(2,3)
# fig1.set_size_inches(12.0, 8.0)
# fig2.set_size_inches(12.0, 8.0)

# mark = 0
# curAx1 = None
# curAx2 = None
# curAx3 = None
# curAx4 = None

# ax1.get_shared_y_axes().join(ax1,ax2,ax3)
# ax4.get_shared_y_axes().join(ax4,ax5,ax6)
# ax7.get_shared_y_axes().join(ax7,ax8,ax9)
# ax10.get_shared_y_axes().join(ax10,ax11,ax12)

# shape_names = pd.unique(df['Shape'])
# shape_areas = pd.unique(df['Shape_Area'])


# sns.set(style="darkgrid")
# mark = ['.','.','.']


# df['intrinsicLabel'] = df['Shape'] + ' Intrinsic Inefficiency'

# for area in shape_areas:
    
#     crit2 = (df['Shape_Area'] == area)  
    
#     if( area== 25):
#         curAx1 = ax1
#         curAx2 = ax4
#         curAx3 = ax7
#         curAx4 = ax10
#     elif( area == 50):
#         curAx1 = ax2   
#         curAx2 = ax5
#         curAx3 = ax8
#         curAx4 = ax11
#     elif( area == 100):
#         curAx1 = ax3     
#         curAx2 = ax6
#         curAx3 = ax9
#         curAx4 = ax12
    
    

#     sns.pointplot( x="CS_Radius", y="area_DIV_cs",
#                 data= df[crit2] ,
#                 markers = mark,
#                 hue = 'Shape', 
#                 dodge = 0.3,
#                 join = False,
#                 style="time",
#                 scale = 1.0 ,
#                 ax = curAx1)



#     sns.pointplot(x="CS_Radius", y="CS_Efficiency", 
#                 data= df[crit2] ,
#                 markers = mark,
#                 hue = 'Shape', 
#                 dodge = 0.3,
#                 join = False,
#                 style="time",
#                 scale = 1.0 ,
#                 ax = curAx2)




#     sns.pointplot(x="CS_Radius", y="Total_Time", 
#                 data= df[crit2] ,
#                 markers = mark,
#                 hue = 'Shape', 
#                 dodge = 0.3,
#                 join = False,
#                 style="time",
#                 scale = 1.0 ,
#                 ax = curAx3)





#     sns.pointplot(x="CS_Radius", y='mission_efficiency', 
#                 data= df[crit2] ,
#                 markers = mark,
#                 hue = 'Shape', 
#                 dodge = 0.3,
#                 join = False,
#                 scale = 1.0 ,
#                 ax = curAx4)  






    
# ax1.set_title('Field with $25 km^{2}$ area')
# ax1.set_ylabel('Covered area per CS')
# ax1.set_xlabel('')
# plt.setp(ax1.get_xticklabels(), visible=False)
# #ax1.legend(prop={'size': 6})

# ax2.set_title('Field with $50 km^{2}$ area')
# ax2.set_ylabel('')
# ax2.set_xlabel('')
# plt.setp(ax2.get_xticklabels(), visible=False)
# plt.setp(ax2.get_yticklabels(), visible=False)

# #ax2.legend(prop={'size': 6})

# ax3.set_title('Field with $100 km^{2}$ area')
# ax3.set_ylabel('')
# ax3.set_xlabel('')
# plt.setp(ax3.get_xticklabels(), visible=False)
# plt.setp(ax3.get_yticklabels(), visible=False)
# #ax3.legend(prop={'size': 6})



# #ax4.set_title('Field with $25 km^{2}$ area')
# ax4.set_ylabel('CS Efficiency')
# ax4.set_xlabel('CS coverage radius')
# #ax4.legend(prop={'size': 6})

# #ax5.set_title('Field with $50 km^{2}$ area')
# ax5.set_ylabel('')
# ax5.set_xlabel('CS coverage radius')
# plt.setp(ax5.get_yticklabels(), visible=False)
# #ax5.legend(prop={'size': 6})

# #ax6.set_title('Field with $100 km^{2}$ area')
# ax6.set_ylabel('')
# ax6.set_xlabel('CS coverage radius')
# plt.setp(ax6.get_yticklabels(), visible=False)
# #ax6.legend(prop={'size': 6})


# handles, labels = ax1.get_legend_handles_labels()
# fig1.legend(handles, labels, loc=7, title = 'Legend')

# for curAx in [ax1,ax2,ax3,ax4,ax5,ax6]:

#     curAx.get_legend().remove()
#     box = curAx.get_position()
#     curAx.set_position([box.x0, box.y0, box.width*0.9, box.height])




# ax7.set_title('Field with $25 km^{2}$ area')
# ax7.set_ylabel('Mission time')
# ax7.set_xlabel('')
# plt.setp(ax7.get_xticklabels(), visible=False)
# #ax7.legend(prop={'size': 6})

# ax8.set_title('Field with $50 km^{2}$ area')
# ax8.set_ylabel('')
# ax8.set_xlabel('')
# plt.setp(ax8.get_xticklabels(), visible=False)
# plt.setp(ax8.get_yticklabels(), visible=False)
# #ax8.legend(prop={'size': 6})

# ax9.set_title('Field with $100 km^{2}$ area')
# ax9.set_ylabel('')
# ax9.set_xlabel('')
# plt.setp(ax9.get_xticklabels(), visible=False)
# plt.setp(ax9.get_yticklabels(), visible=False)
# #ax9.legend(prop={'size': 6})



# #ax10.set_title('Field with $25 km^{2}$ area')
# ax10.set_ylabel('Mission efficiency')
# ax10.set_xlabel('CS coverage radius')
# #ax7.set( ylim = (1.0,2.0) )
# #ax7.legend(prop={'size': 6})

# #ax11.set_title('Field with $50 km^{2}$ area')
# ax11.set_ylabel('')
# ax11.set_xlabel('CS coverage radius')
# plt.setp(ax11.get_yticklabels(), visible=False)
# #ax8.set( ylim = (1.0,2.0) )
# #ax8.legend(prop={'size': 6})

# #ax12.set_title('Field with $100 km^{2}$ area')
# ax12.set_ylabel('')
# ax12.set_xlabel('CS coverage radius')
# plt.setp(ax12.get_yticklabels(), visible=False)
# #ax9.set( ylim = (1.0,2.0) )
# #


# handles, labels = ax10.get_legend_handles_labels()
# fig2.legend(handles, labels, loc=7, title = 'Legend')

# for curAx in [ax7,ax8,ax9,ax10,ax11,ax12]:

#     curAx.get_legend().remove()
#     box = curAx.get_position()
#     curAx.set_position([box.x0, box.y0, box.width*0.9, box.height])




# fig1.subplots_adjust(left = 0.1, right = 0.88, wspace =0.05 , hspace = 0.05)
# fig2.subplots_adjust(left = 0.1, right = 0.88, wspace =0.05, hspace = 0.05)

# imType = ['.png','.eps','.svg']

# for im in imType:
    
#     filename1= '{}{}'.format('TestDataSummary_DistPlot',im)
#     filename2= '{}{}'.format('TestDataSummary_TimePlot',im)
    
#     file_path1 = os.path.join(directory, filename1)
#     file_path2 = os.path.join(directory, filename2)
    

#     fig1.savefig(file_path1)
#     fig2.savefig(file_path2)

















