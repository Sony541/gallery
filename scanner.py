# coding=utf-8
import os, json
import db_update

from config import active_config
from config import Config as cfg
from file_extensions import Extensions
from storage import Storage

LOCATION = os.path.expanduser(active_config['location'])


class Cache(object):
    def __init__(self):
        self.memory = {}

    def _clear(self):
        if self.memory:
            self.memory = {}

    def _read_json(self):
        self.memory['old'] = db_update.read()
        return self.memory['old']

    def _get_file_meta(self, fname):
        stat = os.stat(fname)
        return {
            'st_size': stat.st_size,
            'st_mtime': int(stat.st_mtime)
        }

    def _find_files_on_disk(self):
        ext = Extensions.get_extensinons()
        wlk = os.walk(LOCATION)
        list_of_files = [os.path.join(dp, f) for dp, dn, fn in wlk for f in fn]
        ignore = []
        for x in [x for x in list_of_files]:
            fnd = x.rfind('.')
            if fnd != -1:
                e = x[fnd + 1:].casefold()
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
                if 'tags' in self.memory["old"][key]:
                    if self.memory["old"][key]['tags']:
                        for tag in self.memory["old"][key]['tags']:
                            if tag in self.memory["tags"]:
                                self.memory["tags"][tag] += 1
                            else:
                                self.memory["tags"][tag] = 1

    def _find_files_in_db(self):
        self.memory['old'] = db_update.read()
        if self.memory['old']:
            return True
        return False

    def _find_changed_moved_to_delete(self):
        if 'old' in self.memory and 'new' in self.memory:
            old = set(self.memory['old'].keys())
            new = set(self.memory['new'].keys())

            lost = list(old - new)
            added = new - old
            checked = new & old

            moved = {}
            for name in [x for x in lost]:
                dup = self._find_same_meta_in_new(name)
                if dup:
                    moved[name] = dup
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

            to_view = []
            for name in added:
                if name not in moved and name not in changed:
                    to_view.append(name)
            if to_view:
                self.memory['to_view'] = sorted(to_view)

    @staticmethod
    def _same_meta(ob1, ob2):
        if 'st_size' in ob1 and 'st_size' in ob2 and 'st_mtime' in ob1 and 'st_mtime' in ob2:
            return ob1['st_size'] == ob2['st_size'] and ob1['st_mtime'] == ob2['st_mtime']


    def _find_same_meta_in_new(self, fname):
        try:
            st_size, st_mtime = self.memory['old'][fname]['st_size'], self.memory['old'][fname]['st_mtime']
        except:
            return None
        else:
            for name in self.memory['new']:
                if st_size == self.memory['new'][name]['st_size'] and st_mtime == self.memory['new'][name]['st_mtime']:
                    return name

    def dump(self, name=None):
        db_update.write(self.memory['old'])

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
            self._find_tags()
        else:
            if 'new' in self.memory:
                if self.memory['new']:
                    self.memory['to_view'] = list(self.memory['new'].keys())
        db_update.cache_dump(self.memory)

    def search_tags(self, pattern, tag_list):
        for tag in pattern:
            if not (tag in tag_list):
                return False
        return True

    def resolve_problems(self, d):
        if 'ignore' in d:
            exts = Extensions.get_extensinons()
            for file in d['ignore']:
                fnd = file.rfind('.')
                if fnd != -1:
                    ext = file[fnd + 1:].lower()
                    exts.add(ext)
            Extensions.write_extensinons(sorted(exts))

        if 'moved' in d:
            for files in d['moved']:
                f1, f2 = tuple(files.split("*", maxsplit=1))
                self.memory['old'][f2] = self.memory['old'].pop(f1)

        if 'changed' in d:
            for file in d['changed']:
                self.memory['old'][file] = self.memory['new'].pop(file)

        if 'delete' in d:
            for file in d['delete']:
                del (self.memory['old'][file])

        self.dump()
        self.scan()

    def _find_all_dups(self, folder, st_size, st_mtime):
        ret = []
        for ph in folder:
            if (st_size, st_mtime) == (folder[ph]['st_size'], folder[ph]['st_mtime']):
                ret.append(ph)
        return ret

    def find_dups(self):
        whole = dict(self.memory['old'], **self.memory['new'])
        dups = {}
        while whole:
            name, value = whole.popitem()
            st_size, st_mtime = value['st_size'], value['st_mtime']
            if (st_size, st_mtime) not in dups:
                found_dups = self._find_all_dups(whole, st_size, st_mtime)
                if found_dups:
                    found_dups.append(name)
                    dups[st_size, st_mtime] = found_dups
        self.memory['dups'] = dups


    def md5_check(self):
        pass
