def warshall(matriz):
    n = len(matriz)
    
    # Copiamos la matriz
    alcance = [fila[:] for fila in matriz]
    
    # Algoritmo principal
    for k in range(n):
        for i in range(n):
            for j in range(n):
                alcance[i][j] = alcance[i][j] or (alcance[i][k] and alcance[k][j])
    
    return alcance


# Ejemplo
grafo = [
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

resultado = warshall(grafo)

for fila in resultado:
    print(fila)