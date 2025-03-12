from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import os
import microservicios.scraping.scraper as sp

@csrf_exempt  # 🚨 Desactiva CSRF solo para esta vista
def guardar_usuario(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido. Usa POST."}, status=405)

    try:
        user_data = json.loads(request.body.decode("utf-8"))  # Obtener JSON del cuerpo
    except json.JSONDecodeError:
        return JsonResponse({"error": "Formato de JSON inválido."}, status=400)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
    BASE_DIR = os.path.dirname(BASE_DIR)  
    BASE_DIR = os.path.dirname(BASE_DIR)  

    file_path = os.path.join(BASE_DIR, "data", "modelo_usuario.json")

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(user_data, file, indent=4, ensure_ascii=False)

    sp.guardar_modelo()

    return JsonResponse({"message": "Usuario guardado exitosamente."})
