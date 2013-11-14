#!/usr/bin/evn python

import hashlib
import sys

def md5sum(f):
	md5 = hashlib.md5()
	fd = open(f)
	while True:
		data = fd.read(1024*4)
		if data:
			md5.update(data)
		else:
			break
	fd.close()
	return md5.hexdigest()

if __name__ == '__main__':print md5sum(sys.argv[1])
