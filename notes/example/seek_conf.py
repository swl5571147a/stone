#!/usr/bin/env python

def seek_last(conf):
    list = {}
    with open(conf) as fp:
        data = fp.read()
        n = data.count('\n') * 2
        for i in range(data.count('\n')):
            fp.seek(n -2)
            list[i] = fp.read()
            n -= 2
    return list

def make_data(data):
    for k, v in data.items():
        data[k] = v.split('\n')[0]

def teach(fobj):
    fobj.seek(0,2)
    pos = -1
    while fobj.tell() > 0:
        fobj.seek(pos, 1)
        d = fobj.read(1)
        if fobj.tell() == 1:
            fobj.seek(-1,1)
            yield d
        else:
            pos = -2
        yield d

def main():
    conf = './seek_conf.conf'
    data = seek_last(conf)
    make_data(data)
    print data

if __name__ == "__main__":
    main()

