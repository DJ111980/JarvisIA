# J.A.R.V.I.S. IA Local - Asistente Conversacional

Asistente de Inteligencia Artificial personal inspirado en J.A.R.V.I.S., diseñado desde cero para funcionar de manera **100% local y privada**. Este proyecto combina el poder de los modelos de lenguaje avanzados con una arquitectura de software profesional para crear una base sólida para un asistente de escritorio verdaderamente inteligente.

---

### 🎯 Visión y Objetivo del Proyecto

El objetivo fundamental de este proyecto es construir un asistente personal que vaya más allá de los servicios en la nube, poniendo el control, la privacidad y la personalización en manos del usuario. Se busca crear un sistema que no solo responda preguntas, sino que esté preparado para convertirse en una parte integral del entorno de escritorio del usuario.

La base del proyecto se cimienta en una filosofía de **Clean Architecture**, una metodología de diseño de software que garantiza un sistema:
-   **Modular:** Cada componente (voz, IA, interfaz) es independiente y puede ser reemplazado o actualizado sin afectar al resto del sistema.
-   **Escalable:** La estructura está diseñada para crecer, permitiendo la futura integración de nuevas capacidades como visión artificial, control de IoT o herramientas de automatización.
-   **Testeable:** La lógica de negocio (los "casos de uso") puede ser probada de forma aislada, asegurando la robustez y fiabilidad del código.

---

### ✨ Características de la Versión Inicial (v0.1.0-beta)

Esta primera versión establece el núcleo funcional completo del asistente, demostrando el ciclo de interacción de principio a fin.

-   ✅ **Operación 100% Local y Offline:** Desde el reconocimiento de voz hasta la generación de respuestas, ningún dato sale de tu ordenador. Esto garantiza una privacidad absoluta y un funcionamiento ininterrumpido incluso sin conexión a internet.

-   🎤 **Activación por Palabra Clave ("Hotword"):** El asistente permanece en un estado de escucha pasiva de bajo consumo. Al detectar la palabra clave **"Jarvis"**, se activa instantáneamente, listo para recibir comandos.

-   🧠 **Cerebro de IA Avanzado:** Integración con el modelo de lenguaje **Mistral 7B** a través de Ollama. Esto le otorga una profunda capacidad de comprensión del lenguaje natural, permitiéndole entender preguntas complejas y generar respuestas coherentes y detalladas.

-   💨 **Respuesta en Streaming:** Para una experiencia de usuario fluida, el asistente no espera a tener la respuesta completa para empezar a hablar. Comienza a verbalizar la respuesta tan pronto como la IA genera las primeras palabras, creando una interacción mucho más natural y dinámica.

-   🎨 **Mascota Virtual Animada:** La interacción no es solo auditiva. Una interfaz gráfica (GUI) inspirada en un HUD holográfico, construida con PyQt5, sirve como la manifestación visual de Jarvis. Esta mascota animada cambia su apariencia en tiempo real para reflejar el estado del asistente:
    -   **Inactivo:** Animación sutil y en reposo.
    -   **Escuchando:** Efecto de pulso que indica la captura de audio.
    -   **Procesando:** Animación de "pensamiento" o carga.
    -   **Hablando:** Animación dinámica de ondas que acompaña a la voz.

-   ⚙️ **Gestión de Hilos y Concurrencia:** El sistema está diseñado para ser completamente concurrente, utilizando múltiples hilos para manejar la escucha pasiva, la conversación activa y la interfaz gráfica de forma simultánea sin bloqueos, asegurando que el asistente esté siempre receptivo.

---

### 🧱 Pila Tecnológica (Tech Stack)

| Componente                | Herramienta / Librería                                  | Propósito                                       |
| ------------------------- | ------------------------------------------------------- | ----------------------------------------------- |
| Lenguaje Principal        | Python 3.10+                                            | La base de todo el proyecto.                    |
| IA Local (LLM)            | **Ollama (con Mistral 7B)**                             | Comprensión y generación de lenguaje natural.   |
| Voz a Texto (STT)         | `vosk`                                                  | Transcripción de voz a texto 100% offline.      |
| Texto a Voz (TTS)         | `pyttsx3`                                               | Síntesis de voz funcional y offline.            |
| Mascota Virtual (GUI)     | `PyQt5`                                                 | Creación de la interfaz gráfica y animaciones.  |
| Arquitectura              | Clean Architecture                                      | Separación de responsabilidades y mantenibilidad. |

---

### 🚀 Guía de Instalación y Puesta en Marcha

Sigue estos pasos para dar vida a tu propia instancia de J.A.R.V.I.S.

#### 1. Prerrequisitos

-   **Python 3.10 o superior.**
-   **Git** para clonar el repositorio.
-   **Hardware:** Se recomienda encarecidamente una GPU NVIDIA con al menos 4-6 GB de VRAM para un rendimiento óptimo del modelo Mistral 7B.

#### 2. Instalación

```bash
# 1. Clona este repositorio en tu máquina local
git clone https://github.com/DJ111980/JarvisIA.git
cd JarvisIA

# 2. Crea y activa un entorno virtual para aislar las dependencias
python -m venv env

# En Windows:
env\Scripts\activate

# En Linux/macOS:
# source env/bin/activate

# 3. Instala todas las librerías necesarias
pip install -r requirements.txt
```

#### 3. Configuración de Modelos

-   **Instala Ollama:** Descárgalo desde [ollama.com](https://ollama.com) y sigue las instrucciones de instalación para tu sistema operativo.
-   **Descarga el LLM (Mistral 7B):** Abre una terminal y ejecuta el siguiente comando. Ten paciencia, la descarga puede tardar un rato.
    ```bash
    ollama pull mistral
    ```
-   **Descarga el Modelo de Voz (VOSK):**
    1.  Visita la [página de modelos de VOSK](https://alphacephei.com/vosk/models).
    2.  Descarga un modelo para español. Para la mejor precisión, se recomienda el modelo grande (`vosk-model-es-0.42`).
    3.  Descomprime el archivo `.zip` y coloca la carpeta resultante (`vosk-model-es-0.42`) dentro de la carpeta `models/vosk/` de este proyecto.

---

### ▶️ Cómo Ejecutar a J.A.R.V.I.S.

1.  **Inicia el servidor de Ollama:** En una terminal, carga el modelo en memoria para que esté listo para recibir peticiones.
    ```bash
    ollama run mistral
    ```
    *Deja esta terminal abierta. Es el "cerebro" de Jarvis.*

2.  **Inicia el Asistente J.A.R.V.I.S.:** En una segunda terminal, navega a la raíz del proyecto y, con el entorno virtual activado, ejecuta el módulo de presentación.
    ```bash
    python -m presentation
    ```

La mascota virtual aparecerá en tu escritorio y el sistema estará en modo de escucha. ¡Simplemente di "Jarvis" para comenzar a interactuar!

---

### ✍️ Autor

-   **Danilo Castillejo** - Perfil en GitHub: [DJ111980](https://github.com/DJ111980)