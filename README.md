# Switchable LLM App con Gradio

## Objetivo

Esta aplicación permite probar y comparar diferentes modelos de lenguaje (LLMs) a través de una interfaz interactiva creada con Gradio.
El usuario puede seleccionar el proveedor (Groq, OpenRouter, Gemini u Ollama), elegir un modelo disponible, y realizar distintas tareas de procesamiento de texto como traducción, resumen y análisis de sentimiento.

Además, la app soporta la carga de archivos .txt, lo que permite procesar textos en batch, y muestra métricas rápidas de rendimiento.

## Funcionalidades

- Soporte para 4 proveedores: Ollama (local), OpenRouter, Gemini y Groq.

- Selector de tareas: Traducción EN→ES, Resumen, Análisis de sentimiento.

- Carga de archivos .txt: Permite subir archivos para procesarlos directamente.

- Métricas de inferencia: tiempo de respuesta, longitud de entrada y salida.

- Cambio dinámico de modelos: según el proveedor seleccionado.

- Manejo de errores: texto vacío, modelo no disponible o errores de conexión.

- Ejecutable en entorno local (o remoto sin ollama), incluyendo integración con Ollama.


## Requisitos

Google Collab (Entorno remoto sin ollama), Jupyter Notebook o VS Code, Python 3.10 o superior

Ollama
 instalado y con al menos un modelo cargado (por ejemplo, ollama pull llama3)

Claves API configuradas para los proveedores externos (OpenRouter, Gemini, Groq)

## Variables de Entorno
Crea un archivo .env en la raíz del proyecto con tus claves API:
OPENROUTER_API_KEY=tu_clave
GEMINI_API_KEY=tu_clave
GROQ_API_KEY=tu_clave

## Ejecución
pip install -r requirements.txt
python app.py

## Ejemplos de uso

# Entrada (análisis de sentimiento)
I woke up this morning feeling completely empty. The house was silent, and even the sunlight coming through the window felt cold.

# Resultado
Negativo: El texto expresa tristeza y melancolía.

## Modelos disponibles

| Proveedor      | Modelos disponibles (ejemplo)                       | Tipo        |
| -------------- | --------------------------------------------------- | ----------- |
| **Ollama**     | llama3, mistral, phi3                               | Local       |
| **OpenRouter** | anthropic/claude-sonnet-4.5, mistralai/mixtral-8x7b | API Externa |
| **Gemini**     | gemini-2.5-flash, gemini-2.5-pro                    | API Externa |
| **Groq**       | llama-3.3-70b-versatile, mixtral-8x7b               | API Externa |

## Reflexión técnica
Durante el desarrollo de esta aplicación, se exploró la integración de múltiples proveedores de LLMs dentro de una misma interfaz.
La extensión para análisis de sentimiento y procesamiento de archivos .txt demostró la escalabilidad del diseño, y permitió comparar tiempos y comportamiento entre modelos locales (Ollama) y en la nube.

Los principales retos fueron la gestión de errores entre distintos endpoints y la consistencia en los formatos de respuesta.
Como mejora futura, podría añadirse el conteo real de tokens, costos estimados por proveedor y soporte para nuevas tareas como clasificación o análisis de imágenes.