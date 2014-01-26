from kivy.uix.screenmanager import Screen
#from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.properties import ListProperty

class PlayerScreen(Screen):
    players = ListProperty(["Hugo", "Vladimir"])

    def __init__(self, *args, **kwargs):
        super(PlayerScreen, self).__init__(*args, **kwargs)

    # TODO
