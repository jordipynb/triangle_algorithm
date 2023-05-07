from collections import defaultdict

class node:
    def __init__(self, value):
        self.v = value
        #self.adj_cap_cost = []
    def __str__(self):
        return str(self.v)
    def __repr__(self):
        return self.__str__()

def create_graph(notes:list[int]):
    vertex:list[node] = [node(elem) for elem in notes]
    vertex_2= [node(str(elem)+'*') for elem in notes]
    vertex=vertex+vertex_2
    graph = defaultdict(lambda: defaultdict(lambda :None))
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


# notes = [1, 3, 4, 7, 8, 2]
# graph,s,t=create_graph_2(notes)
# for v1,edges in graph.items():
#     for v2,p in edges.items():
#         print(v1,v2,p)
# print("Done")