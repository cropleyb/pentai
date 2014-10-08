'''
import pentai.t_all as t_m
t_m.main()
import sys
sys.exit(0)
'''

import os
import platform

'''
def _total_size(source):
    total_size = os.path.getsize(source)
    for item in os.listdir(source):
        itempath = os.path.join(source, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            dir_size = _total_size(itempath)
            print "%s: %s" % (itempath, dir_size)
            total_size += dir_size
    return total_size

def main():
    print _total_size("..")

    """
    source = os.path.join(".", "txt")
    for item in os.listdir(source):
        itempath = os.path.join(source, item)
        if os.path.isfile(itempath):
            print "%s: %s" % (itempath, os.path.getsize(itempath))
    """

'''
import sys

def setup_logging():
    formatter = logging.Formatter("[%(asctime)s.%(msecs)03d][%(levelname)s][%(message)s]",
                                          "%H:%M:%S")
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    sys._kivy_logging_handler = console
    sys.setrecursionlimit(500)

    logging.getLogger("ZODB.FileStorage").addHandler(console)
    logging.getLogger("ZODB.lock_file").addHandler(console)
    logging.getLogger("ZODB.Connection").addHandler(console)

def main():
    # TEMP WORKAROUND for Kivy prob.
    os.environ["KIVY_GLES_LIMITS"] = '0'

    if platform.system() == 'Windows':

        # TEST WORKAROUND. SDL2 is supposed to be even better :)
        os.environ['KIVY_AUDIO'] = 'pygame'

    setup_logging()
    import startup
    startup.run()

import logging, sys

if __name__ == "__main__":
    '''
    import pstats, cProfile
    cProfile.runctx("main()", globals(), locals(), "Profile.prof")

    s = pstats.Stats("Profile.prof")
    s.strip_dirs().sort_stats("cumulative").print_stats(20) # or "time"
    #s.strip_dirs().sort_stats("time").print_stats(20)
    '''

    main()

