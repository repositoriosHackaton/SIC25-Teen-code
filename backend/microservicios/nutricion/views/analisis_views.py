from django.http import HttpResponse
from rest_framework.views import APIView
from ..services.analisis_service import AnalisisService

class DificultadVsValoracionAPIView(APIView):
    def get(self, request):
        dificultad = request.GET.get('dificultad', 'todas')
        tipo = request.GET.get('tipo', 'todas')
        return AnalisisService.dificultad_vs_valoracion(dificultad, tipo)

class DuracionVsDificultadAPIView(APIView):
    def get(self, request):
        dificultad = request.GET.get('dificultad', 'todas')
        tipo = request.GET.get('tipo', 'todas')
        return AnalisisService.duracion_vs_dificultad(dificultad, tipo)

class BarrasDificultadAPIView(APIView):
    def get(self, request):
        dificultad = request.GET.get('dificultad', 'todas')
        tipo = request.GET.get('tipo', 'todas')
        return AnalisisService.barras_dificultad(dificultad, tipo)