import json
import os
import glob

def loadJson(file_path):
    """
    Attempts to read a JSON file. 
    If the file is missing or corrupted, it creates an empty one.
    """
    # Ensure the directory exists so we don't crash on the first run
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        # File is missing or contains 'trash' data
        print(f"[!] Database missing or corrupted. Initializing: {file_path}")
        
        default_data = {}
        save_json(file_path, default_data) # Create the file immediately
        return default_data

    except PermissionError:
        print(f"[X] ERROR: Permission denied for {file_path}")
        return {}

def saveJson(file_path, data, indent=4):
    """
    Saves a dictionary or list into a JSON file.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            # ensure_ascii=False allows for French/German accents like 'é' or 'ü'
            json.dump(data, f, indent=indent, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[X] SAVE ERROR: {e}")
        return False

def getLatestFile(base_dir, prefix):
    pattern = os.path.join(base_dir, f"{prefix}_V*.json")
    files = glob.glob(pattern)
    
    if not files:
        return None
    
    # Sort by modification time (newest first)
    latest_file = max(files, key=os.path.getmtime)
    return latest_file