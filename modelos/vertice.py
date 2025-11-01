# modelos/vertice.py

import json

class Vertice:
    def __init__(self, id, adjacent=None):
        self.id = id
        self.adjacent = adjacent or {}  # {id_vecino: peso}

    def add_neighbor(self, neighbor, weight=0):
        """Agrega un vecino con un peso asociado."""
        self.adjacent[neighbor] = weight

    def get_connections(self):
        """Devuelve todos los nodos adyacentes con sus pesos."""
        return self.adjacent

    def get_id(self):
        """Devuelve el identificador del vértice."""
        return self.id

    # === Conversión a y desde JSON ===

    def to_dict(self):
        """Convierte el vértice a diccionario JSON serializable."""
        return {
            "id": self.id,
            "adjacent": self.adjacent
        }

    @classmethod
    def from_dict(cls, data):
        """Crea un objeto Vertice a partir de un diccionario."""
        return cls(
            id=data.get("id"),
            adjacent=data.get("adjacent", {})
        )

    def to_json(self):
        """Convierte el vértice a un string JSON."""
        return json.dumps(self.to_dict(), indent=4, ensure_ascii=False)

    def __repr__(self):
        return f"Vertice({self.id}, vecinos={list(self.adjacent.keys())})"
