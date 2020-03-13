import matplotlib.pyplot as plt
import numpy as np 



class Draw():

    def __init__(self):

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        

    def triangle_boundary(self, lst_pts):
        #Draw shape

        N = len(lst_pts)
        for i in range(N):

            x1 = lst_pts[i][0]
            y1 = lst_pts[i][1]

            if( i == N-1):
                
                self.ax.plot( (0,x1) , (0,y1) ,color='k')

            else:

                x2 = lst_pts[i+1][0]
                y2 = lst_pts[i+1][1]              

                self.ax.plot( (x1,x2) , (y1,y2) ,color='k')


    def path(self,path_pts):

        colors = np.random.rand(3,)
        
        for i in range( len(path_pts) - 1 ):

            x1 = path_pts[i][0]
            y1 = path_pts[i][1]

            x2 = path_pts[i+1][0]
            y2 = path_pts[i+1][1]  

            if ( (x1==0 and y1==0)):

                colors = np.random.rand(3,)
          
            self.ax.plot( (x1,x2) , (y1,y2) , c = colors , linewidth = 2 )

    def show_plot(self):
        plt.gca().set_aspect('equal',adjustable='box')
        plt.show()











