from pentai.gui.kivy_gui_main import *
'''
'KIVY_DPI'
'KIVY_METRICS_DENSITY'
'KIVY_METRICS_FONTSCALE'
'''

#import os
'''
if not os.environ.has_key('KIVY_METRICS_FONTSCALE'):
    os.environ['KIVY_METRICS_FONTSCALE'] = '6'
'''
#os.environ['KIVY_METRICS_FONTSCALE'] = '6'

if __name__ == '__main__':
    Config.set('kivy', 'log_level', 'info')
    Config.set('kivy', 'log_enable', 1)
    Config.set('kivy', 'log_dir', 'logs')
    Config.set('kivy', 'log_name', 'kivy_%y-%m-%d_%_.txt')

    Config.set('graphics', 'width', '457')
    Config.set('graphics', 'height', '720')

    try:
        pa = PentAIApp()
        
        err_fn = os.path.join(pa.user_data_dir, "err.txt")
        try:
            print "Previous crash:"
            with open(err_fn) as err_log:
                print err_log.readlines()
            a = c
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

