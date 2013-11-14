import os
import sys


path = sys.argv[1]
size = os.path.getsize(path)
print path, size
for p,dirs, files in os.walk(path):
    for f in files:
        fp = os.path.join(p,f)
        if os.path.isfile(fp):
            s = os.path.getsize(fp)
            size += s
        
    for d in dirs:
        dp = os.path.join(p,d)
        s = os.path.getsize(dp)
        size += s

print "Size: %s %skb" % (size, size/1024)


