# vistas/menu.py
import tkinter as tk
from tkinter import filedialog, messagebox
from utilidades.admin_json import read_json
from vistas.carga_estrellas import mostrar_estrellas

def abrir_menu():
    root = tk.Tk()
    root.title("Menú - Proyecto Grafos del Burro 🐴✨")
    root.geometry("400x200")
    root.config(bg="#2b2b2b")

    label = tk.Label(
        root,
        text="Proyecto Grafos - Burro Espacial",
        font=("Arial", 14, "bold"),
        fg="white",
        bg="#2b2b2b"
    )
    label.pack(pady=20)

    def cargar_json():
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo JSON",
            filetypes=[("Archivos JSON", "*.json")]
        )
        if not ruta:
            return  # Si el usuario cancela

        try:
            data = read_json(ruta)  # ← usamos tu función del módulo utilidades
            messagebox.showinfo("Éxito", f"Archivo cargado correctamente ✅\n{ruta}")
            root.destroy()  # Cerramos el menú
            mostrar_estrellas(data)  # Mostramos las estrellas
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")

    boton_cargar = tk.Button(
        root,
        text="📂 Cargar archivo JSON",
        command=cargar_json,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12, "bold"),
        width=25
    )
    boton_cargar.pack(pady=40)

    root.mainloop()
