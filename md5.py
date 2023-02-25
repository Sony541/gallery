import config
import os
import hashlib
import json
from time import time

LOCATION = os.path.expanduser(config.active_config['location'])


FILENAME_DICT = {}
MD5_DICT = {}

def get_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


start = time()

wlk = os.walk(LOCATION)
list_of_files = [os.path.join(dp, f) for dp, dn, fn in wlk for f in fn]
length = len(list_of_files)
for f in list_of_files:
    print(length)
    md5 = get_md5(f)
    FILENAME_DICT[f] = md5
    md5_list = MD5_DICT.get(md5, [])
    md5_list.append(f)
    MD5_DICT[md5] = md5_list

    length -= 1

with open("FILENAME_DICT.json", "w") as f:
    json.dump(config.active_config["FILENAME_DICT"], f, indent=4)
with open("MD5_DICT.json", "w") as f:
    json.dump(config.active_config['MD5_DICT'], f, indent=4)
end = time()
total = end - start
print(f"Started: {start} \nEnded: {end}\nTook: {total}")
