#!/usr/bin/env python3
import json
import time
import sys

class BodyweightTimerAI:
    def __init__(self):
        self.filename = "infinite_matrix_memory.json"
        print("[SPORT-TIMER KERN 2100] Eigengewichts-Übungen & Timer-Modus aktiv.")

    def run_timer(self, seconds, title):
        print(f"\n--- [TIMER] {title} ({seconds} Sekunden) ---")
        for remaining in range(seconds, 0, -1):
            sys.stdout.write(f"\rRestzeit: {remaining:02d} Sekunden ... ")
            sys.stdout.flush()
            time.sleep(1)
        print("\r[TIMER ABGELAUFEN! Nächste Phase]              \n")

    def analyze(self, text):
        t = text.lower()
        if "timer" in t or "start" in t or "los" in t or "übung" in t or "sport" in t:
            print("Starte interaktiven Eigengewichts-Sport-Durchlauf:")
            
            # Übung 1
            self.run_timer(30, "Übung 1: Kniebeugen (Ohne Geräte)")
            # Pause
            self.run_timer(10, "Kurze Pause")
            
            # Übung 2
            self.run_timer(30, "Übung 2: Liegestütze (Brust & Arme)")
            # Pause
            self.run_timer(10, "Kurze Pause")
            
            # Übung 3
            self.run_timer(30, "Übung 3: Unterarmstütz / Plank (Rumpf)")
            # Pause
            self.run_timer(10, "Kurze Pause")
            
            # Übung 4
            self.run_timer(30, "Übung 4: Wandsitz (Bein-Kraftausdauer)")
            
            return "Sport-Session mit Timer erfolgreich abgeschlossen. Alle Übungen ohne Geräte absolviert."
        else:
            return f"Eingabe '{text}' erfasst. Tippe 'sport' oder 'timer', um das Eigengewichts-Workout mit Timer zu starten."

    def run(self):
        print("Sämtliche Kanäle offen (Tippe 'exit' zum Beenden):")
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []

        while True:
            try:
                user_input = input("\nKilian [Matrix-2026]: ")
            except EOFError:
                break
            
            if user_input.lower() == 'exit':
                print("KI [2100]: 'Sitzung gesichert.'")
                break
            
            response = self.analyze(user_input)
            
            entry = {
                "timestamp": time.time(),
                "input": user_input,
                "output": response,
                "status": "Sport-Timer aktiv"
            }
            history.append(entry)
            
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=4)
                
            print(f"KI [2100]: '{response}' [Datentransfer: In {self.filename} gesichert]")

if __name__ == "__main__":
    ai = BodyweightTimerAI()
    ai.run()
