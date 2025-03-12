from django.shortcuts import render
from microservicios.scraping.scraper import recomendados
from django.http import JsonResponse

# Vista corregida
def recomendaciones_view(request):  # Ahora acepta `request`
    recomendaciones = recomendados()

    if recomendaciones:
        return JsonResponse(recomendaciones, safe=False)
    else:
        return JsonResponse({"error": "No se encontró ninguna receta."}, status=404)

