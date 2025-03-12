import os
import pygame
import speech_recognition as sr
from gtts import gTTS

def reproducir_audio(texto):
    """Generar y reproducir el audio del texto recibido."""
    archivo_audio = generar_mp3(texto)
    
    # Inicializar pygame para reproducir el audio
    pygame.mixer.init()
    pygame.mixer.music.load(archivo_audio)
    pygame.mixer.music.play()

    # Esperar a que termine la reproducción
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    # Cerrar pygame antes de eliminar el archivo
    pygame.mixer.quit()

    # Eliminar el archivo de audio
    if os.path.exists(archivo_audio):
        os.remove(archivo_audio)

def generar_mp3(texto):
    """Generar archivo de audio desde el texto utilizando gTTS."""
    archivo_audio = "voz_respuesta.mp3"
    
    # Generar archivo de audio usando gTTS
    tts = gTTS(text=texto, lang="es")
    tts.save(archivo_audio)
    return archivo_audio

def escuchar_usuario():
    """Escuchar el input del usuario a través del micrófono y convertirlo a texto."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Escuchando...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        texto = recognizer.recognize_google(audio, language="es-ES")
        print(f"Usuario dijo: {texto}")
        return texto
    except sr.UnknownValueError:
        print("No se entendió lo que dijiste.")
        return None
    except sr.RequestError:
        print("Error de conexión con el servicio de reconocimiento de voz.")
        return None

def procesar_comando(texto):
    """Procesar el comando del usuario y generar una respuesta."""
    if not texto:
        return "No pude entender lo que dijiste. ¿Puedes repetirlo?"
    
    # Lógica básica para generar respuestas
    if "hola" in texto.lower():
        return "¡Hola! ¿Cómo puedo ayudarte hoy?"
    elif "tu nombre" in texto.lower():
        return "Soy el asistente de voz BotRamsey."
    elif "adiós" in texto.lower():
        return "¡Hasta luego! Espero haberte ayudado."
    else:
        return "Lo siento, no tengo una respuesta para eso."

def iniciar_conversacion():
    """Iniciar la conversación con el usuario."""
    while True:
        # Escuchar al usuario
        texto_usuario = escuchar_usuario()

        # Procesar la entrada del usuario
        respuesta = procesar_comando(texto_usuario)

        # Responder al usuario en voz
        reproducir_audio(respuesta)

        # Finalizar si el usuario dice "adiós"
        if "adiós" in texto_usuario.lower():
            break

if __name__ == "__main__":
    # Iniciar la conversación
    iniciar_conversacion()
