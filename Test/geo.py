# -*- coding: utf-8 -*-
import numpy as np

box = [[-10,-10],[-10,10],[10,10],[10,-10]]


points = np.array([[0, 0], [1,1],[0, 1],[1,0]] + box)
from scipy.spatial import Voronoi, voronoi_plot_2d


vor = Voronoi(points)

lst = []


print(vor.points)
print('')
print(vor.point_region)
print('')

for p in vor.regions:
    print(p)



for i in vor.point_region:
    
    reg = np.array(vor.regions[i])
    
    if np.all(reg >= 0) and reg.size > 0:
        lst.append(vor.vertices[reg])

print('')
for p in lst:
    print(p,'\n')

import matplotlib.pyplot as plt
fig = voronoi_plot_2d(vor)
plt.show()