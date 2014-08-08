import os
import logging

def init():
    global initialised
    try:
        if initialised:
            return
    except:
        init_logging()
        import zodb_dict as z_m

        z_m.set_db("test.db")
        initialised = True

def init_logging():
    logger = logging.getLogger('ZODB.FileStorage')
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler('test.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    
init()

def clear_all():
    import zodb_dict as z_m
    z_m.delete_all_dangerous()
    z_m.sync()
    initialise = False
    delete_test_db()

    import misc_db
    misc_db.reset()

def delete_test_db():
    for f in ["test.db.most", "test.db.openings"]:
        for ext in ["", ".lock", ".tmp", ".index"]:
            fn = "%s%s" % (f, ext)
            try:
                os.unlink(fn)
            except Exception, e:
                pass

