from collections import defaultdict
from graph import node 
def create_residual_net(G:dict[node,dict[node,tuple(int,int)]]):
    residual_net = defaultdict(lambda: defaultdict(lambda :None))
    for v1,edges in G.items():
        for v2,p in edges.items():
            residual_net[v1][v2]=p

def min_cost_flow(G):
    G_f=create_residual_net(G)
    flow={}
    for v1,edges in G.items():
        for v2,p in edges.items():
            flow[v1][v2]=0
    path = Dijkstra(G_f)
    cap=1
    while not path==None:
        for v1,v2 in path:
            if  G[v1][v2] == None: # la arista no esta en la red original por tanto es una arista de retroceso
                flow[v2][v1][0]-=cap  #actualizar red original 
                G_f[v1][v2][0]+=cap   #actualizar arista original en la red residual
                G_f[v2][v1][0]-=cap    #actualizar arista original en la red residual
            else:                    # no es una arista de retroceso 
                flow[v1][v2][0]+=cap      #actualizar arista en la red original             
                G_f[v1][v2][0]-=cap       #actualizar arista original en la red residual
                if G_f[v2][v1] == None: G_f[v2][v1][0]=(1,G_f[v1][v2][1])
                else : G_f[v2][v1][0]+=cap       #actualizar arista de retroceso en la red residual
        path, cap = Dijkstra(G_f)    
    return flow

def Dijkstra(G:dict[node,dict[node,tuple(int,int)]]):
    S=[]
    pi=defaultdict(lambda:None)
    d=defaultdict(int)
    Q=Build_Heap(G)
    while len(Q)>0:
        u=Extract_Min(Q)
        if u.v=='t': return pi
        S.append(u)
        for v,p in G[u].items():
            if not p[0] == 0:
                if d[v]>d[u]+G[u][v][1]:
                    d[v]=d[u]+G[u][v][1]
                    pi[v]=u




