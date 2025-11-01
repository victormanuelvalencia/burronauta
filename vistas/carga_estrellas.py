# vistas/carga_estrellas.py

import tkinter as tk

# Colores distintos por constelación
COLORES = ["#00FFFF", "#FFD700", "#FF69B4", "#ADFF2F", "#FFA07A", "#87CEEB"]

def mostrar_estrellas(data):
    root = tk.Tk()
    root.title("Mapa de Constelaciones")
    root.geometry("800x600")
    root.config(bg="black")

    canvas_width, canvas_height = 800, 600
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")
    canvas.pack(fill="both", expand=True)

    constellations = data.get("constellations", [])

    # Detectar estrellas compartidas por coordenadas reales
    coordenadas_usadas = {}  # key=(x_real, y_real) -> lista de constelaciones

    # Primer paso: calcular escala mínima 200x200 um
    # Suponemos que las coordenadas originales están en um
    todas_x = []
    todas_y = []
    for constellation in constellations:
        for star in constellation.get("starts", []):
            todas_x.append(star["coordenates"]["x"])
            todas_y.append(star["coordenates"]["y"])
    if todas_x and todas_y:
        x_min, x_max = min(todas_x), max(todas_x)
        y_min, y_max = min(todas_y), max(todas_y)
        # Escala para que ocupe al menos 200x200 um en el canvas
        escala_x = (canvas_width - 50) / max(x_max - x_min, 200)
        escala_y = (canvas_height - 50) / max(y_max - y_min, 200)
        escala = min(escala_x, escala_y)
    else:
        escala = 3  # Valor por defecto si no hay datos

    # Diccionario para facilitar enlaces bidireccionales
    star_coords = {}  # key=star_id -> (x_canvas, y_canvas)

    # Dibujar constelaciones
    for idx, constellation in enumerate(constellations):
        color = COLORES[idx % len(COLORES)]
        stars = constellation.get("starts", [])

        # Registrar coordenadas de estrellas y detectar compartidas
        for star in stars:
            x_real = star["coordenates"]["x"]
            y_real = star["coordenates"]["y"]
            coord_key = (x_real, y_real)
            if coord_key in coordenadas_usadas:
                coordenadas_usadas[coord_key].append(idx)
            else:
                coordenadas_usadas[coord_key] = [idx]

        # Dibujar estrellas y enlaces
        for star in stars:
            x_real = star["coordenates"]["x"]
            y_real = star["coordenates"]["y"]
            x = (x_real - x_min) * escala + 25  # margenes
            y = (y_real - y_min) * escala + 25
            label = star["label"]

            # Si estrella pertenece a varias constelaciones → rojo
            if len(coordenadas_usadas[(x_real, y_real)]) > 1:
                star_color = "red"
            else:
                star_color = color

            # Guardar coordenadas para enlaces
            star_coords[star["id"]] = (x, y)

            # Dibujar estrella
            canvas.create_oval(
                x - 5, y - 5, x + 5, y + 5,
                fill=star_color,
                outline=""
            )
            canvas.create_text(x + 10, y, text=label, fill="white", font=("Arial", 8, "bold"))

        # Dibujar enlaces bidireccionales
        for star in stars:
            x1, y1 = star_coords[star["id"]]
            for enlace in star.get("linkedTo", []):
                destino_id = enlace["starId"]
                if destino_id in star_coords:
                    x2, y2 = star_coords[destino_id]
                    canvas.create_line(x1, y1, x2, y2, fill=color, width=1)

    tk.Label(root, text="Cierra esta ventana para volver al menú", bg="black", fg="white").pack(side="bottom", pady=10)
    root.mainloop()