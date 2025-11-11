import tkinter as tk

COLORES = ["#00FFFF", "#FFD700", "#FF69B4", "#ADFF2F", "#FFA07A", "#87CEEB"]

def mostrar_ruta(constelaciones_data, ruta):
    """
    Muestra visualmente la ruta planificada del burro.
    Solo colorea las conexiones recorridas.

    Args:
        constelaciones_data (dict): JSON completo de constelaciones.
        ruta (list[str]): IDs de las estrellas visitadas por el burro.
    """
    window = tk.Toplevel()
    window.title("Ruta del burro 🫏✨")
    window.geometry("900x700")
    window.config(bg="black")

    canvas = tk.Canvas(window, bg="black", width=900, height=700)
    canvas.pack(fill="both", expand=True)

    constelaciones = constelaciones_data.get("constellations", [])
    if not constelaciones:
        return

    # --- Escalamos las coordenadas ---
    xs, ys = [], []
    for const in constelaciones:
        for star in const.get("starts", []):
            xs.append(star["coordenates"]["x"])
            ys.append(star["coordenates"]["y"])
    if not xs or not ys:
        return

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    escala = min((900 - 60) / (x_max - x_min + 1), (700 - 60) / (y_max - y_min + 1))

    # --- Guardamos posiciones escaladas ---
    star_coords = {}
    star_info = {}
    for i, const in enumerate(constelaciones):
        color_base = COLORES[i % len(COLORES)]
        for star in const.get("starts", []):
            x = (star["coordenates"]["x"] - x_min) * escala + 30
            y = (star["coordenates"]["y"] - y_min) * escala + 30
            star_coords[str(star["id"])] = (x, y)
            star_info[str(star["id"])] = star

    # --- Dibujar conexiones normales ---
    for i, const in enumerate(constelaciones):
        color = COLORES[i % len(COLORES)]
        for star in const.get("starts", []):
            x1, y1 = star_coords[str(star["id"])]
            for link in star.get("linkedTo", []):
                destino = str(link["starId"])
                if destino in star_coords:
                    x2, y2 = star_coords[destino]
                    canvas.create_line(x1, y1, x2, y2, fill=color, width=1)

    # --- Dibujar estrellas (hipergigantes y normales) ---
    for star_id, (x, y) in star_coords.items():
        star = star_info[star_id]

        # Si es hipergigante, en rojo
        if star.get("hypergiant", False):
            fill_color = "red"
            radius = 6
        else:
            fill_color = "#AAAAAA"
            radius = 4

        # Colorear inicio y fin de la ruta con colores especiales
        if ruta:
            if str(star_id) == str(ruta[0]):  # Inicio
                fill_color = "#00FF00"  # Verde brillante
                radius = 8
            elif str(star_id) == str(ruta[-1]):  # Fin
                fill_color = "#1E90FF"  # Azul brillante
                radius = 8

        canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill=fill_color, outline=""
        )
        canvas.create_text(x + 8, y, text=star["label"], fill="white", font=("Arial", 8))

    # --- Dibujar la ruta planificada ---
    for i in range(len(ruta) - 1):
        a, b = ruta[i], ruta[i + 1]
        if a in star_coords and b in star_coords:
            x1, y1 = star_coords[a]
            x2, y2 = star_coords[b]
            canvas.create_line(x1, y1, x2, y2, fill="red", width=3)

    tk.Label(
        window,
        text="Ruta del burro (en rojo) | Inicio (verde) | Fin (azul) | Hipergigante (rojo)",
        bg="black",
        fg="white",
        font=("Arial", 10, "bold")
    ).pack(pady=6)
