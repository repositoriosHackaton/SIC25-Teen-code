from bs4 import BeautifulSoup
import requests
import json
#import pandas as pd
import os
import microservicios.modelos.modelo as md

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directorio actual de modelo.py
BASE_DIR = os.path.dirname(BASE_DIR)  # Sube un nivel (a "microservicios")
BASE_DIR = os.path.dirname(BASE_DIR)  # Sube otro nivel (a "backend")

def obtener_contenido(enlace):
    """
    Realiza una solicitud HTTP al enlace y devuelve un objeto BeautifulSoup.
    """
    try:
        respuesta = requests.get(enlace)
        respuesta.raise_for_status()
        return BeautifulSoup(respuesta.text, 'html.parser')
    except requests.RequestException:
        return None
    

def obtener_receta(enlace):
    ### Extrae información de la receta de la página y la muestra ### 
    sopa = obtener_contenido(enlace)
    if not sopa:
        return

    titulo = sopa.find('h1', class_='titulo titulo--articulo').get_text(strip=True)
    tipo = sopa.find('a', class_='post-categoria-link').get_text(strip=True)
    try:
        valoracion = sopa.find('div', class_='valoracion').get('style', '').split(':')[-1].strip()
    except AttributeError:
        valoracion = "50.00%"
    propiedades = [prop.get_text(strip=True) for prop in sopa.select('div.properties span')]
    ingredientes = [ing.get_text(strip=True) for ing in sopa.select('div.ingredientes label')]

    guardar_datos(titulo, propiedades, ingredientes, valoracion, tipo)

    return {'link':enlace, 'titulo':titulo, 'propiedades':propiedades, 'ingredientes':ingredientes,'valoracion': valoracion, 'tipo':tipo}


def buscar_receta(busqueda):
    """
    Busca una receta en el sitio web basado en el término de búsqueda.
    """

    enlace_web = f"https://www.recetasgratis.net/busqueda?q={busqueda.replace(' ', '+')}"
    sopa = obtener_contenido(enlace_web)
    if not sopa:
        return None

    enlace = sopa.select_one('div.resultado.link a')
    if enlace:
        href = enlace.get('href')
        receta = obtener_receta(href)
        return receta
    return None



def guardar_datos(titulo, propiedades, ingredientes, valoracion, tipo):

    BD = cargar_datos()

    ### Guarda la receta en la base de datos de sesión ### 
    receta = {
        "ingredientes": [ingrediente.strip() for ingrediente in ingredientes],
        "Valoracion": valoracion,
        "Duracion": propiedades[1] if len(propiedades) > 1 else "Desconocido",
        "Dificultad": next((p.split()[-1] for p in propiedades if "Dificultad" in p), "Desconocida"),
        "Tipo": tipo
    }

    BD[titulo] = receta
    
    guardar_archivos(BD)



def guardar_archivos(Base):
    ### Guarda la base de datos en archivos JSON### 
    if Base:
        # Guardar JSON
        with open(os.path.join(BASE_DIR, "data", "recetas.json"), 'w', encoding='utf-8') as f:
            json.dump(Base, f, indent=4, ensure_ascii=False)
        
        guardar_modelo()

def guardar_modelo():
    path = os.path.join(BASE_DIR, "data", "modelo_usuario.json")
        

    with open(path, 'r', encoding='utf-8') as f:
        user = json.load(f)


    usuario_modelo = md.modelo()

    diccionario_combinado = {**user, **usuario_modelo}

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(diccionario_combinado, f, indent=4, ensure_ascii=False)


def cargar_datos():
    ### Carga los datos desde el archivo JSON si existe ### 
    path = os.path.join(BASE_DIR, "data", "recetas.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def mostrar_pasos(enlace):
    ### Extrae y muestra los pasos de preparación de la receta ### 
    sopa = obtener_contenido(enlace)
    if not sopa:
        return

    pasos = [p.get_text() for p in sopa.select("div.apartado")]

    return pasos


def recomendados():
    path = os.path.join(BASE_DIR, "data", "modelo_usuario.json")
    url = ["https://www.recetasgratis.net/busqueda/type/1"]  # Inicializar url como una lista vacía

    # Cargar el modelo de usuario desde el archivo o generar uno nuevo
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                modelo = json.load(f)
        except json.JSONDecodeError:
            print("Error al decodificar el archivo JSON.")
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")
    else:
        try:
            modelo = md.modelo()  # Generar un nuevo modelo
        except Exception as e:
            print(f"Error al generar el modelo: {e}")

    if "url" in modelo:
        url = modelo.get("url", url)

    recomendacion = {
        "nombre": [],
        "link": [],
        "dificultad": [],
        "comensales": [],
        "duracion": [],
        "imagen": []
    }

    for enlace in url:
        sopa = obtener_contenido(enlace)
        if not sopa:
            continue  # Continuar si no se obtiene contenido

        recomendados = sopa.select('div.resultado.link')

        # Limitar el número de recomendaciones a 10 o menos si hay menos resultados
        for i in range(min(10, len(recomendados))):
            link_tag = recomendados[i].find('a')
            dificultad_tag = recomendados[i].find('span')
            comensales_tag = recomendados[i].find('span', class_='property comensales')
            duracion_tag = recomendados[i].find('span', class_='property duracion')
            img_tag = recomendados[i].find('source').get("srcset")

            # Agregar datos a la recomendación
            recomendacion["nombre"].append(link_tag.get_text(strip=True) if link_tag else "Desconocida")
            recomendacion["link"].append(link_tag['href'] if link_tag and 'href' in link_tag.attrs else "")
            recomendacion["dificultad"].append(dificultad_tag.get_text(strip=True) if dificultad_tag else "Desconocida")
            recomendacion["comensales"].append(comensales_tag.get_text(strip=True) if comensales_tag else "Desconocido")
            recomendacion["duracion"].append(duracion_tag.get_text(strip=True) if duracion_tag else "Desconocido")
            recomendacion["imagen"].append(img_tag)

    return recomendacion

