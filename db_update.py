from config import Config as cfg
from helpers import read_json_file, write_json_file


def read():
    return read_json_file(cfg.DATA_FILE)

def write(ob):
    return write_json_file(cfg.DATA_FILE, ob)

def cache_dump(cache):
    return write_json_file(cfg.CACHE_FILE, cache)
