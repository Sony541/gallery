import os
import json


def get_file_extension(path):
    _, ext = os.path.splittext(path)
    return ext


def decide_folder_ignore(path):
    return path.endswith("_ignore")

def read_json_file(path, default_value={}):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        print(f"{path} - file not found or corrupted: {e.__class__}, {e}")
        return default_value

def write_json_file(path, data):
        try:
            with open(path, "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                return True
        except (FileNotFoundError, TypeError) as e:
            print(f"{path} File not found or can't be written: {e.__class__}, {e}")
            return False
