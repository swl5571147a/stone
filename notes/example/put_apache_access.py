#!/usr/bin/env python

def put_access(log):
    ret = []
    with open(log) as fp:
        data = fp.readlines()
    for i in data:


def main():
    log = '/opt/graphite/storage/log/webapp/access.log'
    put_access(log)

if __name__ == "__main__":
    main()