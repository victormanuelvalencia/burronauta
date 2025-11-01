# main.py

from controladores.grafo_controlador import cargar_grafo_desde_json
from controladores.burro_controlador import BurroControlador
from controladores.planificador import Planificador
from modelos.burro import Burro

from vistas.menu import abrir_menu
from vistas.seleccionar_estrella import seleccionar_estrella_inicio
from vistas.carga_estrellas import mostrar_estrellas
from vistas.editor_estrelllas import abrir_editor_estrellas
from utilidades.admin_json import write_json
from utilidades.admin_json import guardar_estrellas


def main(ruta):
    # 1) Cargar archivo JSON y grafo
    grafo, estrellas_info, data_json = cargar_grafo_desde_json(ruta)

    # 2) Mostrar grafo visualmente
    mostrar_estrellas(data_json)

    # 3) Activar editor científico antes de simular
    def guardar_en_json_local(estrellas_info_mod):
        # Actualizar el JSON cargado con los nuevos valores
        for const in data_json.get("constellations", []):
            for s in const.get("starts", []):
                sid = str(s["id"])
                if sid in estrellas_info_mod:
                    estrella = estrellas_info_mod[sid]
                    s["vida_delta"] = estrella.get("vida_delta", 0)
                    s["salud_delta"] = estrella.get("salud_delta", None)

        # Sobrescribir el archivo original
        write_json(data_json, ruta)

    # Ventana modal para editar efectos investigativos
    abrir_editor_estrellas(
        estrellas_info,
        guardar_callback=lambda cambios: guardar_estrellas(estrellas_info, cambios, ruta)
    )

    # 4) Preparar estado inicial del burro
    burro_modelo = Burro.from_dict(data_json)

    estado_inicial = {
        "edad": burro_modelo.get_start_age(),
        "edad_muerte": burro_modelo.get_death_age(),
        "energia": burro_modelo.get_burroenergia_inicial(),
        "pasto": burro_modelo.get_pasto(),
        "salud": burro_modelo.get_estado_salud()
    }

    # 5) Instanciar planificador
    planificador = Planificador(grafo, estrellas_info, estado_inicial)

    # 6) Lógica cuando el usuario elige estrella de inicio
    def iniciar_con_estrella(origen):
        plan = planificador.sugerir_ruta_optima(origen)

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
    seleccionar_estrella_inicio(list(grafo.get_vertices()), iniciar_con_estrella)


if __name__ == "__main__":
    ruta = abrir_menu()   # Devuelve ruta del JSON
    if ruta:
        main(ruta)