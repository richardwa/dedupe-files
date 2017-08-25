#!/usr/bin/python
import os

class PathHandler:
    def __init__(self, ignore):
            self.ignore = ignore

    def walkFolder(self, folder):
        fileList = []
        for root, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if d not in self.ignore]
            print ('Scanning %s' % root)
            for filename in files:
                path = os.path.join(root,filename)
                path = os.path.realpath(path)
                fileList.append(path)
        return fileList

    def _handle(self, f):
        if os.path.isdir(f):
            return self.walkFolder(f)
        else
            return [f]

    def combine(self, filesOrFolders):
        return sum(map(self.handle, filesOrFolders),[])

    
