from collections import defaultdict
from graph import node 
from math import inf
from graph import create_graph

def create_residual_net(G:dict[node,dict[node,tuple[int,int]]]):
    residual_net = defaultdict(lambda: defaultdict(lambda :None))
    for v1,edges in G.items():
        for v2,p in edges.items():
            residual_net[v1][v2]=p
            residual_net[v2][v1]=(0,-residual_net[v1][v2][1])
    return residual_net


def min_cost_flow(G,node_s,node_t):
    G_f=create_residual_net(G)
    flow=defaultdict(lambda:defaultdict(lambda:None))
    for v1,edges in G.items():
        for v2,_ in edges.items():
            flow[v1][v2]=0
    path, cap = find_path(G_f,node_s,node_t)   
    while not len(path)==0:
        for v1,v2 in path:
            if  G[v1][v2] == None: # la arista no esta en la red original por tanto es una arista de retroceso
                flow[v2][v1]-=cap  #actualizar red original 
                G_f[v1][v2]=(G_f[v1][v2][0]-cap,G_f[v1][v2][1])   #actualizar arista de retroceso en la red residual
                G_f[v2][v1]=(G_f[v2][v1][0]+cap,G_f[v2][v1][1])    #actualizar arista original en la red residual
            else:                    # no es una arista de retroceso 
                flow[v1][v2]+=cap      #actualizar arista en la red original             
                G_f[v1][v2]=(G_f[v1][v2][0]-cap,G_f[v1][v2][1])      #actualizar arista original en la red residual
                G_f[v2][v1]=(G_f[v2][v1][0]+cap,G_f[v2][v1][1])       #actualizar arista de retroceso en la red residual
        path, cap = find_path(G_f,node_s,node_t)    
    return flow

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

def Bellman_Ford(G:dict[node,dict[node,tuple[int,int]]],node_s):
    d=defaultdict(lambda:inf)
    d[node_s]=0
    pi=defaultdict(lambda:None)
    for _ in range(len(G.keys())-1):
        for v1,edges in G.items():
            for v2,p in edges.items():
                if not p==None and not p[0]==0 and not d[v1]==inf and d[v2]>d[v1]+p[1]:
                    d[v2]=d[v1]+p[1]
                    pi[v2]=v1
    for v1,edges in G.items():
        for v2,p in edges.items():
            if not p==None and not p[0]==0 and not d[v2]==inf and not d[v1]==inf and  d[v2]>d[v1]+p[1]:
                return None
    return pi

def find_path(G,node_s,node_t):
    pi=Bellman_Ford(G,node_s)
    cap=inf
    path=[]
    if not pi[node_t]==None:
        current=node_t
        while not current==node_s:
            previous=pi[current]
            cap=min(G[previous][current][0],cap)
            path.append((previous,current))
            current=previous
    return path,cap

def print_network(G):
    for v1,edges in G.items():
        for v2,p in edges.items():
            print(v1,v2,p)

def nmax(G):
    n = 0
    for v1, e in G.items():
        if v1.v != 's': break
        for v2, f in e.items():
            if f == 1:
                n += dfs_visit(G, v2) + 1
    return n

def dfs_visit(G, node):
    for v2,f in G[node].items():
        if f == 1:
            if v2.v == 't': return 0
            elif type(v2.v) != int: return dfs_visit(G, v2)
            else: return dfs_visit(G, v2) + 1
    return 0

a = [1]*100
g,s,t=create_graph(a)
#path,cap=find_path(g,s,t)
#print_network(g)
#for u,v in path:
#    print(u.v,v.v)
print()
print("Max Flow")
#print_network(min_cost_flow(g,s,t))
result = min_cost_flow(g,s,t)
print("Flows Done!")
print(nmax(result))




        






