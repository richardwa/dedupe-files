#!/usr/bin/env python3
import os
import hashlib
import argparse
import db 
from fileutil import PathHandler

digestTable = KeyType(b'H')
pathTable = KeyType('P')
 
def hashfile(path, blocksize = 65536):
    afile = open(path, 'rb')
    hasher = hashlib.sha1()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def merge(files, ignore):
    *source, target = files
    if os.path.isdir(target):
        target_abs = os.path.realpath(target)
        print(target_abs)
        handler = PathHandler()
        for root,files in handler.combineKeyed(source):
            for f in files:
                relpath = os.path.relpath(f,root)
                print('%s -> %s' % (f,os.path.join(target_abs,relpath)))
                digest = hashfile(f)
                if len([c for c in db.get(h) if c != f]) > 1:
                    print('delete file '+f)

    else:
        print('%s is not a folder' % target)

def delete(files, ignore):
    handler = PathHandler(ignore)
    digest = hashfile(path)
    files = db.get(digest)
    if len(files) >= 2:
        os.remove(path)
        db.remove(digest, path)
    elif len(files) == 1 and path not in files:
        os.remove(path)
    else:
        print('%s is not duped, count: %d' % (path, len(files)))

def save(files, ignore):
    handler = PathHandler(ignore)
    for path in handler.combine(files):
        digest = hashfile(path)
        digestTable.append(digest, path)
        pathTable.set(path, digest)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='index and clean your files safely')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s','--save', dest='accumulate',action='store_const',const=save,
            help='save hashes')
    group.add_argument('-d','--delete', dest='accumulate',action='store_const',const=delete,
            help='safe delete, will not delete anything that is not duped')
    group.add_argument('-m','--merge', dest='accumulate',action='store_const',const=merge,
            help='merege files/folders last argument must be a folder')
    parser.add_argument('-i','--ignore', default='.svn,.git',
            help='ignored folders (not used with merge)')
    parser.add_argument('files', metavar='file', nargs='+',
            help='target files/folders')
    args = parser.parse_args()

    args.accumulate(args.files, args.ignore.split(','))
    
