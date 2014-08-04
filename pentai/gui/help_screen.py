from kivy.uix.screenmanager import Screen

class HelpScreen(Screen):
    def on_pre_enter(self):
        self.set_text()

