import kivy.core.window
import pentai.db.zodb_dict as z_m

from pentai.gui.screen import Screen

class GoodByeScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(GoodByeScreen, self).__init__(*args, **kwargs)
        print "init goodbye screen"

    def on_enter(self, *args, **kwargs):
        app = self.app
        app_width, app_height = kivy.core.window.Window.size

        app.config.set("PentAI", "app_width", str(app_width))
        app.config.set("PentAI", "app_height", str(app_height))
        app.config.write()

        z_m.sync()
        z_m.pack()

        self.on_pre_leave()
        self.on_leave()

        app.stop()
