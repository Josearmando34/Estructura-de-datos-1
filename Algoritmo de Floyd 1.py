def floyd_warshall(grafo):
    n = len(grafo)
    
    # Copiar la matriz de distancias
    dist = [fila[:] for fila in grafo]
    
    # Algoritmo principal
    for k in range(n):
        for i in range(n):
            for j in range(n):
                # Verifica si pasar por k mejora el camino
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist


# Ejemplo de uso
INF = float('inf')

grafo = [
    [0,   3, INF, 7],
    [8,   0,   2, INF],
    [5, INF,   0, 1],
    [2, INF, INF, 0]
]

resultado = floyd_warshall(grafo)

print("Matriz de distancias mínimas:")
for fila in resultado:
    print(fila)