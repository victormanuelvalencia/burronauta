import tkinter as tk
import math
from config import RAZON_TIEMPO_COMER
from utilidades.ayudas_vistas import centrar_ventana

# Colores
COLOR_EXCELENTE = "\033[92m"
COLOR_BUENO = "\033[94m"
COLOR_REGULAR = "\033[93m"
COLOR_MALO = "\033[91m"
COLOR_RESET = "\033[0m"

# Parámetros de comportamiento
RAZON_TIEMPO_INVESTIGAR = 1.2  # Multiplica el tiempo base de investigación

def mostrar_ruta(constelaciones_data, ruta):
    """
    Muestra visualmente la ruta planificada del burro 🫏✨
    con animación progresiva, pausas personalizadas y temporizador por nodo.
    """
    # --- Ventana base ---
    window = tk.Toplevel()
    window.title("Ruta del burro 🫏✨")
    window.config(bg="black")
    centrar_ventana(window, 700, 600)  # ✅ misma dimensión y centrado que carga_estrellas.py

    # --- Frame principal ---
    main_frame = tk.Frame(window, bg="black")
    main_frame.pack(fill="both", expand=True)

    canvas_width, canvas_height = 800, 500  # mismo tamaño de canvas
    canvas = tk.Canvas(main_frame, bg="black", width=canvas_width, height=canvas_height)
    canvas.pack(fill="both", expand=True)

    constelaciones = constelaciones_data.get("constellations", [])
    if not constelaciones:
        return

    # --- Escalamos coordenadas ---
    xs, ys = [], []
    for const in constelaciones:
        for star in const.get("starts", []):
            xs.append(star["coordenates"]["x"])
            ys.append(star["coordenates"]["y"])

    if not xs or not ys:
        return

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    escala = min((canvas_width - 60) / (x_max - x_min + 1), (canvas_height - 60) / (y_max - y_min + 1))

    # --- Guardamos posiciones escaladas y tiempos ---
    star_coords = {}
    star_info = {}
    for i, const in enumerate(constelaciones):
        for star in const.get("starts", []):
            x = (star["coordenates"]["x"] - x_min) * escala + 30
            y = (star["coordenates"]["y"] - y_min) * escala + 30
            star_coords[str(star["id"])] = (x, y)
            star_info[str(star["id"])] = star

    # --- Dibujar conexiones base ---
    COLORES = ["#FFA500", "#00FFFF", "#FF00FF", "#00FF00", "#FF0000", "#FFFFFF"]
    for i, const in enumerate(constelaciones):
        color = COLORES[i % len(COLORES)]
        for star in const.get("starts", []):
            x1, y1 = star_coords[str(star["id"])]
            for link in star.get("linkedTo", []):
                destino = str(link["starId"])
                if destino in star_coords:
                    x2, y2 = star_coords[destino]
                    canvas.create_line(x1, y1, x2, y2, fill=color, width=1)

    # --- Dibujar estrellas ---
    for star_id, (x, y) in star_coords.items():
        star = star_info[star_id]
        if star.get("hypergiant", False):
            fill_color = "red"
            radius = 6
        else:
            fill_color = "#AAAAAA"
            radius = 4

        if ruta:
            if str(star_id) == str(ruta[0]):
                fill_color = "#00FF00"  # Inicio
                radius = 8
            elif str(star_id) == str(ruta[-1]):
                fill_color = "#1E90FF"  # Fin
                radius = 8

        canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill=fill_color, outline=""
        )
        canvas.create_text(x + 8, y, text=star["label"], fill="white", font=("Arial", 8))

    # --- Etiquetas informativas ---
    tk.Label(
        main_frame,
        text="Ruta animada del burro (rojo progresivo) 🌌 | Pausas según timeToEat 🌿",
        bg="black",
        fg="white",
        font=("Arial", 10, "bold")
    ).place(x=120, y=5)

    # Temporizador visual (centrado arriba)
    temporizador_label = tk.Label(
        main_frame, text="", bg="black", fg="#00FFAA", font=("Arial", 14, "bold")
    )
    temporizador_label.place(x=300, y=30)

    # --- Botón inferior igual al de carga_estrellas.py ---
    bottom_frame = tk.Frame(window, bg="black")
    bottom_frame.pack(fill="x", pady=20)

    btn_continuar = tk.Button(
        bottom_frame,
        text="Continuar",
        bg="#ff9800",
        activebackground="#FFA500",
        fg="white",
        font=("Arial", 14, "bold"),
        width=20,
        height=2,
        relief="raised",
        command=window.destroy
    )
    btn_continuar.pack(pady=10)

    # --- Animación progresiva con pausas ---
    if not ruta or len(ruta) < 2:
        return

    # Burro inicial
    x0, y0 = star_coords[ruta[0]]
    burro = canvas.create_oval(x0 - 6, y0 - 6, x0 + 6, y0 + 6, fill="lime", outline="")

    def actualizar_temporizador(tiempo_restante, es_final=False):
        if tiempo_restante > 0:
            temporizador_label.config(text=f"⏳ Tiempo de estadía: {tiempo_restante:.0f}s")
            window.after(1000, actualizar_temporizador, tiempo_restante - 1, es_final)
        else:
            if es_final:
                temporizador_label.config(text="🪐 Viaje terminado ✅")
            else:
                temporizador_label.config(text="🌟 ¡Listo para continuar el viaje!")

    def mover_burro(i=0, paso=0):
        if i >= len(ruta) - 1:
            actualizar_temporizador(0, es_final=True)
            return

        a, b = ruta[i], ruta[i + 1]
        if a not in star_coords or b not in star_coords:
            return

        x1, y1 = star_coords[a]
        x2, y2 = star_coords[b]

        total_pasos = 30
        dx = (x2 - x1) / total_pasos
        dy = (y2 - y1) / total_pasos

        if paso > 0:
            x_prev = x1 + dx * (paso - 1)
            y_prev = y1 + dy * (paso - 1)
            x_curr = x1 + dx * paso
            y_curr = y1 + dy * paso
            canvas.create_line(x_prev, y_prev, x_curr, y_curr, fill="red", width=3)
            canvas.coords(burro, x_curr - 6, y_curr - 6, x_curr + 6, y_curr + 6)

        if paso < total_pasos:
            window.after(50, mover_burro, i, paso + 1)
        else:
            star_data = star_info.get(str(b))
            tiempo_espera = star_data.get("timeToEat", 1) * RAZON_TIEMPO_COMER
            print(f"🌟 Burro descansando en {star_data.get('label')} durante {tiempo_espera:.1f}s")

            es_final = (i + 1) == len(ruta) - 1
            actualizar_temporizador(int(tiempo_espera), es_final=es_final)

            if not es_final:
                window.after(int(tiempo_espera * 1000), mover_burro, i + 1, 0)
            else:
                window.after(int(tiempo_espera * 1000), lambda: actualizar_temporizador(0, es_final=True))

    window.after(1000, mover_burro)
