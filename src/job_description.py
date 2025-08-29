import os
import json

JD_FILE = "job_descriptions.json"

def save_job_description(title, description):
    data = []
    if os.path.exists(JD_FILE):
        with open(JD_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    data.append({"title": title, "description": description})
    with open(JD_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_saved_jds():
    if not os.path.exists(JD_FILE):
        return []
    with open(JD_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
