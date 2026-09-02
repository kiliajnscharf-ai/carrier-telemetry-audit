from typing import Dict, Any

def hiw_new_module(input_data: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(input_data, dict):
        return {"status": "error", "reason": "invalid_input_type"}
    
    processed_tasks = input_data.get("tasks", [])
    clean_tasks = list(dict.fromkeys(processed_tasks))

    return {
        "status": "ok",
        "processed": True,
        "details": {
            "task_count": len(clean_tasks),
            "tasks": clean_tasks
        }
    }

def hiw_new_module_action(input_data: Dict[str, Any]) -> Dict[str, Any]:
    return hiw_new_module(input_data)

def register_safe_action(name, func):
    pass

register_safe_action(
    "hiw_new_module",
    lambda input_data, **kwargs: hiw_new_module_action(input_data)
)
