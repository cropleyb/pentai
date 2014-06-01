#/usr/bin/python

from ZODB import FileStorage, DB
from BTrees import OOBTree
from persistent import Persistent
from persistent.mapping import PersistentMapping as ZM
from persistent.list import PersistentList as ZL
import transaction
import zc.zlibstorage
import os

"""
TODO:
A multi-threaded program should open a separate Connection instance for each thread. Different threads can then modify objects and commit their modifications independently.
"""

db = None
_zdbroot = None
conn = None
db_path = None

def set_db(path):
    global db_path
    db_path = path

def load_db():
    global db, _zdbroot, conn

    lock_file_path = db_path + ".lock"
    try:
        os.unlink(lock_file_path)
    except OSError:
        pass
    storage = FileStorage.FileStorage(db_path)
    db = DB(storage, cache_size=1000)
    conn = db.open()
    _zdbroot = conn.root()

def get_section(section_key, tp=None):
    if not _zdbroot:
        load_db()
    if _zdbroot.has_key(section_key):
        section = _zdbroot[section_key]
    else:
        if tp is None:
            tp = OOBTree.OOBTree
        section = _zdbroot[section_key] = tp()
    return section

def root():
    if not _zdbroot:
        load_db()
    return _zdbroot

def sync():
    transaction.commit()

def pack(*args, **kwargs):
    db.pack(*args, **kwargs)
    delete_extra_files(db_path)

def delete_extra_files(base_path):
    for ext in ["tmp", "old", "lock"]:
        # Not currently using indexing?
        extra_file_path = ".".join([base_path, ext])
        try:
            os.unlink(extra_file_path)
        except OSError:
            pass

'''
# TODO?
def pack_in_thread(*args, **kwargs):
    import threading
    db.pack(*args, **kwargs)
'''

def abort():
    transaction.abort()

def delete_all_dangerous():
    """ Only use this for test code!!!"""
    _zdbroot.clear()


