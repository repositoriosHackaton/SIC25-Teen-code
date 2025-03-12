from django.urls import path
from .views.analisis_views import DificultadVsValoracionAPIView, DuracionVsDificultadAPIView, BarrasDificultadAPIView

urlpatterns = [
    path('dificultad-vs-valoracion/', DificultadVsValoracionAPIView.as_view(), name='dificultad_vs_valoracion'),
    path('duracion-vs-dificultad/', DuracionVsDificultadAPIView.as_view(), name='duracion_vs_dificultad'),
    path('barras-dificultad/', BarrasDificultadAPIView.as_view(), name='barras_dificultad'),    
]