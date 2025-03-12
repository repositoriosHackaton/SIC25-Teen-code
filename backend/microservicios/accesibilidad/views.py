from django.http import HttpResponse
from django.shortcuts import render
from .utils.voice_assistant import reproducir_audio

def reproducir_voz(request):
    """Vista que invoca la función de reproducción de voz."""
    texto = "Hola, bienvenido al asistente de voz de accesibilidad."
    
    # Llamada a la función que reproduce el audio
    reproducir_audio(texto)
    
    return HttpResponse("El mensaje de voz ha sido reproducido.")
