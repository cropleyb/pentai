
from persistent import Persistent
from kivy.animation import Animation
from kivy.clock import Clock

from pentai.base.defines import *

BRIGHT_GREEN = (0.4, 3, 0.5, 1)
FLASH_TIME = 0.5

# To prevent unwanted garbage disposal
all_highlights = {}
foo = []
orig_colour_for_id = {}

def stop_all_highlights():
    for id, highlight in all_highlights.iteritems():
        widget = highlight.widget
        highlight.anim.stop(widget)
        widget.background_color = orig_colour_for_id[id]
    global all_highlights
    all_highlights = {}

class Highlight(object):
    def __init__(self, widget, initial_wait=0.1):
        self.widget = widget
        self.finished = False
        self.set_orig_colour()
        self.getting_brighter = True
        Clock.schedule_once(self.change_colour, initial_wait)

        all_highlights[widget.my_id] = self


    def set_orig_colour(self):
        w = self.widget
        w_id = w.my_id

        global orig_colour_for_id
        try:
            print "using %s for %s" % (w.background_color, w_id)
            self.orig_colour = orig_colour_for_id[w_id]
        except KeyError:
            print "setting %s to %s" % (w_id, w.background_color)
            self.orig_colour = orig_colour_for_id[w_id] = w.background_color

    def stop(self, *ignored):
        self.finished = True
        self.anim.stop(self.widget)
        Clock.schedule_once(self._revert_anim, FLASH_TIME + 2.0)

    def _revert_anim(self, *ignored):
        self.widget.background_color = self.orig_colour

    def change_colour(self, *ignored):
        try:
            if not self.finished:
                new_colour = BRIGHT_GREEN
                if self.getting_brighter:
                    new_colour = self.orig_colour
                self.getting_brighter ^= True

                self.anim = Animation(background_color=new_colour,
                        duration=FLASH_TIME)
                self.anim.start(self.widget)
                Clock.schedule_once(self.change_colour, FLASH_TIME)
        except ReferenceError:
            return

class Guide(Persistent):

    def __init__(self):
        self.suggestions = {}

    def start(self, app):
        self.suggestions = sugg = {}
        global the_app
        the_app = app
        # Real: sugg["Menu"] = ["0:rules_demo_id", "1:new_game_id", "1:human_players_id", "1:settings_id"]
        sugg["Menu"] = ["1:human_players_id", "1:settings_id"]
        # sugg["Setup"] = ["1:help_id", "1:start_game_id", "1:wpl_id", "1:beatrice", "1:start_game_id"] # TODO: Beatrice etc.
        sugg["Setup"] = ["1:help_id", "1:start_game_id", "1:wpl_id"]
        sugg["GameSetupHelp"] = ["3:return_id"]
        sugg["Pente"] = ["0:help_id", "G:rematch_id", "G:menu_id"]
        sugg["PenteHelp"] = ["3:return_id"]
        sugg["Human"] = ["F:name_id", "0:menu_id"]
        sugg["HumanHelp"] = ["3:return_id"]
        sugg["Load"] = ["3:help_id", "3:menu_id"]
        sugg["LoadHelp"] = ["3:return_id"]
        sugg["AI"] = ["0:help_id", "F:name_id", "3:menu_id"]
        sugg["AIHelp"] = ["3:return_id"]
        sugg["Settings"] = ["3:help_id", "3:return_id"]
        sugg["SettingsHelp"] = ["3:return_id"]

        for sn in sugg.iterkeys():
            if sn != "Pente":
                self.setup_hooks(sn)

    def on_enter(self, screen_name):
        self.stop()
        
        global current_screen_name
        current_screen_name = screen_name

        if screen_name != "Pente":
            screen = the_app.get_screen(screen_name)
            remaining = self.suggestions[screen_name]
            self.start_activation(remaining, screen)

    def on_pente_panel_switch(self, parent):
        remaining = self.suggestions["Pente"]

        global active_panel
        active_panel = parent

        self.check_for_finished_game()
        self.start_activation(remaining, parent)

    def on_end_of_game(self):
        global end_reached
        end_reached = True

        self.check_for_finished_game()

    def check_for_finished_game(self):
        if current_screen_name == "Pente":
            if waiting_for_end_of_game and end_reached:
                id = waiting_for_end_of_game
                widget = active_panel.ids[id]
                self.activate(widget)

    def start_activation(self, remaining, parent):
        try:
            # Clicking on the suggestion should remove it from the list
            activation_str = remaining[0]
            start_time, widget_id_text = activation_str.split(':')
            if start_time == "F":
                start_time = 0

            widget = parent.ids[widget_id_text]
            widget.my_id = widget_id_text

            if start_time == "G":
                # Trigger by end of game
                global waiting_for_end_of_game
                waiting_for_end_of_game = widget_id_text
            else:
                Clock.schedule_once(lambda dt: self.activate(widget), float(start_time))

        except KeyError:
            pass
        except IndexError:
            pass

    def on_leave(self):
        self.stop()

    def stop(self):
        print "guide stop"

        global waiting_for_end_of_game
        waiting_for_end_of_game = None

        global end_reached
        end_reached = False

        try:
            global highlighted
            highlighted.stop()
            highlighted = None
        except NameError:
            pass
        except AttributeError:
            pass

        stop_all_highlights()

    def setup_pente_panel_hooks(self, parent):
        remaining_for_screen = self.suggestions["Pente"]

        for activation_str in remaining_for_screen:
            trigger_time, widget_id_text = activation_str.split(':')
            try:
                w = parent.ids[widget_id_text]
            except KeyError:
                continue
            w.bind(on_press=self.on_press) 


    def setup_hooks(self, screen_name):
        remaining_for_screen = self.suggestions[screen_name]
        screen = the_app.get_screen(screen_name)
        for activation_str in remaining_for_screen:
            trigger_time, widget_id_text = activation_str.split(':')
            w = screen.ids[widget_id_text]
            w.bind(on_press=self.on_press) 

            if trigger_time == "F":
                # Stop when the focus on the text input
                w.bind(on_focus=self.on_focus)
                
                # TODO. Hack that doesn't work
                global foo
                foo.append(w)

    def on_focus(self, widget, *args):
        try:
            widget_id = widget.my_id
        except AttributeError:
            return

        self.unhighlight(widget_id)

    def on_press(self, widget, *args):
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
