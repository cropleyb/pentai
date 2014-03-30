import persistent_dict as pd_m
import os
import sys
from defines import *

if __name__ == "__main__":
    source_fn = sys.argv[1]

    #source_fn = "%s%s_%s_openings.pkl" % (prefix, rk[1], rk[0])
    dest_fn = source_fn[:-4] + "_b.pkl"
    #dest_fn = "%s%s_%s_openings_b.pkl" % (prefix, rk[1], rk[0])

    size = int(sys.argv[2])

    source_dict = pd_m.PersistentDict(source_fn)
    dest_dict = pd_m.PersistentDict(dest_fn)

    for k,v in source_dict.iteritems():

        k, c1, c2 = k
        h = 0
        for s in k:
            h += s
            h *= 4 ** size

        dest_dict[h] = v

    dest_dict.sync()


