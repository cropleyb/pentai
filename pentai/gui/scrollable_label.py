from kivy.uix.scrollview import *
from kivy.properties import StringProperty

class ScrollableLabel(ScrollView):
    text = StringProperty('')

    def __init__(self, *args, **kwargs):
        super(ScrollableLabel, self).__init__(*args, **kwargs)

# HACK until kivy fixed
class MenuScrollableLabel(ScrollView):
    text1 = StringProperty('')
    text2 = StringProperty('')
    text3 = StringProperty('')
    text4 = StringProperty('')
    text5 = StringProperty('')
    text6 = StringProperty('')

    def __init__(self, *args, **kwargs):
        super(MenuScrollableLabel, self).__init__(*args, **kwargs)

