from config import Config as cfg
from helpers import  read_json_file, write_json_file
import json


class Extensions:
    PATH = cfg.EXTENSIONS_FILE

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
    def find(cls, ext):
        cls.get_extensinons()
        return ext.lower() in cls.CACHE
