from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.clock import Clock

from kivy.properties import *

class CheckBoxList(GridLayout):
    text = StringProperty("")
    group = StringProperty("")
    values = ListProperty([])
    val = StringProperty("")

    def __init__(self, *args, **kwargs):

        super(CheckBoxList, self).__init__(*args, **kwargs)

        # The properties haven't been initialised yet
        Clock.schedule_once(self.setup, 0)

    def setup(self, ignored):
        l = Label(text=self.text)
        self.add_widget(l)
        vals_gl = GridLayout(cols=2)
        self.add_widget(vals_gl)
        self.widgets_by_val = {}

        first = True
        for v in self.values:
            l = Label(text=v, halign="left", padding_x=20)
            vals_gl.add_widget(l)

            cb = CheckBox(group=self.group, active=first)
            cb.bind(active=self.on_checkbox_active)
            cb.val = v
            if first:
                self.on_checkbox_active(cb, None)
            vals_gl.add_widget(cb)
            self.widgets_by_val[v] = cb

            first = False

    def on_checkbox_active(self, checkbox, value):
        if checkbox.active:
            self.val = checkbox.val


    def set_active(self, val):
        """ Set the active value from other python code. """
        old = self.widgets_by_val[str(self.val)]
        old.active = False

        w = self.widgets_by_val[str(val)]
        w.active = True
        self.val = str(val)

