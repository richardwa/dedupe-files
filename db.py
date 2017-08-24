#!/usr/bin/env python3
import dbm
import os
import json

scriptpath = os.path.dirname(os.path.realpath(__file__))
dbfile = '%s/.config/dbm.db' % scriptpath
enc = 'utf-8'
db = dbm.open(dbfile,'c')

def get(digest):
    val = db.get(digest, None)
    if val is None:
        val = []
    else:
        val = json.loads(val.decode(enc))
    return val

def _set(digest, paths):
    db[digest]= json.dumps(paths).encode(enc)

def save(digest, path):
    paths = get(digest)
    if path not in paths:
        paths.append(path)
    _set(digest, paths)

def remove(digest, path):
    paths = get(digest)
    if path in paths:
        paths.remove(path)
        if len(paths) == 0 :
            del db[digest]
        else:
            _set(digest, paths)

