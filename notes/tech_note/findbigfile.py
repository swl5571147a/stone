import os
import sys
import operator



def getFilesSize(path):
    d = {}
    for p,dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(p,f)
            if os.path.isfile(fp):
                d[fp] = os.path.getsize(fp)
    return d

def top10(d):
    return sorted(d.iteritems(), key=operator.itemgetter(1), reverse=True)[:10]


if __name__ == "__main__":
   for k,v in top10(getFilesSize(sys.argv[1])):
       print k,v
