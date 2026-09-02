#!/usr/bin/env python3
import json
import os

class DataTransferAI:
    def __init__(self):
        self.filename = "sport_data_export.json"

    def export_data(self, user_input):
        data = {
            "status": "aktiv",
            "letzte_eingabe": user_input,
            "ziel": "Weltmarktführerschaft Platz 1"
        }
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"KI: 'Datentransfer erfolgreich. Daten wurden in {self.filename} gespeichert.'")

    def run(self):
        print("[Datentransfer-Modul] Bereit für den Export.")
        user_input = input("\nDu: ")
        self.export_data(user_input)

if __name__ == "__main__":
    ai = DataTransferAI()
    ai.run()
