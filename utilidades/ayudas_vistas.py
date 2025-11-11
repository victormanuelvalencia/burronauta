# utilidades/ayudas_vistas.py

def centrar_ventana(ventana, ancho, alto):
    """Centrar una ventana de Tkinter en la pantalla."""
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2) - 50
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
