"""
@fileoverview Implementación concreta del servicio de Voz a Texto usando VOSK.
@author Danilo Castillejo (DJ111980)
@version 1.0.0
@description Implementa la interfaz ISTTService para transcribir comandos de voz.
"""

from domain.services import ISTTService
import vosk
import sounddevice as sd
import json
import queue

class VoskSTTService(ISTTService):
    """
    @class VoskSTTService
    @description Implementa ISTTService usando el motor de VOSK.
    """
    def __init__(self):
        print("Inicializando VoskSTTService...")
        try:
            self.model = vosk.Model("models/vosk/vosk-model-small-es-0.42")
        except Exception as e:
            print(f"Error fatal al cargar el modelo VOSK (STT): {e}")
            self.model = None

    def escuchar_comando(self) -> str | None:
        if not self.model:
            return None

        q = queue.Queue()

        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Status del stream (STT): {status}")
            q.put(bytes(indata))

        print("🎙️  Escuchando tu comando...")
        try:
            device_info = sd.query_devices(kind='input')
            samplerate = int(device_info['default_samplerate'])
            
            with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=None,
                                   dtype='int16', channels=1, callback=audio_callback):
                recognizer = vosk.KaldiRecognizer(self.model, samplerate)
                while True:
                    data = q.get()
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        if result.get("text"):
                            comando = result["text"]
                            print(f"Texto reconocido: '{comando}'")
                            return comando
        except Exception as e:
            print(f"Error durante la escucha del comando: {e}")
            return None
