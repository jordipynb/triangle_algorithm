from collections import defaultdict as dd
from math import inf

class edge:
    def __init__(self, cap:int, cost:int):
        self.cap = cap
        self.cost = cost

    def __repr__(self) -> str:
        return f'({self.cap}, {self.cost})'

def add_edge(graph:dict[int, dict[int, edge]], v:int, u:int, cap:int, cost:int):
    graph[v][u] = edge(cap,  cost) # arista del grafo v -> u
    graph[u][v] = edge(  0, -cost) # arista inversa del grafo residual u -> v

def add_edge_list(graph:dict[int, dict[int, edge]], v:int, index:list[int]):
    for elem in index: add_edge(graph, v, elem, 1, 0)

def create_residual_graph(a:list[int]):
    graph:dict[int, dict[int, edge]] = dd(lambda:dd(lambda:None))  # grafo del sistema donde por cada nota hay 3 vertices y cada arista tiene su inversa
    n = len(a)
    s = 0
    t = 2*n+1
    d = 2*n+2
    refer:dict[int, list[int]] = dd(list)          
    modul:dict[int, list[int]] = dd(list)        

    for i in range(n, 0, -1):
        value = a[i-1]
        add_edge(graph, s, 2*i-1, 1, 0)       # este es vi,1
        add_edge(graph, 2*i-1, 2*i, 1, -1)    # este es vi,2
        add_edge(graph, 2*i, t, 1, 0)     
          
        ig = refer[value+1]
        il = refer[value-1]
        im = modul[value%7]
        
        if len(ig) > 0: add_edge_list(graph, 2*i, ig)
        if len(il) > 0: add_edge_list(graph, 2*i, il)
        if len(im) > 0: add_edge_list(graph, 2*i, im)
        refer[value].append(2*i-1)
        modul[value%7].append(2*i-1)     
    add_edge(graph, t, d, 4, 0)

    return graph, s, d

def min_cost_flow(a:list[int]):
    G_f, s, t = create_residual_graph(a)
    output = 0
    flow = dd(lambda:dd(lambda:None))

    for v1,edges in G_f.items():
        for v2,_ in edges.items():
            if v2 > v1: flow[v1][v2]=0
    
    path, cap = find_path(G_f, s, t)   
    while not len(path)==0:
        for v1, v2 in path:
            if  v2 < v1: # la arista no esta en la red original por tanto es una arista de retroceso
                if G_f[v1][v2].cost == -1: output-=1
                flow[v2][v1] -= cap  #actualizar red original 
                G_f[v1][v2].cap = G_f[v1][v2].cap - cap   #actualizar arista de retroceso en la red residual
                G_f[v2][v1].cap = G_f[v2][v1].cap + cap   #actualizar arista original en la red residual
            else:                    # no es una arista de retroceso 
                if G_f[v1][v2].cost == -1: output+=1
                flow[v1][v2] += cap      #actualizar arista en la red original             
                G_f[v1][v2].cap = G_f[v1][v2].cap - cap     #actualizar arista original en la red residual
                G_f[v2][v1].cap = G_f[v2][v1].cap + cap      #actualizar arista de retroceso en la red residual
        path, cap = find_path(G_f, s, t)   
    return flow, output

#def Dijkstra(G:dict[node,dict[node,tuple(int,int)]],Q:tuple(node,node)):
#    S=[]
#    pi=defaultdict(lambda:None)
#    d=defaultdict(int)
#    while len(Q)>0:
#        u=extract_min(Q)
#        if u.v=='t': return pi
#        S.append(u)
#        for v,p in G[u].items():
#            if not p[0] == 0:
#                if d[v]>d[u]+G[u][v][1]:
#                    d[v]=d[u]+G[u][v][1]
#                    pi[v]=u

def Bellman_Ford(G:dict[int, dict[int, edge]], s:int):
    d = dd(lambda:inf)
    d[s] = 0
    pi = dd(lambda:None)
    for _ in range(len(G.keys())-1):
        for v1,edges in G.items():
            for v2,p in edges.items():
                if not p==None and not p.cap == 0 and not d[v1]==inf and d[v2]> d[v1]+ p.cost:
                    d[v2]=d[v1]+p.cost
                    pi[v2]=v1
    for v1,edges in G.items():
        for v2,p in edges.items():
            if not p==None and not p.cap == 0 and not d[v2]==inf and not d[v1]==inf and  d[v2]>d[v1]+p.cost:
                return None
    return pi

def find_path(G:dict[int, dict[int, edge]], s:int, t:int):
    pi = Bellman_Ford(G, s)
    cap = inf
    path = []
    if not pi[t]==None:
        current = t
        while not current == s:
            previous = pi[current]
            cap = min(G[previous][current].cap,cap)
            path.append((previous,current))
            current=previous
    return path,cap

def print_network(G):
    for v1,edges in G.items():
        for v2,p in edges.items():
            print(v1,v2,p)


print("Max Flow")
# a = [1]*100
result,max = min_cost_flow([1,3,5,4,4,7,9,11])
# print_network(result)
print(max)