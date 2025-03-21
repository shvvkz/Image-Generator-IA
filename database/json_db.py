import json
import uuid
from datetime import datetime
import os

DB_PATH = "database.json"

def load_database():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump([], f)
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_database(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def generate_uid():
    return str(uuid.uuid4())[:8]

def add_entry(prompt, uid):
    db = load_database()
    entry = {
        "uid": uid,
        "prompt": prompt,
        "date": datetime.now().isoformat()
    }
    db.append(entry)
    save_database(db)

def get_all_entries():
    return load_database()
