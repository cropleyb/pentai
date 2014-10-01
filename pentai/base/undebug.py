#!/usr/bin/python

import os

files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    # do something
    if f[-3:] == "pyx":
        base = f[:-3]
        for ext in ["c", "so", "py"]:
            del_path = "%s%s" % (base, ext)
            try:
                os.unlink(del_path)
            except OSError:
                pass

