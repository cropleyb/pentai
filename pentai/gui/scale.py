
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.event import EventDispatcher

class Scale(EventDispatcher):
    dp = NumericProperty(1.0)

    def __init__(self):
        Window.bind(height=self.set_height)

    def set_height(self, provider, height):
        try:
            self.dp = height / 720.0
        except ReferenceError, e:
            # Not sure what is causing this, but it seems ok to just ignore it.
            pass

MyScale = Scale()

