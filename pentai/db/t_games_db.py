#!/usr/bin/env python

import unittest
from game import *
from persistent_dict import *
from priority_filter_2 import *
from ai_player import *
from rules import *
from preserved_game import *
from games_db import *

import pdb

class PreservedGameTest(unittest.TestCase):
    def setUp(self):
        pass

    def create_player(self, name, mmpdl, narrowing, chokes):
        sf = PriorityFilter2()
        return AIPlayer(sf, name=name)


if __name__ == "__main__":
    unittest.main()

