import os, json, config
from hashlib import md5

conf = config.test
LOCATION = os.path.expanduser(conf['location'])


class Cache(object):
    def __init__(self):
        self.memory = {'new': {},
                       'old': {},
                       'to_delete': {},
                       'search': {},
                       'tags': {},
                       'active_tags': {}}

    def _name_in_new(self, name):
        for hash in self.memory["new"]:
            if name in self.memory["new"][hash]["names"]:
                return hash
        return False

    def _read_json(self):
        try:
            f = open(conf['data_file'], 'r')
            self.memory["old"] = json.loads(f.read())
            f.close()
            return True
        except:
            print("No file")
            return False

    def _find_tags(self):
        self.memory["tags"] = {}
        for key in self.memory["old"]:
            if self.memory["old"][key]:
                for tag in self.memory["old"][key]:
                    if tag in self.memory["tags"]:
                        self.memory["tags"][tag] += 1
                    else:
                        self.memory["tags"][tag] = 1

    def _find_files_on_disk(self):
        wlk = os.walk(LOCATION)
        list_of_files = [os.path.join(dp, f)[len(LOCATION):] for dp, dn, fn in wlk for f in fn]
        for name in list_of_files:
            hash = size_and_hash(LOCATION + name)
            if hash in self.memory['new']:
                self.memory['new'][hash]["names"].append(name)
                self.memory['new'][hash]["type"] = "duplicate"
            else:
                self.memory['new'][hash] = {"type": "new", "names": [name]}

    def _find_files_in_json(self):
        if not self._read_json():
            return None
        for hash in self.memory["old"]:
            if hash not in self.memory["new"]:
                found_in_new = self._name_in_new(self.memory["old"][hash]["name"])
                if found_in_new:
                    self.memory["new"][found_in_new]["type"] = "modified"
                    self.memory["new"][found_in_new]["modified_hash"] = hash
                    self.memory["new"][found_in_new]["modified_name"] = self.memory["old"][hash]["name"]
                else:
                    self.memory["to_delete"][hash] = self.memory["old"][hash]
            else:
                if self.memory["old"][hash]["name"] not in self.memory["new"][hash]["names"]:
                    self.memory["new"][hash]["type"] = "moved"
                    self.memory["new"][hash]["moved_from"] = self.memory["old"][hash]["name"]
                else:
                    if len(self.memory["new"][hash]["names"]) != 1:
                        self.memory["new"][hash]["type"] = "duplicate"
                    else:
                        del(self.memory["new"][hash])

    def _clear(self):
        for key in self.memory:
            self.memory[key] = {}


    def dump(self):
        f = open('data.json', 'w')
        f.write(json.dumps(self.memory["old"], ensure_ascii=False, indent=2))
        f.close()

    def len(self):
        r = {}
        for key in self.memory:
            r[key] = len(self.memory[key])
        return r

    def scan(self):
        if self.memory:
            self._clear()
        self._find_files_on_disk()
        self._find_files_in_json()

    def show(self):
        microcache = {}
        for hash in self.memory["new"]:
            type = self.memory["new"][hash]["type"]
            if not type in microcache:
                microcache[type] = {}
            microcache[type][hash] = self.memory["new"][hash]
        if "new" in microcache:
            print("New files:")
            for hash in microcache["new"]:
                print ("  %s : %s" % (hash, microcache["new"][hash]["names"][0]))
        if "duplicate" in microcache:
            print("Duplicate files:")
            for hash in microcache["duplicate"]:
                print ("  %s" % hash)
                for name in microcache["duplicate"][hash]["names"]:
                    print ("    %s" % name)
        if "moved" in microcache:
            print("Moved files:")
            for hash in microcache["moved"]:
                print ("  %s moved from %s to one of places:" % (hash, microcache["moved"][hash]["moved_from"]))
                for name in microcache["moved"][hash]["names"]:
                    print ("    %s" % name)
        if "modified" in microcache:
            print("Modified files:")
            for hash in microcache["modified"]:
                print ("  %s modified from %s to %s:" % (microcache["modified"][hash]["modified_name"],
                                                         microcache["modified"][hash]["modified_hash"], hash))
                if len(microcache["modified"][hash]["names"]) != 1:
                    print("    it also now have duplicates:")
                    for name in microcache["modified"][hash]["names"]:
                        if name != microcache["modified"][hash]["modified_name"]:
                            print ("    %s" % name)


def size_and_hash(fname):
    hash_md5 = md5()
    size = 0
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
            size += len(chunk)
    return "%s_%s" % (size, hash_md5.hexdigest())



def search_tags(pattern, tag_list):
    for tag in pattern:
        if not (tag in tag_list):
            return False
    return True


cache = Cache()
cache.scan()
