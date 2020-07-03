# -*- coding: utf-8 -*-


from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path


graph = [[0,1,0],
         [1,0,1],
         [0,1,0]]


graph = csr_matrix(graph)

dist_matrix, predecessors = shortest_path(csgraph=graph, directed=False, return_predecessors=True)


print(dist_matrix)
print('')
print(predecessors)
print('')


def get_path(Pr, i, j):
    path = [j]
    k = j
    while Pr[i, k] != -9999:
        path.append(Pr[i, k])
        k = Pr[i, k]
    return path[::-1]


print(get_path(predecessors, 2, 0))






