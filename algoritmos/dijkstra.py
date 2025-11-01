# algoritmos/dijkstra.py

import math

def dijkstra_simple(graph, start_id, target_id, verbose=True):
    """
    Implementación simple del algoritmo de Dijkstra.
    Calcula el camino más corto entre dos nodos en un grafo no dirigido.

    Args:
        graph: Objeto Grafo (de modelos.grafo)
        start_id (str): ID del vértice de inicio
        target_id (str): ID del vértice de destino
        verbose (bool): Si es True, imprime el proceso paso a paso

    Returns:
        (distancias, predecesores, camino)
    """
    dist = {v: math.inf for v in graph.get_vertices()}
    pred = {v: None for v in graph.get_vertices()}
    dist[start_id] = 0

    no_visitados = set(graph.get_vertices())

    if verbose:
        print("=== Iteración inicial ===")
        for v in graph.get_vertices():
            print(f"{v}: ({'∞' if dist[v]==math.inf else dist[v]}, {pred[v]})")
        print()

    while no_visitados:
        # Escoge el nodo no visitado con menor distancia
        u = min(no_visitados, key=lambda v: dist[v])
        if dist[u] == math.inf:
            break

        if verbose:
            print(f"Procesando vértice {u} con distancia {dist[u]}")

        no_visitados.remove(u)

        if u == target_id:
            if verbose:
                print(f"\nDestino {target_id} alcanzado. Fin de la búsqueda.\n")
            break

        # Relajación de aristas
        for v, peso in graph.get_vertex(u).get_connections().items():
            if v in no_visitados:
                nueva_dist = dist[u] + peso
                if nueva_dist < dist[v]:
                    dist[v] = nueva_dist
                    pred[v] = u
                    if verbose:
                        print(f"  Actualizado {v}: viene de {u}, nuevo costo = {nueva_dist}")

        if verbose:
            print("\nEtiquetas actuales:")
            for v in graph.get_vertices():
                costo = "∞" if dist[v] == math.inf else dist[v]
                print(f"{v}: ({costo}, {pred[v]})")
            print()

    # Reconstrucción del camino
    path = []
    actual = target_id
    while actual is not None:
        path.insert(0, actual)
        actual = pred[actual]

    if verbose:
        print(f"Camino más corto de {start_id} a {target_id}: {' → '.join(path)}")
        print(f"Distancia total: {dist[target_id]}")

    return dist, pred, path
