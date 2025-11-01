# controladores/planificador.py

import math
from algoritmos.dijkstra import dijkstra_simple
from copy import deepcopy

ENERGIA_POR_SALUD = {
    "Excelente": 5,
    "Buena": 3,
    "Regular": 3,
    "Mala": 2,
    "Moribundo": 1,
    "Muerto": 0
}


class Planificador:
    def __init__(self, grafo, estrellas_info, estado_inicial):
        self.grafo = grafo
        self.estrellas = estrellas_info
        self.estado_inicial = deepcopy(estado_inicial)

    # =====================================================
    # MÉTODO PRINCIPAL
    # =====================================================
    def sugerir_ruta_optima(self, origen):
        """
        Calcula una ruta sin repetir estrellas, maximizando las visitadas
        y minimizando gasto energético y envejecimiento.
        """
        visitadas = set([origen])
        ruta = [origen]
        estado = deepcopy(self.estado_inicial)

        actual = origen
        mejor_costo = 0

        print(f"🧠 Iniciando planificación desde {origen}...\n")

        while True:
            siguiente, costo, estado_resultante = self._mejor_siguiente(actual, visitadas, estado)

            if not siguiente:
                print("No existen más rutas alcanzables sin morir. Finalizando planificación.\n")
                break

            ruta.append(siguiente)
            visitadas.add(siguiente)
            estado = estado_resultante
            mejor_costo += costo

            if estado["energia"] <= 0 or estado["edad"] >= estado["edad_muerte"]:
                print("El burro no puede continuar. Fin de la planificación.\n")
                break

            actual = siguiente

        print(f"✅ Ruta planificada con {len(ruta)} estrellas (sin repeticiones)\n")
        return {
            "ruta": ruta,
            "visited_count": len(ruta),
            "estado_final": estado
        }

    # =====================================================
    # EVALÚA EL SIGUIENTE MEJOR DESTINO POSIBLE
    # =====================================================
    def _mejor_siguiente(self, actual, visitadas, estado):
        """
        Evalúa todos los vecinos no visitados y elige el mejor
        considerando el costo de recorrer caminos reales
        mediante Dijkstra.
        """
        mejor_estrella = None
        mejor_costo = math.inf
        mejor_estado = None

        for vecino in self.grafo.get_vertex(actual).get_connections().keys():
            id_vecino = str(vecino)

            if id_vecino in visitadas:
                continue

            # Ruta real usando Dijkstra
            distancias, pred, camino = dijkstra_simple(self.grafo, actual, id_vecino, verbose=False)
            distancia_real = distancias[id_vecino]

            # Si no existe camino real, ignorar
            if distancia_real == math.inf:
                continue

            nuevo_estado = deepcopy(estado)
            nuevo_estado["edad"] += distancia_real

            if nuevo_estado["edad"] >= nuevo_estado["edad_muerte"]:
                continue

            # Simular llegada solo al destino de ese subcamino
            nuevo_estado = self._simular_llegada(id_vecino, nuevo_estado)
            energia_restante = nuevo_estado.get("energia", 0)

            # Función de costo: distancia + penalización energética
            costo_total = distancia_real + (100 - energia_restante) * 0.5

            if costo_total < mejor_costo:
                mejor_costo = costo_total
                mejor_estrella = id_vecino
                mejor_estado = nuevo_estado

        return mejor_estrella, mejor_costo, mejor_estado

    # =====================================================
    # SIMULA LO QUE PASA AL LLEGAR A UNA ESTRELLA
    # =====================================================
    def _simular_llegada(self, id_estrella, estado):
        estrella = self.estrellas.get(id_estrella, {})
        energia = estado["energia"]
        pasto = estado["pasto"]
        salud = estado["salud"]
        edad = estado["edad"]

        hiper = estrella.get("hypergiant", False)
        time_to_eat = estrella.get("timeToEat", 1)
        energia_por_salud = ENERGIA_POR_SALUD.get(salud, 2)

        # Comer si energía < 50%
        if energia < 50 and pasto > 0:
            tiempo_total = time_to_eat * 10
            tiempo_comer = tiempo_total * 0.5
            kg_posibles = math.floor(tiempo_comer / time_to_eat)
            kg_comidos = min(pasto, kg_posibles)

            if kg_comidos > 0:
                ganancia = kg_comidos * energia_por_salud
                energia = min(100, energia + ganancia)
                pasto -= kg_comidos

        # Investigación
        energia = max(0, energia - 2)

        # Hipergigante
        if hiper:
            recarga = math.floor(energia * 0.5)
            energia = min(100, energia + recarga)
            pasto *= 2

        estado.update({"energia": energia, "pasto": pasto, "edad": edad})
        return estado