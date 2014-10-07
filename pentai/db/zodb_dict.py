#/usr/bin/python

from ZODB import FileStorage, DB
from BTrees import OOBTree
from persistent import Persistent
from persistent.mapping import PersistentMapping as ZM
from persistent.list import PersistentList as ZL
import transaction
import zc.zlibstorage
import os

from pentai.base.defines import *

class DBConn(object):
    def __init__(self, db_name):
        self.db_name = db_name
        self.zdbroot = None

    def get_filepath(self):
        return "%s.%s" % (db_path, self.db_name)

    def load_db(self):
        if self.zdbroot:
            return
        self.delete_extra_files()
        fp = self.get_filepath()
        storage = FileStorage.FileStorage(fp)
        self.db = DB(storage, cache_size=1000)
        self.conn = self.db.open()
        self.zdbroot = self.conn.root()

    def get_section(self, section_key, tp=None):
        if self.zdbroot is None:
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

    def close(self):
        try:
            self.conn.close()
        except AttributeError:
            pass

    def delete_all_dangerous(self):
        """ Only use this for test code!!!"""
        exts = ["", ".tmp", ".lock", ".index", ".old"]
        self.delete_files(exts)

    def delete_extra_files(self):
        """ Delete as yet unnecessary files """
        exts = [".tmp", ".lock", ".index", ".old"]
        self.delete_files(exts)

    def delete_files(self, exts):
        for ext in exts:
            file_path = "%s%s" % (self.get_filepath(), ext)
            try:
                os.unlink(file_path)
            except OSError:
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
    try:
        return db.get_section(section_key, tp)
    except:
        pass

def sync():
    transaction.commit()

def abort():
    transaction.abort()

def close():
    global most, openings
    if most:
        most.close()
    if openings:
        openings.close()

def pack():
    global most, openings
    if most:
        most.pack()
    if openings:
        openings.pack()

def delete_all_dangerous():
    """ Only use this for test code!!!"""
    global most, openings
    if most:
        most.delete_all_dangerous()
    if openings:
        openings.delete_all_dangerous()
    most = None
    openings = None

