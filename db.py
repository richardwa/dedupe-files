#!/usr/bin/env python3
import dbm
import os
import json

scriptpath = os.path.dirname(os.path.realpath(__file__))
dbfile = '%s/.config/dbm.db' % scriptpath
db = dbm.open(dbfile,'c')


def _hashfile(path, blocksize = 65536):
    afile = open(path, 'rb')
    hasher = hashlib.sha1()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

class _KeyType:
    def __init__(self, keyType, encoding='utf-8'):
        self.keyType = keyType
        self.encoding = encoding
    
    def get(self, key):
        return db[self.keyType+key].decode(self.encoding)

    def set(self, key, obj):
        db[self.keyType+key] = obj.encode(self.encoding)

class _JsonListKeyType(_KeyType):
    def get(self, key):
        try:
            return json.loads(_KeyType.get(self,key))
        except KeyError:
            return None

    def set(self, key, obj):
        _KeyType.set(self, key, json.dumps(obj))


    def append(self, key, val):
        ls = self.get(key) or []
        ls.append(val)
        self.set(key,ls)

    def remove(self, key, val):
        ls = self.get(key) or []
        try:
            ls.remove(val)
        except ValueError:
            pass
        self.set(key,ls)


digestTable = _KeyType(b'H')
pathTable = _KeyType('P')

def _checkMtime


def addToIndex(path):
    mtime = os.path.getmtime(path)
    digest = _hashfile(path)
    if os.path.getmtime(path) == mtime:
        digestTable.append(digest, (mtime, path))
        pathTable.set(path,digest)
    else:
        raise 'file modified while hashing'
    

def removeFromIndex(path):
    mtime = os.path.getmtime(path)
    digest = pathTable.get(path)
    digestTable.remove(digest, path)
    pathTable.set(path, None)

def getOthers(path):
    digest = pathTable.get(path)
    paths = digestTable.get(digest) or []
    return [p for p in paths if p != path]




if __name__ == '__main__':
    digestTable = KeyType(b'H')
    pathTable = KeyType('P')
    digestTable.set(b'test', 'test-str')
    print(digestTable.get(b'test'))
    pathTable.set('test', [1,2,3,4])
    print(pathTable.get('test'))
