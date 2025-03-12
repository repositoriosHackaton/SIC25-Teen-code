import re

# Función para convertir la duración a minutos solo para el gráfico
def procesar_minutos(duracion):

    horas = re.search(r"(\d+)h", duracion)
    minutos = re.search(r"(\d+)m", duracion)
    total_minutos = 0
    if horas:
        total_minutos += int(horas.group(1)) * 60
    if minutos:
        total_minutos += int(minutos.group(1))
    
    return total_minutos


def Clasificar_Dificultad(df):
    nivel_map = {
        'muy baja': 'Muy Baja',
        'baja': 'Baja',
        'media': 'Media',
        'alta': 'Alta'
    }
    df['Dificultad'] = df['Dificultad'].map(nivel_map)
    
def procesar_datos(df):
    
    df['Duracion'] = df['Duracion'].apply(procesar_minutos)
    df['Valoracion'] = df['Valoracion'].str.replace('%', '').astype(float)

    df = limpiar(df)

    Clasificar_Dificultad(df)


def limpiar(df):
    df = df.drop_duplicates()

    df = df.dropna()

    df = df[df['Duracion'] > 0]


    df = df[(df['Valoracion'] >= 0) & (df['Valoracion'] <= 100)]


    df = df[df['Dificultad'].isin(['alta', 'media', 'baja', 'muy baja'])]

    return df