class UnionFind:
    def __init__(self, n):
        self.padre = list(range(n))
    
    def find(self, x):
        if self.padre[x] != x:
            self.padre[x] = self.find(self.padre[x])
        return self.padre[x]
    
    def union(self, x, y):
        raizX = self.find(x)
        raizY = self.find(y)
        
        if raizX != raizY:
            self.padre[raizX] = raizY
            return True
        return False


def kruskal(n, aristas):
    # Ordenar aristas por peso
    aristas.sort(key=lambda x: x[2])
    
    uf = UnionFind(n)
    mst = []
    costo_total = 0
    
    for u, v, peso in aristas:
        if uf.union(u, v):  # Si no forma ciclo
            mst.append((u, v, peso))
            costo_total += peso
    
    return mst, costo_total


# Ejemplo
n = 4
aristas = [
    (0, 1, 10),
    (0, 2, 6),
    (0, 3, 5),
    (1, 3, 15),
    (2, 3, 4)
]

mst, costo = kruskal(n, aristas)

print("Árbol de expansión mínima:")
for arista in mst:
    print(arista)

print("Costo total:", costo)