import os
import json
import pandas as pd

def cargar_datos():
    """Carga los datos de recetas y clasificación desde archivos."""
    with open('data/clasificacion.json', 'r') as f:
        clasificacion = json.load(f)

    ruta_archivo = 'data/recetas.csv'
    if os.path.exists(ruta_archivo):
        df = pd.read_csv(ruta_archivo)
    else:
        raise FileNotFoundError("No hay datos que analizar")

    return clasificacion, df

def filtrar_datos(clasificacion, df, dificultad, tipo):
    """Filtra los datos según la dificultad y el tipo de receta."""
    if dificultad and dificultad != 'todas':
        df = df[df['Dificultad'] == dificultad]

    if tipo and tipo != 'todas':
        df = df[df['Tipo'].isin(clasificacion.get(tipo, []))]

    return df