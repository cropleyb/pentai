from pentai.db.zodb_dict import *
from kivy.animation import Animation
from kivy.clock import Clock

from pentai.base.defines import *

BRIGHT_GREEN = (0.4, 3, 0.5, 1)
FLASH_TIME = 0.5

# To prevent unwanted garbage disposal
all_highlights = {}

# Prevent overwriting the default colour
orig_colour_for_id = {}

# Prevent duplicate initialisation
screens_visited = set()

def stop_all_highlights():
    for id, highlight in all_highlights.iteritems():
        widget = highlight.widget
        try:
            anim = highlight.anim.stop(widget)
        except AttributeError:
            pass
        widget.background_color = orig_colour_for_id[id]
    global all_highlights
    all_highlights = {}

class Highlight(object):
    def __init__(self, widget, initial_wait=0.1):
        self.widget = widget
        self.finished = False
        self.save_orig_colour()
        self.getting_brighter = True
        Clock.schedule_once(self.change_colour, initial_wait)

        all_highlights[widget.my_id] = self

    def save_orig_colour(self):
        w = self.widget
        w_id = w.my_id

        global orig_colour_for_id
        try:
            self.orig_colour = orig_colour_for_id[w_id]
        except KeyError:
            self.orig_colour = orig_colour_for_id[w_id] = w.background_color

    def stop(self, *ignored):
        self.finished = True
        self.anim.stop(self.widget)
        self._revert_anim()
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

    def reset(self, app):
        self.suggestions = sugg = ZM()
        global the_app
        the_app = app

        sugg["Menu"]          = ZL(["0:rules_demo_id", "1:new_game_id", "1:human_players_id", "1:new_game_id", "1:settings_id", "1:new_game_id", "1:ai_players_id"])
        # sugg["Setup"]         = ZL(["1:help_id", "1:start_game_id", "1:wpl_id", "0:Beatrice_id", "1:start_game_id", "1:wpl_id", "0:Claude_id", "1:start_game_id"])
        sugg["Setup"]         = ZL(["1:wpl_id", "0:Beatrice_id", "1:start_game_id", "1:wpl_id", "0:Claude_id", "1:start_game_id"])
        sugg["GameSetupHelp"] = ZL(["3:return_id"])
        sugg["Pente"]         = ZL(["0:help_id", "G:rematch_id", "G:menu_id"])
        sugg["PenteHelp"]     = ZL(["15:return_id"])
        sugg["Human"]         = ZL(["F:name_id", "4:menu_id"])
        sugg["HumanHelp"]     = ZL(["5:return_id"])
        sugg["Load"]          = ZL(["3:help_id", "3:menu_id"])
        sugg["LoadHelp"]      = ZL(["10:return_id"])
        sugg["AI"]            = ZL(["0:help_id", "F:player_spinner_id", "0:*nemesis*_id", "3:menu_id"])
        sugg["AIHelp"]        = ZL(["20:return_id"])
        sugg["Settings"]      = ZL(["3:help_id", "3:return_id"])
        sugg["SettingsHelp"]  = ZL(["30:return_id"])

    def setup_spinner_hooks(self, screen_name):
        screen = the_app.get_screen(screen_name)
        screen.updated_players = \
            lambda: self.activate_from_remaining(screen_name)

    def updated_players(self):
        """ This is a bit of a hack; most buttons cause a change of screen,
            but this one doesn't. """
        Clock.schedule_once(lambda dt: self.activate_from_remaining("Setup"), 0.2)

    def on_enter(self, screen_name):
        self.setup_spinner_hooks(screen_name)

        self.stop()
        
        global current_screen_name
        current_screen_name = screen_name
        
        if screen_name != "Pente":
            self.setup_hooks(screen_name)
            self.activate_from_remaining(screen_name)

    def activate_from_remaining(self, screen_name):
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

            try:
                widget = parent.ids[widget_id_text]
            except KeyError:
                widget = parent.text_to_widget[widget_id_text]

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

        bound = set()
        for activation_str in remaining_for_screen:
            trigger_time, widget_id_text = activation_str.split(':')
            try:
                w = parent.ids[widget_id_text]
            except KeyError:
                continue
            if not widget_id_text in bound:
                w.bind(on_press=self.on_press) 
                bound.add(widget_id_text)

    def setup_hooks(self, screen_name):
        if screen_name in screens_visited:
            return
        if screen_name != "Pente":
            # Pente screen is sometimes recreated when reentered.
            screens_visited.add(screen_name)

        remaining_for_screen = self.suggestions[screen_name]
        screen = the_app.get_screen(screen_name)
        bound = set()
        for activation_str in remaining_for_screen:
            trigger_time, widget_id_text = activation_str.split(':')
            try:
                w = screen.ids[widget_id_text]
            except KeyError:
                w = screen.text_to_widget[widget_id_text]
            w.my_id = widget_id_text

            if not widget_id_text in bound:
                w.bind(on_press=self.on_press) 
                bound.add(widget_id_text)

            if trigger_time == "F":
                # TODO: This should work, but doesn't:
                # w.bind(on_focus=self.on_focus)
                screen.set_focus_callback(self.on_focus)

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
