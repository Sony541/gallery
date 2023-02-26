from dataclasses import dataclass, field
import json
import os

@dataclass(order=True)
class MediaFile:
    name: str
    md5: str = field(default=None)
    size: int = field(default=None)
    mtime: int = field(default=None)

    def get_extension(self):
        _, ext = os.path.splitext(self.name)
        if ext:
            return ext[1:]

    def get_file_meta(self):
        stat = os.stat(self.name)
        self.size = stat.st_size
        self.mtime = int(stat.st_mtime)
        return {
            'size': self.size,
            'mtime': self.mtime
        }
