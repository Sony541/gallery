from config import active_config as cfg
import os
from file_extensions import Extensions
from helpers import decide_folder_ignore



class Storage:
    PATH = cfg["location"]

    @classmethod
    def _flush(cls):
        cls.FILELIST = set()
        cls.IGNORED = set()
        cls.UNSUPPORTED = set()

    @classmethod
    def read_filenames_from_disk(cls):
        cls._flush()
        wlk = os.walk()
        for dp, dn, fn in wlk:
            ignore = decide_folder_ignore(dp)
            for f in fn:
                fullname = os.path.join(dp, f)
                if ignore:
                    cls.IGNORED.add(fullname)
                else:
                    supported = Extensions.find(fullname)
                    if supported:
                        cls.FILELIST.add(fullname)
                    else:
                        cls.UNSUPPORTED.add(fullname)
    


