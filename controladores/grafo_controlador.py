# controladores/grafo_controlador.py

from modelos.grafo import Grafo
from utilidades.admin_json import read_json

def cargar_grafo_desde_json(ruta_archivo):
    """
    Carga el grafo y la información de estrellas desde un archivo JSON.

    Retorna:
        grafo (Grafo): grafo con las conexiones entre estrellas
        estrellas_info (dict): info detallada de cada estrella (posiciones, hiper, etc.)
        data (dict): el JSON completo (incluye data del burro)
    """
    data = read_json(ruta_archivo)
    grafo = Grafo(directed=False)
    estrellas_info = {}

    constelaciones = data.get("constellations", [])

    # Recorremos cada constelación
    for const in constelaciones:
        nombre = const.get("name", "SinNombre")
        estrellas = const.get("starts", [])

        # Recorremos las estrellas
        for star in estrellas:
            star_id = str(star["id"])  # aseguramos tipo string
            grafo.add_vertex(star_id)

            # Guardamos su información (posición, tipo, hiper, etc.)
            estrellas_info[star_id] = {
                "label": star.get("label", f"Star_{star_id}"),
                "coordenadas": star.get("coordenates", {}),
                "hypergiant": star.get("hypergiant", False),
                "timeToEat": star.get("timeToEat", 1),
                "galaxy": nombre,
            }

            # Añadimos conexiones (edges)
            for enlace in star.get("linkedTo", []):
                destino_id = str(enlace.get("starId"))
                distancia = enlace.get("distance", 1)
                grafo.add_edge(star_id, destino_id, distancia)

    return grafo, estrellas_info, data
