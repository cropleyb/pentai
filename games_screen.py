from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.clock import * # FOR HACK

from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import ListItemButton, ListItemLabel, \
        CompositeListItem, ListView
from kivy.uix.gridlayout import GridLayout

from defines import *

class GamesScreen(Screen): # TODO: Rename to GamesScreen?!
    def __init__(self, *args, **kwargs):
        super(GamesScreen, self).__init__(*args, **kwargs)

        self.selected_gid = None

    def set_selected_gid(self, gid):
        self.selected_gid = gid

    def delete_game(self):
        print "Del HI"
        pass # TODO

    def edit_game(self):
        print "Edit HI"
        pass # TODO
    
    def load_game(self, gid):
        st()
        game = self.gm.get_game(gid)
        self.app.start_game(game, self.size)

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
    '''Uses :class:`CompositeListItem` for list item views comprised by two
    :class:`ListItemButton`s and one :class:`ListItemLabel`. Illustrates how
    to construct the fairly involved args_converter used with
    :class:`CompositeListItem`.
    '''

    def __init__(self, **kwargs):
        kwargs['cols'] = 2
        super(GamesView, self).__init__(**kwargs)

        Clock.schedule_once(self.fill_er_up, 1) # HACK HACK HACK

        # This is quite an involved args_converter, so we should go through the
        # details. A CompositeListItem instance is made with the args
        # returned by this converter. The first three, text, size_hint_y,
        # height are arguments for CompositeListItem. The cls_dicts list contains
        # argument sets for each of the member widgets for this composite:
        # ListItemButton and ListItemLabel.

        # 
        '''
We have a collection of unfinished games, and another of all games
We want to display them in several orders:
Black Player Name (A or Z first)
White Player Name (A or Z first)
Date (latest as default, or earliest)
Board size
Rules type
        integers_dict = \
                        { str(i): {'text': str(i), 'is_selected': False} for i in xrange(100)}
        '''

    def changed(self, da, *args, **kwargs): # dict adaptor
        gid_str = self.item_strings[da.selection[0].index]
        print "Selected: GID %s" % (gid_str)
        self.parent.parent.set_selected_gid(int(gid_str))

    def fill_er_up(self, unused):
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

        gm = self.parent.parent.gm
        games = gm.get_all_unfinished()

        games_dict = { str(g.game_id): game_data(g) for g in games}

        self.item_strings = ["{0}".format(g_id) for g_id in games_dict.iterkeys() ]

        dict_adapter = DictAdapter(sorted_keys=self.item_strings,
                                   data=games_dict,
                                   args_converter=args_converter,
                                   selection_mode='single',
                                   allow_empty_selection=False,
                                   cls=CompositeListItem)

        dict_adapter.bind(
            on_selection_change=self.changed)

        # Use the adapter in our ListView:
        list_view = ListView(adapter=dict_adapter)

        self.add_widget(list_view)

