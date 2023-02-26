from config import active_config as cfg
import os
from file_extensions import Extensions
from helpers import decide_folder_ignore
from dataclasses import dataclass, asdict, field
from media_file import MediaFile
import json
import jsonpickle


@dataclass
class Storage():
    PATH: str = cfg["location"]
    FILELIST: set[MediaFile] = field(default_factory=set)
    IGNORED: set[MediaFile] = field(default_factory=set)
    UNSUPPORTED: set[MediaFile] = field(default_factory=set)

    def _flush(self):
        self.FILELIST = {}
        self.IGNORED = {}
        self.UNSUPPORTED = {}

    def read_filenames_from_disk(self):
        self._flush()
        wlk = os.walk(self.PATH)
        for dp, dn, fn in wlk:
            ignore = decide_folder_ignore(dp)
            for f in fn:
                fullname = os.path.join(dp, f)
                new_file = MediaFile(fullname)
                if ignore:
                    self.IGNORED[fullname] = new_file
                else:
                    supported = Extensions.find(new_file.get_extension())
                    if supported:
                        new_file.get_file_meta()
                        self.FILELIST[fullname] = new_file
                    else:
                        self.UNSUPPORTED[fullname] = new_file

    def toJSON(self):
        return jsonpickle.encode(s, unpicklable=False, indent=4)
