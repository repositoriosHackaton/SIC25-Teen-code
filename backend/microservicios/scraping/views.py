from django.shortcuts import render
from django.http import JsonResponse
from .scraper import buscar_receta
from .scraper import mostrar_pasos
from google import genai
from dotenv import load_dotenv
import os


def gemini(text, context=""):
    """
    Funcion que pasa el texto del usuario por gemini para obtener los datos.
    """
    load_dotenv()
    API_KEY= os.getenv("API_KEY")
    client = genai.Client(api_key=API_KEY)
    
    context += """
    Necesito que me ayudes a comprender las solicitudes de los usuarios para una aplicación de recetas. A partir de ahora, el usuario pedirá recetas, dietas y posiblemente algunas restricciones como "sin gluten", "sin azúcar", o "sin lactosa". Tu tarea es muy específica:

    Solo quiero que me des como respuesta la comida o receta que pidió el usuario, junto con la restricción o dieta, si es que la menciona.

    No incluyas conectivos ni texto adicional, solo palabras clave.

    Ejemplos de cómo quiero las respuestas:

    Si el cliente dice: "Quisiera pedir pan con carne", tu respuesta debe ser: "pan carne".

    Si el cliente dice: "quiero pan con carne", tu respuesta debe ser: "pan con carne".

    Si el cliente dice: "Quisiera pedir pan con carne pero sin sal", tu respuesta debe ser: "pan carne sin sal".

    Si el cliente dice: "Quisiera un plato vegano de pasta", tu respuesta debe ser: "pasta vegano".

    Por favor, no me des respuestas largas, solo lo que te pedí. Ten en cuenta que las restricciones son lo que no debe tener la comida y las dietas son para las enfermedades o preferencias del usuario. Gracias. \n
    """

    def get_response(text: str) -> str:
        nonlocal context
        contents = f"{context}\n{text}"
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
        )
        context += f"{text}\n{response.text.strip()}\n"
        return response.text.strip()
    
    gemini_text = get_response(text)
    return gemini_text

def buscar_receta_view(request):
    """
    Endpoint que recibe una búsqueda y devuelve una receta.
    """
    query = request.GET.get('query')
    if not query:
        return JsonResponse({"error": "Por favor, proporciona un término de búsqueda."}, status=400)

    promt = gemini(query)
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
