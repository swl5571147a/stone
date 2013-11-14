import hashlib
import sys

def md5(f):
    md5 = hashlib.md5()
    fd = open(f)
    #md5.update(fd.read())
    while True:
        data = fd.read(1024*1024*32)
        if data:
            md5.update(data)
        else:
            break
    fd.close()
    return md5.hexdigest()

if __name__ == "__main__":
    print md5(sys.argv[1])
