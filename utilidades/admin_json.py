# utilidades/admin_json.py

import json
from modelos.grafo import Grafo

def read_json(path: str):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def write_json(data, path):
    """Guardar un diccionario como JSON en disco."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✅ Archivo guardado en {path}")


def guardar_estrellas_en_json(constelaciones_data, estrellas_info, ruta_archivo):
    """
    Mezcla los cambios del editor dentro del JSON original de constelaciones
    y guarda en disco, asegurando que vida_delta y salud_delta se agreguen.
    """
    for const in constelaciones_data.get("constellations", []):
        for s in const.get("starts", []):
            sid = str(s.get("id"))
            if sid in estrellas_info:
                estrella_edit = estrellas_info[sid]
                # Agregar o actualizar las claves vida_delta y salud_delta
                s["vida_delta"] = int(estrella_edit.get("vida_delta", 0))
                salud_val = estrella_edit.get("salud_delta")
                s["salud_delta"] = salud_val if salud_val else None

    # Guardar archivo
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(constelaciones_data, f, indent=4, ensure_ascii=False)

    print("✅ Archivo de constelaciones actualizado correctamente con vida_delta y salud_delta.")
