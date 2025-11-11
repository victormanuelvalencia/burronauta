# main.py

import json
from controladores.grafo_controlador import cargar_grafo_desde_json
from modelos.burro import Burro
from vistas.menu import abrir_menu
from vistas.seleccionar_estrella import seleccionar_estrella_inicio
from vistas.carga_estrellas import mostrar_estrellas
from vistas.editor_estrellas import abrir_editor_estrellas
from utilidades.admin_json import guardar_estrellas_en_json
from vistas.mostrar_ruta import mostrar_ruta

# 🆕 Importamos las nuevas clases
from controladores.ruta_estelar import RutaEstelar
from controladores.simulacion_ruta import SimuladorRuta


def main(ruta_burro, ruta_constelaciones):
    # 1) Cargar burro
    with open(ruta_burro, "r", encoding="utf-8") as f:
        burro_data = json.load(f)
    burro_modelo = Burro.from_dict(burro_data)

    estado_inicial = {
        "edad": burro_modelo.get_start_age(),
        "edad_muerte": burro_modelo.get_death_age(),
        "energia": burro_modelo.get_burroenergia_inicial(),
        "pasto": burro_modelo.get_pasto(),
        "salud": burro_modelo.get_estado_salud()
    }

    # 2) Cargar constelaciones y grafo
    grafo, estrellas_info, constelaciones_data = cargar_grafo_desde_json(ruta_constelaciones)

    print("Estrellas info cargadas:", estrellas_info)
    print("Vertices en grafo:", list(grafo.get_vertices()))

    # 3) Mostrar grafo visualmente
    mostrar_estrellas(constelaciones_data)

    # 4) Abrir editor antes de simular
    abrir_editor_estrellas(
        constelaciones_data,
        guardar_callback=lambda cambios: guardar_estrellas_en_json(
            constelaciones_data, cambios, ruta_constelaciones
        )
    )

    # 5) Instanciar el optimizador de rutas
    optimizador = RutaEstelar(grafo, estrellas_info)
    simulador = SimuladorRuta(estrellas_info, estado_inicial)

    # 6) Lógica cuando el usuario elige estrella de inicio
    def iniciar_con_estrella(origen):
        # 🟢 1️⃣ Obtener la ruta más larga (solo nodos)
        ruta_optima = optimizador.obtener_ruta_mas_larga(origen)
        print("\n🧭 Ruta óptima encontrada:", " → ".join(ruta_optima))

        # 🟢 2️⃣ Simular cómo cambian las variables a lo largo de la ruta
        detalles_simulacion = simulador.simular_ruta(ruta_optima)

        # 🟢 2️⃣b️⃣ Actualizar el objeto Burro con los valores finales de la simulación
        if detalles_simulacion:
            ultimo_detalle = detalles_simulacion[-1]
            burro_modelo.set_burroenergia_inicial(ultimo_detalle["energia"])
            burro_modelo.set_pasto(ultimo_detalle["pasto"])
            burro_modelo.set_start_age(ultimo_detalle["edad"])
            burro_modelo.set_estado_salud(ultimo_detalle["salud"])

        # 🟢 3️⃣ Mostrar visualmente la ruta con detalles
        mostrar_ruta(constelaciones_data, ruta_optima, burro_modelo.to_dict())

        # 🔹 Opcional: imprimir resumen textual
        for detalle in detalles_simulacion:
            print(
                f"🌟 {detalle['estrella']} | Energía: {detalle['energia']:.1f}% | "
                f"Pasto: {detalle['pasto']:.1f} kg | Edad: {detalle['edad']:.1f} | Salud: {detalle['salud']}"
            )

    # 7) Abrir UI para elegir estrella inicial
    if grafo.get_vertices():
        seleccionar_estrella_inicio(list(grafo.get_vertices()), iniciar_con_estrella)
    else:
        print("⚠️ No hay estrellas cargadas en el grafo. Revisa el JSON de constelaciones.")


if __name__ == "__main__":
    ruta_burro = "data/burro_info.json"
    ruta_constelaciones = abrir_menu()  # Devuelve ruta del JSON de constelaciones
    if ruta_constelaciones:
        main(ruta_burro, ruta_constelaciones)
