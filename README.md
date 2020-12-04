
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/3.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/">Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License</a>.


# Optimal Drone Field Coverage




## Required Packages 
- Numpy (1.18.1)
- Scipy (1.4.1)
- Matplotlib (3.1.3)
- Shapely (1.7.0)
- Cvxopt (1.2.0)

 
## Program Submodules


### Mask of Field [(Source)](Main/Field.py)
- First, a large set of 'dots' are created in a grid that captures the region. 
![Rectangular Mask](images/RectangularMask.png)

- Then, we use matplotlib.Path to create the mask of the figure. The 'dots' that remain, are the coordinates that are inside the region.
![Figure Mask](images/FigureMask.png)


### Optimal Charging Station Location [(Source)](Main/minCharge.py)
- We use a linear program that finds the optimal locations to place the charging stations such that it minimizes the mission time of the drone per Charging Station (CS) coverage region.
![Optimal CS](images/OptimalCS.png)


### Voronoi Regions [(Source)](Main/Field.py)
- We create Voronoi regions to specify what region the drone will be covering per CS location.
![Voronoi Region](images/VoronoiRegions.png)


### Walk [(Source)](Main/Tourfn2.py)
- We use a linear program to minimize the edges used to traverse the CS. The area covered by the traversal are removed from the drone mission algorithm applied to each triangular region.
![Walk](images/walk.png)


### Triangularization [(Source)](Main/Field.py)
- We triangulate each Voronoi region to apply the drone mission algorithm.
![Triangularization](images/triangularization.png)

### Drone mission algorithm [(Source)](Main/DronePath2.py)
- Here, we show the path the drone takes in a triangular region. Each color represents a new cycle after each recharge.
![Triangular Path](images/trianglePath.png)

### Run [(Source)](Main/Run.py)
- This is the final product when putting the submodules together.
![Complete Drone Path](images/DronePath.png)



## Contribution
- @[SK-Thomas](https://github.com/SK-Thomas)
- @[christhron](https://github.com/christhron)

## Publication
<a href = 'https://www.mdpi.com/869818'> Cost-Minimizing System Design for Surveillance of Large, Inaccessible Agricultural Areas Using Drones of Limited Range </a>
