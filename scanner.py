import os, json

location = os.path.expanduser("./test_storage")


class Cache(object):
    def __init__(self):
        self.memory = {'new': {},
                       'old': {},
                       'to_delete': {},
                       'to_view': {},
                       'search': {},
                       'tags': {},
                       'active_tags': {}}

    def clear(self):
        for key in self.memory:
            self.memory[key] = {}

    def fill(self):
        try:
            f = open('data.json', 'r')
            self.old = json.loads(f.read())
            f.close()
            self.tags = {}
            for key in self.old:
                if self.old[key]:
                    for tag in self.old[key]:
                        if tag in self.tags:
                            self.tags[tag] += 1
                        else:
                            self.tags[tag] = 1
        except:
            print("No file")

    def dump(self):
        f = open('data.json', 'w')
        f.write(json.dumps(self.old, ensure_ascii=False, indent=2))
        f.close()

    def len(self):
        return {
            "new": len(self.new),
            "old": len(self.old),
            "to_delete": len(self.to_delete),
            "to_view": len(self.to_view),
            "search": len(self.search)
        }


def search_tags(pattern, taglist):
    for tag in pattern:
        if not (tag in taglist):
            return False
    return True


def scan():
    cache.clear()
    wlk = os.walk(location)
    a = [os.path.join(dp, f)[len(location):] for dp, dn, fn in wlk for f in fn]
    for row in a:
        cache.new[row] = None
    cache.fill()

    for row in cache.old:
        if row in cache.new:
            del cache.new[row]
            if cache.old[row] is None:
                cache.to_view[row] = None
        else:
            cache.to_delete[row] = cache.old[row]


cache = Cache()
scan()
