import math
from copy import deepcopy
from config import INVESTIGACION_ENERGIA_POR_SEGUNDO, COMIDA_KG_POR_SEGUNDO

# Energía ganada por kg de pasto según salud
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
        self.estrellas_info = estrellas_info
        self.estado_inicial = deepcopy(estado_inicial)
        self.total_estrellas = len(estrellas_info)

    # ======================================================
    # MÉTODO PRINCIPAL
    # ======================================================
    def sugerir_ruta_optima(self, origen):
        """
        Backtracking que busca la ruta que maximiza la cantidad de estrellas visitadas
        antes de que el burro muera (energía <= 0 o edad >= edad_muerte).
        """
        mejor_ruta = []
        mejor_estado_final = None

        energia_inicial = self.estado_inicial["energia"]
        pasto_inicial = self.estado_inicial["pasto"]
        salud_inicial = self.estado_inicial["salud"]
        edad_inicial = self.estado_inicial["edad"]
        edad_muerte = self.estado_inicial["edad_muerte"]
        estrellas_totales = self.total_estrellas

        # ======================================================
        # Simulación de la primera estrella
        # ======================================================
        estrella_inicial = self.estrellas_info.get(str(origen), {})
        print(f"\n🌟 Primera estrella: {origen}")

        time_to_eat_field = estrella_inicial.get("timeToEat", 1)
        segundos_total = time_to_eat_field * 10.0

        energia = energia_inicial
        pasto = pasto_inicial
        edad = edad_inicial

        # regla de mitad comer / mitad investigar si tiene poca energía
        if energia <= 50:
            segundos_comer = segundos_total * 0.5
            segundos_investigar = segundos_total - segundos_comer
        else:
            segundos_comer = 0.0
            segundos_investigar = segundos_total

        # 🔋 Reducción continua de energía por segundo total
        energia -= INVESTIGACION_ENERGIA_POR_SEGUNDO * segundos_total
        if energia < 0:
            energia = 0

        energia_perdida_investigacion = INVESTIGACION_ENERGIA_POR_SEGUNDO * segundos_investigar
        energia -= energia_perdida_investigacion

        # Comer si aplica
        if segundos_comer > 0 and pasto > 0:
            kg_posibles = math.floor(segundos_comer * COMIDA_KG_POR_SEGUNDO)
            kg_comidos = min(pasto, kg_posibles)
            ganancia_por_kg = ENERGIA_POR_SALUD.get(salud_inicial, 3)
            energia_ganada = kg_comidos * ganancia_por_kg
            energia = min(100.0, energia + energia_ganada)
            pasto -= kg_comidos
            print(f"   🍃 Comió {kg_comidos} kg de pasto (+{energia_ganada:.1f}% energía)")
        else:
            print(f"   🔬 Investigó {segundos_investigar:.1f}s (-{energia_perdida_investigacion:.1f}% energía)")

        # Hipergigante
        if estrella_inicial.get("hypergiant"):
            energia = min(100.0, energia + 50.0)
            pasto *= 2
            print("   💥 Es una hipergigante: energía +50%, pasto x2")

        print(f"   ⚡ Energía actual: {energia:.1f}%")
        print(f"   🌿 Pasto disponible: {pasto:.1f} kg")

        # ======================================================
        # BACKTRACKING
        # ======================================================
        def backtrack(actual, energia, pasto, edad, visitadas, ruta):
            nonlocal mejor_ruta, mejor_estado_final

            if energia <= 0 or edad >= edad_muerte or len(visitadas) == estrellas_totales:
                if len(ruta) > len(mejor_ruta):
                    mejor_ruta = ruta[:]
                    mejor_estado_final = {
                        "energia": energia,
                        "pasto": pasto,
                        "edad": edad,
                        "edad_muerte": edad_muerte,
                        "salud": salud_inicial
                    }
                return

            if len(ruta) > len(mejor_ruta):
                mejor_ruta = ruta[:]
                mejor_estado_final = {
                    "energia": energia,
                    "pasto": pasto,
                    "edad": edad,
                    "edad_muerte": edad_muerte,
                    "salud": salud_inicial
                }

            vertice = self.grafo.get_vertex(actual)
            if not vertice:
                return

            for vecino, distancia in vertice.get_connections().items():
                if vecino in visitadas:
                    continue

                estrella = self.estrellas_info.get(str(vecino), {})

                # El viaje solo envejece al burro y gasta energía
                nueva_energia = energia - (INVESTIGACION_ENERGIA_POR_SEGUNDO * distancia)
                nueva_edad = edad + (distancia / 10.0)
                nuevo_pasto = pasto

                if nueva_energia <= 0 or nueva_edad >= edad_muerte:
                    continue

                # Estadía
                time_to_eat_field = estrella.get("timeToEat", 1)
                segundos_total = time_to_eat_field * 10.0

                if nueva_energia <= 50:
                    segundos_comer = segundos_total * 0.5
                    segundos_investigar = segundos_total - segundos_comer
                else:
                    segundos_comer = 0.0
                    segundos_investigar = segundos_total

                # 🔋 Reducción continua de energía por el tiempo total de estadía
                nueva_energia -= INVESTIGACION_ENERGIA_POR_SEGUNDO * segundos_total
                if nueva_energia < 0:
                    nueva_energia = 0

                energia_perdida_investigacion = INVESTIGACION_ENERGIA_POR_SEGUNDO * segundos_investigar
                nueva_energia -= energia_perdida_investigacion

                if segundos_comer > 0 and nuevo_pasto > 0 and nueva_energia > 0:
                    kg_posibles = math.floor(segundos_comer * COMIDA_KG_POR_SEGUNDO)
                    kg_comidos = min(nuevo_pasto, kg_posibles)
                    if kg_comidos > 0:
                        ganancia_por_kg = ENERGIA_POR_SALUD.get(salud_inicial, 3)
                        energia_ganada = kg_comidos * ganancia_por_kg
                        nueva_energia = min(100.0, nueva_energia + energia_ganada)
                        nuevo_pasto -= kg_comidos

                # Hipergigante
                if estrella.get("hypergiant"):
                    nueva_energia = min(100.0, nueva_energia + 50.0)
                    nuevo_pasto *= 2

                if nueva_energia <= 0 or nueva_edad >= edad_muerte:
                    continue

                nuevas_visitadas = set(visitadas)
                nuevas_visitadas.add(vecino)
                backtrack(
                    vecino,
                    nueva_energia,
                    nuevo_pasto,
                    nueva_edad,
                    nuevas_visitadas,
                    ruta + [vecino]
                )

        # llamada inicial
        backtrack(
            str(origen),
            float(energia),
            float(pasto),
            float(edad),
            {str(origen)},
            [str(origen)]
        )

        # mostrar resumen
        print("\n🧭 Planificador: ruta sugerida =", " → ".join(map(str, mejor_ruta)))
        if mejor_estado_final:
            print(f"   ⚡ Energía final: {mejor_estado_final['energia']:.1f}%")
            print(f"   🌿 Pasto final: {mejor_estado_final['pasto']:.1f} kg")
            print(f"   👴 Edad final: {mejor_estado_final['edad']:.1f}/{mejor_estado_final['edad_muerte']} años")
            print(f"   ❤️ Salud (inicial): {mejor_estado_final['salud']}")

        return {"ruta": mejor_ruta, "detalles": mejor_estado_final}
