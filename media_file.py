from dataclasses import dataclass, field
import json

@dataclass(order=True)
class MediaFile:
    name: str
    md5: str = field(default=None)
    size: int = field(default=None)
    mtime: int = field(default=None)

    def __hash__(self):
        return hash(self.name)
