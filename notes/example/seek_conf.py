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
    line = ""
    while fobj.tell() > 0:
        fobj.seek(pos, 1)
        d = fobj.read(1)
        line += d
        #if d == "\n":
        #    line = "\n" + line
        #else:
        #    line += d
        if fobj.tell() == 1:
            fobj.seek(-1,1)
        else:
            pos = -2
    return line
    #return line

def teach_done(fobj):
    fobj.seek(0, 2)
    pos = -1
    line = ''
    while fobj.tell() > 0:
        fobj.seek(pos, 1)
        d = fobj.read(1)
        if fobj.tell() == 1:
            fobj.seek(-1, 1)
            break
        else:
            pos = -2
            if not d == "\n":
                line = d + line
            else:
                if line:
                    yield line
                line = d

def teach_done(fobj):
    fobj.seek(0, 2)
    pos = -1
    line = ''
    while fobj.tell() > 0:
        fobj.seek(pos, 1)
        d = fobj.read(1)
        if fobj.tell() == 1:
            fobj.seek(-1, 1)
            break
        else:
            pos = -2
            if not d == "\n":
                line = d + line
            else:
                if line:
                    yield line
                line = d

def middle(fp, buff):
    tmp_file = 'abc.tmp'
    fp.seek(0, 2)
    y = fp.tell() % buff
    z = buff
    buff += y
    while fp.tell() > 0:
        d = fp.read(buff)
        with open(tmp_file, 'w') as tmp:
            tmp.write(d)
        with open(tmp_file) as tmp2:
            teach_done(tmp2)
        buff = z

def main():
    conf = './seek_conf.conf'
    conf2 = '/var/log/apache2/access.log.1'
    #data = seek_last(conf)
    #make_data(data)
    #print data
    fp = open(conf2)
    #for i in teach(fp):
     #   print i
    data = teach(fp)
    #for i in data.split("\n"):
    #    if not i.strip() == '':
    #        print i[::-1]
    d = []
    #for i in teach_done(fp):
    #    print i.strip()
    print [i for i in middle(fp, 64)]

if __name__ == "__main__":
    main()


