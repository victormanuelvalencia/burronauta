from .vertice import Vertice

class Grafo:
    def __init__(self, directed=False):
        self.lista_vertices = {}  # {id: Vertice}
        self.num_vertices = 0
        self.directed = directed

    def add_vertex(self, id):
        """Agrega un nuevo vértice si no existe."""
        if id not in self.lista_vertices:
            nuevo_vertice = Vertice(id)
            self.lista_vertices[id] = nuevo_vertice
            self.num_vertices += 1
        return self.lista_vertices[id]

    def get_vertex(self, id):
        """Obtiene un vértice por su id."""
        return self.lista_vertices.get(id)

    def add_edge(self, from_id, to_id, weight=0):
        """Crea una conexión (arista) entre dos vértices."""
        if from_id not in self.lista_vertices:
            self.add_vertex(from_id)
        if to_id not in self.lista_vertices:
            self.add_vertex(to_id)

        self.lista_vertices[from_id].add_neighbor(to_id, weight)

        if not self.directed:
            # Si el grafo es no dirigido, agrega también la conexión inversa
            self.lista_vertices[to_id].add_neighbor(from_id, weight)

    def get_vertices(self):
        return list(self.lista_vertices.keys())

    def __iter__(self):
        return iter(self.lista_vertices.values())

    def __repr__(self):
        return f"Graph(vertices={len(self.lista_vertices)}, directed={self.directed})"
