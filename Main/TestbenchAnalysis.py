
import pandas as pd
import os.path
import matplotlib.pyplot as plt
import seaborn as sns

class Analysis():
    
    
    def __init__(self, df = None, filepath = None):
        
        self.df = None

        if not(df is None) and isinstance(df, pd.DataFrame):
            
            self.df = df
            
        elif not(filepath is None):
            
            self.df = pd.read_csv(filepath)

        else:
            
            raise('panda.Dataframe or filepath does not exist')


    
    def summaryByConfiguration(self, directory = './'):
        
        criteria = self.df['isSuccessful'] > 0

        select_col = ['Shape',
                      'N_Gon',
                      'Shape_Area',
                      'CS_Radius',
                      'numCandidates']
        
        summary_df = self.df[criteria].groupby(select_col,as_index = False).agg({'numChargingStation':['mean', 'std'],
                                                                        'Total_Time': ['mean', 'std'],
                                                                        'Total_Distance_Travel': ['mean', 'std'],
                                                                        'TheoBestDist': ['mean', 'std'], 
                                                                        'TheoBestTime': ['mean', 'std'], 
                                                                        'Runtime':['mean','std'],
                                                                        'cs_DIV_area': ['mean', 'std'],
                                                                        'area_DIV_cs': ['mean', 'std'],
                                                                        'dist_DIV_area': ['mean', 'std'],
                                                                        'area_DIV_dist': ['mean', 'std'],
                                                                        'CS_Efficiency':['mean', 'std'],
                                                                        'Intrinsic_Inefficiency':['mean', 'std'],
                                                                        'coverage_efficiency':['mean', 'std'],
                                                                        'mission_efficiency':['mean', 'std'],
                                                                        'isSuccessful': ['sum']}).round(2)                                                 
        new_col_names = ['nCS_mean',
                          'nCS_std',
                          'TotalTime_mean',
                          'TotalTime_std',
                          'TotalDistanceTravel_mean',
                          'TotalDistanceTravel_std',          
                          'TheoBestDist_mean',
                          'TheoBestDist_std',
                          'TheoBestTime_mean',
                          'TheoBestTime_std',
                          'Runtime_mean',
                          'Runtime_std',
                          'csDIVarea_mean',
                          'csDIVarea_std',         
                          'areaDIVcs_mean',
                          'areaDIVcs_std',
                          'distDIVarea_mean',
                          'distDIVarea_std',                  
                          'areaDIVdist_mean',
                          'areaDIVdist_std',
                          'CS_Efficiency_mean',
                          'CS_Efficiency_std',
                          'Intrinsic_Inefficiency_mean',
                          'Intrinsic_Inefficiency_std',
                          'coverage_efficiency_mean',
                          'coverage_efficiency_std',               
                          'mission_efficiency_mean',
                          'mission_efficiency_std', 
                          'Total_Success']                                                                
                                                                          
        summary_df.columns = select_col + new_col_names  
        summary_df.reset_index()  
        
        
        filename = 'TestDataSummary_ByConfig.csv'
        
        file_path = os.path.join(directory, filename)
        
        if not os.path.isdir(directory):
            os.mkdir(directory)
        
        summary_df.to_csv(file_path)


    def summaryByAreaCSRadius(self, directory = './'):   
        
        # # #######################################
        # # ### SAVE SUMMARY STATS BY AREA & CS RADIUS
        # # ### PANDA DATAFRAME AS CSV FILE 
        # # ####################################### 
          
        criteria = self.df['isSuccessful'] > 0
        
        select_col2 = ['Shape_Area',
                      'CS_Radius',
                      'numCandidates']
        
        areaCSRadius_df = self.df[criteria].groupby(select_col2,as_index = False).agg({'numChargingStation':['mean', 'std'],
                                                                        'Total_Time': ['mean', 'std'],
                                                                        'Total_Distance_Travel': ['mean', 'std'],
                                                                        'TheoBestDist': ['mean', 'std'], 
                                                                        'TheoBestTime': ['mean', 'std'], 
                                                                        'Runtime':['mean','std'],
                                                                        'cs_DIV_area': ['mean', 'std'],
                                                                        'area_DIV_cs': ['mean', 'std'],
                                                                        'dist_DIV_area': ['mean', 'std'],
                                                                        'area_DIV_dist': ['mean', 'std'],
                                                                        'CS_Efficiency':['mean', 'std'],
                                                                        'Intrinsic_Inefficiency':['mean', 'std'],
                                                                        'coverage_efficiency':['mean', 'std'],
                                                                        'mission_efficiency':['mean', 'std'],
                                                                        'isSuccessful': ['sum']}).round(2)
        
        
        new_col_names = ['nCS_mean',
                          'nCS_std',
                          'TotalTime_mean',
                          'TotalTime_std',
                          'TotalDistanceTravel_mean',
                          'TotalDistanceTravel_std',          
                          'TheoBestDist_mean',
                          'TheoBestDist_std',
                          'TheoBestTime_mean',
                          'TheoBestTime_std',
                          'Runtime_mean',
                          'Runtime_std',
                          'csDIVarea_mean',
                          'csDIVarea_std',         
                          'areaDIVcs_mean',
                          'areaDIVcs_std',
                          'distDIVarea_mean',
                          'distDIVarea_std',                  
                          'areaDIVdist_mean',
                          'areaDIVdist_std',
                          'CS_Efficiency_mean',
                          'CS_Efficiency_std',
                          'Intrinsic_Inefficiency_mean',
                          'Intrinsic_Inefficiency_std',
                          'coverage_efficiency_mean',
                          'coverage_efficiency_std',               
                          'mission_efficiency_mean',
                          'mission_efficiency_std', 
                          'Total_Success']                                                                   
           
                                                                       
        areaCSRadius_df.columns = select_col2 + new_col_names  
        areaCSRadius_df.reset_index()                                                                                                                                                                                
        
        
        filename = '{}.csv'.format('TestDataSummary_ByAreaCSRadius')
        
        file_path = os.path.join(directory, filename)
        
        if not os.path.isdir(directory):
            os.mkdir(directory)
        
        areaCSRadius_df.to_csv(file_path)
        
        
    def create_figs(self, directory = './'):
        
        
        criteria = self.df['isSuccessful'] > 0
        

        curDf = self.df[ criteria ]
        
        
        
        # ## NOTE: THESE GRAPHS WERE MADE SPECIFICALLY FOR AREAS OF 25,50,100
        
        
        
        fig1 , ( (ax1,ax2,ax3) , (ax4,ax5,ax6))  = plt.subplots(2,3)
        fig2 , ( (ax7,ax8,ax9) , (ax10,ax11,ax12))  = plt.subplots(2,3)
        fig1.set_size_inches(12.0, 8.0)
        fig2.set_size_inches(12.0, 8.0)
        
        mark = 0
        curAx1 = None
        curAx2 = None
        curAx3 = None
        curAx4 = None
        
        ax1.get_shared_y_axes().join(ax1,ax2,ax3)
        ax4.get_shared_y_axes().join(ax4,ax5,ax6)
        ax7.get_shared_y_axes().join(ax7,ax8,ax9)
        ax10.get_shared_y_axes().join(ax10,ax11,ax12)
        
        #shape_names = pd.unique(curDf['Shape'])
        shape_areas = pd.unique(curDf['Shape_Area'])
        
        
        sns.set(style="darkgrid")
        mark = ['.','.','.']
        
        
        curDf['intrinsicLabel'] = curDf['Shape'] + ' Intrinsic Inefficiency'
        
        for area in shape_areas:
            
            crit2 = (curDf['Shape_Area'] == area)  
            
            if( area== 25):
                curAx1 = ax1
                curAx2 = ax4
                curAx3 = ax7
                curAx4 = ax10
            elif( area == 50):
                curAx1 = ax2   
                curAx2 = ax5
                curAx3 = ax8
                curAx4 = ax11
            elif( area == 100):
                curAx1 = ax3     
                curAx2 = ax6
                curAx3 = ax9
                curAx4 = ax12
            
            
        
            sns.pointplot( x="CS_Radius", y="area_DIV_cs",
                        data= curDf[crit2] ,
                        markers = mark,
                        hue = 'Shape', 
                        dodge = 0.3,
                        join = False,
                        style="time",
                        scale = 1.0 ,
                        ax = curAx1)
        
        
        
            sns.pointplot(x="CS_Radius", y="CS_Efficiency", 
                        data= curDf[crit2] ,
                        markers = mark,
                        hue = 'Shape', 
                        dodge = 0.3,
                        join = False,
                        style="time",
                        scale = 1.0 ,
                        ax = curAx2)
        
        
        
        
            sns.pointplot(x="CS_Radius", y="Total_Time", 
                        data= curDf[crit2] ,
                        markers = mark,
                        hue = 'Shape', 
                        dodge = 0.3,
                        join = False,
                        style="time",
                        scale = 1.0 ,
                        ax = curAx3)
        
        
        
        
        
            sns.pointplot(x="CS_Radius", y='mission_efficiency', 
                        data= curDf[crit2] ,
                        markers = mark,
                        hue = 'Shape', 
                        dodge = 0.3,
                        join = False,
                        scale = 1.0 ,
                        ax = curAx4)  
        
        
        
        
        
        
            
        ax1.set_title('Field with $25 km^{2}$ area')
        ax1.set_ylabel('Covered area per CS')
        ax1.set_xlabel('')
        plt.setp(ax1.get_xticklabels(), visible=False)
        #ax1.legend(prop={'size': 6})
        
        ax2.set_title('Field with $50 km^{2}$ area')
        ax2.set_ylabel('')
        ax2.set_xlabel('')
        plt.setp(ax2.get_xticklabels(), visible=False)
        plt.setp(ax2.get_yticklabels(), visible=False)
        
        #ax2.legend(prop={'size': 6})
        
        ax3.set_title('Field with $100 km^{2}$ area')
        ax3.set_ylabel('')
        ax3.set_xlabel('')
        plt.setp(ax3.get_xticklabels(), visible=False)
        plt.setp(ax3.get_yticklabels(), visible=False)
        #ax3.legend(prop={'size': 6})
        
        
        
        #ax4.set_title('Field with $25 km^{2}$ area')
        ax4.set_ylabel('CS Efficiency')
        ax4.set_xlabel('CS coverage radius')
        #ax4.legend(prop={'size': 6})
        
        #ax5.set_title('Field with $50 km^{2}$ area')
        ax5.set_ylabel('')
        ax5.set_xlabel('CS coverage radius')
        plt.setp(ax5.get_yticklabels(), visible=False)
        #ax5.legend(prop={'size': 6})
        
        #ax6.set_title('Field with $100 km^{2}$ area')
        ax6.set_ylabel('')
        ax6.set_xlabel('CS coverage radius')
        plt.setp(ax6.get_yticklabels(), visible=False)
        #ax6.legend(prop={'size': 6})
        
        
        handles, labels = ax1.get_legend_handles_labels()
        fig1.legend(handles, labels, loc=7, title = 'Legend')
        
        for curAx in [ax1,ax2,ax3,ax4,ax5,ax6]:
        
            curAx.get_legend().remove()
            box = curAx.get_position()
            curAx.set_position([box.x0, box.y0, box.width*0.9, box.height])
        
        
        
        
        ax7.set_title('Field with $25 km^{2}$ area')
        ax7.set_ylabel('Mission time')
        ax7.set_xlabel('')
        plt.setp(ax7.get_xticklabels(), visible=False)
        #ax7.legend(prop={'size': 6})
        
        ax8.set_title('Field with $50 km^{2}$ area')
        ax8.set_ylabel('')
        ax8.set_xlabel('')
        plt.setp(ax8.get_xticklabels(), visible=False)
        plt.setp(ax8.get_yticklabels(), visible=False)
        #ax8.legend(prop={'size': 6})
        
        ax9.set_title('Field with $100 km^{2}$ area')
        ax9.set_ylabel('')
        ax9.set_xlabel('')
        plt.setp(ax9.get_xticklabels(), visible=False)
        plt.setp(ax9.get_yticklabels(), visible=False)
        #ax9.legend(prop={'size': 6})
        
        
        
        #ax10.set_title('Field with $25 km^{2}$ area')
        ax10.set_ylabel('Mission efficiency')
        ax10.set_xlabel('CS coverage radius')
        #ax7.set( ylim = (1.0,2.0) )
        #ax7.legend(prop={'size': 6})
        
        #ax11.set_title('Field with $50 km^{2}$ area')
        ax11.set_ylabel('')
        ax11.set_xlabel('CS coverage radius')
        plt.setp(ax11.get_yticklabels(), visible=False)
        #ax8.set( ylim = (1.0,2.0) )
        #ax8.legend(prop={'size': 6})
        
        #ax12.set_title('Field with $100 km^{2}$ area')
        ax12.set_ylabel('')
        ax12.set_xlabel('CS coverage radius')
        plt.setp(ax12.get_yticklabels(), visible=False)
        #ax9.set( ylim = (1.0,2.0) )
        #
        
        
        handles, labels = ax10.get_legend_handles_labels()
        fig2.legend(handles, labels, loc=7, title = 'Legend')
        
        for curAx in [ax7,ax8,ax9,ax10,ax11,ax12]:
        
            curAx.get_legend().remove()
            box = curAx.get_position()
            curAx.set_position([box.x0, box.y0, box.width*0.9, box.height])
        
        
        
        
        fig1.subplots_adjust(left = 0.1, right = 0.88, wspace =0.05 , hspace = 0.05)
        fig2.subplots_adjust(left = 0.1, right = 0.88, wspace =0.05, hspace = 0.05)
        
        imType = ['.png','.eps','.svg']
        
        for im in imType:
            
            filename1= '{}{}'.format('TestDataSummary_DistPlot',im)
            filename2= '{}{}'.format('TestDataSummary_TimePlot',im)
            
            file_path1 = os.path.join(directory, filename1)
            file_path2 = os.path.join(directory, filename2)
            
        
            fig1.savefig(file_path1)
            fig2.savefig(file_path2)
        
        
        


if __name__ == '__main__':
    
    
    directory = './data/09_16_2020__19_12_29'
    filename = 'TestData_nTrial_5.csv'
    file_path = os.path.join(directory, filename)
    
    
    
    analysis = Analysis(filepath = file_path)
    analysis.create_figs(directory = directory)
    analysis.summaryByConfiguration(directory = directory)
    analysis.summaryByAreaCSRadius(directory = directory)














