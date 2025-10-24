class Vertice:
    def __init__(self, id):
        self.id = id
        self.adjacent = {}  # {neighbor_id: weight}

    def add_neighbor(self, neighbor, weight=0):
        """Agrega un vecino con un peso asociado."""
        self.adjacent[neighbor] = weight

    def get_connections(self):
        """Devuelve todos los nodos adyacentes."""
        return self.adjacent

    def get_id(self):
        """Devuelve el identificador del vértice."""
        return self.id

    def __repr__(self):
        return f"Vertex({self.id}, neighbors={list(self.adjacent.keys())})"
