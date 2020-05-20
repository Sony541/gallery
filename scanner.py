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

    def _write_extensions(self, ext):
        try:
            f = open('file_extensions.json', 'w+')
            f.write(json.dumps(sorted(ext)))
            f.close()
        except Exception as e:
            print ('Error writing extens: %s' % e)
            return None

    def _get_extensinons(self):
        try:
            f = open('file_extensions.json')
            ext = json.loads(f.read())
            f.close()
            return set(ext)
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
        ext = self._get_extensinons() or set()
        wlk = os.walk(LOCATION)
        list_of_files = [os.path.join(dp, f) for dp, dn, fn in wlk for f in fn]
        ignore = []
        for x in [x for x in list_of_files]:
            fnd = x.rfind('.')
            if fnd != -1:
                e = x[fnd+1:].casefold()
                if e in map(str.casefold, ext):
                    continue
            list_of_files.remove(x)
            ignore.append(x[len(LOCATION):])
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
        if 'old' in self.memory and 'new' in self.memory:
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
            if st_size == self.memory['new'][name]['st_size'] and st_mtime == self.memory['new'][name]['st_mtime']:
                return name


    def dump(self, name=None):
        db_update.write(self.memory['old'], name)


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


    def search_tags(self, pattern, tag_list):
        for tag in pattern:
            if not (tag in tag_list):
                return False
        return True


    def resolve_problems(self, d):

        print(json.dumps(d, indent=2))

        if 'ignore' in d:
            exts = self._get_extensinons() or set()
            for file in d['ignore']:
                fnd = file.rfind('.')
                if fnd != -1:
                    ext = file[fnd+1:].lower()
                    exts.add(ext)
            self._write_extensions(sorted(exts))

        if 'moved' in d:
            for files in d['moved']:
                f1, f2 = tuple(files.split("*", maxsplit=1))
                self.memory['old'][f2] = self.memory['old'].pop(f1)

        if 'changed' in d:
            for file in d['changed']:
                self.memory['old'][file] = self.memory['new'].pop(file)

        if 'delete' in d:
            for file in d['delete']:
                del(self.memory['old'][file])

        #self.dump()
        self.scan()
