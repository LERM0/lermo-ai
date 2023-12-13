import torch
from TTS.api import TTS
import wave

VOICE_ENGINE = None

def init_voice_engine():
    global VOICE_ENGINE
    if not VOICE_ENGINE:
      print("Voice engine initialized")
      device = "cuda" if torch.cuda.is_available() else "cpu"
      VOICE_ENGINE = TTS("tts_models/en/vctk/vits").to(device)
      print("Voice engine loaded")

def tex_to_voice(text: str, file_path: str, speaker: str):
    if VOICE_ENGINE:
      VOICE_ENGINE.tts_to_file(text, file_path=file_path, speaker=speaker)
      print("Voice Generated")
    else:
      init_voice_engine()

def get_audio_duration(file_path):
    with wave.open(file_path, 'rb') as audio_file:
        frames = audio_file.getnframes()
        frame_rate = audio_file.getframerate()
        duration = frames / frame_rate
        return int(duration)
