from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.clock import * # FOR HACK

from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import ListItemButton, ListItemLabel, \
        CompositeListItem, ListView
from kivy.uix.gridlayout import GridLayout

import popup as p_m

from defines import *

class GamesScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(GamesScreen, self).__init__(*args, **kwargs)

        self.selected_gid = None

    def games_view(self):
        return self.ids.games_view

    def on_pre_enter(self):
        self.games_view().refresh()

    def set_selected_gid(self, gid):
        self.selected_gid = gid

    def load_game(self):
        if not self.selected_gid:
            # Ignore
            return
        game = self.gm.get_game(self.selected_gid)
        self.app.start_game(game, self.size)

    def edit_game(self):
        print "Edit HI"
        # TODO: show setup screen for this game, return to here?
        # TODO: Perhaps this should be per field by double clicking?
        pass # TODO

    def delete_game(self):
        msg_str = "Delete this game?"
        p_m.ConfirmPopup.create_and_open(message=msg_str,
            action=self.delete_confirmed,
            size_hint=(.8, .2))
        self.delete_confirmed()

    def delete_confirmed(self):
        self.gm.delete_game(self.selected_gid)
        self.games_view().refresh()


def game_data(game):
    data = {}
    data['id'] = game.game_id
    data['black'] = game.get_player_name(BLACK)
    data['white'] = game.get_player_name(WHITE)
    data['date'] = str(game.get_date())
    data['size'] = str(game.size())
    data['rules'] = str(game.rules.get_type_name())
    data['is_selected'] = False
    # TODO: Winner
    return data


class GamesView(GridLayout):

    def __init__(self, **kwargs):
        kwargs['cols'] = 2
        super(GamesView, self).__init__(**kwargs)

        Clock.schedule_once(self.fill_er_up, 1) # HACK HACK HACK

        '''
        TODO:
        We have a collection of unfinished games, and another of all games
        We want to display them in several orders:
        Black Player Name (A or Z first)
        White Player Name (A or Z first)
        Date (latest as default, or earliest)
        Board size
        Rules type
        '''

    def refresh(self):
        try:
            w = self.view
            self.remove_widget(w)
        except:
            pass
        self.fill_er_up()

    def changed_selection(self, da, *args, **kwargs): # da == dict adaptor
        try:
            gid_str = self.item_strings[da.selection[0].index]
            print "Selected: GID %s" % (gid_str)
            # TODO: parent.parent. ?!
            self.parent.parent.set_selected_gid(int(gid_str))
        except IndexError:
            print "Removed"

    def fill_er_up(self, unused=None):
        args_converter = \
            lambda row_index, rec: \
                {'game_id': rec['id'],
                 'size_hint_y': None,
                 'height': 25,
                 'cls_dicts': [
                       {'cls': ListItemButton,
                           'kwargs': {'text': rec['black']}},
                       {'cls': ListItemButton,
                           'kwargs': {'text': rec['white']}},
                       {'cls': ListItemButton,
                           'kwargs': {'text': rec['date']}},
                       {'cls': ListItemButton,
                           'kwargs': {'text': rec['size'], 'size_hint': (.2,1)}},
                       {'cls': ListItemButton,
                           'kwargs': {'text': rec['rules']}},
                       ]}

        # Another hack - parent.parent.
        gm = self.parent.parent.gm
        games = gm.get_all_unfinished()

        # TODO: The 'if' is a hack
        games_dict = { str(g.game_id): game_data(g) for g in games if g }

        self.item_strings = ["{0}".format(g_id) for g_id in games_dict.iterkeys() ]

        dict_adapter = DictAdapter(sorted_keys=self.item_strings,
                                   data=games_dict,
                                   args_converter=args_converter,
                                   selection_mode='single',
                                   allow_empty_selection=False, # Not working?
                                   cls=CompositeListItem)

        dict_adapter.bind(
            on_selection_change=self.changed_selection)

        self.adapter = dict_adapter

        # Use the adapter in our ListView:
        list_view = ListView(adapter=dict_adapter)

        self.add_widget(list_view)
        self.view = list_view

