from kivy.animation import Animation
from kivy.clock import Clock

from pentai.db.zodb_dict import *
import pentai.base.logger as log
from pentai.base.defines import *

BRIGHT_GREEN = (0.4, 3, 0.5, 1)
FLASH_TIME = 0.5

# To prevent unwanted garbage disposal
all_highlights = {}

# Prevent overwriting the default colour
orig_colour_for_id = {}

# Prevent duplicate initialisation
screens_visited = set()

disabled = False

queued_to_highlight = False

def stop_all_highlights():
    global all_highlights
    global queued_to_highlight

    log.debug("in stop_all_highlights")

    queued_to_highlight = False

    for id, highlight in all_highlights.iteritems():
        widget = highlight.widget
        try:
            try:
                anim = highlight.anim.stop(widget)
            except AttributeError:
                pass
            log.debug("resetting colour of %s" % id)
            widget.background_color = orig_colour_for_id[id]
        except ReferenceError:
            pass

    log.debug("Clearing all_highlights")
    all_highlights.clear()

class Highlight(object):
    def __init__(self, widget, initial_wait=0.1):
        print "in Highlight __init__"
        global all_highlights
        self.widget = widget
        self.finished = False
        self.save_orig_colour()
        self.getting_brighter = True
        all_highlights[widget.my_id] = self

        Clock.schedule_once(self.change_colour, initial_wait)

    def save_orig_colour(self):
        w = self.widget
        w_id = w.my_id

        global orig_colour_for_id
        try:
            self.orig_colour = orig_colour_for_id[w_id]
            log.debug("loading orig_colour for %s" % w_id)
        except KeyError:
            log.debug("saving orig colour for %s" % w_id)
            self.orig_colour = orig_colour_for_id[w_id] = w.background_color

    def stop(self, *ignored):
        self.finished = True
        try:
            self.anim.stop(self.widget)
        except ReferenceError:
            pass
        try:
            self._revert_anim()
            Clock.schedule_once(self._revert_anim, FLASH_TIME + 2.0)
        except ReferenceError:
            pass

    def _revert_anim(self, *ignored):
        self.widget.background_color = self.orig_colour

    def change_colour(self, *ignored):
        try:
            if not self.finished:
                new_colour = BRIGHT_GREEN
                if disabled:
                    new_colour = self.orig_colour
                if self.getting_brighter:
                    new_colour = self.orig_colour
                self.getting_brighter ^= True

                self.anim = Animation(background_color=new_colour,
                        duration=FLASH_TIME)
                self.anim.start(self.widget)
                Clock.schedule_once(self.change_colour, FLASH_TIME)
        except ReferenceError:
            log.debug("REFERENCE ERROR in Guide change_colour")
            return

class Guide(Persistent):

    def disable(self):
        # Keep running the Guide, just don't show it, then if they turn it
        # on it won't suggest what they have tried already.
        global disabled
        disabled = True

    def enable(self):
        global disabled
        disabled = False

    def is_enabled(self):
        global disabled
        return not disabled

    def restart(self):
        self.suggestions = sugg = ZM()
        
        sugg["Menu"]          = ZL(["0:rules_demo_id", "1:new_game_id", "1:human_players_id", "1:new_game_id", "1:settings_id", "1:new_game_id", "1:ai_players_id"])
        sugg["Setup"]         = ZL(["1:help_id", "1:start_game_id", "1:wpl_id", "0:Beatrice_id", "1:start_game_id", "1:wpl_id", "0:Claude_id", "1:start_game_id"])
        sugg["GameSetupHelp"] = ZL(["3:return_id"])
        sugg["Pente"]         = ZL(["0:help_id", "G:rematch_id", "G:menu_id", "G:rematch_id", "G:menu_id", "G:rematch_id", "G:menu_id"])
        sugg["PenteHelp"]     = ZL(["15:return_id"])
        sugg["Human"]         = ZL(["F:name_id", "0:menu_id"])
        sugg["HumanHelp"]     = ZL(["5:return_id"])
        sugg["Load"]          = ZL(["3:help_id", "3:menu_id"])
        sugg["LoadHelp"]      = ZL(["10:return_id"])
        sugg["AI"]            = ZL(["0:help_id", "F:player_spinner_id", "0:*nemesis*_id", "3:menu_id"])
        sugg["AIHelp"]        = ZL(["20:return_id"])
        sugg["Settings"]      = ZL(["3:help_id", "3:return_id"])
        sugg["SettingsHelp"]  = ZL(["30:return_id"])

        the_app.set_default_game()

    def setup_spinner_hooks(self, screen_name):
        screen = the_app.get_screen(screen_name)
        screen.updated_players = \
            lambda: self.activate_from_remaining(screen_name)

    def updated_players(self):
        """ This is a bit of a hack; most buttons cause a change of screen,
            but this one doesn't. """
        Clock.schedule_once(lambda dt: self.activate_from_remaining("Setup"), 0.2)

    def on_enter(self, screen_name):
        log.debug("on_enter %s" % screen_name)
        self.setup_spinner_hooks(screen_name)

        self.stop()
        
        global current_screen_name
        current_screen_name = screen_name
        
        if screen_name != "Pente":
            self.setup_hooks(screen_name)
            self.activate_from_remaining(screen_name)

    def activate_from_remaining(self, screen_name):
        screen = the_app.get_screen(screen_name)
        try:
            remaining = self.suggestions[screen_name]
        except KeyError:
            # TODO: Log error
            log.debug("couldn't find screen %s in activate_from_remaining" % screen_name)
            return
        log.debug("activating from remaining %s" % remaining)
        self.start_activation(remaining, screen)

    def on_pente_panel_switch(self, parent):
        try:
            remaining = self.suggestions["Pente"]
        except KeyError:
            log.debug("No Pente suggestions")
            return

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
                try:
                    widget = active_panel.ids[id]
                    self.activate(widget)
                except:
                    log.debug("Can't activate unknown id after finished game: %s" % id)
                    return

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
        log.debug("In guide.on_leave()")
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
        except ReferenceError:
            pass
        except NameError:
            pass
        except AttributeError:
            pass

        stop_all_highlights()

    def setup_pente_panel_hooks(self, parent):
        try:
            remaining_for_screen = self.suggestions["Pente"]
        except KeyError:
            log.debug("WARNING: No Pente suggestions to setup hooks")
            return

        bound = set()
        for activation_str in remaining_for_screen:
            trigger_time, widget_id_text = activation_str.split(':')
            try:
                w = parent.ids[widget_id_text]
            except KeyError:
                log.debug("WARNING: Pente: No such id: %s" % widget_id_text)
                #st()
                continue
            if not widget_id_text in bound:
                w.bind(on_press=self.on_press) 
                bound.add(widget_id_text)

    def setup_hooks(self, screen_name):
        if screen_name in screens_visited:
            log.debug("WARNING: Screen %s has already been visited" % screen_name)
        if screen_name != "Pente":
            # Pente screen is sometimes recreated when reentered.
            screens_visited.add(screen_name)

        try:
            remaining_for_screen = self.suggestions[screen_name]
        except KeyError:
            log.debug("No suggestions left for %s" % screen_name)
            return

        screen = the_app.get_screen(screen_name)
        bound = set()
        for activation_str in remaining_for_screen:
            trigger_time, widget_id_text = activation_str.split(':')
            try:
                w = screen.ids[widget_id_text]
            except KeyError:
                try:
                    w = screen.text_to_widget[widget_id_text]
                except:
                    log.debug("WARNING: Guide could not find %s" % widget_id_text)
                    continue
            w.my_id = widget_id_text

            if not widget_id_text in bound:
                w.bind(on_press=self.on_press) 
                bound.add(widget_id_text)
            else:
                log.debug("Widget %s is already bound" % widget_id_text)

    def set_state(self, guide_setting):
        log.debug("set_state %s" % guide_setting)
        if guide_setting == "Off":
            self.disable()
        elif guide_setting == "Restart":
            self.restart()
            self.on_enter("Settings")
        elif guide_setting == "On":
            self.enable()
            self.on_enter("Settings")

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
            log.debug("WARNING: my_id not found")
            return

        self.unhighlight(widget_id)

    def unhighlight(self, widget_id):
        try:
            remaining_for_screen = self.suggestions[current_screen_name]
        except KeyError:
            log.debug("WARNING: Trying to unhighlight for another screen: %s" % current_screen_name)
            return

        found = None
        for rem in remaining_for_screen:
            if widget_id in rem:
                found = rem
                break

        if not found:
            log.debug("WARNING: %s not found in remaining list" % widget_id)
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
        except ReferenceError:
            pass

    def activate(self, widget):
        try:
            if highlighted and highlighted.widget.my_id == widget.my_id:
                #st()
                print "Already activated %s, ignoring" % widget.my_id
                return
        except NameError:
            pass
        except ReferenceError:
            return

        try:
            log.debug("activating %s" % widget.text)
            global highlighted
            highlighted = Highlight(widget)
        except ReferenceError:
            log.debug("WARNING: Attempt to activate GCed widget")
