from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import *

from pentai.base.defines import *
import pentai.base.logger as log

class BigCheckBox(CheckBox):
    pass

class CheckBoxRow(GridLayout):
    value = StringProperty("")
    group = StringProperty("")

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.parent.set_active(self.value)
            return True
        return False

class CheckBoxList(GridLayout):
    text = StringProperty("")
    group = StringProperty("")
    values = ListProperty([""])
    val = StringProperty("")

    def __init__(self, *args, **kwargs):
        self.cols = 1
        self.widgets_by_val = {}

        super(CheckBoxList, self).__init__(*args, **kwargs)

        # The properties haven't been initialised yet (for self.values)
        Clock.schedule_once(self.setup, 0)

    def setup(self, ignored):
        for v in self.values:
            row = CheckBoxRow(value=v, group=self.group)
            self.add_widget(row)
            self.widgets_by_val[v] = row.children[1]

    def set_active(self, val):
        """ Set the active value from anywhere. """

        val = str(val)
        for key,widget in self.widgets_by_val.items():
            widget.active = (key == val)

        self.val = str(val)

