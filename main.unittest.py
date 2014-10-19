# Use this file to temporarily replace main.py, to run the PentAI
# unit test suite. Some kivy platforms (iOS) require the entry point to 
# be called main.py

import __builtin__
openfiles = set()
oldfile = __builtin__.file

class newfile(oldfile):
    def __init__(self, *args):
        self.x = args[0]
        #print "### OPENING %s ###" % str(self.x)            
        oldfile.__init__(self, *args)
        openfiles.add(self)

    def close(self):
        #print "### CLOSING %s ###" % str(self.x)
        oldfile.close(self)
        openfiles.remove(self)

oldopen = __builtin__.open
def newopen(*args):
    return newfile(*args)
__builtin__.file = newfile
__builtin__.open = newopen

def printOpenFiles():
    print "### %d OPEN FILES: [%s]" % (len(openfiles), ", ".join(f.x for f in openfiles))

'''
# Use this for detailed single case testing

import unittest
import pentai.db.t_op_pos as tmod

suite = unittest.defaultTestLoader.loadTestsFromModule(tmod)
#suite = unittest.TestSuite()
#suite.addTest(tmod.O_PosPersistenceTest('test_add_omgd_to_db'))
unittest.TextTestRunner().run(suite)
'''
import pentai.t_all as t_m
t_m.main()

print "BEFORE CLOSE"
printOpenFiles()
import pentai.db.zodb_dict as z_m
z_m.close()
print "AFTER CLOSE"
printOpenFiles()
