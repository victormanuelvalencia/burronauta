# modelos/grafo.py
from modelos.vertice import Vertice
import json

class Grafo:
    def __init__(self, directed=False):
        self.lista_vertices = {}  # {id: Vertice}
        self.directed = directed

    def add_vertex(self, id):
        """Agrega un nuevo vértice si no existe."""
        if id not in self.lista_vertices:
            nuevo = Vertice(id)
            self.lista_vertices[id] = nuevo
        return self.lista_vertices[id]

    def get_vertex(self, id):
        return self.lista_vertices.get(id)

    def add_edge(self, from_id, to_id, weight=0):
        """Agrega una arista entre dos vértices."""
        if from_id not in self.lista_vertices:
            self.add_vertex(from_id)
        if to_id not in self.lista_vertices:
            self.add_vertex(to_id)

        self.lista_vertices[from_id].add_neighbor(to_id, weight)
        if not self.directed:
            self.lista_vertices[to_id].add_neighbor(from_id, weight)

    def get_vertices(self):
        return list(self.lista_vertices.keys())

    def to_dict(self):
        """Convierte el grafo a un diccionario serializable."""
        return {
            "directed": self.directed,
            "vertices": [v.to_dict() for v in self.lista_vertices.values()]
        }

    @classmethod
    def from_dict(cls, data):
        """Crea un grafo a partir de un diccionario."""
        g = cls(directed=data.get("directed", False))
        for vdata in data.get("vertices", []):
            v = Vertice.from_dict(vdata)
            g.lista_vertices[v.id] = v
        return g

    def to_json(self):
        """Convierte el grafo a string JSON."""
        return json.dumps(self.to_dict(), indent=4, ensure_ascii=False)

    def __repr__(self):
        return f"Grafo(vertices={len(self.lista_vertices)}, dirigido={self.directed})"
