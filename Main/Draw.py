import matplotlib.pyplot as plt
import numpy as np 

########################################
# Class name: Draw()
# Class Author: Luis E. Vargas Tamayo
# Purpose of the class: Create Plots that shows the path of the Drone
# Date: 3/12/2020
# List of changes with dates: none
########################################
class Draw():

    ##############################################
    # Method Name: __init__
    # Purpose: Class Constructor
    # Parameter: None
    # Method used: None
    # Return Value: None
    # Date:  3/12/2020
    ##############################################
    def __init__(self):

        # CREATE A FIGURE OBJECT (REFERENCE IT?)
        self.fig = plt.figure()
        # CREATE A SUBPLOT IN THE FIGURE 
        self.ax = self.fig.add_subplot(111)
        
    ##############################################
    # Method Name: boundary()
    # Purpose: Create a plot that draws the boundary of a 2D shape
    # Parameter: A list of points (x,y)
    # Method used: None
    # Return Value: None
    # Date:  3/12/2020
    ##############################################
    def boundary(self, lst_pts, col = 'k'):
        
        # GET THE SIZE OF THE LIST
        N = len(lst_pts)

        # ITERATE THROUGH THE LIST OF POINTS
        for i in range(N):

            # SELECT i ELEMENT FROM THE LIST
            x1 = lst_pts[i][0]
            y1 = lst_pts[i][1]

            # IF THIS IS THE LAST ELEMENT IN THE LIST
            if( i == N-1):
                
                # DRAW A LINE FROM THE LAST ELEMENT TO THE FIRST ELEMENT 
                self.ax.plot( (lst_pts[0][0] ,  x1) , (lst_pts[0][1] ,y1) ,color= col)


            else:
                # SELECT i+1 ELEMENT FROM THE LIST
                x2 = lst_pts[i+1][0]
                y2 = lst_pts[i+1][1]              

                # DRAW A LINE FROM i ELEMENT TO i+1 ELEMENT
                self.ax.plot( (x1,x2) , (y1,y2) ,color=col)

    ##############################################
    # Method Name: path()
    # Purpose: Create a plot that draws a sequence of points
    # Parameter: A list of points (x,y)
    # Method used: None
    # Return Value: None
    # Date:  3/12/2020
    ##############################################
    def path(self,path_pts):

        # CREATE A TUPLE WITH THREE RANDOM NUMBERS ( USED FOR RGM COLORING)
        colors = np.random.rand(3,)
        
        # ITERATE THROUGH THE LIST OF POINTS
        for i in range( len(path_pts) - 1 ):

            # SELECT i ELEMENT FROM THE LIST
            x1 = path_pts[i][0]
            y1 = path_pts[i][1]

            # SELECT i+1 ELEMENT FROM THE LIST
            x2 = path_pts[i+1][0]
            y2 = path_pts[i+1][1]  

            # IF i ELEMENT IS IN THE ORIGIN, CHANGE COLORS
            # THIS HELPS IDENTIFY NEW PATHS FROM THE DRONE PROJECT
            if ( (x1==path_pts[0][0] and y1==path_pts[0][1])):
               
                # CREATE A TUPLE WITH THREE RANDOM NUMBERS ( USED FOR RGM COLORING)
                colors = np.random.rand(3,)
          
            # DRAW A LINE FROM i ELEMENT TO i+1 ELEMENT
            self.ax.plot( (x1,x2) , (y1,y2) , c = colors , linewidth = 1, alpha = 0.7 )


    def draw_sites_path(self,site_pts):

        # GET THE SIZE OF THE LIST
        N = len(site_pts)

        # ITERATE THROUGH THE LIST OF POINTS
        for i in range(N):

            # SELECT i ELEMENT FROM THE LIST
            x1 = site_pts[i][0]
            y1 = site_pts[i][1]

            # IF THIS IS THE LAST ELEMENT IN THE LIST
            if( i == N-1):

                self.ax.arrow(x1, y1, site_pts[0][0]-x1,site_pts[0][1]-y1, linewidth = 2, head_width=1, head_length=1, fc='k', ec='k')


            else:
                # SELECT i+1 ELEMENT FROM THE LIST
                x2 = site_pts[i+1][0]
                y2 = site_pts[i+1][1]              

                # DRAW A LINE FROM i ELEMENT TO i+1 ELEMENT
                self.ax.arrow(x1, y1, x2-x1, y2-y1, linewidth = 2,head_width=1, head_length=1, fc='k', ec='k')


    def draw_sites(self,sites):

        for p in sites:
            self.ax.plot(p[0],p[1],'ro')


    ##############################################
    # Method Name: show_plot()
    # Purpose: Show the plots created (if any), otherwise, show a blank GUI
    # Parameter: None
    # Method used: None
    # Return Value: None
    # Date:  3/12/2020
    ##############################################
    def show_plot(self):

        # MAKES SURE THE PLOT IS EVEN AND WONT HAVE DISTURSIONS
        plt.gca().set_aspect('equal',adjustable='box')
        # SHOW PLOTS
        plt.show()











