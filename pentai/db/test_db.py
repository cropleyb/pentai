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
    delete_test_db()

def delete_test_db():
    for f in ["test.db.most", "test.db.openings"]:
        for ext in ["", ".lock", ".tmp", ".index"]:
            fn = "%s%s" % (f, ext)
            try:
                os.unlink(fn)
            except:
                pass

