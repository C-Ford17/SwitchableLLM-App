# ===============================================
# Switchable LLM App con Gradio
# ===============================================
import time
import gradio as gr
from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv(override=True)
open_router_api_key = os.getenv('OPEN_ROUTER_API_KEY')
gemini_api_key = os.getenv('GEMINI_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')

# --- Configura tus claves (pon tus tokens aquí) ---
OPENROUTER_API_KEY = open_router_api_key
GEMINI_API_KEY = gemini_api_key
GROQ_API_KEY = groq_api_key

# --- Configuración de proveedores ---
providers = {
    "Ollama": {
        "client": OpenAI(base_url="http://localhost:11434/v1", api_key="ollama"),
        "models": ["llama3"]
    },
    "OpenRouter": {
        "client": OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY),
        "models": ["anthropic/claude-sonnet-4.5", "mistralai/mixtral-8x7b"]
    },
    "Gemini": {
        "client": OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=GEMINI_API_KEY),
        "models": ["gemini-2.5-flash", "gemini-2.5-pro"]
    },
    "Groq": {
        "client": OpenAI(base_url="https://api.groq.com/openai/v1", api_key=GROQ_API_KEY),
        "models": ["llama-3.3-70b-versatile", "mixtral-8x7b"]
    },
}

# --- Función principal ---
def process_text(provider, task, model, input_text,archivo):
    if archivo is not None:
        try:
            with open(archivo.name, "r", encoding="utf-8") as f:
                input_text = f.read()
        except Exception as e:
            return f"❌ Error leyendo el archivo: {e}", None, None, None
    
    if not input_text.strip():
        return "⚠️ Ingresa un texto para procesar.", None, None, None

    client = providers[provider]["client"]

    prompt = ""
    # Prompt según tarea
    if task == "Traducción EN→ES":
        prompt = f"Traduce el siguiente texto del inglés al español:\n\n{input_text}"
    elif task == "Resumen":
        prompt = f"Resume el siguiente texto de manera breve y clara:\n\n{input_text}"
    elif task == "Análisis de sentimiento":
        prompt = (
            f"Analiza el sentimiento del siguiente texto. "
            f"Responde si es positivo, negativo o neutral, y explica brevemente:\n\n{input_text}"
        )
    else:
        return "❌ Tarea no reconocida.", None, None, None

    try:
        start_time = time.time()

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        output_text = response.choices[0].message.content.strip()
        elapsed = round(time.time() - start_time, 2)

        return (
            output_text,
            f"{elapsed} s",
            len(input_text.split()),
            len(output_text.split())
        )

    except Exception as e:
        return f"❌ Error: {str(e)}", None, None, None


# --- Interfaz Gradio ---
with gr.Blocks(title="Switchable LLM App") as demo:
    gr.Markdown("# 🤖 Switchable LLM App con Gradio")
    gr.Markdown("Selecciona el **proveedor**, el **modelo** y la **tarea** que deseas ejecutar.")

    with gr.Row():
        provider = gr.Dropdown(label="Proveedor", choices=list(providers.keys()), value="Ollama")
        task = gr.Dropdown(
            label="Tarea",
            choices=["Traducción EN→ES", "Resumen", "Análisis de sentimiento"],
            value="Traducción EN→ES"
        )


    model = gr.Dropdown(label="Modelo", choices=providers["Ollama"]["models"], value="llama3")

    # Actualiza modelos según el proveedor seleccionado
    def update_models(selected_provider):
        return gr.update(choices=providers[selected_provider]["models"], value=providers[selected_provider]["models"][0])

    provider.change(update_models, inputs=provider, outputs=model)

    input_text = gr.Textbox(lines=8, label="Texto de entrada")
    archivo_input = gr.File(label="Sube un archivo .txt (opcional)", file_types=[".txt"])
    output_text = gr.Textbox(lines=8, label="Resultado", interactive=False)

    with gr.Row():
        time_box = gr.Textbox(label="⏱️ Tiempo de inferencia", interactive=False)
        in_len = gr.Textbox(label="🔤 Palabras input", interactive=False)
        out_len = gr.Textbox(label="💬 Palabras output", interactive=False)

    run_button = gr.Button("🚀 Procesar")

    run_button.click(
        fn=process_text,
        inputs=[provider, task, model, input_text, archivo_input],
        outputs=[output_text, time_box, in_len, out_len]
    )

demo.launch()
