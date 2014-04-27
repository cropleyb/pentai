#/usr/bin/python

from ZODB import FileStorage, DB
from BTrees import OOBTree
from persistent import Persistent
from persistent.mapping import PersistentMapping as ZM
from persistent.list import PersistentList as ZL
import transaction
import zc.zlibstorage

"""
TODO:
A multi-threaded program should open a separate Connection instance for each thread. Different threads can then modify objects and commit their modifications independently.
"""

db = None
zdbroot = None
conn = None

def set_db(filename):
    global db, zdbroot, conn

    storage = zc.zlibstorage.ZlibStorage(
                        FileStorage.FileStorage(filename))
    db = DB(storage)
    conn = db.open()
    zdbroot = conn.root()

def get_section(section_key, tp=None):
    if zdbroot.has_key(section_key):
        section = zdbroot[section_key]
    else:
        if tp is None:
            tp = OOBTree.OOBTree
        section = zdbroot[section_key] = tp()
    return section

def sync():
    transaction.commit()

def abort():
    transaction.abort()

def delete_all_dangerous():
    """ Only use this for test code!!!"""
    zdbroot.clear()


