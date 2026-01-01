import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import pyttsx3
import time

WHISPER_MODEL_SIZE = "base.en" 
COMPUTE_TYPE = "int8"        

class VoiceStream:
    def __init__(self):
        print("[INIT] Loading Whisper Model (Ears)...")

        self.ears = WhisperModel(WHISPER_MODEL_SIZE, device="cpu", compute_type=COMPUTE_TYPE)

    def listen_once(self):
        """
        Records audio for a fixed duration.
        """
        duration = 8 # seconds
        fs = 16000
        
        print("\n[LISTENING] Speak command now... (8s)")
        try:
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, blocking=True)
            sd.wait() 
        except Exception as e:
            print(f"[MIC ERROR] Could not record: {e}")
            return None

        print("[PROCESSING] Transcribing...")
        
        try:
            segments, _ = self.ears.transcribe(recording[:, 0], beam_size=5)
            text = " ".join([segment.text for segment in segments]).strip()
        except Exception as e:
            print(f"[WHISPER ERROR] {e}")
            return None
        
        if not text or text.strip() in ["you", "Thank you.", ""]: 
            return None
            
        print(f"[USER VOICE]: {text}")
        return text

    def speak(self, text):
        """
        Creates a FRESH TTS engine instance for every sentence.
        This prevents the 'Zombie Audio' bug where the driver locks up.
        """
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 160)
            voices = engine.getProperty('voices')
            try:
                engine.setProperty('voice', voices[1].id) 
            except:
                engine.setProperty('voice', voices[0].id) 
            engine.say(text)
            engine.runAndWait()
            del engine
            
        except Exception as e:
            print(f"[AUDIO ERROR] TTS Failed: {e}")