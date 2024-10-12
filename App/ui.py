import gradio as gr
import requests
import time

# FastAPI backend URL
API_URL = "http://localhost:8000"

def generate_podcast(source_type, source, analogy, emphasis, style):
    # Send request to generate podcast
    response = requests.post(f"{API_URL}/generate_podcast", json={
        "source_type": source_type,
        "source": source,
        "analogy": analogy,
        "emphasis": emphasis,
        "style": style
    })
    podcast_id = response.json()["podcast_id"]
    
    # Poll for podcast status
    while True:
        status_response = requests.get(f"{API_URL}/podcast_status/{podcast_id}")
        status = status_response.json()
        
        if status["status"] == "completed":
            return status["podcast_url"]
        elif status["status"] == "failed":
            return f"Podcast generation failed: {status['podcast_url']}"
        
        time.sleep(30)  # Wait for 30 seconds before polling again

def podcast_interface(source_type, source, analogy, emphasis, style):
    podcast_url = generate_podcast(source_type, source, analogy, emphasis, style)
    return podcast_url

# Create Gradio interface
iface = gr.Interface(
    fn=podcast_interface,
    inputs=[
        gr.Dropdown(["url", "pdf", "doc"], label="Source Type"),
        gr.Textbox(label="Source (URL or file path)"),
        gr.Textbox(label="Analogy"),
        gr.Textbox(label="Emphasis"),
        gr.Textbox(label="Style"),
    ],
    outputs=gr.Audio(label="Generated Podcast", type="filepath"),
    title="AI Podcast Generator",
    description="Generate engaging podcasts from various sources using AI!",
    theme="huggingface",
)

# Launch the interface
iface.launch()