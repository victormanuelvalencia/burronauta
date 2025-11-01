# main.py

from controladores.grafo_controlador import cargar_grafo_desde_json
from controladores.burro_controlador import BurroControlador
from controladores.planificador import Planificador
from modelos.burro import Burro
from vistas.menu import abrir_menu
from vistas.seleccionar_estrella import seleccionar_estrella_inicio
from vistas.carga_estrellas import mostrar_estrellas

def main(ruta):
    grafo, estrellas_info, data_json = cargar_grafo_desde_json(ruta)

    mostrar_estrellas(data_json)   # Ahora, aquí sí abrimos el grafo

    burro_modelo = Burro.from_dict(data_json)

    estado_inicial = {
        "edad": burro_modelo.get_start_age(),
        "edad_muerte": burro_modelo.get_death_age(),
        "energia": burro_modelo.get_burroenergia_inicial(),
        "pasto": burro_modelo.get_pasto(),
        "salud": burro_modelo.get_estado_salud()
    }

    planificador = Planificador(grafo, estrellas_info, estado_inicial)

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

    seleccionar_estrella_inicio(list(grafo.get_vertices()), iniciar_con_estrella)


if __name__ == "__main__":
    ruta = abrir_menu()
    if ruta:
        main(ruta)
