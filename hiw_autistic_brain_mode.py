from typing import Dict, Any

def autistic_brain_mode(input_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
    filtered_text = input_text.strip()
    ueberfordert = False
    if len(input_text) > 500 or len(context.get("topics", [])) > 3:
        ueberfordert = True
    focused_context = {
        "tasks": context.get("tasks", [])[:3],
        "topics": context.get("topics", [])[:2]
    }
    safe_tasks = list(dict.fromkeys(focused_context["tasks"]))
    safe_topics = list(dict.fromkeys(focused_context["topics"]))
    safe_context = {
        "tasks": safe_tasks,
        "topics": safe_topics
    }
    final_text = filtered_text
    return {
        "ueberfordert": ueberfordert,
        "context": safe_context,
        "response": final_text
    }

def autistic_brain_mode_action(input_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
    return autistic_brain_mode(input_text, context)

def register_safe_action(name, func):
    pass
