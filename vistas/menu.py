# vistas/menu.py

import tkinter as tk
from tkinter import filedialog, messagebox
from utilidades.admin_json import read_json
from utilidades.ayudas_vistas import centrar_ventana

def abrir_menu():
    root = tk.Tk()
    root.title("Menú - Burronauta")
    root.config(bg="#2b2b2b")
    centrar_ventana(root, 700, 400)

    label = tk.Label(
        root,
        text="Proyecto Grafos - Burronauta",
        font=("Arial", 14, "bold"),
        fg="white",
        bg="#2b2b2b"
    )
    label.pack(pady=(110, 20))

    ruta_seleccionada = {"ruta": None}

    def cargar_json():
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo JSON",
            filetypes=[("Archivos JSON", "*.json")]
        )

        if not ruta:
            return

        try:
            read_json(ruta)
            messagebox.showinfo("Éxito", "Archivo cargado correctamente ✅")
            ruta_seleccionada["ruta"] = ruta
            root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")

    tk.Button(
        root,
        text="📂 Cargar archivo JSON",
        command=cargar_json,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12, "bold"),
        width=25
    ).pack(pady=40)

    root.mainloop()
    return ruta_seleccionada["ruta"]