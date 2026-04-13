import heapq

def dijkstra(grafo, inicio):
    # Inicializar distancias
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    
    # Cola de prioridad (min-heap)
    cola = [(0, inicio)]
    
    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)
        
        # Si ya tenemos una mejor distancia, ignoramos
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
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 5), ('D', 10)],
    'C': [('E', 3)],
    'D': [('F', 11)],
    'E': [('D', 4)],
    'F': []
}

resultado = dijkstra(grafo, 'A')

for nodo, distancia in resultado.items():
    print(f"Distancia desde A hasta {nodo}: {distancia}")