from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import httpx
import asyncio
from openai import AsyncOpenAI
from bs4 import BeautifulSoup
import PyPDF2
import docx
import re
from dotenv import load_dotenv
from pydub import AudioSegment
import os
import uuid
import json
import requests

app = FastAPI()
load_dotenv()
# Configuration
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY "))

AudioSegment.converter = "/usr/local/bin/ffmpeg"  
AudioSegment.ffmpeg = "/usr/local/bin/ffprobe"    

# Voice settings for each speaker
VOICE_SETTINGS = {
    "Interviewer": "echo",
    "Expert": "alloy",
}

BASE_DIR = os.path.expanduser("~/Desktop/LearnCast/App/generated")


class PodcastRequest(BaseModel):
    source_type: str
    source: str
    analogy: str
    emphasis: str
    style: str

class PodcastStatus(BaseModel):
    id: str
    status: str
    podcast_url: str = None


podcast_statuses = {}

@app.post("/generate_podcast")
async def generate_podcast(request: PodcastRequest, background_tasks: BackgroundTasks):
    podcast_id = str(uuid.uuid4())
    podcast_statuses[podcast_id] = PodcastStatus(id=podcast_id, status="pending")
    background_tasks.add_task(generate_podcast_task, podcast_id, request)
    
    return {"podcast_id": podcast_id}

@app.get("/podcast_status/{podcast_id}")
async def podcast_status(podcast_id: str):
    status = podcast_statuses.get(podcast_id)
    if not status:
        print(f"[DEBUG] Podcast status not found for ID: {podcast_id}")
        return {"error": "Podcast not found"}
    
    return status

async def generate_podcast_task(podcast_id: str, request: PodcastRequest):
    print(f"[DEBUG] Starting podcast generation task for ID: {podcast_id}")
    try:
       
        content = await extract_content(request.source_type, request.source)
        
        
        conversation_script = await generate_conversation(content, request.analogy, request.emphasis, request.style)
       
       
        podcast_url = await create_podcast_audio(conversation_script, request.style)
      
        
        podcast_statuses[podcast_id] = PodcastStatus(id=podcast_id, status="completed", podcast_url=podcast_url)
       
    except Exception as e:
       
        podcast_statuses[podcast_id] = PodcastStatus(id=podcast_id, status="failed", podcast_url=str(e))

async def extract_content(source_type: str, source: str) -> str:
    async def clean_text(text: str) -> str:
        cleaned_text = re.sub(r'\s+', ' ', text).strip()
        paragraphs = cleaned_text.split('. ')
        cleaned_text = '\n\n'.join(p.strip() + '.' for p in paragraphs if p)
        return cleaned_text

    if source_type == "url":
        async with httpx.AsyncClient() as client:
            response = await client.get(source)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            content = ' '.join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])
    elif source_type == "pdf":
        with open(source, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            content = " ".join([page.extract_text() for page in reader.pages])
    elif source_type == "doc":
        doc = docx.Document(source)
        content = " ".join([paragraph.text for paragraph in doc.paragraphs])
    else:
        
        raise ValueError(f"Unsupported source type: {source_type}")
    
    return await clean_text(content)

async def generate_conversation(content: str, analogy: str, emphasis: str, style: str) -> str:
    print(f"[DEBUG] Generating conversation with analogy: {analogy}, style: {style} with emphasis: {emphasis}" )
    prompt = f"""
Generate a compelling, in-depth, and highly detailed {style} conversational podcast script for a 50-minute episode. The dialogue should be between a male interviewer and a female expert with 20 years of experience in the field. The expert should explain the content clearly and concisely, with a particular focus on {emphasis}.

Key Requirements:
1. Natural Flow: Ensure the conversation feels organic, engaging, and flows smoothly between the interviewer and expert.
2. Emotional Depth: Incorporate appropriate emotional reactions such as laughter, dramatic pauses, or expressions of surprise to enhance authenticity.
3. Question Quality: The interviewer should ask probing, relevant questions that drive the conversation forward.
4. Expert Responses: The expert's answers should be clear, informative, and showcase her deep knowledge and experience.
5. Analogies: Use a {analogy} analogy where appropriate to elucidate complex concepts. This analogy should particularly illuminate the emphasis on {emphasis}.
6. Make sure you expound on the {emphasis} with clear and well thought out, feasible {analogy}.
7. Pacing: Vary the pacing of the conversation. Include moments of quick back-and-forth as well as longer, more detailed explanations.
8. Audience Consideration: Periodically address the audience directly, acknowledging their presence and explaining technical terms when necessary.
9. Segmentation: Divide the content into clear segments or topics, with smooth transitions between them.
10. Ad Integration: Seamlessly and subtly incorporate an ad segment once during the script in a conversational way between the speakers, either at the end or at another suitable point for LearnCast, revolutionary new way to learn by generating instant podcasts on any topic just like this one!, its built by a seasoned and handsome AI engineer called "luwaangaar Cayleb".the interviwer should talk about Cayleb's smarts a little and expert should assert that he is very handsome. They should checkout Learncast dot co to get started.
   

Content to Cover: {content}

Format the conversation in strictly in perfect JSON format as follows, without using backticks(```Json) please:

[
    {{
        "Interviewer": "<question>"
        
    }},
    {{
        "Expert": "<answer>"
        
    }}
]

Additional Guidelines:
-Ensure you talk about all the points in the emphasis.
- Aim for approximately 6000-7000 words to fill a 50-minute episode.
- Include a brief introduction and conclusion segment.
- Pepper the conversation with relevant anecdotes or case studies from the expert's 20 years of experience.
- Ensure the interviewer occasionally summarizes key points for clarity.
- Include 2-3 moments where the expert corrects a common misconception in the field.

Begin the conversation now and return in clear perfect JSON format only.
"""

    print("[DEBUG] Sending request to OpenAI API")
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI assistant that generates engaging podcast conversations."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=15000
    )
    conversation = response.choices[0].message.content
    tokens_used = response.usage.total_tokens
    print(f"[DEBUG] Conversation generated, length: {len(conversation)} characters and {tokens_used} tokens used")
    print(conversation)
    return conversation

async def create_podcast_audio(conversation_script: str, style: str) -> str:
    print("[DEBUG] Creating podcast audio")
    try:
        conversation = json.loads(conversation_script)
        print("[DEBUG] JSON conversation script successfully parsed")
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse conversation script JSON: {e}")
        raise ValueError("Invalid JSON in conversation script")

    podcast = AudioSegment.empty()

    # Load intro and outro
    intro = AudioSegment.from_mp3("App/intro2.mp3")[:18000]  # First 15 seconds
    outro = AudioSegment.from_mp3("App/outro.mp3")[:8000]  # First 8 seconds

    # Reduce volume of intro and outro
    intro = intro - 20  # Reduce volume by 20 dB
    outro = outro - 20  # Reduce volume by 20 dB

    # Apply fade out to the last 3 seconds of the intro
    fade_duration = 3000  # 3 seconds
    intro = intro.fade_out(duration=fade_duration)

    # Load and prepare background music based on style
    bg_file = f"App/background_music/bg{2 if style == 'informative' else 4 if style == 'entertaining' else 3}.mp3"
    print(f"[DEBUG] Loading background music: {bg_file}")
    try:
        bg_music = AudioSegment.from_mp3(bg_file)
        print(f"[DEBUG] Background music loaded. Duration: {len(bg_music)/1000} seconds")
        bg_music = bg_music - 18 # Reduce volume by 20 dB for background
    except Exception as e:
        print(f"[ERROR] Failed to load background music: {e}")
        bg_music = None

    first_part = True
    for i, part in enumerate(conversation):
        speaker = list(part.keys())[0]
        text = part[speaker]
        voice_id = VOICE_SETTINGS[speaker]  # Get the voice ID for the speaker
        
        print(f"[DEBUG] Generating audio for part {i+1}, speaker: {speaker}")
        audio_file = await text_to_speech(text, voice_id)
        segment = AudioSegment.from_mp3(audio_file)
        
        if first_part:
            # For the first part, overlay the intro with the speaker's audio
            if len(segment) < len(intro):
                # If the first segment is shorter than the intro
                combined = intro.overlay(segment)
                podcast += combined
                podcast += intro[len(segment):]  # Add the remaining part of the intro
            else:
                # If the first segment is longer than or equal to the intro
                combined = segment.overlay(intro)
                podcast += combined
            first_part = False
        else:
            podcast += segment
        
        podcast += AudioSegment.silent(duration=850)
        os.remove(audio_file)
        print(f"[DEBUG] Audio generated and added for part {i+1}")
        print(f"[DEBUG] Main podcast audio created. Duration: {len(podcast)/1000} seconds")

    if bg_music:
        # Prepare background music
        podcast_duration = len(podcast) - 8000  # Podcast length minus outro
        bg_music_duration = len(bg_music)
        
        # Calculate how many times we need to loop the background music
        loops_needed = int(podcast_duration / bg_music_duration) + 1
        
        # Create looped background music
        looped_bg_music = bg_music * loops_needed
        
        # Trim the looped background music to match the podcast duration
        looped_bg_music = looped_bg_music[:podcast_duration]
        
        # Apply fade in and fade out to the background music
        looped_bg_music = looped_bg_music.fade_in(duration=fade_duration).fade_out(duration=fade_duration)
        
        
        # Overlay background music starting from the end of intro
        podcast = podcast.overlay(looped_bg_music, position=18000)
     

    # Add outro with fade in
    outro = outro.fade_in(duration=1000)  # 1 second fade in for outro
    podcast = podcast.overlay(outro, position=len(podcast) - 8000)
    
    filename = f"{uuid.uuid4()}.mp3"
    output_file = f"{BASE_DIR}/{filename}"
    
    podcast.export(output_file, format="mp3")
    return output_file

async def text_to_speech(text: str, voice_id: str) -> str:
    
    try:
        # Generate audio using OpenAI API
        response = await client.audio.speech.create(
            model="tts-1",
            voice=voice_id,
            input=text
        )
        
        # Generate a unique filename
        uuid_str = str(uuid.uuid4())
        short_uuid = uuid_str[:8]  
        filename = f"{short_uuid}.mp3"
        
        # Save the generated audio to a file
        response.stream_to_file(filename)
        
        print(f"[DEBUG] Text-to-speech audio saved to file: {filename}")
        return filename
    except Exception as e:
        print(f"[ERROR] Failed to generate speech: {str(e)}")
        raise

if __name__ == "__main__":
    print("[DEBUG] Starting FastAPI server")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
