
from kivy.uix.button import Button
import audio as a_m

class MyButton(Button):
    def on_touch_up(self, *args, **kwargs):
        if not hasattr(self, "silent"):
            a_m.instance.click()
        super(MyButton, self).on_touch_up(*args, **kwargs)

    def sim_press(self):
        self.state = "down"

    def sim_release(self):
        self.state = "normal"
        if not hasattr(self, "silent"):
            a_m.instance.click()


