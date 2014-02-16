
from kivy.uix.button import Button
import audio as a_m

class MyButton(Button):
    def on_touch_down(self, *args, **kwargs):
        a_m.instance.click()
        super(MyButton, self).on_touch_down(*args, **kwargs)

