#/usr/bin/python

from ZODB import FileStorage, DB
from BTrees import OOBTree
from persistent import Persistent
from persistent.mapping import PersistentMapping as ZM
from persistent.list import PersistentList as ZL
import transaction
import zc.zlibstorage
import os

class DBConn(object):
    def __init__(self, db_name):
        self.db_name = db_name
        self.zdbroot = None

    def get_filepath(self):
        return "%s.%s" % (db_path, self.db_name)

    def load_db(self):
        if self.zdbroot:
            return
        fp = self.get_filepath()
        lock_file_path = fp + ".lock"
        try:
            os.unlink(lock_file_path)
        except OSError:
            pass
        storage = FileStorage.FileStorage(fp)
        self.db = DB(storage, cache_size=1000)
        self.conn = self.db.open()
        self.zdbroot = self.conn.root()

    def get_section(self, section_key, tp=None):
        if not self.zdbroot:
            self.load_db()
        if self.zdbroot.has_key(section_key):
            section = self.zdbroot[section_key]
        else:
            if tp is None:
                tp = OOBTree.OOBTree
            section = self.zdbroot[section_key] = tp()
        return section

    def root(self):
        if not self.zdbroot:
            load_db()
        return self.zdbroot

    def pack(self, *args, **kwargs):
        self.db.pack(*args, **kwargs)
        self.delete_extra_files()

    def delete_extra_files(self):
        for ext in ["tmp", "old", "lock", "index"]:
            extra_file_path = ".".join([self.get_filepath(), ext])
            try:
                os.unlink(extra_file_path)
            except OSError:
                pass

    def delete_all_dangerous(self):
        """ Only use this for test code!!!"""
        try:
            self.zdbroot.clear()
        except AttributeError:
            pass

db_path = None
most = None
openings = None

def set_db(path):
    global db_path
    db_path = path

def load_db(): # TODO: Rename
    global most, openings
    most = DBConn("most")
    most.load_db()
    openings = DBConn("openings")
    openings.load_db()

def get_section(section_key, tp=None):
    if not most:
        load_db()
    db = most
    if section_key == "openings":
        db = openings
    return db.get_section(section_key, tp)

def sync():
    transaction.commit()

def abort():
    transaction.abort()

def delete_all_dangerous():
    """ Only use this for test code!!!"""
    most.delete_all_dangerous()
    openings.delete_all_dangerous()



