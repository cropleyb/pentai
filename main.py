from pentai.gui.kivy_gui_main import *
'''
'KIVY_DPI'
'KIVY_METRICS_DENSITY'
'KIVY_METRICS_FONTSCALE'
'''

import pentai.db.zodb_dict as z_m
import pentai.gui.scale as sc_m

import kivy.core.window as w_m

import os
import sys

if __name__ == '__main__':
    Config.set('kivy', 'log_level', 'info')
    Config.set('kivy', 'log_enable', 1)
    Config.set('kivy', 'log_dir', 'logs')
    Config.set('kivy', 'log_name', 'kivy_%y-%m-%d_%_.txt')

    f = w_m.Window.size[1] / 720.0
    sc_m.set_scale_factor(f)

    try:
        pentai_path = os.environ['PENTAIPATH']
    except KeyError:
        pentai_path = None

    try:
        pa = PentAIApp()

        if pentai_path == None:
            pentai_path = pa.user_data_dir

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
                print "logging to %s" % err_fn
                traceback.print_exc(None, err_log)
        except:
            pass

