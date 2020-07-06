# -*- coding: utf-8 -*-

import pandas as pd


df = pd.read_csv('TestData_nTrial_2.csv')



# #######################################
# ### SAVE SUMMARY STATS BY AREA & CS RADIUS
# ### PANDA DATAFRAME AS CSV FILE 
# #######################################           



criteria = df['numChargingStation'] > 0
col = ['Shape_Area',
        'CS_Radius',
        'numCandidates',
        'numChargingStation',
        'Total_Time',
        'Total_Distance_Travel',
        'isSuccessful']

areaCSRadius_df = df[criteria][col].groupby(['Shape_Area',
                                    'CS_Radius',
                                    'numCandidates'],as_index = False).agg({'numChargingStation':['mean', 'std'],
                                                          'Total_Time': ['mean', 'std'],
                                                          'Total_Distance_Travel': ['mean', 'std'],
                                                          'isSuccessful': ['sum']}).round(2)  

                                                           
                                                       
                                                           
areaCSRadius_df['csDIVarea'] = areaCSRadius_df['numChargingStation']['mean']  / areaCSRadius_df['Shape_Area']                                                                                            
areaCSRadius_df['distDIVarea'] = areaCSRadius_df['Total_Distance_Travel']['mean']  / areaCSRadius_df['Shape_Area']                                                                                                 


print(areaCSRadius_df)                                                          
   

# import matplotlib.pyplot as plt                                                        
                                                           
                                                           
# fig1 = plt.figure(1)
# ax1 = fig1.add_subplot(1,3,1)
# ax2 = fig1.add_subplot(1,3,1)
# ax3 = fig1.add_subplot(1,3,1)






# mark = 0
# curAx = 0

# for name in names:
    
    
#     if(name == 'Square'):
#         mark = '*'
#         curAx = ax1
#     if(name == 'Rectangle'):
#         mark = 'o'   
#         curAx = ax2
#     if name == 'Octagon':
#         mark = '-'
#         curAx = ax3
    
    
#     for csRadius in CS_radius:
        
#         y = summary_AreaCSRadius_df[df['CS_Radius'] == csRadius & df['Shape'] == name]['csDIVarea']
        
#         curAx.scatter( csRadius, y ,marker = mark)


# filename = '{}.png'.format('csDIVarea_plot')

# file_path = os.path.join(directory, filename)

# if not os.path.isdir(directory):
#     os.mkdir(directory)

# plt.savefig(file_path)













