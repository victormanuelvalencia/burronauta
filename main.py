from controladores.grafo_controlador import cargar_grafo_desde_json
from controladores.burro_controlador import BurroControlador
from controladores.planificador import Planificador
from modelos.burro import Burro

def main():
    # === 1️⃣ Cargar data del JSON ===
    ruta = "data/constelaciones.json"
    grafo, estrellas_info, data_json = cargar_grafo_desde_json(ruta)

    # === 2️⃣ Crear el modelo del Burro ===
    burro_modelo = Burro.from_dict(data_json)

    # Mostrar estado inicial
    print("🐴 Estado inicial del Burro:")
    print(f" - Salud: {burro_modelo.get_estado_salud()}")
    print(f" - Energía: {burro_modelo.get_burroenergia_inicial()}%")
    print(f" - Edad: {burro_modelo.get_start_age()}/{burro_modelo.get_death_age()}")
    print(f" - Pasto: {burro_modelo.get_pasto()} kg")
    print("=====================================\n")

    # === 3️⃣ Crear el Planificador ===
    estado_inicial = {
        "edad": burro_modelo.get_start_age(),
        "edad_muerte": burro_modelo.get_death_age(),
        "energia": burro_modelo.get_burroenergia_inicial(),
        "pasto": burro_modelo.get_pasto(),
        "salud": burro_modelo.get_estado_salud()
    }

    planificador = Planificador(grafo, estrellas_info, estado_inicial)

    # === 4️⃣ Sugerir una ruta óptima ===
    origen = "1"  # ID de la estrella inicial
    print(f"🧠 Calculando la mejor ruta desde la estrella {origen}...\n")

    plan = planificador.sugerir_ruta_optima(origen)

    print("🌌 Ruta sugerida:", " → ".join(plan["ruta"]))
    print(f"⭐ Estrellas visitadas: {plan['visited_count']}")
    print(f"🧾 Estado final estimado: {plan['estado_final']}")
    print("=====================================\n")

    # === 5️⃣ Crear el controlador del burro ===
    burro_controlador = BurroControlador(
        grafo=grafo,
        estrellas_info=estrellas_info,
        estado_inicial=estado_inicial
    )

    # === 6️⃣ Ejecutar el recorrido sugerido ===
    print("🚀 Iniciando viaje real del burro...\n")

    for i in range(1, len(plan["ruta"])):
        origen = plan["ruta"][i - 1]
        destino = plan["ruta"][i]
        burro_controlador.mover_a(origen, destino)
        if not burro_controlador.vivo:
            break

    # === 7️⃣ Mostrar resumen final ===
    burro_controlador.resumen()


if __name__ == "__main__":
    main()
