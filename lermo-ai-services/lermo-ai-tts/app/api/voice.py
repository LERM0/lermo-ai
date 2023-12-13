import uvicorn
from contextlib import asynccontextmanager
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
from fastapi import APIRouter, HTTPException, Path, Request
from app import engine, db
import json

router = APIRouter()

@router.post("/voice")
async def voice(request: Request):
    # Params 1: voice male/female
    # Params 2: text

    # Ex
    # Create, voice1, male, hello world.
    # Params
    params = await request.json()
    prompt = params.get("prompt")
    text = params.get("text")
    # Split prompt to array
    # [Create, voice1, male, hello world]
    # Array 0: Create, Update
    # Array 1: File Path
    # Array 2: Voice Category
    # Array 3: TTS

    prompt_array = prompt.split(", ")[:3] 
    action = prompt_array[0]
    voice_name = prompt_array[1]
    voice_category = prompt_array[2]

    if voice_category == "male":
        speaker = "p230"
    elif voice_category == "female":
        speaker = "p240"
    else:
        speaker = "p240"
        print("Default Voice")

    file_path = "app/" + voice_name + ".wav"
    # text = params.get("text")
    # path = params.get("path")
    # speaker = params.get("speaker")
    engine.tex_to_voice(text=text, file_path=file_path, speaker=speaker)

    duration = engine.get_audio_duration(file_path)
    print(f"The duration of the audio file is: {duration} seconds")
    # Connect to redis 
    # set to redis
    # how to get voice duration from file 
    # voice.wav using python

    voiceJson = {
        "voice_path": file_path,
        "voice_duration": duration
    }

    db.set(voice_name, json.dumps(voiceJson))
    print(db.get(voice_name))
    return params