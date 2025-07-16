import json
import os

LEARNED_FILE = "learned.json"
TO_LEARN_FILE = "to_learn.json"

def load_list(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

def save_list(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def add_to_learned(topic):
    learned = load_list(LEARNED_FILE)
    if topic not in learned:
        learned.append(topic)
        save_list(LEARNED_FILE, learned)

def add_to_future_list(topic):
    to_learn = load_list(TO_LEARN_FILE)
    if topic not in to_learn:
        to_learn.append(topic)
        save_list(TO_LEARN_FILE, to_learn)

def already_learned(topic):
    return topic in load_list(LEARNED_FILE)

def get_to_learn_topics():
    return load_list(TO_LEARN_FILE)
