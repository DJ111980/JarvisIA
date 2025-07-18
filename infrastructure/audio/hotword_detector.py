"""
@fileoverview Implementación concreta del detector de palabra clave usando VOSK.
@author Danilo Castillejo (DJ111980)
@version 1.0.0
@description Esta clase implementa la interfaz IHotwordDetector, utilizando la
             librería VOSK para una detección 100% local y offline.
"""

from domain.services import IHotwordDetector
import vosk
import sounddevice as sd
import queue
import threading

class VoskHotwordDetector(IHotwordDetector):
    """
    @class VoskHotwordDetector
    @description Implementa IHotwordDetector usando el motor de VOSK.
    """
    def __init__(self, on_hotword_callback=None, keyword="jarvis"):
        print("Inicializando VoskHotwordDetector...")
        self.on_hotword_callback = on_hotword_callback
        self.keyword = keyword.lower()

        try:
            self.model = vosk.Model("models/vosk/vosk-model-small-es-0.42")
        except Exception as e:
            raise RuntimeError(f"Error cargando modelo VOSK para hotword: {e}")

        self.device_info = sd.query_devices(kind='input')
        self.samplerate = int(self.device_info['default_samplerate'])
        self.q = queue.Queue()
        self._is_paused = threading.Event()
        self._is_paused.set()
        self._stop_event = threading.Event()

    def _audio_callback(self, indata, frames, time, status):
        """Callback privado para manejar los datos del stream de audio."""
        if status:
            print(f"Status del stream (hotword): {status}")
        self.q.put(bytes(indata))

    def start(self):
        print(f"👂 Escuchando pasivamente por la palabra clave '{self.keyword}'...")
        try:
            with sd.RawInputStream(samplerate=self.samplerate, blocksize=8000,
                                   device=None, dtype='int16', channels=1,
                                   callback=self._audio_callback):
                recognizer = vosk.KaldiRecognizer(self.model, self.samplerate, f'["{self.keyword}", "[unk]"]')
                while not self._stop_event.is_set():
                    self._is_paused.wait()
                    data = self.q.get()
                    if recognizer.AcceptWaveform(data):
                        result = recognizer.Result()
                        if f'"{self.keyword}"' in result:
                            print(f"✅ ¡Palabra clave '{self.keyword}' detectada!")
                            if self.on_hotword_callback:
                                self.on_hotword_callback()
        except Exception as e:
            print(f"Error en el bucle de detección de hotword: {e}")

    def pause(self):
        print("⏸️  Detector de palabra clave pausado.")
        self._is_paused.clear()

    def resume(self):
        print("▶️  Detector de palabra clave reanudado.")
        self._is_paused.set()

    def stop(self):
        print("Deteniendo detector de palabra clave...")
        self._stop_event.set()