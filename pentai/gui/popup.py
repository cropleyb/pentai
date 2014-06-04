from kivy.uix.popup import *
from kivy.properties import StringProperty
from kivy.clock import Clock

import audio as a_m

#from defines import *

class BasePopup(Popup):
    """ There should only be one active popup at a time. """

    my_active = None

    def __init__(self, *args, **kwargs):
        super(BasePopup, self).__init__(*args, **kwargs)

    @staticmethod
    def confirm():
        if BasePopup.my_active != None:
            BasePopup.my_active.ok_confirm()

    def ok_confirm(self):
        if BasePopup.my_active != None:
            a_m.instance.click()
            BasePopup.my_active = None
            self.dismiss()
        return True

    @staticmethod
    def is_active():
        return not BasePopup.my_active is None

    @staticmethod
    def clear():
        a = BasePopup.my_active
        BasePopup.my_active = None
        a.dismiss()

    def on_open(self):
        BasePopup.my_active = self 

class MessagePopup(BasePopup):
    """ Message Popup is for errors and help so far.
        Click anywhere to dismiss. """

    def __init__(self, timeout_val=None, *args, **kwargs):
        self.auto_dismiss = True
        self.going = False

        if timeout_val:
            Clock.schedule_once(self.timeout, timeout_val)
        super(MessagePopup, self).__init__(*args, **kwargs)
    
    def on_touch_down(self, touch):
        if not touch.is_mouse_scrolling:
            self.going = True
            return True
        return super(BasePopup, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if not touch.is_mouse_scrolling:
            if self.going:
                self.ok_confirm()
            self.going = not self.going
            return True
        return super(BasePopup, self).on_touch_up(touch)

    def timeout(self, dt):
        self.ok_confirm()

class ConfirmPopup(BasePopup):
    """ ConfirmPopup is for True/False confirmation popup with a message """
    confirm_prompt = StringProperty("")

    def __init__(self, message, action, *args, **kwargs):
        self.auto_dismiss = False
        self.title = "" # I don't like the default :)
        self.confirm_prompt = message
        self.action = action
        super(ConfirmPopup, self).__init__(*args, **kwargs)

    bypass = True

    @staticmethod
    def create_and_open(message, action, force=False, *args, **kwargs):
        if ConfirmPopup.bypass and not force:
            action()
            return
        if BasePopup.my_active == None:
            # TODO: Do we dismiss any existing popup?
            BasePopup.my_active = \
                ConfirmPopup(*args, message=message,
                        action=action, **kwargs)
            BasePopup.my_active.open()

    def ok_confirm(self):
        if super(ConfirmPopup, self).ok_confirm():
            self.action()
