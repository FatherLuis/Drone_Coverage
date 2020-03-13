
import Triangle
import Drone
import Drone_Path
import Draw


### INITIALIZE ###

rad = 2
mxDist = 500

a = (0,0) # CHARGING STATION
b = (0,100) # LONGEST SIDE
c = (80,60) # OTHER SIDE

### ALGORITHM ###

shape = Triangle.Triangle(a,b,c)

drone = Drone.Drone(radius=rad, max_distance = mxDist)

path = Drone_Path.Drone_Path(shape , drone)

path.algorithm()

### DRAW PLOTS ###
Canvas = Draw.Draw()

Canvas.triangle_boundary(shape.get_all_points())

Canvas.path(path.path)

Canvas.show_plot()










