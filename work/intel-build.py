#!/usr/bin/env python

import os

def update_kernel(kernel_version):
    cmd = 'dpkg -i /usr/local/tnb/linux-headers/*-%s-*'
    try:
        os.system(cmd)
    except:
        pass
    