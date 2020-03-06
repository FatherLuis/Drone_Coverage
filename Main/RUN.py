
import Triangle
import Drone
import Drone_Path
import matplotlib.pyplot as plt


a = (0,0)
b = (0,100)
c = (50,60)


shape = Triangle.Triangle(a,b,c)

print(shape)

drone = Drone.Drone(radius=1)

path = Drone_Path.Drone_Path(shape,drone)
path.algorithm()

# print(path.print_path())



# Very simple way to draw the triangle and lines
polygon = shape.get_all_points()
poly = [ [x[0] for x in polygon] , [y[1] for y in polygon] ]
points =  [ [x[0] for x in path.path] , [y[1] for y in path.path] ]

#Draw shape
for i in range(len(poly)+1):
    
    if(i==len(poly)):
        plt.plot((poly[0][0],poly[0][-1]),(poly[1][0],poly[1][-1]),color='b')

    else:
        plt.plot(poly[0][i:i+2],poly[1][i:i+2],color='b')




for i in range(len(points[0])):

    plt.plot( points[0][i:i+2], points[1][i:i+2])




plt.show()









