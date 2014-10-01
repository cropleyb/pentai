from pentai.gui.kivy_gui_main import *
import pentai.db.zodb_dict as z_m

import kivy.core.window as w_m
from kivy.config import Config

import os, sys

def run():
    #Config.set('kivy', 'log_level', 'info')
    Config.set('kivy', 'log_level', 'debug')
    Config.set('kivy', 'log_enable', 1)
    Config.set('kivy', 'log_dir', 'logs')
    Config.set('kivy', 'log_name', 'kivy_%y-%m-%d_%_.txt')

    try:
        pentai_path = os.environ['PENTAIPATH']
    except KeyError:
        pentai_path = None

    try:
        pa = PentAIApp()

        if pentai_path == None:
            pentai_path = pa.user_data_dir
        print "User Data Dir: %s" % pa.user_data_dir

        db_path = os.path.join(pentai_path, "db.fs")
        print "Loading DB from %s" % db_path
        lockfile_path = db_path + ".lock"
        if os.path.isfile(lockfile_path):
            os.unlink(lockfile_path)
            print "Cleared DB lock"
        z_m.set_db(db_path)
        err_fn = os.path.join(pentai_path, "err.txt")

        try:
            print "Previous crash:"
            with open(err_fn) as err_log:
                print err_log.readlines()
        except:
            pass
        pa.run()
    except Exception, e:
        print
        print "PentAI crashed!"
        import traceback
        traceback.print_exc()
        try:
            with open(err_fn, "w") as err_log:
                print "saving traceback to %s" % err_fn
                traceback.print_exc(None, err_log)
        except:
            pass

if __name__ == '__main__':
    import pstats, cProfile
    cProfile.runctx("main()", globals(), locals(), "Profile.prof")

    s = pstats.Stats("Profile.prof")
    s.strip_dirs().sort_stats("cumulative").print_stats(20) # or "time"
    #s.strip_dirs().sort_stats("time").print_stats(20)
    # main()

