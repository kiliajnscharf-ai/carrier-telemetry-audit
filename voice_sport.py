#!/usr/bin/env python3
import time
try:
    import pyttsx3
    engine = pyttsx3.init()
    # Sprache explizit auf Deutsch setzen, um den Fehler zu umgehen
    voices = engine.getProperty('voices')
    for voice in voices:
        if "german" in voice.name.lower() or "de" in voice.id:
            engine.setProperty('voice', voice.id)
            break
except Exception as e:
    print(f"Hinweis zum Sprachmodul: {e}")
    engine = None

class VoiceSportAI:
    def __init__(self):
        self.name = "Sport-KI Live-Sprachmodus"

    def speak(self, text):
        print(f"KI sagt: {text}")
        if engine:
            try:
                engine.say(text)
                engine.runAndWait()
            except Exception:
                pass

    def run(self):
        self.speak("Hallo! Ich höre dich jetzt und bin bereit für dein Training.")
        time.sleep(1)
        self.speak("Erste Übung: Kniebeugen. Mach dich bereit.")

if __name__ == "__main__":
    ai = VoiceSportAI()
    ai.run()
