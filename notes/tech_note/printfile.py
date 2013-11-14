import sys
import os
from md5 import md5
def print_files(path):
    isdir, isfile, join = os.path.isdir, os.path.isfile, os.path.join 
    lsdir = os.listdir(path)
    dirs = [i for i in lsdir if isdir(join(path,i))]
    files = [join(path,i) for i in lsdir if isfile(join(path,i))]
    for d in dirs:
        files += print_files(join(path,d))
    return files

for f in print_files(sys.argv[1]):
    print f
 
