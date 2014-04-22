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
        self.sw.size_hint_x = .1
        gl.add_widget(self.sw)

        self.load_value()
        self.sw.bind(active=self.save_value)                  

        # TODO?
        #l = Label() # Padding
        #sw.size_hint_x = .02
        #gl.add_widget(l)

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
        gl.add_widget(sl)

        self.sp = sp = Spinner()
        sp.values = self.values
        sp.font_size = my.dp(20)
        sp.option_cls = MySpinnerOption
        gl.add_widget(sp)

        dl = TinyLabel(text=self.desc)
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
        
        self.size_hint_y = .45
       
    def setup(self, ignored):
        #gl = GridLayout(rows=1)
        #self.add_widget(gl)

        sl = SmallLabel(text=self.text)
        #gl.add_widget(sl)
        self.add_widget(sl)

        gl = GridLayout(rows=1)
        self.add_widget(gl)

        l = Label(size_hint_x=0.05)
        gl.add_widget(l)

        self.slider = slider = Slider()
        slider.min = self.min
        slider.max = self.max
        slider.step = self.step
        #slider.id = "s_id"
        gl.add_widget(slider)

        self.display = Label()
        self.display.size_hint_x = 0.15
        #display.text = str(self.value)
        #display.text = "%.1f" % s_id.value
        gl.add_widget(self.display)

        dl = TinyLabel(text=self.desc)
        self.add_widget(dl)

        self.slider.bind(value=self.save_value)                  
        self.slider.bind(value=self.display_value)
        self.load_value()

    def load_value(self):
        self.slider.value = self.get_config().getfloat('PentAI', self.key)

    def save_value(self, switch, val):
        self.value = val
        self.get_config().set('PentAI', self.key, val)
        self.get_config().write()

    def display_value(self, slider, val):
        v = val
        if self.display_factor == 100:
            self.display.text = "%d%%" % int(100 * val)
        else:
            self.display.text = "%.1fs" % val

