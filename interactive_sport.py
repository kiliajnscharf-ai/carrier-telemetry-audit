#!/usr/bin/env python3
import json
import time

class PersistentSportAI:
    def __init__(self):
        self.name = "Sport-KI Live-Modus"
        self.filename = "sport_data_export.json"

    def save_data(self, user_input, response):
        data = {
            "timestamp": time.time(),
            "letzte_eingabe": user_input,
            "ki_antwort": response,
            "status": "aktiv"
        }
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def chat_loop(self):
        print(f"[{self.name}] Bereit mit Datentransfer. (Tippe 'exit' zum Beenden)")
        while True:
            user_input = input("\nDu: ")
            if user_input.lower() == 'exit':
                print("KI: 'Training beendet. Starker Einsatz!'")
                break
            
            # Intelligente Antwort basierend auf Eingabe
            text = user_input.lower()
            if "sport" in text or "erstes" in text or "schritt" in text or "machen" in text:
                response = "Erster Schritt: 5 Minuten leichtes Aufwärmen (auf der Stelle gehen und Arme kreisen). Danach starten wir mit 3 Sätzen Kniebeugen."
            elif "gemini" in text:
                response = "Ja, ich bin deine über die Gemini App erstellte Sport-KI, die lokal auf deinem Ubuntu-System läuft und die Daten direkt sichert."
            else:
                response = f"Empfang bestätigt. Lass uns fokussiert bleiben: {user_input}"
            
            # Datentransfer ausführen
            self.save_data(user_input, response)
            print(f"KI: '{response}' [Datentransfer: Gespeichert in {self.filename}]")

if __name__ == "__main__":
    ai = PersistentSportAI()
    ai.chat_loop()
