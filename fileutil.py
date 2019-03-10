#!/usr/bin/env python3
import os
import argparse

class PathHandler:
    def __init__(self, ignore=None):
            self.ignore = ignore

    def _walkFolder(self, folder):
        fileList = []
        for root, dirs, files in os.walk(folder):
            if self.ignore != None:
                dirs[:] = [d for d in dirs if d not in self.ignore]
            #print ('Scanning %s' % root)
            for filename in files:
                path = os.path.join(root, filename)
                path = os.path.realpath(path)
                fileList.append(path)
        return fileList

    def _handle(self, f):
        dirname = os.path.dirname(os.path.realpath(f));
        if os.path.isdir(f):
            return (dirname, self._walkFolder(f))
        else:
            return (dirname, [os.path.realpath(f)])

    def combine(self, filesOrFolders):
        return sum([val for _,val in self.combineKeyed(filesOrFolders)],[])

    def combineKeyed(self, filesOrFolders):
        return list(map(self._handle, filesOrFolders))

if __name__ == '__main__':
    p = PathHandler()
    parser = argparse.ArgumentParser(description='index and clean your files safely')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c','--combine', dest='accumulate',action='store_const',const=p.combine)
    group.add_argument('-ck','--combine keyed', dest='accumulate',action='store_const',const=p.combineKeyed)
    parser.add_argument('files', metavar='file', nargs='+',
            help='target files/folders')

    args = parser.parse_args()
    print(args.accumulate(args.files))


