# coding=utf-8
import os, json
import db_update

from config import active_config

LOCATION = os.path.expanduser(active_config['location'])


class Cache(object):
    def __init__(self):
        self.memory = {}

    def _clear(self):
        if self.memory:
            self.memory = {}

    def _get_extensinons(self):
        try:
            f = open('file_extenstions.json')
            ext = json.loads(f.read())
            f.close()
            return ext
        except Exception as e:
            print ('Error getting extens: %s' % e)
            return None


    def _read_json(self):
        js = db_update.get_old()
        if js:
            self.memory['old'] = js
            return True
        else:
            return False


    def _get_file_meta(self, fname):
        stat = os.stat(fname)
        return {
            'st_size': stat.st_size,
            'st_mtime': str(stat.st_mtime),
            'tags': []
        }


    def _find_files_on_disk(self):
        ext = self._get_extensinons()
        wlk = os.walk(LOCATION)
        list_of_files = [os.path.join(dp, f) for dp, dn, fn in wlk for f in fn]
        if ext:
            print("MATCH")
            ignore = []
            for x in [x for x in list_of_files]:
                fnd = x.rfind('.')
                if fnd != -1:
                    e = x[fnd+1:].lower()
                    if e in ext:
                        continue
                list_of_files.remove(x)
                ignore.append(x)
            if ignore:
                self.memory['ignore'] = ignore

        if list_of_files:
            self.memory['new'] = {}
            for name in list_of_files:
                id = name[len(LOCATION):]
                meta = self._get_file_meta(name)
                self.memory['new'][id] = meta


    def _find_tags(self):
        self.memory["tags"] = {}
        for key in self.memory["old"]:
            if self.memory["old"][key]:
                for tag in self.memory["old"][key]:
                    if tag in self.memory["tags"]:
                        self.memory["tags"][tag] += 1
                    else:
                        self.memory["tags"][tag] = 1


    def _find_files_in_db(self):
        old = db_update.get_old()
        if old:
            self.memory['old'] = old
            return True


    def _find_changed_moved_to_delete(self):
        old = set(self.memory['old'].keys())
        new = set(self.memory['new'].keys())

        lost = list(old - new)
        added = new - old
        checked = new & old

        moved = []
        for name in [x for x in lost]:
            dup = self._find_same_meta_in_new(name)
            if dup:
                moved.append((name, dup))
                lost.remove(name)
        if moved:
            self.memory['moved'] = moved
        if lost:
            self.memory['to_delete'] = lost

        changed = []
        for name in checked:
            if not self._same_meta(self.memory['old'][name], self.memory['new'][name]):
                changed.append(name)
            else:
                del self.memory['new'][name]
        if changed:
            self.memory['changed'] = changed




    def _same_meta(self, ob1, ob2):
        return ob1['st_size'] == ob2['st_size'] and ob1['st_mtime'] == ob2['st_mtime']


    def _find_same_meta_in_new(self, fname):
        st_size, st_mtime = self.memory['old'][fname]['st_size'], self.memory['old'][fname]['st_mtime']
        for name in self.memory['new']:
            print("names: %s - %s,\n new: %s,\n old: %s" % (fname, name, self.memory['old'][fname], self.memory['new'][name]))
            if st_size == self.memory['new'][name]['st_size'] and st_mtime == self.memory['new'][name]['st_mtime']:
                print("MATCH")
                return name


    def dump(self, name=None):
        db_update.write(self.memory['new'], name)


    def len(self):
        r = {}
        for key in self.memory:
            r[key] = len(self.memory[key])
        return r

    def scan(self):
        self._clear()
        self._find_files_on_disk()
        if self._find_files_in_db():
            self._find_changed_moved_to_delete()
        print (json.dumps(self.memory, indent=2))


def search_tags(pattern, tag_list):
    for tag in pattern:
        if not (tag in tag_list):
            return False
    return True


cache = Cache()

cache.scan()
