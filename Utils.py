import json

from pathlib import Path
from collections import OrderedDict


def read_json(fname):
    if not fname:
        return {}
    fname = Path(fname)
    with fname.open('rt') as handle:
        return json.load(handle, object_hook=OrderedDict)


def write_json(content, fname):
    if not fname:
        return {}
    fname = Path(fname)
    with fname.open('wt') as handle:
        json.dump(content, handle, indent=4, sort_keys=False, ensure_ascii=False)
