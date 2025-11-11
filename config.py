import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# Variables globales del proyecto
RAZON_TIEMPO_COMER = float(os.getenv("RAZON_TIEMPO_COMER", 5))
RAZON_TIEMPO_INVESTIGAR = float(os.getenv("RAZON_TIEMPO_INVESTIGAR", 1.2))
INVESTIGACION_ENERGIA_POR_SEGUNDO = float(os.getenv("INVESTIGACION_ENERGIA_POR_SEGUNDO", 0.02))
COMIDA_KG_POR_SEGUNDO = float(os.getenv("COMIDA_KG_POR_SEGUNDO", 1.0))
