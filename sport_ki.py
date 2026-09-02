#!/usr/bin/env python3
import random


class SportCoachAI:

    def __init__(self):
        self.exercises = [
            {
                "name": "Liegestütze",
                "sets": 3,
                "reps": "12-15",
                "desc": "Brust- und Trizepstraining.",
            },
            {
                "name": "Kniebeugen",
                "sets": 4,
                "reps": "15-20",
                "desc": "Bein- und Rumpftraining.",
            },
            {
                "name": "Plank (Unterarmstütz)",
                "sets": 3,
                "reps": "45 Sekunden",
                "desc": "Rumpfstabilität.",
            },
            {
                "name": "Burpees",
                "sets": 3,
                "reps": "10",
                "desc": "Ganzkörper-Cardio-Training.",
            },
        ]

    def generate_workout(self):
        print("--- DEIN SPORT-KI TRAININGSPROGRAMM ---")
        selected = random.sample(self.exercises, 3)
        for i, ex in enumerate(selected, 1):
            print(
                f"{i}. Übung: {ex['name']} | Sätze: {ex['sets']} | Wiederholungen: {ex['reps']}"
            )
            print(   f"   Fokus: {ex['desc']}")
        print("---------------------------------------")


if __name__ == "__main__":
    coach = SportCoachAI()
    coach.generate_workout()
