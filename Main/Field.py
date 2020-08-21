import numpy as np 
from Triangle import Triangle
from scipy.spatial import Voronoi
from shapely.geometry import Polygon
from shapely.geometry import LineString
from matplotlib.path import Path

########################################
class Field():



    ##############################################
    # Method Name: create_matrix_field()
    # Purpose: create a mask vector that represents the shape from the given boundary field points
    # Parameter: None
    # Method used: None
    # Return Value: binary 1D array, xVec yVec, nx, ny
    # Date: 8/18/2020
    ##############################################
    def create_matrix_field(self, poly , step = 0.1, direction = 'cw'):

        # THE DIRECTION OF THE BOUNDARY VERTICES ORDER MATTER.
        # WHEN USING 'contain_path' WE WANT TO ALSO INCLUDE THE POINTS IN THE EDGES. THE PADDING WILL INCREASE 'path' 
        # SO THAT ANYTHING IN THE PATH AND ALONG IT WILL BE INCLUDED IN THE RESULT.
        if direction == 'ccw':
            
            pathPadding = 1E-8
            
        elif direction == 'cw':
            
            pathPadding = -1E-8
            
        else:
            
            pathPadding = 0
        
        
        
        
        # CREATE A LIST THAT HOLDS THE X-VALUES FROM THE POINTS
        x_lst = [x[0] for x in poly]
        # CREATE A LIST THAT HOLDS THE Y-VALUES FROM THE POINTS
        y_lst = [y[1] for y in poly]
        
        # THE 'step' IS ADDED TO THE MIN AND MAX TO CREATE A PADDING AROUND THE SHAPE

        # STORE THE MIN VALUE FROM X-LIST
        xmin = np.min(x_lst) - step
        # STORE THE MAX VALUE FROM THE X-LIST
        xmax = np.max(x_lst) + 2*step # THE ARANGE() WILL STOP AT 1*STEP

        # STORE THE MIN VALUE FROM THE Y-LIST
        ymin = np.min(y_lst) - step
        # STORE THE MAX VALUE FROM THE Y-LIST
        ymax = np.max(y_lst) + 2*step # THE ARANGE() WILL STOP AT 1*STEP


        # CREATE AN ARRAY WITH EVENLY SPACED VALUES FROM MIN TO MAX, QUANTITY BEING THE NUMBER OF PIXELS
        x_values = np.arange(xmin,xmax,step)
        y_values = np.arange(ymin,ymax,step)
        
        nx = len(x_values)
        ny = len(y_values)
        


        # CREATE VECTORS
        xVec = np.repeat( x_values, ny ) # [1,1,1.....2,2,2......3,3,3.....] 
        yVec = np.tile( y_values , nx ) # [1,2,3......1,2,3......1,2,3.....]
        
        # CREATE COORDINATES FOR THE GRID
        coors = [(x,y) for x,y in zip(xVec,yVec)]
        
        # PATH OBJECT CREATED
        poly_path = Path(poly)
        
        # CREATE A MASK OF THE POLYNOMIAL (RETURNS 1D) (bool)
        mask = poly_path.contains_points(coors,radius = pathPadding)


        # import matplotlib.pyplot as plt
        # matrix = mask.reshape(nx, ny)
        # plt.imshow(matrix)
        # plt.show()
        
  
        

        return mask, xVec,yVec, nx, ny


    ##############################################
    # Method Name: create_triangle()
    # Purpose: Given a polygon, split the polygon into triangles from a given point within the polygon
    # Parameter: poly: a list of points that define the perimeter of a polygon
    #            vertex: a point inside the polygon that will be used to split the polygon into triangles
    # Method used: none
    # Return Value: return a list of triangles
    # Date: 3/26/2020
    ##############################################
    def create_triangle(self, poly, vertex):

        
        
        def isOnEdge(vertices,pOI):
            
            isOn = False
            edge = None
            dist = lambda p1,p2: np.sqrt( (p2[1]-p1[1])**2 +(p2[0]-p1[0])**2)
            
            # CREATE A LIST OF VERTICES
            lst1 = vertices.copy()
            
            # CREATE A LIST OF VERTICES WITH A SHIFT OF 1 
            # THAT IS, THE FIRST ELEM IS MOVED TO THE END OF THE LIST
            lst2 = vertices.copy()
            lst2.append(lst2.pop(0))
            
            EPSILON = 1E-8
            
            # WE'LL CREATE AN EDGE USING THE LSTS CREATED ABOVE
            
            for p1,p2 in zip(lst1,lst2):
                
                if abs(dist(p1, pOI) + dist(p2, pOI) - dist(p1, p2)) < EPSILON:
                    
                    isOn = True
                    edge = [p1,p2]
                    break
                
            return isOn,edge
        

        
        # THERE ARE THREE CASES TO CONSIDER
        # CASE 1: VERTEX IS ONE OF THE VERTICES OF THE POLYGON
        # CASE 2: VERTEX IS ON THE EDGE OF THE POLYGON
        # CASE 3: VERTEX IS INSIDE THE POLYGON
        
        
        # NOTE: WE ARE ASSUMING POINT OF INTEREST 
        #       WILL NOT BE OUTSIDE THE POLYGON
        
        
        # POINT OF INTEREST
        pOI = list(vertex)
        
        # LIST OF VERTICES
        # ( MAKE SURE THE ELEMS ARE OF TYPE LIST: SAME AS THE 'pOI')
        vertices = list(poly)
        vertices = [list(x) for x in vertices]
        
        
        # LIST THAT WILL STORE THE TRIANGLE OBJECTS
        triangleLst = [] 
        
        nV = len(vertices)
        
        A = pOI
        B = None
        C = None
       
        

        
        ############################
        # CASE I: pOI IS ONE OF THE VERTICES OF THE POLYGON
        ############################
        
        if vertex in poly:

            
            # LET THE VERTEX BE THE FIRST ELEMENT IN THE LIST
            while not(np.array_equal(pOI,vertices[0])):
                # POP OFF THE FIRST ELEM, AND PLACE IT AT THE END OF THE LIST
                vertices.append(vertices.pop(0))           
                    
            for i in range(1,nV-1):
                
                B = vertices[i]
                C = vertices[i+1]
                
                
                tri = Triangle(A,B,C)
                
                triangleLst.append(tri)
                
            return triangleLst
                

        
        
        ############################
        # CASE II: pOI IS ON THE EDGE OF THE POLYGON
        ############################
        
        # CHECK IF POINT IS ON THE EDGE
        # EDGE: CONTAINS THE POINTS THAT CREATE THE EDGE IN WHICH 
        # THE POINT IS LOCATED
        isOn , edge = isOnEdge(vertices,pOI)
        
        if isOn:
            
            
            for i in range(nV):
                
                
                if i == nV-1:
                    
                    B = vertices[0]
                    C = vertices[-1]  
                    
                else: 
                    
                    B = vertices[i]
                    C = vertices[i+1]

                # CHECK IF B AND C ARE THE VERTICES OF THE EDGE
                isEdgeVertex1 = ( np.array_equal(B,edge[0]) or np.array_equal(B,edge[1])) 
                isEdgeVertex2 = ( np.array_equal(C,edge[0]) or np.array_equal(C,edge[1]))
                
                # IF B AND C ARE NOT BOTH THE VERTICES OF THE  EDGE
                if not(isEdgeVertex1 and isEdgeVertex2):
                    
                    tri = Triangle(A,B,C)
                    
                    triangleLst.append(tri)
         
                    
            return triangleLst        
        
        
        
        ############################
        # CASE III: pOI IS INSIDE THE POLYGON
        ############################
        
        # pOI WAS NOT A VERTEX NOR WAS IT ON THE EDGE OF THE POLYGON
        # THIS, IT MUST BE INSIDE THE POLYGON
                
        
        for i in range(nV):

            # IF THIS IS THE LAST POINT IN THE LIST, THEN WE'LL CREATE A TRIANGLE
            # USING THE LAST POINT, VERTEX, AND THE FIRST POINT
            if(i == nV-1):
                
                # VERTEX B IS THE LAST POINT IN THE LIST
                B = vertices[i]
                # VERTEX C IS THE FIRST POINT IN THE LIST
                C = vertices[0]
            
            else:
                # VERTEX B IS THE CURRENT POINT IN THE LIST
                B = vertices[i]
                # VERTEX C IS THE NEXT POINT IN THE LIST
                C = vertices[i+1]

            # CREATE A TRIANGLE BASED ON THE THREE POINTS GIVEN
            curTriangle =  Triangle(A,B,C)

            # ADD THE TRIANGLE IN THE ARRAY
            triangleLst.append(curTriangle)     
        
        
        return triangleLst
        




    def create_voronoi_polygons(self,site=None,boundary = None):
        # site is a list

        if len(site) == 1:
            return [ [boundary, site[0]] ]


        ### Create a box to bound
        
        xVal = np.array([x[0] for x in boundary])
        yVal = np.array([y[1] for y in boundary])
        
        xmin = np.min(xVal) 
        xmax = np.max(xVal) 
        ymin = np.min(yVal) 
        ymax = np.max(yVal) 
        
        diffx = xmax - xmin
        diffy = ymax - ymin

        xmin -= 5*diffx
        xmax += 5*diffx 
        ymin -= 5*diffy  
        ymax += 5*diffy          
        
        
        # CREATE FOUR PROXY SITES TO BOUND THE VORONOI REGIONS OF INTEREST
        box = [ [xmin,ymin] , [xmin,ymax], [xmax,ymax] , [xmax,ymin] ] 
        
        
        ###################################

        # CREATE VORONOI REGIONS USING SCIPY LIBRARY
        vor = Voronoi(site + box)
        
        # CREATE A LIST THAT WILL STORE THE VORONOI REGIONS (LIST OF VERTICES)
        voronois = []
        
        # CONNECTING THE INFORMATION GIVEN BY THE VORONOI CLASS
        # TO CREATE OUR REGIONS OF INTEREST
        for i in vor.point_region:
            
            reg = np.array(vor.regions[i])
            
            if np.all(reg >= 0) and reg.size > 0:
                voronois.append(vor.vertices[reg])
            

        

        boundary_poly = Polygon(boundary)

        voronoi_lst = []
        for voronoi in voronois:
            voronoi_poly = Polygon(voronoi)
            result = boundary_poly.intersection(voronoi_poly)
        
            if result.is_empty:
                
                voronoi_lst.append(voronoi_poly)
        
            else:
                result_lst = list(result.exterior.coords)
                result_lst = result_lst[:-1]
    
                voronoi_lst.append(result_lst)


        

        return [ item  for item in zip(voronoi_lst,site)    ]














