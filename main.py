# main.py
from controladores.grafo_controlador import cargar_grafo_desde_json
from controladores.burro_controlador import BurroControlador
from modelos.burro import Burro

def main():
    # === 1️⃣ Cargar data del JSON ===
    ruta = "data/constelaciones.json"
    grafo, estrellas_info, data_json = cargar_grafo_desde_json(ruta)

    # === 2️⃣ Crear el modelo del Burro ===
    burro_modelo = Burro.from_dict(data_json)

    # Mostramos los valores iniciales
    print("🐴 Estado inicial del Burro:")
    print(f" - Salud: {burro_modelo.get_estado_salud()}")
    print(f" - Energía: {burro_modelo.get_burroenergia_inicial()}")
    print(f" - Edad: {burro_modelo.get_start_age()}/{burro_modelo.get_death_age()}")
    print(f" - Pasto: {burro_modelo.get_pasto()} kg")
    print("=====================================\n")

    # === 3️⃣ Crear el controlador del burro ===
    burro_controlador = BurroControlador(
        grafo=grafo,
        estrellas_info=estrellas_info,
        estado_inicial={
            "edad": burro_modelo.get_start_age(),
            "edad_muerte": burro_modelo.get_death_age(),
            "energia": burro_modelo.get_burroenergia_inicial(),
            "pasto": burro_modelo.get_pasto(),
            "salud": burro_modelo.get_estado_salud()
        }
    )

    # === 4️⃣ Elegir un recorrido (ejemplo) ===
    origen = "1"   # id de la estrella inicial
    destino = "15"  # id de la estrella final (puede ser otra galaxia)
    print(f"🌌 Calculando viaje del burro desde {origen} hasta {destino}...\n")

    camino = burro_controlador.mover_a(origen, destino)

    if camino:
        print(f"🛣️ Ruta calculada: {' → '.join(camino)}")

    # === 5️⃣ Mostrar resumen final ===
    burro_controlador.resumen()


if __name__ == "__main__":
    main()
