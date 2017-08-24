#!/usr/bin/python
import os, sys
import hashlib
import argparse

def walk(folder, ignore):
    fileList = []
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in ignore]
        print ('Scanning %s' % root)
        for filename in files:
            path = os.path.join(root,filename)
            path = os.path.realpath(path)
            fileList.append(path)
    return fileList
 
def hashfile(path, blocksize = 65536):
    afile = open(path, 'rb')
    hasher = hashlib.sha1()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()
 

def merge(files):
    print 'merge '+str(files)

def delete(files):
    print 'delete '+str(files)

def index(files):
    print 'index '+str(files)
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='index and clean your files safely')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i','--index', dest='accumulate',action='store_const',const=index)
    group.add_argument('-d','--delete', dest='accumulate',action='store_const',const=delete)
    group.add_argument('-m','--merge', dest='accumulate',action='store_const',const=merge)

    parser.add_argument('files', metavar='file', nargs='+',
            help='target files/folders')
    args = parser.parse_args()
    for f in args.files:
        for l in walk(f, ['.svn','.git']):
            args.accumulate(l)
    
