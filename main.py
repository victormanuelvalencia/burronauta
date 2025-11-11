# main

from controladores.grafo_controlador import cargar_grafo_desde_json
from controladores.burro_controlador import BurroControlador
from controladores.planificador import Planificador
from modelos.burro import Burro
from vistas.menu import abrir_menu
from vistas.seleccionar_estrella import seleccionar_estrella_inicio
from vistas.carga_estrellas import mostrar_estrellas
from vistas.editor_estrellas import abrir_editor_estrellas
from utilidades.admin_json import write_json, guardar_estrellas_en_json
import json

# 🆕 Importamos la nueva vista para mostrar la ruta del burro
from vistas.mostrar_ruta import mostrar_ruta


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
        constelaciones_data,  # <-- pasa todo el JSON de constelaciones
        guardar_callback=lambda cambios: guardar_estrellas_en_json(
            constelaciones_data, cambios, ruta_constelaciones
        )
    )

    # 5) Instanciar planificador
    planificador = Planificador(grafo, estrellas_info, estado_inicial)

    # 6) Lógica cuando el usuario elige estrella de inicio
    def iniciar_con_estrella(origen):
        plan = planificador.sugerir_ruta_optima(origen)

        # 🆕 Mostrar visualmente la ruta del burro antes de moverlo
        if "ruta" in plan and plan["ruta"]:
            mostrar_ruta(constelaciones_data, plan["ruta"])

        burro_controlador = BurroControlador(
            grafo=grafo,
            estrellas_info=estrellas_info,
            estado_inicial=estado_inicial
        )

        for i in range(1, len(plan["ruta"])):
            burro_controlador.mover_a(plan["ruta"][i-1], plan["ruta"][i])
            if not burro_controlador.vivo:
                break

        burro_controlador.resumen()

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
