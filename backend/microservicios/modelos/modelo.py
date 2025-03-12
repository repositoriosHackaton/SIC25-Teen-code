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
    df_recetas = cargar_recetas(ruta_recetas)
    tiempo_favorito, dificultad_favorita, categoria_favorita = procesar_historial(df_recetas)
    similitud = vectorizar(df_recetas)
    recomendacion = recomendar_receta(df_recetas, similitud, df_recetas["nombre"].iloc[-1])
    tipo = tridente_predictivo(recomendacion, ruta_clasificacion)

    return {"categoria":categoria_favorita,"dificultad":dificultad_favorita,"tiempo":tiempo_favorito,"url":create_url(tipo, tiempo_favorito, dificultad_favorita, ruta_filtros)}
    


def cargar_recetas(ruta_recetas):
    with open(ruta_recetas, "r", encoding="utf-8") as f:
        recetas = json.load(f)
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

def create_url(recipes, time, mode, ruta_filtros):
    with open(ruta_filtros, "r", encoding="utf-8") as f:
        filtros = json.load(f)
    BASE = "https://www.recetasgratis.net/busqueda/type/1"
    def filtrar(filter_key, value):
        return [filtros[filter_key].get(str(value), "")] if str(value) in filtros[filter_key] else []
    categorias = sum([filtrar("Categoría", r) for r in recipes], [])
    tiempo = filtrar("Duración", int(time))
    dificultad = filtrar("Dificultad", mode)
    return [f"{BASE}{i}{','.join(tiempo)}{','.join(dificultad)}" for i in categorias]

if __name__ == "__main__":
    modelo()
