class node:
    def __init__(self, value):
        self.v = value
        self.adj_cap_cost = []


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


notes = [1, 3, 4, 7, 8, 2]
s, s , v = create_graph(notes)
print("Done")