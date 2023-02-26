from config import Config as cfg
import json
from helpers import get_file_extension, read_json_file, write_json_file


def read():
    return read_json_file(cfg.DATA_FILE)

def write(ob):
    return write_json_file(cfg.DATA_FILE, cache)

def cache_dump(cache):
    return write_json_file(cfg.CACHE_FILE, cache)
