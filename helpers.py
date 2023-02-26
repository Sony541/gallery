import os
import jsonpickle


def decide_folder_ignore(path):
    return path.endswith("_ignore")

def read_json_file(path, default_value={}):
    try:
        with open(path, encoding='utf-8') as f:
            return jsonpickle.decode(f.read())
    except (FileNotFoundError) as e:
        print(f"{path} - file not found or corrupted: {e.__class__}, {e}")
        return default_value

def write_json_file(path, data):
        try:
            txt = jsonpickle.encode(data, indent=4)
            with open(path, "w", encoding='utf-8') as f:
                f.write(txt)
                return True
        except (FileNotFoundError, TypeError) as e:
            print(f"{path} File not found or can't be written: {e.__class__}, {e}")
            return False
