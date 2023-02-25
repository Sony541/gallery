# coding=utf-8
from os.path import join

class Config:
    LOCATION = "D:\\Treasury\\Media\\Photos\\2008"
    DATA_FOLDER = "data"
    DATA_FILE = join(DATA_FOLDER, "data.json")
    CACHE_FILE = join(DATA_FOLDER, "cache.json")
    FILENAME_DICT = join(DATA_FOLDER, "FILENAME_DICT.json")
    MD5_DICT = join(DATA_FOLDER, "MD5_DICT.json")

test = {
    "location": "D:\\Treasury\\Media\\Photos\\2008",
    "data_file": "data.json",
    "FILENAME_DICT": "FILENAME_DICT.json",
    "MD5_DICT": "MD5_DICT.json",
}


prod = {
    "location": "D:\\Treasury\\Media\\Photos\\2008",
    "data_folder": "data",
    "data_file": "data.json",
    "FILENAME_DICT": "FILENAME_DICT.json",
    "MD5_DICT": "MD5_DICT.json",
}

active_config = prod
