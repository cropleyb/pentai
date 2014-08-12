import os
import logging

def init():
    """ TODO: Call this setUp """
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
    """ TODO: Call this tearDown """
    import zodb_dict as z_m
    z_m.sync()
    z_m.close()
    z_m.delete_all_dangerous()

    global initialised
    initialised = False

    import misc_db
    misc_db.reset()

    import openings_book as ob_m
    ob_m.instance = None

