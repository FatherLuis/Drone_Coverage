import numpy as np




##############################################
# Method Name: dist()
# Purpose: Calculate eucledian distance between two points
# Parameter: two tuples-like objects (x,y)
# Method used: None
# Return Value: Float
# Date:  3/2/2020
##############################################  
def dist(p1,p2):
    return np.sqrt( (p2[1]-p1[1])**2 +(p2[0]-p1[0])**2)













