# controladores/burro_controlador.py

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
        self.grafo = grafo
        self.estrellas = estrellas_info
        self.estado = estado_inicial.copy()
        self.eventos = []
        self.vivo = True

    # ==================================================
    # MÉTODO PRINCIPAL DE MOVIMIENTO
    # ==================================================
    def mover_a(self, origen, destino):
        """Mueve al burro desde un nodo origen hasta un destino usando Dijkstra."""
        if not self.vivo:
            print("💀 El burro ha muerto, no puede seguir viajando.")
            return None

        dist, pred, camino = dijkstra_simple(self.grafo, origen, destino, verbose=False)
        distancia_total = dist[destino]

        print(f"\n🐴 El burro viajará de {origen} a {destino} (distancia: {distancia_total})")

        # Aumentar la edad según la distancia recorrida
        self.estado["edad"] += distancia_total

        # Si la edad supera la edad de muerte, el burro muere durante el viaje
        if self.estado["edad"] >= self.estado["edad_muerte"]:
            self.vivo = False
            self._registrar_evento(destino, ["💀 Murió en el camino (por vejez durante el viaje)."])
            return camino

        # Procesar cada estrella del recorrido
        for estrella in camino[1:]:
            self._procesar_llegada(estrella)
            if not self.vivo:
                break

        return camino

    # ==================================================
    # MÉTODOS DE PROCESO
    # ==================================================
    def _procesar_llegada(self, id_estrella):
        """Aplica las reglas al llegar a una estrella, corrigiendo vida_delta y salud_delta."""
        estrella = self.estrellas.get(id_estrella, {})
        energia, pasto, salud, edad = (
            self.estado["energia"],
            self.estado["pasto"],
            self.estado["salud"],
            self.estado["edad"]
        )

        evento = {"estrella": id_estrella, "acciones": []}

        # --- Aplicar efectos de la estrella ---
        # Vida_delta ahora afecta la 'vida_restante' o la energía, pero no la edad
        vida_delta = estrella.get("vida_delta", 0)
        if vida_delta != 0:
            # Aquí transformamos vida_delta en porcentaje de energía perdido o ganado
            energia -= abs(vida_delta)  # los negativos restan energía
            energia = max(0, energia)
            evento["acciones"].append(f"⏳ Vida ajustada: {'-' if vida_delta<0 else '+'}{abs(vida_delta)} (afecta energía)")

        # Salud_delta: reemplaza el estado de salud si existe
        salud_delta = estrella.get("salud_delta")
        if salud_delta:
            salud = salud_delta
            evento["acciones"].append(f"🩺 Salud ajustada a {salud_delta}.")

        # --- Comer si la energía es baja ---
        energia, pasto = self._accion_comer(estrella, energia, pasto, salud, evento)

        # --- Investigar ---
        energia = self._accion_investigar(energia, evento)

        # --- Hipergigante ---
        energia, pasto = self._accion_hipergigante(estrella, energia, pasto, evento)

        # --- Actualizar estado del burro ---
        self.estado.update({"energia": energia, "pasto": pasto, "edad": edad, "salud": salud})

        # --- Verificar si el burro muere ---
        self._verificar_muerte(energia, evento)
        self._registrar_evento(id_estrella, evento["acciones"])

        # --- Mostrar resumen del paso ---
        print(f"\n⭐ Llegó a {id_estrella}")
        for acc in evento["acciones"]:
            print("   -", acc)
        print(f"   Estado actual: energía={energia}, pasto={pasto}, edad={edad}, salud={salud}\n")

    # ==================================================
    # SUBFUNCIONES DE COMIDA, INVESTIGACIÓN, HIPER
    # ==================================================
    def _accion_comer(self, estrella, energia, pasto, salud, evento):
        """
        El burro come solo si tiene menos del 50% de energía.
        Solo puede usar el 50% del tiempo de la estrella para comer.
        La ganancia depende de la salud.
        """
        time_to_eat = estrella.get("timeToEat", 1)
        if energia < 50 and pasto > 0:
            tiempo_total = time_to_eat * 10  # tiempo total estimado en la estrella
            tiempo_comer = tiempo_total * 0.5
            kg_posibles = math.floor(tiempo_comer / time_to_eat)
            kg_comidos = min(pasto, kg_posibles)
            if kg_comidos > 0:
                ganancia = kg_comidos * ENERGIA_POR_SALUD.get(salud, 2)
                energia = min(100, energia + ganancia)
                pasto -= kg_comidos
                evento["acciones"].append(f"🍃 Comió {kg_comidos}kg, energía +{ganancia}%")
        return energia, pasto

    def _accion_investigar(self, energia, evento):
        """
        Pierde energía por investigar.
        No aplica vida_delta ni salud_delta aquí, eso se hace en _procesar_llegada.
        """
        energia_perdida = 2
        energia = max(0, energia - energia_perdida)
        evento["acciones"].append(f"🔬 Investigó y perdió {energia_perdida}% de energía.")
        return energia

    def _accion_hipergigante(self, estrella, energia, pasto, evento):
        if estrella.get("hypergiant", False):
            recarga = math.floor(energia * 0.5)
            energia = min(100, energia + recarga)
            pasto *= 2
            evento["acciones"].append("🌠 Hipergigante: +50% energía y pasto duplicado.")
        return energia, pasto

    def _verificar_muerte(self, energia, evento):
        if self.estado["edad"] >= self.estado["edad_muerte"]:
            self.vivo = False
            evento["acciones"].append("💀 Murió por vejez.")
        elif energia <= 0:
            self.vivo = False
            evento["acciones"].append("💤 Murió por falta de energía.")

    def _registrar_evento(self, estrella, acciones):
        self.eventos.append({"estrella": estrella, "acciones": acciones})

    # ==================================================
    # RESUMEN FINAL
    # ==================================================
    def resumen(self):
        print("\n=== 📋 RESUMEN DEL VIAJE ===")
        for e in self.eventos:
            print(f"\n🪐 Estrella {e.get('estrella', 'Desconocida')}:")
            for a in e.get("acciones", []):
                print(f"   - {a}")

        print("\n=== 🧾 ESTADO FINAL DEL BURRO ===")
        print(f"Edad: {self.estado['edad']} / {self.estado['edad_muerte']}")
        print(f"Energía: {self.estado['energia']}%")
        print(f"Pasto: {self.estado['pasto']} kg")
        print(f"Salud: {self.estado['salud']}")
        print(f"Vivo: {'✅ Sí' if self.vivo else '❌ No'}")
        print("=================================\n")
