"""
@fileoverview Implementación concreta del servicio de LLM usando Ollama.
@author Danilo Castillejo (DJ111980)
@version 1.0.0
@description Se conecta a una instancia local de Ollama para generar respuestas
             de texto en modo streaming, implementando la interfaz ILLMService.
"""

from domain.services import ILLMService
import requests
import json
from typing import Generator

class OllamaLLMService(ILLMService):
    """
    @class OllamaLLMService
    @description Implementa ILLMService para interactuar con un servidor Ollama.
    """
    def __init__(self, url="http://localhost:11434/api/generate"):
        print("Inicializando OllamaLLMService...")
        self.url = url

    def stream_preguntar_a_jarvis(self, prompt: str, model: str = "mistral") -> Generator[str, None, None]:
        try:
            payload = {"model": model, "prompt": prompt, "stream": True}
            with requests.post(self.url, json=payload, stream=True) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line.decode('utf-8'))
                        yield chunk.get("response", "")
                        if chunk.get("done"):
                            break
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión con Ollama: {e}")
            yield "Lo siento, no puedo conectarme con mi cerebro."
        except Exception as e:
            print(f"Error inesperado en el servicio LLM: {e}")
            yield "Ha ocurrido un error inesperado."