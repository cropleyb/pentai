from pentai.gui.kivy_gui_main import *
'''
'KIVY_DPI'
'KIVY_METRICS_DENSITY'
'KIVY_METRICS_FONTSCALE'
'''

import pentai.db.persistent_dict as pd_m

import os

if __name__ == '__main__':
    '''
    import pentai.base.bit_reverse as br_m
    print "bit_reverse imported!"
    import pentai.ai.alpha_beta as ab_m
    print "alpha_beta imported!"
    import pentai.ai.priority_filter as pf_m
    print "priority_filter imported!"
    import pentai.ai.length_lookup_table as llt_m
    print "llt imported!"
    import pentai.ai.utility_stats as us_m
    print "us imported!"
    import pentai.ai.utility_calculator as uc_m
    print "uc imported!"
    import pentai.ai.ab_state as abs_m
    print "ab_state imported!"
    '''

    Config.set('kivy', 'log_level', 'info')
    Config.set('kivy', 'log_enable', 1)
    Config.set('kivy', 'log_dir', 'logs')
    Config.set('kivy', 'log_name', 'kivy_%y-%m-%d_%_.txt')

    Config.set('graphics', 'width', '457')
    Config.set('graphics', 'height', '720')

    try:
        pentai_path = os.environ['PENTAIPATH']
    except KeyError:
        pentai_path = None

    try:
        pa = PentAIApp()

        if pentai_path == None:
            pentai_path = pa.user_data_dir
        pd_m.base_dir = pentai_path
        
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

