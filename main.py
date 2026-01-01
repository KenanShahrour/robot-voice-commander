import sys
import time

sys.path.append(".")

from src.agent import MicrospotAgent
from src.voice_stream import VoiceStream

def main():
    print("==========================================")
    print("   MICROPOLIS FIELD COMMANDER (Prototype) ")
    print("   Running on Local Machine Simulation    ")
    print("==========================================")
    
    # Initialize Components
    try:
        voice = VoiceStream()
        brain = MicrospotAgent()
    except Exception as e:
        print(f"[CRITICAL ERROR] Startup failed: {e}")
        return

    # The Loop
    print("\n[SYSTEM] READY. WAITING FOR VOICE INPUT.")
    
    while True:
        try:
            # Listen
            user_text = voice.listen_once()
            
            if user_text:
                ai_response = brain.ask(user_text)
                voice.speak(ai_response)
                
                print("[SYSTEM] Audio Reset...") 
                time.sleep(1.0)
            
            else:
                print("...")

        except KeyboardInterrupt:
            print("\n[SYSTEM] SHUTTING DOWN.")
            break

if __name__ == "__main__":
    main()