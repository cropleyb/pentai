import glob
import os

files = glob.glob("*.wav")
i = 0

for fn in files:
    i += 1
    next_fn = "place%s.wav" % i
    os.rename(fn, next_fn)
