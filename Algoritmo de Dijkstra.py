import heapq

def dijkstra(grafo, inicio):
    # Inicializar distancias con infinito
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    
    # Cola de prioridad
    cola = [(0, inicio)]
    
    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)
        
        # Si ya encontramos una mejor distancia, ignoramos
        if distancia_actual > distancias[nodo_actual]:
            continue
        
        # Revisar vecinos
        for vecino, peso in grafo[nodo_actual]:
            distancia = distancia_actual + peso
            
            # Si encontramos un camino más corto
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                heapq.heappush(cola, (distancia, vecino))
    
    return distancias


# Ejemplo de uso
grafo = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('C', 2), ('D', 5)],
    'C': [('A', 4), ('B', 2), ('D', 1)],
    'D': [('B', 5), ('C', 1)]
}

resultado = dijkstra(grafo, 'A')

print("Distancias más cortas desde A:")
for nodo, distancia in resultado.items():
    print(f"{nodo}: {distancia}")