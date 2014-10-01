#!/usr/bin/python

import os
import re
import sys

def cythonized(fn):
    f = open(fn, "r")

    for line in f:
        if re.search("import cython", line) or re.search("cdef ", line):
            return True
    return False

files = [fn for fn in os.listdir('.') if os.path.isfile(fn)]

for fn in files:

    # do something
    if fn[-3:] == "pyx":
        if cythonized(fn):
            continue
        base = fn[:-3]
        for ext in ["c", "so", "py"]:
            del_path = "%s%s" % (base, ext)
            try:
                os.unlink(del_path)
            except OSError:
                pass
        src_path = "%s%s" % (base, "pyx")
        dest_path = "%s%s" % (base, "py")
        os.symlink(src_path, dest_path)

