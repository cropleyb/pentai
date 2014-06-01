from kivy.uix.screenmanager import Screen
from kivy.uix.listview import ListView
import kivy.uix.gridlayout as gl_m
from kivy.adapters.dictadapter import DictAdapter

import popup as p_m
import audio as a_m
import gl_cli as cli_m

from pentai.base.defines import *

class GamesScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(GamesScreen, self).__init__(*args, **kwargs)

        self.clear_selected()

    def games_view(self):
        return self.ids.games_view

    def on_enter(self):
        self.games_view().refresh()
        self.clear_selected()

    def clear_selected(self):
        self.selected_gid = None

    def set_selected_gid(self, gid):
        self.selected_gid = gid

    def load_game(self):
        if not self.selected_gid:
            # Ignore it
            return
        game = self.gm.get_game(self.selected_gid)
        self.clear_selected()
        self.app.start_game(game, self.size)

    def edit_game(self):
        if not self.selected_gid:
            # Ignore it
            return

        game = self.gm.get_game(self.selected_gid)
        self.clear_selected()
        self.app.edit_game(game)

    def delete_game(self):
        if not self.selected_gid:
            # Ignore it
            return

        msg_str = "Delete game %s?" % self.selected_gid
        p_m.ConfirmPopup.create_and_open(message=msg_str,
            action=self.delete_confirmed,
            size_hint=(.8, .2))

    def delete_confirmed(self):
        self.gm.delete_game(self.selected_gid)
        self.games_view().refresh()
        self.clear_selected()


def game_data(game, players_mgr):
    data = {}
    data["id"] = str(game.game_id)

    data["black"] = players_mgr.get_player_name(game.get_player_id(BLACK))
    data["white"] = players_mgr.get_player_name(game.get_player_id(WHITE))

    data["date"] = str(game.get_date())
    #data["status_colour"] = [0,0,0,.5] #game.get_won_by()
    wb = game.get_won_by()
    if wb == BLACK:
        data["deselected_color"] = [0,0,0,.5] #game.get_won_by()
        data["selected_color"] = [0,0,0,.5] #game.get_won_by()
    data["height"] = 50
    data["size"] = str(game.get_size())
    data["rules"] = str(game.get_rules_type_name())
    data["is_selected"] = False
    # TODO: Winner
    return data

class TwoLevelCompositeListItem(cli_m.CompositeListItem):
    pass

class GamesView(gl_m.GridLayout):

    def __init__(self, **kwargs):
        kwargs["cols"] = 2
        super(GamesView, self).__init__(**kwargs)

        """
        We have a collection of unfinished games, and another of all games
        We want to display them in several orders:
        Black Player Name (A or Z first)
        White Player Name (A or Z first)
        Date (latest as default, or earliest)
        Board size
        Rules type
        """

    def on_enter(self):
        self.fill_er_up()

    def refresh(self):
        try:
            w = self.view
            self.remove_widget(w)
        except:
            pass
        self.fill_er_up()

    def changed_selection(self, da, *args, **kwargs):
        try:
            # TODO: Fix this incredibly ugly hack
            try:
                # For some reason this is not opening a selected game if it
                # was selected through the other row for the same game
                gid_str = da.selection[0].parent.children[-1].text
                log.debug("Selected: GID %s" % (gid_str))
                self.parent.parent.set_selected_gid(int(gid_str))
            except AttributeError, e:
                # It is selected already, load the game.
                self.parent.parent.load_game()
        except IndexError:
            log.debug("Removed")

    def fill_er_up(self, unused=None):
        dc = "deselected_color"
        sc = "selected_color"
        args_converter = \
            lambda row_index, rec: \
                {"size_hint_y": None,
                 "height": 25,
                 #"height": rec["height"],
                 #"background_color": rec["status_colour"],
                 "cls_dicts": [
                       {"cls": MyListItemButton,
                           "kwargs": {"text": rec["id"]}}, #, dc: rec[dc]}},
                       {"cls": MyListItemButton,
                           "kwargs": {"text": rec["black"]}},
                       {"cls": MyListItemButton,
                           "kwargs": {"text": rec["white"]}},
                       {"cls": MyListItemButton,
                           "kwargs": {"text": rec["date"]}},
                       {"cls": MyListItemButton,
                           "kwargs": {"text": rec["size"]}},
                       {"cls": MyListItemButton,
                           "kwargs": {"text": rec["rules"]}},
                       ]}

        # TODO: Another hack - parent.parent
        gm = self.parent.parent.gm
        pm = gm.get_players_mgr()
        games = gm.get_all_unfinished_preserved()

        # TODO: The "if" is a hack
        games_dict = { g.game_id: game_data(g, pm) for g in games if g }

        self.item_strings = ["{0}".format(g_id) for g_id in games_dict.iterkeys() ]

        dict_adapter = DictAdapter(data=games_dict,
                                   args_converter=args_converter,
                                   selection_mode="single",
                                   allow_empty_selection=False, # Not working?
                                   cls=TwoLevelCompositeListItem)

        dict_adapter.bind(
            on_selection_change=self.changed_selection)

        self.adapter = dict_adapter

        # Use the adapter in our ListView:
        list_view = ListView(adapter=dict_adapter)

        self.add_widget(list_view)
        self.view = list_view

class MyListItemButton(cli_m.ListItemButton):
    """ Add click sound """
    def on_touch_down(self, touch):
        # TODO: Check Scroll
        if super(MyListItemButton, self).on_touch_down(touch):
            a_m.instance.click()

