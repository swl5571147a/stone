#!/usr/bin/env python

import sys

#print sys.argv[1]

f = open(sys.argv[1]).read()
charts = len(f)
words = len(f.split())
lines = f.count("\n")

print "cahrts:%(charts)s   words:%(words)s   lines:%(lines)s" %locals()
