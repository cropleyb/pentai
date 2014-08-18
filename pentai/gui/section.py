from kivy.uix.gridlayout import GridLayout
#from kivy.uix.label import Label
from kivy.properties import *

from pentai.base.defines import *
#import pentai.base.logger as log

class Section(GridLayout):
    title = StringProperty("")
    text = StringProperty("")

    def __init__(self, *args, **kwargs):
        self.cols = 1

        super(GridLayout, self).__init__(*args, **kwargs)

