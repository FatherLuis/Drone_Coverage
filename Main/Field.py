import numpy as np 
from Triangle import Triangle


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


        return matrix.astype(int), xmin, xmax, ymin, ymax, nx, ny  


    ##############################################
    # Method Name: create_triangle()
    # Purpose: 
    # Parameter: None
    # Method used: 
    # Return Value: return a list of triangles
    # Date: 3/26/2020
    ##############################################
    def create_triangle(self,poly, vertex , vertex_acute_angle = False):


        A = vertex
        B = None
        C = None
        triangles = []

        N = len(poly)
        for i in range(N):

            if(i == N-1):
                
                B = np.array(poly[i])
                C = np.array(poly[0])
             
            else:

                B = np.array(poly[i])
                C = np.array(poly[i+1])


            curTriangle =  Triangle(A,B,C)

            if( vertex_acute_angle and curTriangle.A_angle > np.pi/2):

                x = np.array(  [ B[0],C[0]  ]    )
                y = np.array(  [ B[1],C[1]  ]    )

                x_mean = np.mean(x)
                y_mean = np.mean(y)

                xy_mean = np.array( [x_mean , y_mean] )

  

                triangle1 = Triangle(A , B , xy_mean)
                triangle2 = Triangle(A , xy_mean , C)

                triangles.append(triangle1)
                triangles.append(triangle2)
            
            else:

                triangles.append(curTriangle)

            
            
        
        return triangles







########### Testing the Class ###################################################

#poly = [ (1,1) , (5,1) , (5,5) ]
#poly = [ (1,1), (1,5),(5,5),(5,1) ]
#poly = [ (0,0) , (3,0) , (5,4), (4,7) , (2,5)]
#poly = [ (0,0) , (3,1), (6,0) , (9,1), (4,7), (0,4) ]
#poly = [ (0,2), (4,2), (4,6),(8,6),(8,2),(12,2),(12,10),(0,10)  ]
# poly = [ (0,0) , (3,0) , (6,0), (4,1), (3,4), (1,1), (0,4)  ]
# field = Field( poly )

# matrix = field.create_matrix_field(pixel = 200)

# #print(matrix)

# np.savetxt("field.txt" ,matrix, fmt='%0.f' )