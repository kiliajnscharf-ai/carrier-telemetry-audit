#!/usr/bin/env python3
import json
import time

class AutoSportAI:
    def __init__(self):
        self.filename = "sport_data_export.json"
        print("[Auto-Sport-KI] System erfolgreich selbst erstellt und initialisiert.")

    def run(self):
        print("Bereit für dein Training. (Tippe 'exit' zum Beenden)")
        while True:
            user_input = input("\nDu: ")
            if user_input.lower() == 'exit':
                print("KI: 'Training beendet.'")
                break
            
            response = f"Autonome Antwort auf: {user_input}"
            data = {"eingabe": user_input, "antwort": response}
            
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            print(f"KI: '{response}' [Datentransfer: Gespeichert]")

if __name__ == "__main__":
    ai = AutoSportAI()
    ai.run()
