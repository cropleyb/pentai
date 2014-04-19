
import persistent_dict as pd_m
import zodb_dict as zd_m
import glob
import sys, os
from os.path import join

directory = sys.argv[1]
print "DIR: %s" % directory

zdb_filename = join(directory, "db.fs")
zd_m.set_db(zdb_filename)

def convert(fn):
    pd = pd_m.PersistentDict(fn)
    section_name = fn[fn.index("db/"):]
    section = zd_m.get_section(section_name)
    section.update(pd)
    zd_m.sync()

for filename in glob.glob(join(directory, "db/*")):
    print "Converting: %s" % filename
    convert(filename)

print "Done."

