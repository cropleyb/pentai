from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.clock import Clock

from kivy.properties import *
from pentai.base.defines import *

class ClickLabel(Label):
    def __init__(self, *args, **kwargs):
        self.register_event_type('on_press')
        return super(ClickLabel, self).__init__(*args, **kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.dispatch('on_press')
            return True
        return super(ClickLabel, self).on_touch_down(touch)

    def on_press(self):
        pass

class CheckBoxList(GridLayout):
    text = StringProperty("")
    group = StringProperty("")
    values = ListProperty([])
    val = StringProperty("")

    def __init__(self, *args, **kwargs):
        self.cols = 1

        super(CheckBoxList, self).__init__(*args, **kwargs)

        # The properties haven't been initialised yet
        Clock.schedule_once(self.setup, 0)

    def setup(self, ignored):
        vals_gl = GridLayout(cols=3)
        self.add_widget(vals_gl)
        self.widgets_by_val = {}

        first = True
        for v in self.values:
            l = ClickLabel(text=v)
            l.bind(on_press=self.label_clicked)
            vals_gl.add_widget(l)

            cb = CheckBox(group=self.group, active=first, size_hint_x=0.1)
            cb.bind(active=self.on_checkbox_active)
            cb.val = v
            if first:
                self.on_checkbox_active(cb, None)
            vals_gl.add_widget(cb)
            self.widgets_by_val[v] = cb

            # This is just padding
            l2 = Label(size_hint_x=0.2)
            vals_gl.add_widget(l2)

            first = False

    def label_clicked(self, l):
        log.debug("CheckBoxList: label_clicked")
        self.set_active(l.text)

    def on_checkbox_active(self, checkbox, value):
        log.debug("CheckBoxList: on_checkbox_active")
        if checkbox.active:
            log.debug("CheckBoxList: on_checkbox_active True")
            self.val = checkbox.val

    def set_active(self, val):
        """ Set the active value from other python code. """
        log.debug("CheckBoxList: set_active")
        old = self.widgets_by_val[str(self.val)]
        old.active = False

        w = self.widgets_by_val[str(val)]
        w.active = True
        self.val = str(val)

