from kivy.uix.popup import *
from kivy.properties import StringProperty

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
        BasePopup.my_active = None
        self.dismiss()
        return True

    @staticmethod
    def clear():
        a = BasePopup.my_active
        BasePopup.my_active = None
        a.dismiss()

    def on_open(self):
        BasePopup.my_active = self 

class MessagePopup(BasePopup):
    """ Message Popup is for errors so far. Click anywhere to dismiss. """

    def __init__(self, *args, **kwargs):
        self.auto_dismiss = True
        self.going = False
        super(MessagePopup, self).__init__(*args, **kwargs)
    
    def on_touch_down(self, touch):
        self.going = True
        return True

    def on_touch_up(self, touch):
        if self.going:
            self.ok_confirm()
        self.going = not self.going
        return super(BasePopup, self).on_touch_up(touch)

class ConfirmPopup(BasePopup):
    """ ConfirmPopup is for True/False confirmation popup with a message """
    confirm_prompt = StringProperty("")

    def __init__(self, message, action, *args, **kwargs):
        self.auto_dismiss = False
        self.title = "" # I don't like the default :)
        self.confirm_prompt = message
        self.action = action
        super(ConfirmPopup, self).__init__(*args, **kwargs)

    @staticmethod
    def create_and_open(message, action, *args, **kwargs):
        if BasePopup.my_active == None:
            # TODO: Do we dismiss any existing popup?
            BasePopup.my_active = \
                ConfirmPopup(*args, message=message,
                        action=action, **kwargs)
            BasePopup.my_active.open()

    def ok_confirm(self):
        if super(ConfirmPopup, self).ok_confirm():
            self.action()
