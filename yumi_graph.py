from collections import defaultdict as dd
from math import inf

class edge:
    def __init__(self, to:int, cost:int, cap:int, flow:int, rev_edge:int):
        self.to = to
        self.cost = cost
        self.cap = cap
        self.flow = flow
        self.rev_edge = rev_edge
    
    def __repr__(self):
        return f"-> {self.to}"

graph:dict[int, list[edge]] = dd(list)  # grafo del sistema donde por cada nota hay 3 vertices y cada arista tiene su inversa

def add_edge(v:int, u:int, cost:int, cap:int):
    # para acceder a la arista inversa en el grafo residual u -> v sería graph[e.to][e.rev_edge]
    # lo mismo para desde la inversa ir a la arista del grafo
    index_v = len(graph[v])                           # donde se va a ubicar la arista del grafo
    index_u = len(graph[u])                           # donde se va a ubicar la arista reversa del grafo residual
    graph[v].append(edge(u,  cost, cap, 0, index_u))  # arista del grafo v -> u
    graph[u].append(edge(v, -cost,   0, 0, index_v))  # arista inversa del grafo residual u -> v


def create_graph(a:list[int]):
    n = len(a)
    s = 0
    t = 3*n+1
    refer:dict[int, int] = {}          # diccionario que guarda la posicion mas cercana de los valores visitados
    modul:dict[int, int] = {}          # diccionario a lo sumo con tamaño 7 que guarda la posicion mas cercana de los valores % 7 (congruencia)

    for i in range(n, 0, -1):
        value = a[i-1]
        add_edge(s, 3*i-1, 0, 1)       # este es vi,1
        add_edge(s, 3*i-2, 0, 1)       # este es vi,2
        add_edge(3*i-1, 3*i, -1, 1)
        add_edge(3*i-2, 3*i, -1, 1)    
        add_edge(3*i, t, 0, 1)         # este es vi,3        
        
        iequal_valid = igreater_valid = ilower_valid = imodule_valid = False  
        try:
            ie = refer[value]
            iequal_valid = True
        except: None
        try:
            ig = refer[value+1]
            igreater_valid = True
        except: None
        try:
            il = refer[value-1]
            ilower_valid = True
        except: None
        try:
            im = modul[value%7]
            imodule_valid = True
        except: None
        
        if iequal_valid: add_edge(3*i-1, 3*ie-1, 0, 1)
        if igreater_valid and (not iequal_valid or ig < ie): add_edge(3*i, 3*ig-1, 0, 1)
        if ilower_valid   and (not iequal_valid or il < ie): add_edge(3*i, 3*il-1, 0, 1)
        if imodule_valid: 
            add_edge(3*i-2, 3*im-2, 0, 1)
            add_edge(3*i, 3*im-2, 0, 1)
        refer[value] = modul[value%7] = i
    
    return s, t

s, t = create_graph([1, 3, 4, 7, 8, 2])
print(graph)