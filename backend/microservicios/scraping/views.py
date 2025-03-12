from django.shortcuts import render
from django.http import JsonResponse
from .scraper import buscar_receta
from .scraper import mostrar_pasos
import os
import torch
from transformers import AutoModelForTokenClassification, AutoTokenizer
import numpy as np

def bertRamsey(texto):

    repo_id = "Misterclon06/bertRamsey"

    # Descargar y cargar modelo + tokenizer
    model = AutoModelForTokenClassification.from_pretrained(repo_id)
    tokenizer = AutoTokenizer.from_pretrained(repo_id)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # 📌 3. Mapeo de etiquetas (Asegúrate de usar las mismas etiquetas que en el entrenamiento)
    id2label = {0: "O", 1: "B-NOMBRE", 2: "I-NOMBRE", 3: "B-GUSTO", 4: "I-GUSTO", 5: "B-RESTRICCION", 6: "I-RESTRICCION"}


    # Tokenizar la oración
    tokens = tokenizer(texto, truncation=True, padding="max_length", max_length=128, return_tensors="pt")
    tokens = {key: value.to(device) for key, value in tokens.items()}  # Enviar a GPU si está disponible

    # Hacer la predicción con el modelo
    with torch.no_grad():
        outputs = model(**tokens)

    logits = outputs.logits
    predictions = torch.argmax(logits, dim=-1).squeeze().tolist()  # Obtener las etiquetas predichas

    # Convertir tokens en palabras
    tokens_decoded = tokenizer.convert_ids_to_tokens(tokens["input_ids"].squeeze().tolist())

    # Extraer solo palabras clave (ignorar etiquetas "O")
    palabras_clave = []
    for token, label_id in zip(tokens_decoded, predictions):
        label = id2label.get(label_id, "O")
        if label.startswith("B-") or label.startswith("I-"):
            palabras_clave.append(token)

    return " ".join(palabras_clave).replace(" ##", "")  # Limpiar subpalabras unidas por BERT

def buscar_receta_view(request):
    """
    Endpoint que recibe una búsqueda y devuelve una receta.
    """
    query = request.GET.get('query')
    if not query:
        return JsonResponse({"error": "Por favor, proporciona un término de búsqueda."}, status=400)

    promt = bertRamsey(query)
    print("Promt:", promt)
    receta = buscar_receta(promt)

    if receta:
        return JsonResponse(receta, safe=False)
    else:
        return JsonResponse({"error": "No se encontró ninguna receta."}, status=404)

def mostrar_pasos_view(request):

    query = request.GET.get('query')
    if not query:
        return JsonResponse({"error": "Por favor, proporciona un término de búsqueda."}, status=400)

    preparacion = mostrar_pasos(query)
    if preparacion:
        return JsonResponse(preparacion, safe=False)
    else:
        return JsonResponse({"error": "No se encontró ninguna receta."}, status=404)


