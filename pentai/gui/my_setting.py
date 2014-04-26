from kivy.uix.gridlayout import GridLayout
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.clock import Clock

from kivy.properties import *
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.config import Config

import pentai.gui.scale as my

class SmallLabel(Label):
    pass
class TinyLabel(Label):
    pass


class MySetting(GridLayout):
    text = StringProperty("Unset Text")
    desc = StringProperty("Unset Desc")
    key = StringProperty("Unset Key")
    value = StringProperty("Unset Value")

    def __init__(self, *args, **kwargs):
        super(MySetting, self).__init__(*args, **kwargs)
        
        self.cols = 1
        self.size_hint_y = .3

        # The properties haven't been initialised yet
        Clock.schedule_once(self.setup, 0)

    def get_config(self):
        # TODO: Eliminate Hack
        return self.parent.parent.config

class SwitchSetting(MySetting):
    def setup(self, ignored):
        gl = GridLayout(rows=1)
        self.add_widget(gl)

        sl = SmallLabel(text=self.text)
        gl.add_widget(sl)

        self.sw = Switch()
        self.sw.size_hint_x = .35
        self.sw.align = "center"
        gl.add_widget(self.sw)

        self.load_value()
        self.sw.bind(active=self.save_value)                  

        dl = TinyLabel(text=self.desc)
        self.add_widget(dl)

    def load_value(self):
        self.sw.active = self.get_config().getint('PentAI', self.key)

    def save_value(self, switch, val):
        self.get_config().set('PentAI', self.key, int(val))
        self.get_config().write()

class MySpinnerOption(SpinnerOption):
    def __init__(self, *args, **kwargs):
        super(MySpinnerOption, self).__init__(*args, **kwargs)
        self.font_size = my.dp(20)

class OptionsSetting(MySetting):
    values = ListProperty([])

    def setup(self, ignored):
        gl = GridLayout(rows=1)
        self.add_widget(gl)

        sl = SmallLabel(text=self.text)
        sl.valign = "middle"
        gl.add_widget(sl)

        self.sp = sp = Spinner()
        sp.values = self.values
        sp.valign = 'bottom'
        sp.size_hint_x = .5
        sp.font_size = my.dp(20)
        sp.option_cls = MySpinnerOption
        gl.add_widget(sp)

        # Padding only.
        l = Label()
        l.size_hint_x = .05
        gl.add_widget(l)

        dl = TinyLabel(text=self.desc)
        dl.size_hint_y = .8
        self.add_widget(dl)

        self.load_value()
        self.sp.bind(text=self.save_value)                  

    def load_value(self):
        self.sp.text = self.get_config().get('PentAI', self.key)

    def save_value(self, switch, val):
        self.get_config().set('PentAI', self.key, val)
        self.get_config().write()

class SliderSetting(MySetting):
    value = NumericProperty()
    min = NumericProperty()
    max = NumericProperty()
    step = NumericProperty()
    display_factor = NumericProperty(1)

    def __init__(self, *args, **kwargs):
        super(SliderSetting, self).__init__(*args, **kwargs)
        
        self.size_hint_y = .35
       
    def setup(self, ignored):
        sl = SmallLabel(text=self.text)
        self.add_widget(sl)

        gl = GridLayout(rows=1)
        self.add_widget(gl)

        l = Label(size_hint_x=0.05)
        gl.add_widget(l)

        self.slider = slider = Slider()
        slider.min = self.min
        slider.max = self.max
        slider.step = self.step
        gl.add_widget(slider)

        self.display = Label()
        self.display.size_hint_x = 0.2
        gl.add_widget(self.display)

        dl = TinyLabel(text=self.desc)
        self.add_widget(dl)

        self.slider.bind(value=self.save_value)                  
        self.slider.bind(value=self.display_value)

        # This call should not be necessary, Kivy bug (value 0 not being passed through bind)?
        self.display_value()

        self.load_value()

    def load_value(self):
        self.slider.value = self.get_config().getfloat('PentAI', self.key)

    def save_value(self, switch, val):
        self.get_config().set('PentAI', self.key, val)
        self.get_config().write()

        # Set value last so observers of self.value can use config.
        self.value = val

    def display_value(self, *unused):
        v = self.slider.value
        if self.display_factor == 100:
            self.display.text = "%d%%" % int(100 * v)
        else:
            self.display.text = "%.1fs" % v

