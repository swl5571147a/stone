#!/usr/bin/env python

import re

with open(filename) as fp:
    data = fp.read()
    re.findall(r'^ftp:',data,re.M)


reg = r'''
    ([a-z]{3})
    \s+
    (\d{1,2})
    \s+
    (\d{2}:\d{2}:\d{2})
    \s+
    (\w+)
    \s+
    (\w+)
'''
re.findall(reg,log,re.X|re.M)
