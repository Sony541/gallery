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
        self.FILELIST = set()
        self.IGNORED = set()
        self.UNSUPPORTED = set()

    def read_filenames_from_disk(self):
        self._flush()
        wlk = os.walk(self.PATH)
        for dp, dn, fn in wlk:
            ignore = decide_folder_ignore(dp)
            for f in fn:
                fullname = os.path.join(dp, f)
                if ignore:
                    self.IGNORED.add(MediaFile(fullname))
                else:
                    supported = Extensions.find(fullname)
                    if supported:
                        self.FILELIST.add(MediaFile(fullname))
                    else:
                        self.UNSUPPORTED.add(MediaFile(fullname))

    def toJSON(self):
        return jsonpickle.encode(s, unpicklable=False, indent=4)
