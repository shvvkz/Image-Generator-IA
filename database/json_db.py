import json
import uuid
from datetime import datetime
import os

DB_PATH = "database.json"

def load_database():
    """
    Load the local JSON database.

    Returns:
        list: List of all stored entries.
    """
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump([], f)
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_database(data):
    """
    Save data to the local JSON database.

    Args:
        data (list): List of entries to be saved.
    """
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def generate_uid():
    """
    Generate a short unique identifier.

    Returns:
        str: The generated UID.
    """
    return str(uuid.uuid4())[:8]

def add_entry(prompt, uid):
    """
    Add a new entry to the database.

    Args:
        prompt (str): The original user prompt.
        uid (str): The unique identifier associated with the entry.
    """
    db = load_database()
    entry = {
        "uid": uid,
        "prompt": prompt,
        "date": datetime.now().isoformat()
    }
    db.append(entry)
    save_database(db)

def get_all_entries():
    """
    Retrieve all entries from the database.

    Returns:
        list: List of all stored entries.
    """
    return load_database()
