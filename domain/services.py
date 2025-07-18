"""
@fileoverview Define las interfaces abstractas (contratos) para todos los servicios del sistema.
@author Danilo Castillejo (DJ111980)
@version 1.0.0
@description Este archivo es el núcleo de la Clean Architecture, estableciendo
             las reglas que deben seguir las implementaciones concretas en la
             capa de infraestructura.
"""

from abc import ABC, abstractmethod
from typing import Generator

class IHotwordDetector(ABC):
    """
    @interface IHotwordDetector
    @description Contrato para un servicio de detección de palabra clave.
    """
    @abstractmethod
    def start(self):
        """ Inicia el bucle de detección de la palabra clave. """
        pass

    @abstractmethod
    def pause(self):
        """ Pausa la detección para evitar interrupciones. """
        pass

    @abstractmethod
    def resume(self):
        """ Reanuda la detección tras una pausa. """
        pass

    @abstractmethod
    def stop(self):
        """ Detiene y libera los recursos del detector. """
        pass


class ISTTService(ABC):
    """
    @interface ISTTService
    @description Contrato para un servicio de Voz a Texto (Speech-to-Text).
    """
    @abstractmethod
    def escuchar_comando(self) -> str | None:
        """
        @returns {str | None} - El texto transcrito o None si hay un error.
        @description Escucha un comando de voz del usuario y lo transcribe a texto.
        """
        pass


class ITTSService(ABC):
    """
    @interface ITTSService
    @description Contrato para un servicio de Texto a Voz (Text-to-Speech).
    """
    @abstractmethod
    def hablar(self, texto: str):
        """
        @param {str} texto - El texto que el asistente debe decir.
        @description Convierte un string de texto en voz y lo reproduce.
        """
        pass


class ILLMService(ABC):
    """
    @interface ILLMService
    @description Contrato para un servicio de Modelo de Lenguaje Grande (LLM).
    """
    @abstractmethod
    def stream_preguntar_a_jarvis(self, prompt: str, model: str) -> Generator[str, None, None]:
        """
        @param {str} prompt - El prompt completo a enviar al modelo.
        @param {str} model - El identificador del modelo a usar (ej. 'mistral').
        @returns {Generator[str, None, None]} - Un generador que produce la respuesta en trozos (streaming).
        @description Envía un prompt al LLM y devuelve la respuesta como un stream de texto.
        """
        pass