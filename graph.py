from collections import defaultdict

class node:
    def __init__(self, value):
        self.v = value
        self.adj_cap_cost = []
    def __str__(self):
        return str(self.v)


def create_graph(notes:list[int]):
    vertex:list[node] = [node(elem) for elem in notes+notes]
    source = node(4)
    skin = node(4)
    
    for i, vi in enumerate(notes):
        source.adj_cap_cost.append((vertex[i], 1, 0))  # raiz a todos los vertices
        vertex[i].adj_cap_cost.append((vertex[len(notes)+i], 1, -1)) # cada vertice con su duplicado
        for j, vj in enumerate(notes[i+1:], i+1):
            if abs(vi - vj) == 1 or abs(vi - vj) % 7 == 0:
                vertex[len(notes)+i].adj_cap_cost.append((vertex[j], 1, 0)) # duplicado con quien cumple condicion
        vertex[len(notes)+i].adj_cap_cost.append((skin, 1, 0)) # duplicado con la salida

    return source, skin, vertex

def create_graph_2(notes:list[int]):
    vertex:list[node] = [node(elem) for elem in notes+notes]
    graph = defaultdict(lambda: defaultdict(lambda :None))
    s=node('s')
    t=node('t')
    for i,vi in enumerate(notes):
        graph[s][vertex[i]]=(1,0)
        graph[vertex[i]][vertex[len(notes)+i]]=(1,-1)
        for j,vj in enumerate(notes[i+1:],i+1):
            if abs(vi-vj) == 1 or abs(vi-vj) % 7 == 0:
                graph[vertex[len(notes)+i]][vertex[j]]=(1,0)
            graph[vertex[len(notes)+i]][t]=(1,0)
    return graph


notes = [1, 3, 4, 7, 8, 2]
graph=create_graph_2(notes)
for v1,edges in graph.items():
    for v2,p in edges.items():
        print(v1,v2,p)
print("Done")