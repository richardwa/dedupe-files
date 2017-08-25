#!/usr/bin/env python3
import os
import hashlib
import argparse
import db as db
import FileHander


 
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
    if os.isdir(target):
        handler = new PathHandler()
        for path in handler.combine(source):

    else:
        print '$s is not a folder' % target

def delete(files, ignore):
    handler = new PathHandler(ignore)

    digest = hashfile(path)
    files = db.get(digest)
    if len(files) >= 2:
        os.remove(path)
        db.remove(digest, path)
    elif len(files) == 1 and path not in files:
        os.remove(path)
    else:
        print '%s is not duped, count: %d' % (path, len(files))

def save(files, ignore):
    handler = new PathHandler(ignore)
    for path in handler.combine(files)
        digest = hashfile(path)
        db.save(digest, path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='index and clean your files safely')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s','--save', dest='accumulate',action='store_const',const=index,
            help='save hashes')
    group.add_argument('-d','--delete', dest='accumulate',action='store_const',const=delete,
            help='safe delete, will not delete anything that is not duped')
    group.add_argument('-m','--merge', dest='accumulate',action='store_const',const=merge,
            help='merege files/folders last argument must be a folder')
    parser.add_argument('-i','--ignore', default='.svn,.git'
            help='ignored folders (not used with merge)')
    parser.add_argument('files', metavar='file', nargs='+',
            help='target files/folders')
    args = parser.parse_args()

    args.accumulate(args.files, args.ignore.split(','))
    
