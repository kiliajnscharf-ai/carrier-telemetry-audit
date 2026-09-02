#!/usr/bin/env python3
import subprocess
import time


class AllInOneCoach:

    def __init__(self, name):
        self.name = name

    def get_fitness_routine(self):
        return "Tages-Routine: 20 Minuten HIIT-Training und 30 Minuten leichtes Joggen."

    def get_coding_tip(self):
        return "Linux-Tipp: Nutze `htop`, um die Server-Performance in Echtzeit zu überwachen."

    def get_recipe_idea(self):
        return "Kulinarik-Tipp von Sebastian Lege: Probiere eine schnelle Bowl mit frischem Gemüse und hochwertigem Protein."

    def get_language_practice(self):
        return "Python-Lektion: Der heutige Fokus liegt auf Schleifen und Listen-Kompetenzen."

    def get_ubuntu_updates(self):
        try:
            result = subprocess.run(
                ["apt", "list", "--upgradable"],
                capture_output=True,
                text=True,
                check=True,
            )
            count = max(0, len(result.stdout.strip().split("\n")) - 1)
            return f"Ubuntu-System: {count} Updates verfügbar."
        except Exception:
            return "Ubuntu-System: Update-Prüfung erfordert Administratorrechte."

    def run_daily_briefing(self):
        print(f"--- Tages-Briefing von {self.name} ---")
        print(self.get_fitness_routine())
        print(self.get_coding_tip())
        print(self.get_recipe_idea())
        print(self.get_language_practice())
        print(self.get_ubuntu_updates())
        print("--- Ende des Briefings ---")


if __name__ == "__main__":
    ai_coach = AllInOneCoach("All-in-One KI")
    ai_coach.run_daily_briefing()
