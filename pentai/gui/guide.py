
from persistent import Persistent
from kivy.animation import Animation
from kivy.clock import Clock

from pentai.base.defines import *

BRIGHT_GREEN = (0.4, 3, 0.5, 1)
FLASH_TIME = 0.5

# To prevent unwanted garbage disposal
all_highlights = set()

class Highlight(object):
    def __init__(self, widget, initial_wait=0.1):
        self.widget = widget
        self.finished = False
        self.orig_colour = widget.background_color
        Clock.schedule_once(self.go_brighter, initial_wait)
        all_highlights.add(self)

    def stop(self, *ignored):
        self.finished = True
        Clock.schedule_once(self._revert_anim, FLASH_TIME + 2)

    def _revert_anim(self, *ignored):
        self.widget.background_color = self.orig_colour
        all_highlights.remove(self)

    def go_brighter(self, *ignored):
        if not self.finished:
            anim = Animation(background_color=BRIGHT_GREEN,
                    duration=FLASH_TIME)
            anim.start(self.widget)
            Clock.schedule_once(self.go_dimmer, FLASH_TIME)

    def go_dimmer(self, *ignored):
        if not self.finished:
            anim = Animation(background_color=self.orig_colour,
                    duration=FLASH_TIME)
            anim.start(self.widget)
            Clock.schedule_once(self.go_brighter, FLASH_TIME)


class Guide(Persistent):

    def __init__(self):
        self.suggestions = {}

    def start(self, app):
        self.suggestions = sugg = {}
        global the_app
        the_app = app
        sugg["Menu"] = ["0:rules_demo_id", "1:new_game_id", "1:human_players_id", "1:settings_id"]
        # sugg["Setup"] = ["1:help_id", "1:start_game_id", "1:wpl_id", "1:beatrice", "1:start_game_id"] # TODO: Beatrice etc.
        sugg["Setup"] = ["1:help_id", "1:start_game_id", "1:wpl_id"]
        sugg["GameSetupHelp"] = ["3:return_id"]
        # sugg["Pente"] = ["G:rematch", "G:menu"] # TODO: Not created initially
        sugg["PenteHelp"] = ["3:return_id"]
        sugg["Human"] = ["0:name_id", "0:menu_id"]
        sugg["HumanHelp"] = ["3:return_id"]
        sugg["Load"] = ["3:help_id", "3:menu_id"]
        sugg["LoadHelp"] = ["3:return_id"]
        sugg["AI"] = ["0:help_id", "0:name_id", "3:menu_id"]
        sugg["AIHelp"] = ["3:return_id"]
        sugg["Settings"] = ["3:help_id", "3:return_id"]
        sugg["SettingsHelp"] = ["3:return_id"]

        for sn in sugg.iterkeys():
            self.setup_hooks(sn)

    def on_enter(self, screen_name):
        self.stop()

        global current_screen_name
        current_screen_name = screen_name
        try:
            # Clicking on the suggestion should remove it from the list
            remaining_for_screen = self.suggestions[screen_name]
            activation_str = remaining_for_screen[0]
            screen = the_app.get_screen(screen_name)
            trigger_time, widget_id_text = activation_str.split(':')
            widget = screen.ids[widget_id_text]
            widget.my_id = widget_id_text
            if trigger_time != "G":
                Clock.schedule_once(lambda dt: self.activate(widget), float(trigger_time))
            # TODO: Trigger by end of game

        except KeyError:
            #st()
            print "No suggestions for %s" % screen_name
        except IndexError:
            #st()
            print "No more suggestions for %s" % screen_name

    def on_leave(self):
        self.stop()

    def stop(self):
        print "guide stop"
        try:
            global highlighted
            highlighted.stop()
            highlighted = None
        except NameError:
            pass
        except AttributeError:
            pass

    def setup_hooks(self, screen_name):
        remaining_for_screen = self.suggestions[screen_name]
        screen = the_app.get_screen(screen_name)
        for activation_str in remaining_for_screen:
            trigger_time, widget_id_text = activation_str.split(':')
            w = screen.ids[widget_id_text]
            w.bind(on_press=self.on_press) 

    def on_press(self, widget):
        try:
            widget_id = widget.my_id
        except AttributeError:
            return

        self.unhighlight(widget_id)

    def unhighlight(self, widget_id):

        remaining_for_screen = self.suggestions[current_screen_name]

        found = None
        for rem in remaining_for_screen:
            if widget_id in rem:
                found = rem
                break

        if not found:
            return

        remaining_for_screen.remove(found)

        try:
            global highlighted
            if highlighted.widget.my_id == widget_id:
                highlighted.stop()
        except NameError:
            pass
        except AttributeError:
            pass

    def activate(self, widget):
        global highlighted
        highlighted = Highlight(widget)
