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
import pentai.base.logger as log

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
        log.debug("zodb load_db 1")
        storage = FileStorage.FileStorage(fp)
        log.debug("zodb load_db 2")
        self.db = DB(storage, cache_size=1000)
        log.debug("zodb load_db 3")
        self.conn = self.db.open()
        log.debug("zodb load_db 4")
        self.zdbroot = self.conn.root()
        log.debug("zodb load_db 5")

    def get_section(self, section_key, tp=None):
        log.debug("zodb a")
        if self.zdbroot is None:
            self.load_db()
        log.debug("zodb b")
        if self.zdbroot.has_key(section_key):
            section = self.zdbroot[section_key]
        else:
            if tp is None:
                tp = OOBTree.OOBTree
            section = self.zdbroot[section_key] = tp()
        return section

    def root(self):
        if not self.zdbroot:
            self.load_db()
        return self.zdbroot

    def pack(self, *args, **kwargs):
        self.db.pack(*args, **kwargs)
        self.delete_extra_files()

    def close(self):
        try:
            self.conn.close()
            self.conn = None
            self.db.close()
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

def load_most():
    global most, openings
    log.debug("zodb 1a")
    most = DBConn("most")
    log.debug("zodb 1b")
    most.load_db()
    log.debug("zodb 1c")

def load_openings():
    global openings
    log.debug("zodb 1d")
    openings = DBConn("openings")
    log.debug("zodb 1e")
    openings.load_db()
    log.debug("zodb 1f")

def load_both_dbs():
    load_most()
    load_openings()

def get_section(section_key, tp=None):
    log.debug("zodb 1")
    if not most:
        load_most()
    log.debug("zodb 2")
    db = most
    if section_key == "openings":
        load_openings()
        db = openings
    log.debug("zodb 3")
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
    log.info("Packing")
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

