from config import active_config as cfg
from helpers import get_file_extension, read_json_file, write_json_file
import json
import os


class Extensions:
    PATH = os.path.join(cfg["data_folder"], "file_extensions.json")

    @classmethod
    def get_extensinons(cls):
        cls.CACHE = set(read_json_file(cls.PATH))
        return cls.CACHE
    
    @classmethod
    def write_extensinons(cls, ext):
        try:
            with open(cls.PATH, "w") as f:
                json.dump(list(ext), f)
            cls.get_extensinons()
        except (FileNotFoundError, TypeError) as e:
            print(f"File not found or can't be written: {e}")
            return set()
    
    @classmethod
    def test(cls, path):
        ext = get_file_extension(path)
        return ext.lower() in cls.CACHE
