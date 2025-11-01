# vistas/carga_estrellas.py

import tkinter as tk
import random

# Colores distintos por constelación
COLORES = ["#00FFFF", "#FFD700", "#FF69B4", "#ADFF2F", "#FFA07A", "#87CEEB"]

def mostrar_estrellas(data):
    root = tk.Tk()
    root.title("Mapa de Constelaciones 🪐")
    root.geometry("800x600")
    root.config(bg="black")

    canvas = tk.Canvas(root, width=800, height=600, bg="black")
    canvas.pack(fill="both", expand=True)

    constellations = data.get("constellations", [])

    coordenadas_usadas = {}  # Para detectar estrellas compartidas

    for idx, constellation in enumerate(constellations):
        color = COLORES[idx % len(COLORES)]
        stars = constellation.get("starts", [])

        for star in stars:
            x = star["coordenates"]["x"] * 3  # Escalamos para mayor visibilidad
            y = star["coordenates"]["y"] * 3
            label = star["label"]

            coord_key = (x, y)

            # Si la estrella pertenece a varias constelaciones → rojo
            if coord_key in coordenadas_usadas:
                color = "red"
            else:
                coordenadas_usadas[coord_key] = True

            canvas.create_oval(
                x - 5, y - 5, x + 5, y + 5,
                fill=color,
                outline=""
            )
            canvas.create_text(x + 10, y, text=label, fill="white", font=("Arial", 8, "bold"))

            # Dibujar enlaces (edges)
            for enlace in star.get("linkedTo", []):
                destino_id = enlace["starId"]
                # Buscar destino en la misma constelación
                destino = next((s for s in stars if s["id"] == destino_id), None)
                if destino:
                    x2 = destino["coordenates"]["x"] * 3
                    y2 = destino["coordenates"]["y"] * 3
                    canvas.create_line(x, y, x2, y2, fill=color, width=1)

    tk.Label(root, text="Cierra esta ventana para volver al menú", bg="black", fg="white").pack(side="bottom", pady=10)
    root.mainloop()
