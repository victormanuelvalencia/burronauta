# vistas/seleccionar_estrella.py

import tkinter as tk
from tkinter import ttk

def seleccionar_estrella_inicio(estrellas_ids, callback):
    """
    Ventana para que el usuario seleccione la estrella inicial.

    Args:
        estrellas_ids (list[str]): lista de IDs disponibles
        callback (func): función a ejecutar cuando se seleccione la estrella
    """
    window = tk.Tk()
    window.title("Seleccionar estrella inicial")
    window.geometry("350x220")
    window.config(bg="#1a1a1a")

    tk.Label(
        window,
        text="Seleccione la estrella inicial",
        fg="white",
        bg="#1a1a1a",
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    combo = ttk.Combobox(window, values=estrellas_ids, state="readonly", font=("Arial", 11))
    combo.pack(pady=10)
    combo.set(estrellas_ids[0])  # valor por defecto

    def confirmar():
        seleccion = combo.get()
        window.destroy()
        callback(seleccion)

    tk.Button(
        window,
        text="🚀 Iniciar misión",
        command=confirmar,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 11, "bold"),
        width=20
    ).pack(pady=15)

    window.mainloop()