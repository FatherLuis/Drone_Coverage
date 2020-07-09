import numpy as np 
from Triangle import Triangle
from scipy.spatial import Voronoi
from shapely.geometry import Polygon
from shapely.geometry import LineString

########################################
# Class name: Edge
# Class Author: Luis E. Vargas Tamayo
# Purpose of the class: Create an object that acts as an Edge of a Figure. 
#                       Has methods that are useful for the Field Class
# Date: 3/18/2020
# List of changes with dates: none
########################################
class Edge():

    ##############################################
    # Method Name: __init__
    # Purpose: Class Constructor
    # Parameter: two tuples (x,y)
    # Method used: None
    # Return Value: None
    # Date: 3/18/2020
    ##############################################
    def __init__(self,p1,p2):

        # SAVES THE EDGE END POINTS
        
        self.a = np.array( p1 )
        self.b = np.array( p2 )

        # STORE THE DOMAIN AND RANGE OF THE EDGE
        self.xdomain = np.array( sorted((p1[0],p2[0])) )
        self.yrange = np.array( sorted((p1[1],p2[1])) )

    ##############################################
    # Method Name: in_range()
    # Purpose: checks if a y-value is in the edge's range
    # Parameter: Float
    # Method used: None
    # Return Value: Boolean
    # Date: 3/18/2020
    ##############################################
    def in_range(self, y_value):
        return self.yrange[0] <= y_value and y_value <= self.yrange[1]

    ##############################################
    # Method Name: in_domain()
    # Purpose: checks if a x-value is in the edge's domain
    # Parameter: Float
    # Method used: None
    # Return Value: Boolean
    # Date: 3/18/2020
    ##############################################
    def in_domain(self, x_value):
        return self.xdomain[0] <= x_value and x_value <= self.xdomain[1]   

    ##############################################
    # Method Name: intersect_horizontal_line()
    # Purpose: Given a horizontal line, find the x-value of the intersection (if any)
    # Parameter: Float
    # Method used: None
    # Return Value: (x1,x2): if intersection is the whole domain of the edge
    #               (x1,): if the intersection is a vertices
    #               (x1,x1): if intersection hits one point on the edge, that's not a vertex
    #               NONE : if not intersection occured
    # Date: 3/18/2020
    ##############################################
    def intersect_horizontal_line(self,y_value):


        if ( self.in_range(y_value) ):

            # IF EDGE IS HORIZONTAL
            if( self.b[1] - self.a[1] == 0 ):
                return (self.xdomain[0], self.xdomain[1]) 
            # IF Y-VALUE IS THE B VERTEX
            elif( self.b[1] == y_value ):
                return (self.b[0],) 
            # IF Y-VALUE IS THE A VERTEX
            elif( self.a[1] == y_value ):
                return (self.a[0],) 
            # IF EDGE IS VERTICAL
            elif( self.b[0] - self.a[0] == 0 ):
                return (self.xdomain[0], self.xdomain[1]) 
            else:

                slope = ( self.b[1] - self.a[1] ) / ( ( self.b[0] - self.a[0] )*1.0 )
                x_val = ( (y_value - self.a[1])/ slope ) + self.a[0]

            return (x_val,x_val)
        
        return None


    ##############################################
    # Method Name: __str__()
    # Purpose: overrides the default print() method used on this object. When print() is used, information of the triangle is printed
    # Parameter: None
    # Method used: None
    # Return Value: None
    # Date:  3/2/2020
    ##############################################
    def __str__(self):
        str_points = "Edge Points: a:{}, b:{}".format(self.a,self.b)
        str_domain = "Domain: {}".format(self.xdomain)
        str_range = "Range: {}".format(self.yrange)

        return "{}\n{}\n{}\n".format(str_points,str_domain,str_range)


########################################
# Class name: Field
# Class Author: Luis E. Vargas Tamayo
# Purpose of the class: Create a binary grid from a given shape
# Date: 3/18/2020
# List of changes with dates: none
########################################
class Field():

    ##############################################
    # Method Name: create_edges()
    # Purpose: From the given list of boundary points, create edge objects
    # Parameter: None
    # Method used: None
    # Return Value: None
    # Date: 3/18/2020
    ##############################################
    def create_edges(self,poly):

        # GET SIZE OF THE ARRAY
        N = len(poly)
        # CREATE EMPTY LIST TO STORE EDGE OBJECTS
        edges = []

        # LOOP THOUGH ALL THE POINTS AND CREATE EDGES
        for i in range(N):

            if( i == N-1):
                edge = Edge(poly[i] , poly[0])
            else:      
                edge = Edge(poly[i] , poly[i+1])

            edges.append(edge)

        return edges

    ##############################################
    # Method Name: domain_set()
    # Purpose: given a y_value, find the domains from the edges, that are contained within the boundary
    # Parameter: y_value
    # Method used: None
    # Return Value: list of tuples (x1,x2) or(x1,x1)
    # Date: 3/18/2020
    ##############################################
    def domain_set(self,y_value,edges):

        # CREATE A EMPTY LIST TO STORE TUPLES ( REPRESENTS DOMAINS)
        border_domain = []

        # LOOP THROUGH ALL THE EDGES
        for edge in edges:

            # STORE VALUE RETURNED FROM THE METHOD
            x_value = edge.intersect_horizontal_line(y_value)

            # CHECK IF THERE WAS AN INTERSECTION
            if ( not( x_value == None) ):
                
                # ADD DOMAIN TO THE LIST
                border_domain.append( x_value ) 

        # IF THERE IS ELEMENT IN THE LIST, THEN RETURN NOTHING
        if ( len(border_domain) == 0):
            return None 
      


        #######################
        # THERE ARE THREE DIFFERENT ELEMENTS IN THE LIST
        # (X1,X2) : A DOMAIN 
        # (X1,) : A VERTEX OF THE FIELD
        # (X1,X1): A X-VALUE FROM INTERSECTION

        # WHEN RAY CASTING, ELEMENT[i]  WILL TELL US THAT WE'RE INSDE THE SHAPE
        # ELEMENT[i+1] WILL TELL US WE'RE OUTSIDE THE SHAPE

        # HOW TO CREATE DOMAINS THAT SHOW WE'RE INSDE THE SHAPE?

        # IF AN ELEMENT IS:
        # (X1,X2), THEN THAT'S ALREADY A DOMAIN
        # (X1,) , (X2,X2) OR (X1,X1),(X2,) : THEN, CREATE A DOMAIN, SUCH AS (X1,X2)
        # (X1,) , (X1,): THEN, CREATE A DOMAIN, SUCH AS (X1,X1) IF ELEMENT[I+2] IS NOT (X2,X2)
        # (X1,X1) , (X2,X2): THEN, CREATE A DOMAIN, SUCH AS (X1,X2)

        #######################

        # SORT THE TUPLES BASED ON THE FIRST ELEMENT 
        border_domain_sort = sorted(border_domain, key= lambda x: x[0])
        #print(border_domain_sort)

        # CREATE A EMPTY SET TO STORE THE DOMAIN SETS
        domain_set = set([])

        # GET THE SIZE OF THE BORDER DOMAINS
        N = len(border_domain_sort)

        i = 0
        # LOOPS THROUGH ALL THE DOMAINS AND ENSURE THAT THERE ARE VALID
        while (i < N):

            # IF ELEMENT[i] IS (X1,X2), THEN ADD THIS TO THE DOMAIN SET
            # SINCE THIS IS A DOMAIN
            if(len(border_domain_sort[i])==2 and len(border_domain_sort[i]) == len(set(border_domain_sort[i]))):

                domain_set.add(border_domain_sort[i])

            else:
                
                # IF THE ELEMENT[i] IS A VERTEX AND THERE IS EXIST ELEMENT[i+2] AND ELEMENT[i+2] IS NOT A VERTEX OR A (X1,X2)
                if( len(border_domain_sort[i])==1 and (i+2 < N) and (len(set(border_domain_sort[i+2])) == 1) and (len(border_domain_sort[i+2]) == 2)  ):
                    
                    # CREATE A TUPLE THAT REPRESENTS A DOMAIN (ELEMENT[i], ELEMENT [i+2])
                    domain_set.add( (border_domain_sort[i][0] , border_domain_sort[i+2][0] ) )
                    # SKIP TWO ITERATIONS
                    i = i + 2

                # IF THERE EXIST AN ELEMENT[i+1]
                elif(i+1 < N):
                    
                    # IF ELEMENT[i+1] IS A VERTEX (X1,)
                    if( len(set(border_domain_sort[i+1])) == 1 ):

                        # CREATE A TUPLE THAT REPRESENTS A DOMAIN (ELEMENT[i], ELEMENT [i+1])
                        domain_set.add( (border_domain_sort[i][0] , border_domain_sort[i+1][0] ) )
                        i = i + 1

                    else:
                        # CREATE A TUPLE THAT REPRESENTS A DOMAIN (ELEMENT[i], ELEMENT [i])
                        domain_set.add( (border_domain_sort[i][0] , border_domain_sort[i][0]  ) )

                # IF ELEMENT IS NOT A VERTEX (X1,) OR A DOMAIN (X1,X2)
                else:
                    # CREATE A TUPLE THAT REPRESENTS A DOMAIN (ELEMENT[i], ELEMENT [i])
                    domain_set.add( (border_domain_sort[i][0] , border_domain_sort[i][0]  ) )             
            
            i+=1

        #print(domain_set)
        return domain_set

    ##############################################
    # Method Name: ccreate_matrix_field()
    # Purpose: create a binary grid that represents the shape from the given boundary field points
    # Parameter: None
    # Method used: domain_set(),create_edge()
    # Return Value: binary 2D array
    # Date: 3/18/2020
    ##############################################
    def create_matrix_field(self, poly , step = 0.1):

        edges = self.create_edges(poly)

        # CREATE A LIST THAT HOLDS THE X-VALUES FROM THE POINTS
        x_lst = [x[0] for x in poly]
        # CREATE A LIST THAT HOLDS THE Y-VALUES FROM THE POINTS
        y_lst = [y[1] for y in poly]

        # STORE THE MIN VALUE FROM X-LIST
        xmin = np.min(x_lst) - step
        # STORE THE MAX VALUE FROM THE X-LIST
        xmax = np.max(x_lst) + step


        # STORE THE MIN VALUE FROM THE Y-LIST
        ymin = np.min(y_lst) - step
        # STORE THE MAX VALUE FROM THE Y-LIST
        ymax = np.max(y_lst) + step


        # CREATE AN ARRAY WITH EVENLY SPACED VALUES FROM MIN TO MAX, QUANTITY BEING THE NUMBER OF PIXELS
        x_values = np.arange(xmin,xmax,step)
        y_values = np.arange(ymin,ymax,step)
        
        nx = len(x_values)
        ny = len(y_values)
        
        # CREATE A 2D ARRAY OF SIZE PIXEL X PIXEL
        matrix = np.zeros( (nx,ny) )

        # ITERATE THROUGH EACH COLUMN
        for i in range(ny):

            #print("")
            #print("Index: ", i , "Y-Value: ", y_values[i] )
            # STORE THE DOMAINS THAT ARE INSIDE THE SHAPE FROM THE GIVEN Y-VALUE
            domain_set = self.domain_set(y_values[i],edges)

            # CHECK IF THERE EXIST DOMAINS THAT ARE VALID FOR Y-VALUE
            if(not (domain_set == None)):
                
                # ITERATE THROUGH ALL THE DOMAINS IN THE SET
                for domain in domain_set:
                    
                    # CHECK IF X-VALUES ARE IN THE DOMAIN
                    inDomain = (domain[0] <= x_values) == (x_values <= domain[1])
                    # ALL THE X_VALUES THAT ARE VALID WILL RECEIVE A 1
                    matrix[inDomain,i] = 1


        return matrix.astype(int), xmin,xmax,ymin,ymax,nx, ny


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














