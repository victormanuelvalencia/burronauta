# controladores/ruta_estelar.py
from copy import deepcopy

class RutaEstelar:
    def __init__(self, grafo, estrellas_info):
        self.grafo = grafo
        self.estrellas_info = estrellas_info
        self.total_estrellas = len(estrellas_info)

    def obtener_ruta_mas_larga(self, origen):
        mejor_ruta = []

        def backtrack(actual, visitadas, ruta):
            nonlocal mejor_ruta
            if len(ruta) > len(mejor_ruta):
                mejor_ruta = ruta[:]

            vertice = self.grafo.get_vertex(actual)
            if not vertice:
                return

            for vecino, _ in vertice.get_connections().items():
                if vecino in visitadas:
                    continue
                nuevas_visitadas = set(visitadas)
                nuevas_visitadas.add(vecino)
                backtrack(vecino, nuevas_visitadas, ruta + [vecino])

        backtrack(str(origen), {str(origen)}, [str(origen)])
        return mejor_ruta
