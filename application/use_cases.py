"""
@fileoverview Contiene los casos de uso o la lógica de negocio de la aplicación.
@author Danilo Castillejo (DJ111980)
@version 1.0.0
@description Orquesta los servicios del dominio para ejecutar el flujo de conversación
             del asistente J.A.R.V.I.S. Es agnóstico a la tecnología subyacente.
"""

import threading
from domain.services import IHotwordDetector, ISTTService, ITTSService, ILLMService

# Este lock previene que múltiples conversaciones se pisen entre sí, garantizando
# que solo una instancia de 'conversation_flow' esté activa a la vez.
is_conversing = threading.Lock()

def _stream_and_speak(text_generator, tts_service: ITTSService, hotword_detector: IHotwordDetector, comm_queue=None):
    """
    @private
    @function _stream_and_speak
    @description Procesa el generador de texto del LLM, acumula frases y las envía al
                 servicio de TTS. Se ejecuta en su propio hilo para no bloquear.
                 Al finalizar, se encarga de reanudar el detector de hotword y
                 liberar el lock de conversación.
    @param {Generator} text_generator - El stream de texto del LLM.
    @param {ITTSService} tts_service - La implementación del servicio de voz.
    @param {IHotwordDetector} hotword_detector - La implementación del detector.
    @param {queue.Queue} comm_queue - Cola para comunicarse con la GUI.
    """
    sentence_buffer = ""
    sentence_terminators = ['.', '?', '!', ':', '\n']

    try:
        if comm_queue: comm_queue.put({"state": "speaking"})
        
        for text_chunk in text_generator:
            sentence_buffer += text_chunk
            
            last_terminator_pos = -1
            for terminator in sentence_terminators:
                pos = sentence_buffer.rfind(terminator)
                if pos > last_terminator_pos:
                    last_terminator_pos = pos
            
            if last_terminator_pos != -1:
                sentence_to_speak = sentence_buffer[:last_terminator_pos + 1].strip()
                if sentence_to_speak:
                    tts_service.hablar(sentence_to_speak)
                sentence_buffer = sentence_buffer[last_terminator_pos + 1:]
    
    finally:
        # Habla cualquier resto que haya quedado en el buffer
        if sentence_buffer.strip():
            tts_service.hablar(sentence_buffer.strip())
        
        # Tareas de limpieza cruciales al final de la respuesta
        if comm_queue: comm_queue.put({"state": "idle"})
        hotword_detector.resume()
        is_conversing.release() # Se libera el lock aquí, al final de la operación.

def conversation_flow(hotword_detector: IHotwordDetector, stt_service: ISTTService, tts_service: ITTSService, llm_service: ILLMService, comm_queue=None):
    """
    @function conversation_flow
    @description Gestiona el flujo completo de una interacción: adquiere el lock,
                 saluda, escucha, procesa y lanza un hilo para hablar la respuesta.
    """
    if not is_conversing.acquire(blocking=False):
        return

    try:
        hotword_detector.pause()
        if comm_queue: comm_queue.put({"state": "listening"})
        tts_service.hablar("Sí, señor?")
        
        comando = stt_service.escuchar_comando()

        if comando and comando.strip():
            if comm_queue: comm_queue.put({"state": "processing"})
            prompt_completo = (
                "Eres un asistente IA llamado Jarvis. Responde de forma útil y concisa. "
                f"La pregunta del usuario es: {comando}"
            )
            
            response_generator = llm_service.stream_preguntar_a_jarvis(prompt_completo, model="mistral")
            
            # Lanzamos la función de streaming en su propio hilo.
            # Este hilo será el responsable de liberar el lock.
            speak_thread = threading.Thread(
                target=_stream_and_speak, 
                args=(response_generator, tts_service, hotword_detector, comm_queue)
            )
            speak_thread.start()
            
        else:
            tts_service.hablar("No he entendido el comando.")
            # Si no hay comando, debemos liberar el lock y reanudar nosotros mismos.
            hotword_detector.resume()
            is_conversing.release()
            
    except Exception as e:
        print(f"Error inesperado en conversation_flow: {e}")
        # En caso de error, asegurar la liberación de recursos.
        hotword_detector.resume()
        if is_conversing.locked():
             is_conversing.release()

def start_assistant(hotword_detector: IHotwordDetector, stt_service: ISTTService, tts_service: ITTSService, llm_service: ILLMService, comm_queue=None):
    """
    @function start_assistant
    @description Punto de entrada para el backend. Configura el callback de activación
                 e inicia el bucle infinito de escucha del detector de hotword.
    """
    print("Iniciando el asistente J.A.R.V.I.S...")
    
    def on_activation():
        conv_args = (hotword_detector, stt_service, tts_service, llm_service, comm_queue)
        conv_thread = threading.Thread(target=conversation_flow, args=conv_args)
        conv_thread.start()

    hotword_detector.on_hotword_callback = on_activation
    hotword_detector.start()