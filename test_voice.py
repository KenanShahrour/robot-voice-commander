import pyttsx3

try:
    print("Initializing engine...")
    engine = pyttsx3.init()
    
    # Set properties (optional)
    engine.setProperty('rate', 150)
    
    print("Speaking...")
    engine.say("System check. Audio interface online.")
    engine.runAndWait()
    print("Done.")

except Exception as e:
    print(f"CRITICAL AUDIO ERROR: {e}")