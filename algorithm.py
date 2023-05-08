from collections import defaultdict as dd
from math import inf

class node:
    def __init__(self, value):
        self.v = value

    def __str__(self):
        return str(self.v)
    def __repr__(self):
        return self.__str__()

def create_graph(notes:list[int]):
    vertex:list[node] = [node(elem) for elem in notes]
    vertex_2= [node(str(elem)+'*') for elem in notes]
    vertex=vertex+vertex_2
    graph = dd(lambda: dd(lambda :None))
    s=node('s')
    t=node('t')
    d=node('d')
    for i,vi in enumerate(notes):
        graph[s][vertex[i]]=(1,0)
        graph[vertex[i]][vertex[len(notes)+i]]=(1,-1)
        for j,vj in enumerate(notes[i+1:],i+1):
            if abs(vi-vj) == 1 or abs(vi-vj) % 7 == 0:
                graph[vertex[len(notes)+i]][vertex[j]]=(1,0)
        graph[vertex[len(notes)+i]][t]=(1,0)
    graph[t][d]=(4,0)
    return graph,s,d

def create_residual_net(G:dict[node,dict[node,tuple[int,int]]]):
    residual_net = dd(lambda: dd(lambda :None))
    for v1,edges in G.items():
        for v2,p in edges.items():
            residual_net[v1][v2]=p
            residual_net[v2][v1]=(0,-residual_net[v1][v2][1])
    return residual_net


def min_cost_flow(G,node_s,node_t):
    output=0
    G_f=create_residual_net(G)
    flow=dd(lambda:dd(lambda:None))
    for v1,edges in G.items():
        for v2,_ in edges.items():
            flow[v1][v2]=0
    path, cap = find_path(G_f,node_s,node_t)   
    while not len(path)==0:
        for v1,v2 in path:
            if  G[v1][v2] == None: # la arista no esta en la red original por tanto es una arista de retroceso
                if G_f[v1][v2][1] == -1: output-=1
                flow[v2][v1]-=cap  #actualizar red original 
                G_f[v1][v2]=(G_f[v1][v2][0]-cap,G_f[v1][v2][1])   #actualizar arista de retroceso en la red residual
                G_f[v2][v1]=(G_f[v2][v1][0]+cap,G_f[v2][v1][1])    #actualizar arista original en la red residual
            else:                    # no es una arista de retroceso 
                if G_f[v1][v2][1] == -1: output+=1
                flow[v1][v2]+=cap      #actualizar arista en la red original             
                G_f[v1][v2]=(G_f[v1][v2][0]-cap,G_f[v1][v2][1])      #actualizar arista original en la red residual
                G_f[v2][v1]=(G_f[v2][v1][0]+cap,G_f[v2][v1][1])       #actualizar arista de retroceso en la red residual
        path, cap = find_path(G_f,node_s,node_t)   
     
    return flow,output

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
    d=dd(lambda:inf)
    d[node_s]=0
    pi=dd(lambda:None)
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

# def print_network(G):
#     for v1,edges in G.items():
#         for v2,p in edges.items():
#             print(v1,v2,p)

print()
print("Max Flow")
# a = [1]*100
g,s,t=create_graph([1,3,5,4,4,7,9,11])
result,max = min_cost_flow(g,s,t)
print(max)