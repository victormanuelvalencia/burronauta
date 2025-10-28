# controladores/burro_controlador.py
from modelos.burro import Burro
from algoritmos.dijkstra import dijkstra_simple
import math

ENERGIA_POR_SALUD = {
    "Excelente": 5,
    "Buena": 3,
    "Regular": 3,
    "Mala": 2,
    "Moribundo": 1,
    "Muerto": 0
}

class BurroControlador:
    def __init__(self, grafo, estrellas_info, estado_inicial):
        """
        Controlador que simula el recorrido del burro.

        Args:
            grafo: objeto Grafo cargado.
            estrellas_info: diccionario {id: info_estrella}.
            estado_inicial: dict con {
                "edad": int,
                "edad_muerte": int,
                "energia": int (0-100),
                "pasto": int,
                "salud": str
            }
        """
        self.grafo = grafo
        self.estrellas = estrellas_info
        self.estado = estado_inicial.copy()
        self.eventos = []
        self.vivo = True

    # === Métodos ===

    def mover_a(self, origen, destino):
        if not self.vivo:
            print("💀 El burro ha muerto, no puede seguir viajando.")
            return None

        dist, pred, camino = dijkstra_simple(self.grafo, origen, destino, verbose=False)
        distancia_total = dist[destino]

        print(f"\n🐴 El burro viajará de {origen} a {destino} (distancia: {distancia_total})")

        # Actualizar edad
        self.estado["edad"] += distancia_total
        if self.estado["edad"] >= self.estado["edad_muerte"]:
            self.vivo = False
            self.eventos.append({"estrella": destino, "evento": "💀 Murió en el camino."})
            print("💀 El burro ha muerto durante el viaje.")
            return camino

        # Procesar cada estrella
        for estrella in camino[1:]:
            self._procesar_llegada(estrella)
            if not self.vivo:
                break

        return camino

    def _procesar_llegada(self, id_estrella):
        estrella = self.estrellas.get(id_estrella, {})
        energia = self.estado["energia"]
        pasto = self.estado["pasto"]
        salud = self.estado["salud"]
        edad = self.estado["edad"]

        hiper = estrella.get("hypergiant", False)
        time_to_eat = estrella.get("timeToEat", 1)

        evento = {"estrella": id_estrella, "acciones": []}

        # 🥬 Comer si energía < 50%
        if energia < 50 and pasto > 0:
            tiempo_total = time_to_eat * 10
            tiempo_comer = tiempo_total * 0.5
            kg_posibles = math.floor(tiempo_comer / time_to_eat)
            kg_comidos = min(pasto, kg_posibles)
            if kg_comidos > 0:
                ganancia = kg_comidos * ENERGIA_POR_SALUD.get(salud, 2)
                energia = min(100, energia + ganancia)
                pasto -= kg_comidos
                evento["acciones"].append(f"🍃 Comió {kg_comidos}kg, energía +{ganancia}%.")

        # 🔬 Investigación
        energia = max(0, energia - 2)
        evento["acciones"].append("🔬 Investigó y perdió 2% de energía.")

        # 🌠 Hipergigante
        if hiper:
            recarga = math.floor(energia * 0.5)
            energia = min(100, energia + recarga)
            pasto *= 2
            evento["acciones"].append("🌠 Hipergigante: +50% energía y pasto duplicado.")

        # Actualizar estado
        self.estado.update({"energia": energia, "pasto": pasto, "edad": edad})

        # Verificar muerte
        if self.estado["edad"] >= self.estado["edad_muerte"]:
            self.vivo = False
            evento["acciones"].append("💀 Murió por vejez.")
        elif energia <= 0:
            self.vivo = False
            evento["acciones"].append("💤 Murió por falta de energía.")

        self.eventos.append(evento)

    def resumen(self):
        """Muestra los eventos del recorrido."""
        print("\n=== 📋 RESUMEN DEL VIAJE ===")
        for e in self.eventos:
            print(f"🪐 Estrella {e['estrella']}:")
            for a in e["acciones"]:
                print(f"   - {a}")
        print("\n=== 🧾 ESTADO FINAL DEL BURRO ===")
        print(f"Edad: {self.estado['edad']} / {self.estado['edad_muerte']}")
        print(f"Energía: {self.estado['energia']}%")
        print(f"Pasto: {self.estado['pasto']} kg")
        print(f"Salud: {self.estado['salud']}")
        print(f"Vivo: {'✅ Sí' if self.vivo else '❌ No'}")
        print("=================================\n")

