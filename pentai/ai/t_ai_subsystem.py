#!/usr/bin/env python

import unittest

import pentai.base.rules as r_m
import pentai.base.human_player
import pentai.base.game as g_m

from pentai.ai.ai_player import *
from pentai.db.ai_factory import *

class AIPlayerSubsystemTest(unittest.TestCase):

    def create_player(self): #, name, mmpdl, narrowing, chokes):
        aif = AIFactory()
        genome = AIGenome("Whatever")
        genome.use_openings_book = False
        return aif.create_player(genome)

    def setUp(self):
        self.p1 = self.create_player()
        self.p2 = self.create_player()

        r = r_m.Rules(13, "standard")
        self.game = g_m.Game(r, self.p1, self.p2)

    # !./pentai/ai/t_ai_subsystem.py AIPlayerSubsystemTest.test_find_one_move
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

    """
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

    """
    def test_dodgy_move_part2(self):
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
        """
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
"""

    def test_freebie(self):
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

    # !./t_ai_subsystem.py AIPlayerSubsystemTest.test_strange
    def test_strange(self):
        self.p1.set_max_depth(6)
        game_str = \
"""Mark versus DT
13x13
standard rules
1. (6, 6)
2. (6, 7)
3. (4, 6)
4. (5, 8)
5. (7, 6)
6. (5, 6)
7. (4, 9)
"""
        self.game.load_game(game_str)
        m = self.p2.do_the_search()
        self.assertEquals(m, (8,6))

    def test_draw(self): # TODO
        r = r_m.Rules(9, "standard")
        self.game = g_m.Game(r, self.p1, self.p2)

        self.p1.set_max_depth(6)
        game_str = \
"""DT versus Itself
9x9
standard rules
1. (4, 4)
2. (5, 5)
3. (6, 4)
4. (5, 4)
5. (5, 6)
6. (5, 3)
7. (5, 2)
8. (6, 5)
9. (7, 6)
10. (4, 5)
11. (4, 3)
12. (6, 5)
13. (3, 5)
14. (2, 6)
15. (3, 5)
16. (7, 5)
17. (8, 5)
18. (6, 1)
19. (6, 6)
20. (4, 6)
21. (3, 7)
22. (4, 6)
23. (3, 6)
24. (3, 4)
25. (2, 3)
26. (3, 4)
27. (4, 3)
28. (5, 5)
29. (5, 1)
30. (1, 4)
31. (3, 3)
32. (2, 4)
33. (4, 4)
34. (2, 8)
35. (4, 2)
36. (2, 7)
37. (2, 5)
38. (4, 7)
39. (2, 5)
40. (2, 2)
41. (4, 4)
42. (4, 1)
43. (3, 3)
44. (0, 3)
45. (1, 5)
46. (4, 5)
47. (3, 6)
48. (0, 4)
49. (0, 5)
50. (0, 2)
51. (0, 0)
52. (4, 8)
53. (3, 8)
54. (4, 0)
55. (1, 3)
56. (5, 0)
57. (3, 0)
58. (6, 0)
59. (8, 4)
60. (8, 0)
61. (7, 0)
62. (8, 6)
63. (8, 3)
64. (8, 2)
65. (7, 4)
66. (5, 4)
67. (7, 2)
68. (6, 3)
69. (7, 1)
70. (7, 3)
71. (8, 7)
72. (8, 8)
73. (6, 8)
74. (2, 1)
75. (0, 1)
76. (6, 2)
77. (1, 0)
78. (2, 0)
79. (1, 1)
80. (3, 1)
"""
        self.game.load_game(game_str)
        m = self.p1.do_the_search()
        self.assertEquals(self.game.finished(), True)
        self.assertEquals(self.game.get_won_by(), BLACK+WHITE)

    def test_missed_win(self): # TODO
        self.p1.set_max_depth(2)
        game_str = \
"""Black versus White
13x13
standard rules
1. (6, 6)
2. (8, 4)
3. (8, 6)
4. (10, 6)
5. (7, 6)
6. (5, 6)
7. (6, 4)
8. (9, 5)
9. (7, 3)
10. (11, 7)
11. (12, 8)
12. (8, 2)
13. (5, 5)
14. (8, 1)
15. (3, 7)
16. (4, 6)
17. (3, 6)
18. (4, 6)
19. (8, 3)
20. (6, 3)
21. (9, 3)
22. (10, 3)
23. (10, 5)
24. (11, 4)
25. (5, 6)
26. (9, 6)
27. (11, 6)
28. (9, 6)
29. (7, 7)
30. (9, 2)
31. (8, 0)
"""
        self.game.load_game(game_str)
        m = self.p2.do_the_search()
        self.assertEquals(m, (8,1))

    def test_pacifist(self):
        self.p1.set_max_depth(4)
        game_str = \
"""Black versus White
9x9
standard rules
1. (4, 4)
2. (5, 4)
3. (2, 6)
4. (5, 5)
5. (3, 5)
6. (5, 3)
7. (5, 6)
8. (1, 7)
9. (5, 2)
10. (6, 3)
11. (4, 3)
12. (4, 5)
13. (6, 5)
14. (4, 5)
15. (3, 6)
16. (4, 6)
"""
        self.game.load_game(game_str)
        m = self.p1.do_the_search()
        self.assertEquals(m, (4,7))

    def test_another(self):
        self.p1.set_max_depth(4)
        game_str = \
"""Black versus White
13x13
standard rules
1. (6, 6)
2. (7, 5)
3. (5, 5)
4. (7, 7)
5. (4, 4)
6. (3, 3)
7. (7, 6)
8. (8, 6)
9. (9, 7)
10. (6, 4)
"""
        self.game.load_game(game_str)
        m = self.p1.do_the_search()
        self.assertNotEquals(m, (4,6))

    def test_bother(self):
        self.p1.set_max_depth(8)
        game_str = \
"""DT versus BC
13x13
standard rules
1. (6, 6)
2. (5, 7)
3. (8, 8)
4. (7, 7)
5. (8, 7)
6. (8, 6)
7. (6, 8)
8. (9, 5)
9. (6, 7)
10. (6, 5)"""
        self.game.load_game(game_str)
        m = self.p1.do_the_search()
        #print m
        self.assertNotIn(m, ((7,8),(5,8)))

    def test_block_one_end(self):
        self.p1.set_max_depth(8)
        game_str = \
"""Bruce versus DT
13x13
Standard rules
1. (6, 6)
2. (5, 5)
3. (7, 6)
4. (7, 4)
5. (8, 6)
6. (9, 3)
7. (9, 6)"""
        self.game.load_game(game_str)
        m = self.p2.do_the_search()
        self.assertIn(m, ((10,6),(5,6)))

    def atest_think_in_opponents_move(self):
        #self.p1.set_max_depth(8)
        game_str = \
"""Bruce versus DT
13x13
Standard rules
1. (6, 6)"""
        self.game.load_game(game_str)
        m = self.p1.do_the_search()
        self.assertIsNone(m)

    # TODO
    def atest_trap(self):
        self.p1.set_max_depth(8)
        game_str = \
"""Killer versus Kang
19x19
Standard rules
1. (9, 9)
2. (8, 10)
3. (6, 9)
4. (8, 8)
5. (8, 9)
6. (7, 9)"""
        self.game.load_game(game_str)
        m = self.p1.do_the_search()
        self.assertNotEquals(m, (10,9))

if __name__ == "__main__":
    unittest.main()
