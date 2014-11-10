
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.event import EventDispatcher

class Scale(EventDispatcher):
    dp = NumericProperty(1.0)

    def __init__(self):
        Window.bind(height=self.set_height)

    def set_height(self, provider, height):
        self.dp = height / 720.0

MyScale = Scale()

dp = MyScale.dp

