"""
@fileoverview Implementación concreta del servicio de Texto a Voz usando pyttsx3.
@author Danilo Castillejo (DJ111980)
@version 1.0.0
@description Implementa la interfaz ITTSService, proporcionando una voz robótica
             pero funcional y 100% offline para el asistente.
"""

from domain.services import ITTSService
import pyttsx3
import threading

class Pyttsx3TTSService(ITTSService):
    """
    @class Pyttsx3TTSService
    @description Implementa ITTSService usando la librería pyttsx3.
                 Está diseñado para ser thread-safe creando una nueva instancia
                 del motor en cada llamada a 'hablar'.
    """
    def __init__(self):
        print("Inicializando Pyttsx3TTSService...")
        self.tts_lock = threading.Lock()
        self.spanish_voice_id = None
        self._find_voice()

    def _find_voice(self):
        """Método privado para encontrar y almacenar el ID de una voz en español."""
        try:
            temp_engine = pyttsx3.init()
            voices = temp_engine.getProperty('voices')
            spanish_voice_names = ["helena", "sabina", "spanish"]
            for voice in voices:
                for name in spanish_voice_names:
                    if name in voice.name.lower():
                        self.spanish_voice_id = voice.id
                        break
                if self.spanish_voice_id:
                    break
            temp_engine.stop()
            del temp_engine
            if self.spanish_voice_id:
                print(f"Voz en español encontrada: {self.spanish_voice_id}")
        except Exception as e:
            print(f"ERROR: No se pudo buscar voces de pyttsx3: {e}")

    def hablar(self, texto: str):
        with self.tts_lock:
            try:
                print(f"Jarvis (pyttsx3) dice: {texto}")
                engine = pyttsx3.init()
                if self.spanish_voice_id:
                    engine.setProperty('voice', self.spanish_voice_id)
                engine.setProperty('rate', 165)
                engine.setProperty('volume', 0.9)
                engine.say(texto)
                engine.runAndWait()
                engine.stop()
            except Exception as e:
                print(f"Error en el motor pyttsx3: {e}")