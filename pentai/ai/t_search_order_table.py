#!/usr/bin/env python

import unittest

from pentai.base.defines import *

from pentai.ai.search_order_table import *

#from pentai.base import mock
#from pentai.base import board_strip

#from pentai.ai.utility_stats import *

class SearchOrderTableTest(unittest.TestCase):
    '''
    def setUp(self):
        pass
    '''

    def testSOT_4_Us(self):
        #get_priority_slot_index(our_turn, length, ps, ns) -> i
        psi = get_priority_slot_index(True, 4, 0, 0)
        self.assertEquals(psi, 0)

    def testSOT_4_Them(self):
        #get_priority_slot_index(our_turn, length, ps, ns) -> i
        psi = get_priority_slot_index(False, 4, 0, 0)
        self.assertEquals(psi, 1)

    def testSOT_4_p_Us(self):
        #get_priority_slot_index(our_turn, length, ps, ns) -> i
        psi1 = get_priority_slot_index(True, 4, 1, 0)
        psi2 = get_priority_slot_index(True, 4, 2, 0)
        self.assertEquals(psi1, 0)
        self.assertEquals(psi2, 0)

    def testSOT_3_us(self):
        psi = get_priority_slot_index(True, 3, 1, 2)
        self.assertEquals(psi, 2)

        psi = get_priority_slot_index(True, 3, 2, 2)
        self.assertEquals(psi, 3)

        psi = get_priority_slot_index(True, 3, 1, 1)
        self.assertEquals(psi, 4)

        psi = get_priority_slot_index(True, 3, 0, 1)
        self.assertEquals(psi, 5)

        psi = get_priority_slot_index(True, 3, 1, 0)
        self.assertEquals(psi, 6)



"""
  Length    PS      NS    Order  Rep
X   4       0       0       0   XXaXX For completeness. Won game
    4       1       0       0   XXXaX
    4       2       0       0   XXXXa

O   4       0       0       1   OOaOO If X doesn't block then they lose, so all are 
O   4       1       0       1   OOOaO equivalent
O   4       2       0       1   OOOOa

X   3       1       2       2   .XXaX These ones first because they
                                XXaX. close up the threat

X   3       2       2           aXXXa These can often form an open four.

X   3       1       1           aXX.X Not so good
X   3       0       1           XXa.X Same resultant structure as below,
                                      but stops a threat to us

X   3       0       1           XaXaX Same resultant structure, but no threat stopped

X   3       1       0           XX.Xa Two threats to us when it is blocked

O   3       1       2           .OOaO OOaO. Threat + block

O   3       1       1           aOO.O Threat + block, but prob X 4 response

O   3       2       2           aOOOa .aOOO

O   3       0       1           OaOaO

O   3       1       0           OO.Oa

O   3       2       1           a.OOO Rarely wise

X   2       2       2           .aXX. This blocks a potential threat

X   2       2       2           .XaX. ..XaX

X   2       0       1           X.aX.
X   2       2       1           X.Xa.

X   2       0       0           X..Xa
X   2       0       0           X..aX

O   2       2       2           .OaO. ..OaO

O   2       1       2           .aOO. ..OOa Threaten

O   2       1       1           O.aO. Allows two potential threats

O   2       2       1           O.Oa.

O   2       0       0           O..aO Not sure which is better, if any
O   2       0       0           O.a.O

O   2       0       0           O..Oa A bit remote

O   2       1       2           aOOa.

O   2       1       1           .OO.a

X   1       0       2           .a.X.

X   1       0       1           ..aX.

X   1       0       0           a..X.

O   1       0       1           ..aO.

O   1       0       2           .a.O.

O   1       0       0           a..O.

    Take                        .XOO.
    Threat                      ..OO.
"""
