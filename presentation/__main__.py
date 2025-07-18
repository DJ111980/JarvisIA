"""
@fileoverview Punto de entrada principal de la aplicación J.A.R.V.I.S.
@author Danilo Castillejo (DJ111980)
@version 1.0.0
@description Este script realiza el "ensamblaje" de la aplicación siguiendo el
             principio de Inyección de Dependencias. Crea las instancias de los
             servicios concretos y las pasa a los casos de uso, desacoplando
             las capas del sistema.
"""

import sys
import os
import threading
import queue
from PyQt5.QtWidgets import QApplication

# --- Añadir la raíz del proyecto al path para que Python encuentre los módulos ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- Ensamblaje de la Aplicación (Dependency Injection) ---
# 1. Importar las IMPLEMENTACIONES CONCRETAS desde infrastructure
from infrastructure.audio.hotword_detector import VoskHotwordDetector
from infrastructure.audio.stt_service import VoskSTTService
from infrastructure.audio.tts_service import Pyttsx3TTSService
from infrastructure.llm.llm_service import OllamaLLMService

# 2. Importar el CASO DE USO desde application
from application.use_cases import start_assistant

# 3. Importar la GUI desde presentation
from presentation.mascot_gui import MascotWindow

def main():
    """
    @function main
    @description Función principal que ensambla e inicia la aplicación J.A.R.V.I.S.
    """
    print("Ensamblando la aplicación J.A.R.V.I.S...")
    
    # --- Creación de Dependencias (Instancias de los servicios) ---
    stt_service = VoskSTTService()
    tts_service = Pyttsx3TTSService()
    llm_service = OllamaLLMService()
    hotword_detector = VoskHotwordDetector() # El callback se asignará dentro de start_assistant
    
    comm_queue = queue.Queue()

    # --- Inyección de Dependencias y Arranque de Hilos ---
    backend_args = (hotword_detector, stt_service, tts_service, llm_service, comm_queue)
    
    backend_thread = threading.Thread(
        target=start_assistant, 
        args=backend_args, 
        daemon=True
    )
    
    print("Iniciando el backend de Jarvis en un hilo secundario...")
    backend_thread.start()

    print("Iniciando la interfaz gráfica de Jarvis en el hilo principal...")
    app = QApplication(sys.argv)
    mascot = MascotWindow(comm_queue=comm_queue)
    mascot.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()