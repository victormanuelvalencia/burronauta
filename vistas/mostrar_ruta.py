import tkinter as tk
import math
from config import RAZON_TIEMPO_COMER
from controladores.simulacion_ruta import SimuladorRuta, salud_por_energia
from utilidades.ayudas_vistas import centrar_ventana

def mostrar_ruta(constelaciones_data, ruta, burro_info):
    """
    Muestra visualmente la ruta planificada del burronauta 🫏✨
    Incluye edad, energía, salud, pasto, posición actual, destino y temporizador.
    """
    # --- Ventana base ---
    window = tk.Toplevel()
    window.title("Ruta del Burronauta 🫏✨")
    window.config(bg="black")
    centrar_ventana(window, 1200, 750)

    # --- Temporizador superior ---
    timer_frame = tk.Frame(window, bg="black")
    timer_frame.pack(side="top", fill="x", pady=5)
    timer_label = tk.Label(timer_frame, text="⏳ Tiempo restante: 0 s", bg="black", fg="yellow",
                           font=("Consolas", 14, "bold"))
    timer_label.pack(pady=5)

    # --- Canvas principal ---
    canvas = tk.Canvas(window, bg="black", width=950, height=580)
    canvas.pack(side="left", padx=10, pady=20)

    # --- Panel lateral ---
    sidebar = tk.Frame(window, bg="#111111", width=220)
    sidebar.pack(side="right", fill="y")

    tk.Label(sidebar, text="📜 Información del Burronauta",
             font=("Arial", 12, "bold"), fg="white", bg="#111111").pack(pady=10)

    info_text = tk.Text(sidebar, bg="#1b1b1b", fg="white", font=("Consolas", 10), width=26, height=40)
    info_text.pack(padx=10, pady=10)

    def actualizar_panel_lateral(edad_actual, energia, salud, pasto):
        info_text.delete("1.0", tk.END)
        info_text.insert(tk.END, f"🫏 BURRONAUTA\n\n")
        info_text.insert(tk.END, f"Edad actual: {int(edad_actual)}\n")
        info_text.insert(tk.END, f"Energía: {int(energia)}%\n")
        info_text.insert(tk.END, f"Salud: {salud}\n")
        info_text.insert(tk.END, f"Pasto: {pasto} kg\n")

    # --- Escalado y dibujo del grafo ---
    constelaciones = constelaciones_data.get("constellations", [])
    if not constelaciones:
        return

    xs, ys = [], []
    for const in constelaciones:
        for star in const.get("starts", []):
            xs.append(star["coordenates"]["x"])
            ys.append(star["coordenates"]["y"])

    if not xs or not ys:
        return

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    escala = min((900 - 60) / (x_max - x_min + 1), (580 - 60) / (y_max - y_min + 1))

    star_coords, star_info = {}, {}
    for const in constelaciones:
        for star in const.get("starts", []):
            x = (star["coordenates"]["x"] - x_min) * escala + 30
            y = (star["coordenates"]["y"] - y_min) * escala + 30
            star_coords[str(star["id"])] = (x, y)
            star_info[str(star["id"])] = star

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
                    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                    canvas.create_text(mx, my, text=f"{link['distance']}", fill="#888888", font=("Arial", 7))

    for star_id, (x, y) in star_coords.items():
        star = star_info[star_id]
        fill_color = "red" if star.get("hypergiant", False) else "#AAAAAA"
        radius = 6 if star.get("hypergiant", False) else 4
        if ruta:
            if str(star_id) == str(ruta[0]):
                fill_color = "#00FF00"
                radius = 8
            elif str(star_id) == str(ruta[-1]):
                fill_color = "#1E90FF"
                radius = 8
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=fill_color, outline="")
        canvas.create_text(x + 8, y, text=star["label"], fill="white", font=("Arial", 8))

    # --- Simulación previa ---
    estado_inicial = {
        "energia": burro_info.get("burroenergiaInicial", 100),
        "pasto": burro_info.get("pasto", 100),
        "edad": burro_info.get("startAge", 0),
        "edad_muerte": burro_info.get("deathAge", 5000)
    }
    simulador = SimuladorRuta(star_info, estado_inicial)
    detalles_ruta = simulador.simular_ruta(ruta)

    # --- Panel de estado inferior ---
    estado_frame = tk.Frame(window, bg="black")
    estado_frame.pack(fill="x", pady=10)
    estado_text = tk.Text(estado_frame, bg="black", fg="white", font=("Consolas", 12), height=7, width=80)
    estado_text.pack(padx=10)

    def actualizar_estado(posicion_actual, destino, energia, edad, salud, pasto):
        barra_energia = "█" * int(energia / 10) + "-" * (10 - int(energia / 10))
        estado_text.delete("1.0", tk.END)
        estado_text.insert(tk.END,
f"""🪐 Estado del Burronauta
-----------------------------
Edad actual:  {int(edad)} años
Edad máxima:  {estado_inicial['edad_muerte']} años
Energía:      [{barra_energia}] {int(energia)}% 
Salud:        {salud} 💚
Pasto:        {pasto} kg 🌿
-----------------------------
Posición actual: {posicion_actual}
Destino: {destino}
""")

    # --- Burro inicial ---
    x0, y0 = star_coords[ruta[0]]
    burro = canvas.create_oval(x0 - 6, y0 - 6, x0 + 6, y0 + 6, fill="lime", outline="")

    detalle_inicial = detalles_ruta[0]
    actualizar_estado(star_info[str(ruta[0])]["label"], star_info[str(ruta[-1])]["label"],
                      detalle_inicial["energia"], detalle_inicial["edad"], detalle_inicial["salud"], detalle_inicial["pasto"])
    actualizar_panel_lateral(detalle_inicial["edad"], detalle_inicial["energia"], detalle_inicial["salud"], detalle_inicial["pasto"])

    # --- Botón inferior ---
    bottom_frame = tk.Frame(window, bg="black")
    bottom_frame.pack(side="bottom", fill="x", pady=5)
    tk.Button(bottom_frame, text="Continuar", bg="#ff9800", activebackground="#FFA500", fg="white",
              font=("Arial", 14, "bold"), width=20, height=2, relief="raised",
              command=window.destroy).pack(pady=5)

    # --- Movimiento con temporizador ---
    def mover_burro(i=0, paso=0):
        if i >= len(ruta) - 1:
            detalle_final = detalles_ruta[-1]
            actualizar_estado(star_info[str(ruta[-1])]["label"], "-", detalle_final["energia"],
                              detalle_final["edad"], detalle_final["salud"], detalle_final["pasto"])
            actualizar_panel_lateral(detalle_final["edad"], detalle_final["energia"],
                                     detalle_final["salud"], detalle_final["pasto"])
            timer_label.config(text="⏱ Ruta completada")
            return

        a, b = ruta[i], ruta[i + 1]
        x1, y1 = star_coords[a]
        x2, y2 = star_coords[b]
        total_pasos = 30
        dx, dy = (x2 - x1) / total_pasos, (y2 - y1) / total_pasos

        # Mover burro
        if paso < total_pasos:
            x_curr = x1 + dx * paso
            y_curr = y1 + dy * paso
            if paso > 0:
                x_prev = x1 + dx * (paso - 1)
                y_prev = y1 + dy * (paso - 1)
                canvas.create_line(x_prev, y_prev, x_curr, y_curr, fill="red", width=3)
            canvas.coords(burro, x_curr - 6, y_curr - 6, x_curr + 6, y_curr + 6)
            window.after(50, mover_burro, i, paso + 1)
            return

        # Llegada a la estrella
        detalle_actual = detalles_ruta[i + 1]
        actualizar_estado(star_info[str(b)]["label"], star_info[str(ruta[-1])]["label"],
                          detalle_actual["energia"], detalle_actual["edad"],
                          detalle_actual["salud"], detalle_actual["pasto"])
        actualizar_panel_lateral(detalle_actual["edad"], detalle_actual["energia"],
                                 detalle_actual["salud"], detalle_actual["pasto"])

        # Temporizador de la estrella (en segundos)
        tiempo_segundos = int(star_info[str(b)].get("timeToEat", 1) * RAZON_TIEMPO_COMER)

        def cuenta_regresiva(segundos):
            if segundos >= 0:
                timer_label.config(text=f"⏳ Tiempo restante en estrella: {segundos} s")
                window.after(1000, cuenta_regresiva, segundos - 1)
            else:
                mover_burro(i + 1, 0)

        cuenta_regresiva(tiempo_segundos)

    window.after(1000, mover_burro)
