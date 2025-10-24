import json
from modelos.grafo import Grafo

def read_json(path: str):
    """
    Read and return the contents of a JSON file.

    Args:
        path (str): Path to the JSON file.

    Returns:
        dict | list: Parsed JSON data.
    """
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(data, path: str):
    """
    Write data to a JSON file at the specified path.

    Args:
        data (dict | list): Data to be serialized as JSON.
        path (str): Path to the output JSON file.
    """
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def cargar_constelaciones(path_json):
    data = read_json(path_json)

    universe_graphs = {}  # {"nombre_constelacion": Grafo()}
    shared_stars = {}

    for constelacion in data['constellations']:
        nombre = constelacion['name']
        grafo = Grafo(directed=False)

        # Crear vértices (estrellas)
        for star in constelacion['starts']:
            v = grafo.add_vertex(star['id'])
            v.label = star['label']
            v.radius = star['radius']
            v.time_to_eat = star['timeToEat']
            v.amount_of_energy = star['amountOfEnergy']
            v.coords = (star['coordenates']['x'], star['coordenates']['y'])
            v.hypergiant = star['hypergiant']

        # Crear aristas (distancias)
        for star in constelacion['starts']:
            for link in star['linkedTo']:
                grafo.add_edge(star['id'], link['starId'], link['distance'])

        universe_graphs[nombre] = grafo

    # Detectar estrellas compartidas
    star_occurrences = {}
    for name, grafo in universe_graphs.items():
        for v in grafo.get_vertices():
            star_occurrences.setdefault(v, []).append(name)

    for star_id, const_list in star_occurrences.items():
        if len(const_list) > 1:
            shared_stars[star_id] = const_list

    return universe_graphs, shared_stars, data
