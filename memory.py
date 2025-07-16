import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def get_learned_topics():
    memory = load_memory()
    return [entry["title"] for entry in memory]

def update_memory(title, feedback):
    memory = load_memory()
    memory.append({"title": title, "feedback": feedback})
    save_memory(memory)
