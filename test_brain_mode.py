from hiw_autistic_brain_mode import autistic_brain_mode

test_input = "Dies ist ein Testtext zur Validierung des Systems im Projekt Haus im Wind."
test_context = {
    "tasks": ["Task A", "Task B", "Task A"],
    "topics": ["Thema 1", "Thema 2"]
}

result = autistic_brain_mode(test_input, test_context)
print("SYSTEM-START ERFOLGREICH:")
print(result)
