# urls.py principal

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from microservicios.scraping.views import buscar_receta_view
from microservicios.modelos.views import recomendaciones_view
from microservicios.scraping.views import mostrar_pasos_view
from microservicios.usuarios.views import guardar_usuario
# from microservicios.analisis import views  # Asegúrate de que la vista está correctamente importada

def home(request):
    return HttpResponse("Bienvenido a BotRamsey. Usa /api/chatbot/ para interactuar con el chatbot.")
'''
def llamar_asistente_voz(request):
    """Vista que llama al asistente de voz desde el core."""
    texto = "Hola, Como oyes el CORE esta llamando a el asistente de voz y las subdependecias asociadas a ella "
    
    # Llamada a la función que reproduce el audio
    reproducir_audio(texto)
    
    return HttpResponse("El mensaje de voz ha sido reproducido desde el core.")
'''
urlpatterns = [
    path('', home, name='home'),  # Redirige la raíz a una vista básica.
    path('admin/', admin.site.urls),
    # path('asistente_voz/', llamar_asistente_voz, name='llamar_asistente_voz'),  # Ruta para el asistente de voz
    # path('analisis/', views.analisis_view, name='analisis'),
    path('api/', include('microservicios.nutricion.urls')),  # URLs del 
    path('api/buscar_receta/', buscar_receta_view, name='buscar_receta'),
    path('api/guardar_user/',guardar_usuario, name='guardar_usuario'),
    path('api/recomendacion/', recomendaciones_view, name='recomendaciones'),
    path('api/preparacion/', mostrar_pasos_view, name='preparacion')
]
