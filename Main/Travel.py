



def traveling(voronoi_lst):


    N = len(voronoi_lst)


    travel = []

    set1 = None
    set2 = None 

    for i in range(N):

        voronoi = voronoi_lst[i][0]

        CS = voronoi_lst[i][1]

        if( i == 0 ):
            
            set1 = set(voronoi)
            #travel.append(CS)

        else:

            set2 = set(voronoi)

            interPts = set1.intersection(set2)
            print('------------------------------')
            print(set1)
            print('\n')
            print(set2)

            for p in interPts:

                if not(p in travel):
                    travel.append(p)
                    break

            #travel.append(CS)
            set1 = set(voronoi)


            if( i == N-1 ):
                print('------------------------------')
                print(set1)
                print('\n')
                print(set2)
                print('\n\n\n')

                set2 = set(voronoi_lst[0][0])

                interPts = set1.intersection(set2)
            
                for p in interPts:

                    if not(p in travel):
                        travel.append(p)
                        break

    return travel , formatPts(travel)


def formatPts(travelPts):


    N = len(travelPts)

    entry_exit_lst = []

    for i in range(N):

        if( i == 0 ):

            entry_exit = [travelPts[i],travelPts[-1]]
            entry_exit_lst.append(entry_exit)

        else:

            entry_exit = [travelPts[i-1],travelPts[i]]
            entry_exit_lst.append(entry_exit)

    return entry_exit_lst





if __name__ == '__main__':

    # IF THIS FILE IS RUN, THE FOLLOWING CODE WILL BE READ

    v1 = [  [ (0,0), (0,10), (10,10), (10,0)  ]  , (5,5)  ]
    v2 = [  [ (0,10), (0,20), (10,20), (10,10)  ]  , (5,15)  ]
    v3 = [  [ (10,10), (10,20), (20,20), (20,10)  ]  , (15,15)  ]
    v4 = [  [ (10,0), (10,10), (20,10), (20,0)  ]  , (15,5)  ]


    voronoi_lst = [ v1, v2, v3, v4 ]

    a = traveling(voronoi_lst)

    print(a[0])
    print('')
    print(a[1])







