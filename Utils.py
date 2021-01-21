import json

from pathlib import Path
from collections import OrderedDict


def read_json(fname):
    """
    Reads a json file to an ordered dictionary.
    :param fname: The path of the file to read.
    :return: The content of the file as a dictionary.
    """
    if not fname:
        return {}
    fname = Path(fname)
    with fname.open('rt') as handle:
        return json.load(handle, object_hook=OrderedDict)


def write_json(content, fname):
    """
    Writes a dictionary to a json file in the path specified in fname.
    :param content: The content to save in the file. (expecting dictionary).
    :param fname: The path in which to save the file. (path + file name).
    """
    if not fname:
        return {}
    fname = Path(fname)
    with fname.open('wt') as handle:
        json.dump(content, handle, indent=4, sort_keys=False, ensure_ascii=False)
