# controladores/simulacion_ruta.py
import math
from copy import deepcopy
from config import RAZON_TIEMPO_COMER

# Energía ganada por kg de pasto según salud
ENERGIA_POR_SALUD = {
    "Excelente": 5,
    "Buena": 3,
    "Regular": 3,
    "Mala": 2,
    "Moribundo": 1,
    "Muerto": 0
}

# Función para determinar la salud según la energía
def salud_por_energia(energia):
    if energia > 75:
        return "Excelente"
    elif energia > 50:
        return "Buena"
    elif energia > 25:
        return "Regular"
    elif energia > 0:
        return "Mala"
    else:
        return "Moribundo"

class SimuladorRuta:
    def __init__(self, estrellas_info, estado_inicial):
        """
        estrellas_info: dict con la información de cada estrella (id, timeToEat, hypergiant, delta vida/salud, linkedTo)
        estado_inicial: dict con la información inicial del burro
                        {"energia":..., "pasto":..., "edad":..., "edad_muerte":...}
        """
        self.estrellas_info = estrellas_info
        self.estado_inicial = deepcopy(estado_inicial)

    def simular_ruta(self, ruta):
        energia = self.estado_inicial["energia"]
        pasto = self.estado_inicial["pasto"]
        edad = self.estado_inicial["edad"]
        edad_muerte = self.estado_inicial["edad_muerte"]

        detalles_por_estrella = []

        for i, nodo in enumerate(ruta):
            estrella = self.estrellas_info.get(str(nodo), {})
            time_to_eat_field = estrella.get("timeToEat", 1)

            # 1️⃣ Tiempo total que el burro pasa en la estrella (segundos)
            segundos_total = time_to_eat_field * RAZON_TIEMPO_COMER

            # 2️⃣ Pérdida de energía por movimiento (no por comer tiempo)
            distancia = 0
            if i < len(ruta) - 1:
                siguiente_nodo = int(ruta[i + 1])
                distancia = next(
                    (link["distance"] for link in estrella.get("linkedTo", [])
                     if int(link["starId"]) == siguiente_nodo),
                    0
                )
                energia -= distancia * 0.5  # pérdida proporcional a distancia
                edad += distancia  # suma de distancia a la edad
                energia = max(0, energia)

            # 3️⃣ Comer pasto si energía <50%
            if energia < 50 and pasto > 0:
                kg_posibles = min(pasto, 5)  # máximo 5 kg por estrella
                energia += kg_posibles * 5  # 5% por kg
                energia = min(100, energia)
                pasto -= kg_posibles

            # 4️⃣ Hipergigante (solo suma energía, no multiplica pasto)
            if estrella.get("hypergiant", False):
                energia = min(100, energia + energia * 0.5)

            # 5️⃣ Salud según energía
            salud = salud_por_energia(energia)

            # 6️⃣ Delta de vida de la estrella
            vida_delta = estrella.get("vida_delta", 0)
            edad += vida_delta

            # 7️⃣ Guardar detalle
            detalles_por_estrella.append({
                "estrella": nodo,
                "energia": energia,
                "pasto": pasto,
                "edad": edad,
                "edad_muerte": edad_muerte,
                "salud": salud,
                "vida_delta": vida_delta,
                "distancia_recorrida": distancia
            })

            if energia <= 0 or edad >= edad_muerte:
                break

        return detalles_por_estrella
