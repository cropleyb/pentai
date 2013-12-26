#!/usr/bin/env python

import unittest

import gui
import human_player
import rules
import game

from ai_player import *

import pdb

class AIPlayerSubsystemTest(unittest.TestCase):

    def setUp(self):
        self.p1 = AIPlayer(name="Deep thunk", mmpdl=9, narrowing=0)
        self.p2 = AIPlayer(name="Deep thunk2", mmpdl=9, narrowing=0)
        r = rules.Rules(13, "standard")
        self.game = game.Game(r, self.p1, self.p2)

    # !./t_ai_subsystem.py AIPlayerSubsystemTest.test_find_one_move
    def test_find_one_move(self):
        self.p2.set_max_depth(2)
        game_str = \
"""Black versus White
13x13
standard rules
1. (6, 6)
2. (7, 7)
3. (8, 6)
4. (9, 6)
5. (6, 4)
6. (9, 7)
7. (9, 8)
8. (9, 5)
9. (6, 5)
10. (6, 7)
11. (8, 7)
12. (9, 4)
13. (9, 3)
14. (7, 6)
15. (6, 3)
16. (6, 2)
17. (5, 7)
"""
        self.game.load_game(game_str)
        m = self.p2.do_the_search()
        self.assertEquals(m, (6,7))

    # !./t_ai_player.py AIPlayerSubsystemTest.test_dont_waste_a_pair
    def test_dont_waste_a_pair(self):
        self.p1.set_max_depth(6)
        game_str = \
"""Black versus White
13x13
standard rules
1. (6, 6)
2. (6, 7)
3. (8, 8)
4. (5, 5)
5. (8, 6)
6. (7, 6)
7. (8, 5)
8. (8, 7)
9. (8, 4)
10. (5, 8)
"""
        self.game.load_game(game_str)
        m = self.p1.do_the_search()
        self.assertNotEquals(m, (6,5))

    def test_dodgy_move(self):
        self.p2.set_max_depth(6)
        game_str = \
"""Black versus White
13x13
standard rules
1. (6, 6)
2. (6, 5)
3. (8, 6)
4. (7, 6)
5. (5, 4)
6. (8, 7)
7. (6, 8)
8. (7, 7)
9. (6, 7)
"""
        self.game.load_game(game_str)
        m = self.p2.do_the_search()
        self.assertNotEquals(m, (7,5))
        # Why not 9,7? i.e. why does 7,5 have a high score?

    '''
10.  Captures: [0, 0, 0]  Lines: [None, [50, 1, 1, 0, 0], [23, 6, 1, 0, 0]], Takes: [0, 1, 0], Threats: [0, 2, 0], Best: [{}, {}, {}] 
[(-31739848.999999996, ((7, 8), )), (-6948522.0, ((6, 10), )), (-6926498.0, ((7, 9), )), (-6913542.0, ((9, 8), )), (-6913424.0, ((10, 9), )), (-6912718.0, ((7, 4), )), (-6911684.0, ((6, 9), )), (75972, ((9, 7), )), (1488020, ((7, 5), ))]
 => (7, 5)

This is the sequence of moves that leads to a score of 1488020:
 12. (7, 5) 13. (7, 4) 14. (9, 7) 15. (10, 9) 16. (10, 7) 17. (11, 7)
And the utility_stats:

    Lines: [None, [60, 4, 1, 0, 0], [30, 5, 1, 0, 0]], Takes: [0, 0, 0], Threats: [0, 2, 0], Best: [{}, {}, {(11, 7): 0}]

c.f. 75972, ((9, 7)
10. (9, 7) 11. (6, 9) 12. (6, 10) 13. (10, 9) 14. (10, 7) 15. (11, 7)

Now compare for black's next move:
    [(-6.25e+27, ((7, 3), )), (-6.25e+27, ((7, 9), )), (-6.25e+27, ((9, 8), )), (-6.25e+27, ((10, 9), )), (-659473320.0, ((7, 8), )), (-657688842.0, ((9, 7), )), (-2978217, ((6, 9), )), (-2961948, ((6, 10), )), (-1541249, ((7, 4), ))]

    (9, 7) (good) -657688842.0
    vs.
    (7, 4) (inferior) -1541249

    '11. (7, 4) 12. (9, 7) 13. (7, 9) 14. (6, 9) 15. (10, 9) '
    Lines: [None, [51, 8, 0, 0, 0], [23, 8, 1, 0, 0]], Takes: [0, 0, 0], Threats: [0, 2, 2], Best: [{}, {}, {}] Captured: [0, 0, 0]

    '11. (9, 7) 12. (10, 8) 13. (6, 9) 14. (6, 10) 15. (8, 7) '
    Lines: [None, [78, 9, 1, 1, 0], [36, 2, 0, 0, 0]], Takes: [0, 0, 0], Threats: [0, 0, 0], Best: [{}, {(6, 10): 0, (6, 5): 1}, {}] Captured: [0, 4, 4]

    '''
    def test_dodgy_move_part2(self):
        #pdb.set_trace()
        self.p1.set_max_depth(5)
        game_str = \
"""Black versus White
13x13
standard rules
1. (6, 6)
2. (6, 5)
3. (8, 6)
4. (7, 6)
5. (5, 4)
6. (8, 7)
7. (6, 8)
8. (7, 7)
9. (6, 7)
10. (7, 5)
"""
        self.game.load_game(game_str)
        m = self.p1.do_the_search()
        self.assertEquals(m, (9,7))
        '''
Black should respond 9,7

11.  Captures: [0, 0, 0]  Lines: [None, [42, 1, 1, 0, 0], [22, 8, 4, 0, 0]], Takes: [0, 1, 0], Threats: [0, 2, 0], Best: [{}, {}, {}] 
[(-6.25e+27, ((7, 3), )), (-6.25e+27, ((7, 9), )), (-6.25e+27, ((9, 8), )), (-6.25e+27, ((10, 9), )), (-659473320.0, ((7, 8), )), (-657688842.0, ((9, 7), )), (-2978217, ((6, 9), )), (-2961948, ((6, 10), )), (-1541249, ((7, 4), ))]
 => (7, 4)
Why is 7,4 so good for black?
How does it evaluate 12. 9,7

(Pdb) p utility_stats
Lines: [None, [51, 8, 0, 0, 0], [23, 8, 1, 0, 0]], Takes: [0, 0, 0], Threats: [0, 2, 2], Best: [{}, {}, {}]

Tools:
Ability to switch players mid-game
    Key press on game screen to jump to Setup screen
    Resume button?
View AI search on screen
Best line utility stats embedded in the AB score? and/or best line?

Work out the inputs for the 2 positions that are evaluating incorrectly
(i.e. the UtilityStats at the leaf nodes)
Check the positions on the board, and write a utility function test
for the correct order.
'''
    def test_throw_away_pair(self):
        #pdb.set_trace()
        self.p1.set_max_depth(8)
        game_str = \
"""DT versus Rich
13x13
standard rules
1. (6, 6)
2. (7, 7)
3. (8, 6)
4. (7, 6)
5. (7, 5)
6. (6, 4)
"""
        self.game.load_game(game_str)
        m = self.p1.do_the_search()
        self.assertEquals(m, (9,7))

    '''
7.  Captures: [0, 0, 0]  Lines: [None, [20, 5, 0, 0, 0], [31, 1, 0, 0, 0]], Takes: [0, 1, 1], Threats: [0, 0, 2], Best: [{}, {}, {}] 
[(-1700500.9999999998, ((10, 2), )), (-1696577.9999999998, ((9, 3), )), (-1671226.9999999998, ((10, 8), )), (-1670188.9999999998, ((11, 9), )), (-361400.0, ((4, 8), )), (-11750, ((5, 7), )), (-11750, ((7, 8), )), (-9431, ((9, 7), )), (-9358, ((8, 4), ))]

'7. (9, 7)\n8. (8, 4)\n9. (10, 8)\n10. (11, 9)\n11. (7, 8)\n12. (7, 4)\n13. (9, 4)\n14. (5, 7)\n'
(-9431, ((9, 7), ))
Lines: [None, [59, 4, 0, 0, 0], [61, 3, 1, 0, 0]], Takes: [0, 0, 0], Threats: [0, 0, 0], Best: [{}, {(11, 9): 0}, {}]
Captured: [0, 2, 2]

(-9358, ((8, 4), ))
Lines: [None, [49, 4, 0, 0, 0], [48, 5, 1, 0, 0]], Takes: [0, 0, 0], Threats: [0, 2, 0], Best: [{}, {}, {}]
Captured: [0, 2, 2]


(Pdb) state.history_string()
'7. (9, 7)\n8. (7, 8)\n9. (4, 8)\n10. (8, 4)\n11. (5, 7)\n12. (3, 9)\n13. (10, 8)\n14. (11, 9)\n'

(Pdb) c
> /Users/cropleyb/Dropbox/pente/utility_calculator.py(85)utility()
-> return ret
(Pdb) state.history_string()
'7. (9, 7)\n8. (8, 4)\n9. (5, 7)\n10. (7, 8)\n11. (10, 8)\n12. (11, 9)\n13. (4, 8)\n14. (3, 9)\n'
(Pdb) c
> /Users/cropleyb/Dropbox/pente/utility_calculator.py(85)utility()
-> return ret
(Pdb) state.history_string()
'7. (9, 7)\n8. (8, 4)\n9. (10, 8)\n10. (11, 9)\n11. (5, 7)\n12. (7, 8)\n13. (4, 8)\n14. (3, 9)\n'
(Pdb) c
> /Users/cropleyb/Dropbox/pente/utility_calculator.py(85)utility()
-> return ret
(Pdb) state.history_string()
'7. (5, 7)\n8. (7, 8)\n9. (9, 7)\n10. (8, 4)\n11. (10, 8)\n12. (11, 9)\n13. (4, 8)\n14. (3, 9)\n'
(Pdb) c
> /Users/cropleyb/Dropbox/pente/utility_calculator.py(85)utility()
-> return ret
(Pdb) state.history_string()
'7. (5, 7)\n8. (8, 4)\n9. (9, 7)\n10. (7, 8)\n11. (10, 8)\n12. (11, 9)\n13. (4, 8)\n14. (3, 9)\n'
(Pdb) c
> /Users/cropleyb/Dropbox/pente/utility_calculator.py(85)utility()
-> return ret
(Pdb) state.history_string()
'7. (5, 7)\n8. (8, 4)\n9. (4, 8)\n10. (3, 9)\n11. (9, 7)\n12. (7, 8)\n13. (10, 8)\n14. (11, 9)\n'
(Pdb) c
> /Users/cropleyb/Dropbox/pente/utility_calculator.py(85)utility()
-> return ret
(Pdb) state.history_string()
'7. (10, 8)\n8. (8, 4)\n9. (9, 7)\n10. (11, 9)\n11. (5, 7)\n12. (7, 8)\n13. (4, 8)\n14. (3, 9)\n'

New:
7.  Captures: [0, 0, 0]  Lines: [None, [20, 5, 0, 0, 0], [31, 1, 0, 0, 0]], Takes: [0, 1, 1], Threats: [0, 0, 2], Best: [{}, {}, {}] 
[(-1373060.0, ((7, 8), )), (-210101.0, ((10, 2), )), (-206178.0, ((9, 3), )), (-180827.0, ((10, 8), )), (-179789.0, ((11, 9), )), (-37400.0, ((4, 8), )), (-14362, ((5, 7), )), (-14362, ((9, 7), )), (-9358, ((8, 4), ))]
 => (8, 4)

(Pdb) u1
147571
(Pdb) u2
-9358

9,7 NEW:
(Pdb) eval_colour
2
(Pdb) state.get_captured(1)
0
(Pdb) p utility_stats
Lines: [None, [58, 0, 0, 0, 0], [62, 4, 1, 0, 0]], Takes: [0, 0, 0], Threats: [0, 0, 0], Best: [{}, {(3, 9): 0, (11, 9): 0}, {}]
Captured: [0, 0, 0]

8,4 NEW:

(Pdb) p utility_stats
Lines: [None, [49, 4, 0, 0, 0], [48, 5, 1, 0, 0]], Takes: [0, 0, 0], Threats: [0, 2, 0], Best: [{}, {}, {}]
Captured: [0, 2, 2]




7.  Captures: [0, 0, 0]  Lines: [None, [20, 5, 0, 0, 0], [31, 1, 0, 0, 0]], Takes: [0, 1, 1], Threats: [0, 0, 2], Best: [{}, {}, {}] 
[(-1373060.0, ((7, 8), )), (-210101.0, ((10, 2), )), (-206178.0, ((9, 3), )), (-180827.0, ((10, 8), )), (-179789.0, ((11, 9), )), (-14362, ((4, 8), )), (147571, ((9, 7), )), (147664, ((5, 7), )), (314642.0, ((8, 4), ))]
 => (8, 4)

Need utility stats for 9,7 (147571) and 8,4 (314642.0)

9,7
Lines: [None, [34, 5, 1, 0, 0], [49, 6, 0, 0, 0]], Takes: [0, 0, 1], Threats: [0, 0, 0], Best: [{}, {(11, 9): 0}, {}]
(no captures)

Should be > 

8,4
Lines: [None, [49, 4, 0, 0, 0], [48, 5, 1, 0, 0]], Takes: [0, 0, 0], Threats: [0, 2, 0], Best: [{}, {}, {}]
Captures: [0, 2, 2]

    '''

    def test_freebie(self):
        #pdb.set_trace()
        self.p1.set_max_depth(8)
        game_str = \
"""Black versus White
13x13
standard rules
1. (6, 6)
2. (6, 5)
3. (8, 6)
4. (7, 6)
5. (5, 4)
6. (8, 7)
7. (6, 8)
8. (7, 7)
9. (6, 7)
10. (7, 5)
11. (9, 7)
12. (10, 8)
"""
        self.game.load_game(game_str)
        m = self.p1.do_the_search()
        self.assertEquals(m, (8,7))

if __name__ == "__main__":
    unittest.main()
