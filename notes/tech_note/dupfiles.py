import os
import sys

from md5sum import md5sum


filedict = {}
for p, dirs, files in os.walk(sys.argv[1]):
    for f in files:
        fp = os.path.join(p,f)
        md5 = md5sum(fp)
        if md5 in filedict:
            filedict[md5].append(fp)
        else:
            filedict[md5] = [fp]

for k in filedict:
    if len(filedict[k]) > 1:
        print k,','.join(filedict[k])
    
