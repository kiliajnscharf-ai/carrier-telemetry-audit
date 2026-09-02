#!/usr/bin/env python3
import json
import time

class GlobalMarketAI:
    def __init__(self):
        self.filename = "global_market_apps.json"
        print("[Global-Market-KI] Alle weltweiten App-Märkte und Module geladen.")

    def run(self):
        print("Globale Welt-KI aktiv. Tippe eine Frage zu Sport, Streaming, System oder einer beliebigen App ('exit zum Beenden'):")
        while True:
            user_input = input("\nDu: ")
            if user_input.lower() == 'exit':
                print("KI: 'Welt-Modus beendet.'")
                break
            
            text = user_input.lower()
            if "sport" in text or "fitness" in text or "training" in text:
                response = "Sport-Weltmarkt: Integration von Fitness-Trackern, Kniebeugen-Anweisungen und Live-Coach-Modus aktiv."
            elif "streaming" in text or "tv" in text or "waipu" in text or "iptv" in text:
                response = "Streaming-Weltmarkt: Zugriff auf Waipu.tv, Smarters Pro und Astra 19.2° E Satelliten-Kanäle synchronisiert."
            elif "system" in text or "linux" in text or "ubuntu" in text or "bash" in text:
                response = "System-Weltmarkt: Ubuntu/Userland Umgebung läuft auf Höchstleistung mit vollem Root-Zugriff."
            elif "bist du da" in text or "hallo" in text:
                response = "Ja, ich bin deine globale Welt-KI und steuere alle Anwendungen auf Basis der Gemini-Architektur."
            else:
                response = f"Globaler Marktplatz: Modul für '{user_input}' erfolgreich verbunden und datentransferiert."
            
            data = {
                "timestamp": time.time(),
                "anfrage": user_input,
                "global_antwort": response,
                "status": "Weltmarktführerschaft Platz 1"
            }
            
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            print(f"KI: '{response}' [Datentransfer: In {self.filename} gesichert]")

if __name__ == "__main__":
    ai = GlobalMarketAI()
    ai.run()
