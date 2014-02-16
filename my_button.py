
from kivy.uix.button import Button
import audio as a_m

class MyButton(Button):
    def on_touch_up(self, *args, **kwargs):
        a_m.instance.click()
        super(MyButton, self).on_touch_up(*args, **kwargs)

