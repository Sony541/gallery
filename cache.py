from config import active_config as cfg
import os
from file_extensions import Extensions
from helpers import decide_folder_ignore
from dataclasses import dataclass, asdict, field
from media_file import MediaFile
import json
import jsonpickle
import db_update
from copy import deepcopy


@dataclass
class Cache():
    PATH: str = cfg["location"]
    NEW: dict[MediaFile] = field(default_factory=dict)
    IGNORED: dict[MediaFile] = field(default_factory=dict)
    UNSUPPORTED: dict[MediaFile] = field(default_factory=dict)
    OLD: dict[MediaFile] = field(default_factory=dict)
    STAGED: dict[MediaFile] = field(default_factory=dict)
    TO_DELETE: dict[MediaFile] = field(default_factory=dict)
    MOVED: dict[str] = field(default_factory=dict)
    CHANGED: dict[MediaFile] = field(default_factory=dict)

    def get_conflicts_number(self):
        return len(self.TO_DELETE) + len(self.MOVED) + len(self.CHANGED)

    def get_to_view_number(self):
        return len(self.NEW)

    def _flush(self):
        self.NEW = {}
        self.IGNORED = {}
        self.UNSUPPORTED = {}
        self.OLD = {}
        self.STAGED = {}
        self.TO_DELETE = {}
        self.MOVED = {}
        self.CHANGED = {}

    def scan(self):
        self._flush()
        # Loading OLD database
        self._load_old_database()
        # Loading NEW database
        self._read_files_from_disk()
        # Merging those
        self._calculate_differences()


    def _find_same_meta_in_new(self, media_file):
        for file in self.NEW.values():
            if media_file.compare_meta(file):
                return file

    def _calculate_differences(self):
        self.TO_DELETE = deepcopy(self.OLD)
        file_list = list(self.NEW.values())
        for file in file_list:
            # Absolutely new file
            if file.name not in self.TO_DELETE:
                self.STAGED[file.name] = file
                continue
            # File is in OLD, checking if it changed:
            existing = self.TO_DELETE[file.name]
            if file.size == existing.size and file.mtime == existing.mtime:
                self.TO_DELETE.pop(file.name)
                self.NEW.pop(file.name)
                continue
            # It changed
            self.CHANGED[file.name] = file
            self.NEW.pop(file.name)
            self.TO_DELETE.pop(file.name)

        # Checking if some of LOST files were moved:
        lost_file_list = list(self.TO_DELETE.values())
        for file in lost_file_list:
            dup = self._find_same_meta_in_new(file)
            if dup:
                self.MOVED[file.name] = dup.name
                self.NEW.pop(dup.name)
                self.TO_DELETE.pop(file.name)

    def _read_files_from_disk(self):
        wlk = os.walk(self.PATH)
        for dp, dn, fn in wlk:
            ignore = decide_folder_ignore(dp)
            for f in fn:
                fullname = os.path.join(dp, f)
                new_file = MediaFile(fullname)
                # in "_ignore" folder
                if ignore:
                    self.IGNORED[fullname] = new_file
                    continue

                # we don't support extension
                supported = Extensions.find(new_file.get_extension())
                if not supported:
                    self.UNSUPPORTED[fullname] = new_file
                    continue

                new_file.get_file_meta()
                self.NEW[fullname] = new_file


    def _load_old_database(self):
        self.OLD = db_update.read()

    def _write_old_database(self):
        db_update.write(self.NEW)

    def toJSON(self):
        return jsonpickle.encode(s, indent=4)



# s = Cache()


# s.scan()
# s.load_old_database()

# print(s.toJSON())