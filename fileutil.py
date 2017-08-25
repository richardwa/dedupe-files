#!/usr/bin/python
import os

class PathHandler:
    def __init__(self, ignore=None):
            self.ignore = ignore
            self.cwd = os.getcwd()

    def walkFolder(self, folder):
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
        if os.path.isdir(f):
            return (os.path.join(self.cwd, f), self.walkFolder(f))
        else:
            return (self.cwd, [os.path.realpath(f)])

    def combine(self, filesOrFolders):
        return sum([val for _,val in self.combineKeyed(filesOrFolders)],[])

    def combineKeyed(self, filesOrFolders):
        return map(self._handle, filesOrFolders)

#Tests
if __name__ == '__main__':
    p = PathHandler()
    print p.walkFolder('.')
    print p.combine(['..','.'])
    print p.combineKeyed(['..','.'])


