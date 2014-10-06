import shutil
import os

"""
Instructions
------------
# Build the app
# Look at the timestamps in the generated app directory
# Wait a bit

pushd pai/dist/Content/MacOS

# Find all the files that haven't been accessed since they were created
find . ! -atime -4m > unused.txt

# Don't remove any of the files that we know we'll need
grep -v pentai unused.txt | grep -v media | grep -v Droid > unused.txt

mkdir bak

# Then run this script
python ../../../trim.py

# And check that ./pai runs
"""

dest = "bak"

for fn in file("unused3.txt"):
    fn = fn.strip()
    try:
        shutil.move(fn, dest)
    except:
        print "Could not move %s, removing" % fn
        try:
            os.remove(fn)
        except:
            pass
