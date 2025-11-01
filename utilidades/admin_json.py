# utilidades/admin_json.py

import json
from modelos.grafo import Grafo

def read_json(path: str):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(data, path: str):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def guardar_estrellas(original_json, cambios_editor, ruta_archivo):
    """
    Mezcla los cambios del editor dentro del JSON original y guarda en disco.
    """
    # Aplicar cambios en memoria
    for id_, cambios in cambios_editor.items():

        # Convertir ID a string si el JSON usa strings como keys
        id_key = str(id_)

        if id_key not in original_json:
            print(f"⚠️ ID {id_key} no existe en el JSON, se ignora.")
            continue

        if "vida_delta" in cambios:
            original_json[id_key]["vida_delta"] = cambios["vida_delta"]

        if "salud_delta" in cambios:
            original_json[id_key]["salud_delta"] = cambios["salud_delta"]

    # Guardar archivo actualizado
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(original_json, f, indent=4, ensure_ascii=False)

    print("✅ Archivo actualizado exitosamente.")


