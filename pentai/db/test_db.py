import zodb_dict as z_m
import os

def init():
    global initialised
    try:
        if initialised:
            return
    except:
        z_m.set_db("test.db")
        initialised = True

init()

def clear_all():
    z_m.delete_all_dangerous()

def delete_test_db():
    os.unlink("test.db")
    os.unlink("test.db.lock")
    os.unlink("test.db.tmp")
    os.unlink("test.db.index")

