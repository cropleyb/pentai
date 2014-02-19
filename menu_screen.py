from kivy.uix.screenmanager import Screen

from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty

class ScrollableLabel(ScrollView):
    text = StringProperty('')

class MenuScreen(Screen):
    """ This is more of a travel agency or a directory than a menu """
    about_text = StringProperty("")

    def __init__(self, *args, **kwargs):
        super(MenuScreen, self).__init__(*args, **kwargs)
        self.about_text = \
"""PentAI by Bruce Cropley\n
Pente is a strategy board game for two or more players, created in 1977 by Gary Gabrel. It is now owned by Hasbro, and the board game can be bought from Winning Ways. TODO: Link to http://winning-moves.com/product/Pente.asp.
The rules of the game are very simple: The first player to get 5 stones in a straight line wins. Pairs of stones can be captured by placing a stone at each end of the pair. Capturing 5 pairs first also wins. Click "Demo" below!

PentAI is a computer program (Artificial Intelligence) to play Pente. It can be configured to play in a wide range of ability levels, from a complete beginner to a strong amateur player. There are several settings that can be adjusted for a given AI player profile:
    Depth: Controls how many moves the AI looks ahead each move.
    Vision: How often does the AI miss a move possibility entirely?
    Openings book: Should the AI be able to refer to previous games?
    Lines/Captures: How much value should the AI place on lines versus captures?
    Misjudgement: How badly should the AI misjudge the value of positions?

Several profiles are included, have a look at and experiment with their configurations, or create your own.

For more information about how PentAI works, see my website: www.bruce-cropley.com.

If you get a sore brain, you can create a game between a couple of AI players and watch what they do. Human versus human games are also possible, though you are much better off playing with a real set.

Games are automatically saved, and can be resumed if they were left unfinished.

There are a few settings that you might like to change, for things such as move confirmation style, sound volume and so on.












"""

