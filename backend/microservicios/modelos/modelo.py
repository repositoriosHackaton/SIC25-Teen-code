import json
import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import microservicios.limpieza.procesar_datos as prd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directorio actual de modelo.py
BASE_DIR = os.path.dirname(BASE_DIR)  # Sube un nivel (a "microservicios")
BASE_DIR = os.path.dirname(BASE_DIR)  # Sube otro nivel (a "backend")


def modelo():
    ruta_recetas = os.path.join(BASE_DIR, "data", "recetas.json")
    ruta_clasificacion = os.path.join(BASE_DIR, "data", "clasificacion.json")
    ruta_filtros = os.path.join(BASE_DIR, "data", "filtros.json")
    ruta_usuario = os.path.join(BASE_DIR, "data", "modelo_usuario.json")
    if os.path.exists(ruta_recetas):
        df_recetas = cargar_recetas(ruta_recetas)
        tiempo_favorito, dificultad_favorita, categoria_favorita = procesar_historial(df_recetas)
        similitud = vectorizar(df_recetas)
        recomendacion = recomendar_receta(df_recetas, similitud, df_recetas["nombre"].iloc[-1])
        tipo = tridente_predictivo(recomendacion, ruta_clasificacion)

        return {"categoria":categoria_favorita,"dificultad":dificultad_favorita,"tiempo":tiempo_favorito,"url":create_url(tipo, tiempo_favorito, dificultad_favorita, ruta_filtros, ruta_usuario)}
    else:
        return  {"categoria":"","dificultad":"","tiempo":"","url":create_url({}, "", "", ruta_filtros, ruta_usuario)}


def cargar_recetas(ruta_recetas):
    if os.path.exists(ruta_recetas):
        with open(ruta_recetas, "r", encoding="utf-8") as f:
            recetas = json.load(f)

    else:
        recetas={}
    df_recetas = pd.DataFrame.from_dict(recetas, orient="index").reset_index()
    df_recetas = df_recetas.dropna()
    df_recetas.columns = ["nombre", "ingredientes", "valoracion", "duracion", "dificultad", "tipo"]
    df_recetas["duracion_min"] = df_recetas["duracion"].apply(prd.procesar_minutos)
    df_recetas["valoracion"] = df_recetas["valoracion"].str.replace("%", "").astype(float)
    return df_recetas

def procesar_historial(df_recetas):
    df_historial = df_recetas.copy()
    categoria_favorita = df_historial["tipo"].mode()[0]
    ingredientes_favoritos = Counter(sum(df_historial["ingredientes"].tolist(), [])).most_common(5)
    tiempo_favorito = df_historial["duracion_min"].median()
    dificultad_favorita = df_historial["dificultad"].mode()[0]
    return tiempo_favorito, dificultad_favorita, categoria_favorita

def vectorizar(df_recetas):
    df_recetas["ingredientes_texto"] = df_recetas["ingredientes"].apply(lambda x: " ".join(x))
    vectorizer = TfidfVectorizer()
    matriz_vectores = vectorizer.fit_transform(df_recetas["ingredientes_texto"])
    return cosine_similarity(matriz_vectores)

def recomendar_receta(df_recetas, similitud, nombre_receta, n=5):
    idx = df_recetas[df_recetas["nombre"].str.contains(nombre_receta, case=False, na=False)].index[0]
    similitudes = sorted(list(enumerate(similitud[idx])), key=lambda x: x[1], reverse=True)
    return set(df_recetas.iloc[i[0]]["tipo"] for i in similitudes[1:n+1])

def tridente_predictivo(recomendacion, ruta_clasificacion):
    with open(ruta_clasificacion, "r", encoding="utf-8") as f:
        clasificacion = json.load(f)
    tipo = {j.replace("Recetas de ", "") for i in recomendacion for j in clasificacion if i in clasificacion[j]}
    return tipo

def filtrar(filtros, filter_key, value):
    """Filtra los valores según la clave y el valor proporcionados."""
    return [filtros[filter_key].get(str(value), "")] if str(value) in filtros[filter_key] else []

def create_url(recipes, time, mode, ruta_filtros, restricciones):
    # Cargar preferencias del usuario si el archivo existe
    user = {}
    if os.path.exists(restricciones):
        with open(restricciones, 'r', encoding='utf-8') as f:
            user = json.load(f)

    # Cargar filtros desde el archivo especificado
    with open(ruta_filtros, "r", encoding="utf-8") as f:
        filtros = json.load(f)

    BASE = "https://www.recetasgratis.net/busqueda/type/1"

    # Inicializar listas para filtros
    categorias = []
    tiempo = []
    dificultad = []
    preferencias = []
    alimentacion = []

    # Aplicar filtros a categorías, tiempo y dificultad solo si no hay una URL almacenada
    if "url" in user:
        categorias = [filtrar(filtros, "Categoría", r) for r in recipes]
        tiempo = filtrar(filtros, "Duración", int(time)) if time else []
        dificultad = filtrar(filtros, "Dificultad", mode)

    # Manejo seguro de claves en `user`
    if "preferencias" in user:
        preferencias = [filtrar(filtros, "Propiedades", i) for i in user["preferencias"]]
    if "alimentacion" in user:
        alimentacion = [filtrar(filtros, "Alimentación", i) for i in user["alimentacion"]]

    # Asegurar que no haya listas anidadas en `categorias`
    categorias = [item for sublist in categorias for item in sublist]  # Aplana listas

    urls = []

    # Generar combinaciones de URLs
    for p in preferencias or [""]:  # Si está vacío, usar cadena vacía
        for a in alimentacion or [""]:
            if not categorias or not tiempo or not dificultad:
                urls.append(f"{BASE}{','.join(p)}{','.join(a)}")
            else:
                urls.extend(
                    f"{BASE}{','.join([c])}{','.join(tiempo)}{','.join(dificultad)}{','.join(p)}{','.join(a)}"
                    for c in categorias
                )

    return urls



if __name__ == "__main__":
    modelo()
