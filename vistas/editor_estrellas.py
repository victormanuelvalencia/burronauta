# vistas/editor_estrellas.py

import tkinter as tk
from tkinter import ttk, messagebox
from utilidades.ayudas_vistas import centrar_ventana

SALUD_STATES = ["Sin cambios", "Excelente", "Buena", "Regular", "Mala", "Moribundo", "Muerto"]


def abrir_editor_estrellas(json_data: dict, guardar_callback=None):
    """
    Abre una ventana para que el usuario pueda editar los efectos investigativos
    de cada estrella (vida_delta y salud_delta) antes de iniciar la simulación.
    json_data: JSON cargado que contiene constelaciones y estrellas
    """
    # --- Convertir todas las estrellas a un diccionario plano ---
    estrellas_info = {}
    for constelacion in json_data.get("constellations", []):
        for star in constelacion.get("starts", []):
            star_copy = star.copy()
            # Normalizar clave de coordenadas
            if "coordenates" in star_copy:
                star_copy["coordenadas"] = star_copy.pop("coordenates")
            estrellas_info[str(star_copy["id"])] = star_copy

    if not estrellas_info:
        messagebox.showerror("Error", "No se encontraron estrellas en el JSON.")
        return

    root = tk.Toplevel()
    root.title("Editor de efectos investigativos (pre-misión)")
    root.config(bg="#222222")
    centrar_ventana(root, 700, 400)

    editing = False

    def set_editing(*_):
        nonlocal editing
        editing = True

    # --- Frame izquierdo: lista de estrellas ---
    frame_left = tk.Frame(root, bg="#222222")
    frame_left.pack(side="left", fill="y", padx=10, pady=10)

    tk.Label(frame_left, text="Estrellas", bg="#222222", fg="white", font=("Arial", 11, "bold")).pack(pady=(0,6))
    lb = tk.Listbox(frame_left, width=20, height=20)
    lb.pack()

    id_map = []
    for id_ in sorted(estrellas_info.keys(), key=lambda x: int(x)):
        label = estrellas_info[id_].get("label", str(id_))
        id_map.append(id_)
        lb.insert("end", f"{id_} - {label}")

    # --- Frame derecho: edición de efectos ---
    frame_right = tk.Frame(root, bg="#222222")
    frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    tk.Label(frame_right, text="Editar efectos investigativos", bg="#222222", fg="white", font=("Arial", 12, "bold")).pack(pady=(0,8))

    vida_var = tk.StringVar(value="0")
    salud_var = tk.StringVar()

    def build_input(label_text, var):
        frame = tk.Frame(frame_right, bg="#222222")
        frame.pack(fill="x", pady=6)
        tk.Label(frame, text=label_text, bg="#222222", fg="white").pack(anchor="w")
        entry = tk.Entry(frame, textvariable=var)
        entry.pack(fill="x")
        entry.bind("<FocusIn>", set_editing)
        return entry

    vida_entry = build_input("Años de vida (vida_delta):", vida_var)

    salud_frame = tk.Frame(frame_right, bg="#222222")
    salud_frame.pack(fill="x", pady=6)
    tk.Label(salud_frame, text="Estado de salud resultante (salud_delta):", bg="#222222", fg="white").pack(anchor="w")
    salud_combo = ttk.Combobox(salud_frame, values=SALUD_STATES, textvariable=salud_var, state="readonly")
    salud_combo.pack(fill="x")
    salud_combo.bind("<<ComboboxSelected>>", set_editing)

    lbl_coords = tk.Label(frame_right, text="", bg="#222222", fg="#cccccc", justify="left")
    lbl_coords.pack(anchor="w")
    lbl_timeToEat = tk.Label(frame_right, text="", bg="#222222", fg="#cccccc", justify="left")
    lbl_timeToEat.pack(anchor="w")
    lbl_hyper = tk.Label(frame_right, text="", bg="#222222", fg="#cccccc", justify="left")
    lbl_hyper.pack(anchor="w")

    # --- Función para mostrar info de una estrella ---
    def _mostrar(id_sel):
        info = estrellas_info[id_sel]

        # Efectos investigativos
        vida_var.set(str(info.get("vida_delta", 0)))
        salud_var.set(info.get("salud_delta") or "")

        # Coordenadas normalizadas
        coords = info.get("coordenadas", {})
        x = coords.get("x", "?")
        y = coords.get("y", "?")
        lbl_coords.config(text=f"Coordenadas: {x}, {y}")

        # Tiempo para comer y estado hipergigante
        lbl_timeToEat.config(text=f"timeToEat: {info.get('timeToEat', 'N/A')}")
        lbl_hyper.config(text=f"Hipergigante: {'Sí' if info.get('hypergiant', False) else 'No'}")

    def on_select(evt):
        nonlocal editing
        if editing:
            return
        sel = lb.curselection()
        if not sel:
            return
        _mostrar(id_map[sel[0]])

    lb.bind("<<ListboxSelect>>", on_select)

    def aplicar():
        nonlocal editing
        sel = lb.curselection()
        if not sel:
            return
        idx = id_map[sel[0]]

        # Validar y aplicar vida_delta
        try:
            estrellas_info[idx]["vida_delta"] = int(vida_var.get())
        except ValueError:
            messagebox.showerror("Error", "vida_delta debe ser un entero")
            return

        # Aplicar salud_delta solo si no es "Sin cambios"
        salud_seleccionada = salud_var.get()
        if salud_seleccionada and salud_seleccionada != "Sin cambios":
            estrellas_info[idx]["salud_delta"] = salud_seleccionada
        else:
            estrellas_info[idx]["salud_delta"] = None  # o conservar valor previo, si existe

        editing = False
        messagebox.showinfo("OK", "Cambios aplicados")

    def guardar():
        if guardar_callback:
            guardar_callback(estrellas_info)
            messagebox.showinfo("✅ Guardado", "Cambios guardados en el JSON")

    bot_kwargs = {
        "width": 20,  # ancho en caracteres
        "height": 1,  # alto en líneas
        "font": ("Arial", 11, "bold"),
        "fg": "white",
    }

    tk.Button(frame_right, text="💾 Aplicar cambios", bg="#4CAF50", command=aplicar, **bot_kwargs).pack(pady=5)
    tk.Button(frame_right, text="Guardar todo", bg="#0b84ff", command=guardar, **bot_kwargs).pack(pady=5)
    tk.Button(frame_right, text="Continuar", bg="#ff9800", command=root.destroy, **bot_kwargs).pack(pady=5)

    # Mostrar la primera estrella si hay al menos una
    if id_map:
        lb.selection_set(0)
        _mostrar(id_map[0])

    root.transient()
    root.grab_set()
    root.wait_window()