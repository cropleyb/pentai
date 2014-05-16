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
    z_m.sync()
    initialise = False
    #delete_test_db()

def delete_test_db():
    try:
        os.unlink("test.db")
    except:
        pass
    try:
        os.unlink("test.db.lock")
    except:
        pass
    try:
        os.unlink("test.db.tmp")
    except:
        pass
    try:
        os.unlink("test.db.index")
    except:
        pass

