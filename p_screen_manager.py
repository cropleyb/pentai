from kivy.uix.screenmanager import *

class PScreenManager(ScreenManager):
    def __init__(self, *args, **kwargs):
        self.demo_mode = False
        super(PScreenManager, self).__init__(*args, **kwargs)

    def set_demo_mode(self, val):
        self.demo_mode = val

    def on_touch_down(self, *args, **kwargs):
        if self.demo_mode:
            print "ON TOUCH DOWN IGNORED"
        else:
            return super(PScreenManager, self).on_touch_down(*args, **kwargs)
    
    def on_touch_move(self, *args, **kwargs):
        if self.demo_mode:
            print "ON TOUCH MOVE IGNORED"
        else:
            return super(PScreenManager, self).on_touch_move(*args, **kwargs)
    
    def on_touch_up(self, *args, **kwargs):
        if self.demo_mode:
            print "ON TOUCH UP IGNORED"
        else:
            return super(PScreenManager, self).on_touch_up(*args, **kwargs)
    
