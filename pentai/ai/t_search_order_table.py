#!/usr/bin/env python

import unittest

from pentai.base.defines import *

from pentai.ai.search_order_table import *

#from pentai.base import mock
#from pentai.base import board_strip

#from pentai.ai.utility_stats import *

class PrioritySlotIndexTest(unittest.TestCase):
    def testPSI_4_Us(self):
        #get_priority_slot_index(our_turn, length, ps, ns) -> i
        psi = get_priority_slot_index(True, 4, 0, 0)
        self.assertEquals(psi, 0)

    def testPSI_4_Them(self):
        #get_priority_slot_index(our_turn, length, ps, ns) -> i
        psi = get_priority_slot_index(False, 4, 0, 0)
        self.assertEquals(psi, 1)

    def testPSI_4_p_Us(self):
        #get_priority_slot_index(our_turn, length, ps, ns) -> i
        psi1 = get_priority_slot_index(True, 4, 1, 0)
        psi2 = get_priority_slot_index(True, 4, 2, 0)
        self.assertEquals(psi1, 0)
        self.assertEquals(psi2, 0)

    def testPSI_take_us(self):
        psi = get_take_slot_index(True)
        self.assertEquals(psi, 2)

    def testPSI_3_us_part1(self):
        psi = get_priority_slot_index(True, 3, 1, 2)
        self.assertEquals(psi, 3)

        psi = get_priority_slot_index(True, 3, 2, 2)
        self.assertEquals(psi, 4)

        psi = get_priority_slot_index(True, 3, 1, 1)
        self.assertEquals(psi, 5)

    def testPSI_take_them(self):
        """ This is actually defending a pair """
        psi = get_take_slot_index(False)
        self.assertEquals(psi, 6)

    def testPSI_3_us_part2(self):
        psi = get_priority_slot_index(True, 3, 0, 1)
        self.assertEquals(psi, 7)

        psi = get_priority_slot_index(True, 3, 2, 1)
        self.assertEquals(psi, 8)

        psi = get_priority_slot_index(True, 3, 1, 0)
        self.assertEquals(psi, 9)

    def testPSI_3_them(self):
        psi = get_priority_slot_index(False, 3, 1, 2) # .OOaO OOaO. Threat + block
        self.assertEquals(psi, 10)

        psi = get_priority_slot_index(False, 3, 1, 1) # aOO.O Threat + block, but prob X 4 response
        self.assertEquals(psi, 11)

        psi = get_priority_slot_index(False, 3, 2, 2) # aOOOa .aOOO
        self.assertEquals(psi, 12)

        psi = get_priority_slot_index(False, 3, 0, 1) # OaOaO
        self.assertEquals(psi, 13)

        psi = get_priority_slot_index(False, 3, 1, 0) # OO.Oa
        self.assertEquals(psi, 14)

        psi = get_priority_slot_index(False, 3, 2, 1) # a.OOO Rarely wise
        self.assertEquals(psi, 15)

    def testPSI_threat_us(self):
        psi = get_threat_slot_index(True)
        self.assertEquals(psi, 16)

    # Don't need our defense against a potential threat
    # - extending 2 already covered

    def testPSI_2_us(self):
        psi = get_priority_slot_index(True, 2, 1, 2) # .aXX. This blocks a potential threat
        self.assertEquals(psi, 17)

        psi = get_priority_slot_index(True, 2, 2, 2) # .XaX. ..XaX
        self.assertEquals(psi, 18)

        psi = get_priority_slot_index(True, 2, 0, 1) # X.aX.
        self.assertEquals(psi, 19)

        psi = get_priority_slot_index(True, 2, 2, 1) # X.Xa.
        self.assertEquals(psi, 20)

        psi = get_priority_slot_index(True, 2, 1, 1) # X..Xa
        self.assertEquals(psi, 21)

        psi = get_priority_slot_index(True, 2, 0, 0) # X..Xa
        self.assertEquals(psi, 22)

    def testPSI_2_them(self):
        psi = get_priority_slot_index(False, 2, 2, 2) # .OaO. ..OaO
        self.assertEquals(psi, 23)

        psi = get_priority_slot_index(False, 2, 1, 2) # .aOO. ..OOa Threaten
        self.assertEquals(psi, 24)

        psi = get_priority_slot_index(False, 2, 0, 1) # O.aO. Allows two potential threats
        self.assertEquals(psi, 25)

        psi = get_priority_slot_index(False, 2, 2, 1) # O.Oa.
        self.assertEquals(psi, 26)

        psi = get_priority_slot_index(False, 2, 0, 0) # O..aO / O.a.O / O..Oa 
        self.assertEquals(psi, 27)

        psi = get_priority_slot_index(False, 2, 1, 1) # .OO.a
        self.assertEquals(psi, 28)

    def testPSI_1_us(self):
        psi = get_priority_slot_index(True, 1, 0, 2) # .a.X.
        self.assertEquals(psi, 29)

        psi = get_priority_slot_index(True, 1, 0, 1) # ..aX.
        self.assertEquals(psi, 30)

        psi = get_priority_slot_index(True, 1, 0, 0) # a..X.
        self.assertEquals(psi, 31)

    def testPSI_1_them(self):
        psi = get_priority_slot_index(False, 1, 0, 1) # ..aO.
        self.assertEquals(psi, 32)

        psi = get_priority_slot_index(False, 1, 0, 2) # .a.O.
        self.assertEquals(psi, 33)

        psi = get_priority_slot_index(False, 1, 0, 0) # a..O.
        self.assertEquals(psi, 34)

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

# Can't separate this yet
# X   3       0       1           XXa.X Same resultant structure as below, but stops a threat to us

X   3       0       1           XaXaX Same resultant structure, but no threat stopped

X   3       1       0           XX.Xa Two threats to us when it is blocked

O   3       1       2           .OOaO OOaO. Threat + block

O   3       1       1           aOO.O Threat + block, but prob X 4 response

O   3       2       2           aOOOa .aOOO

O   3       0       1           OaOaO

O   3       1       0           OO.Oa

O   3       2       1           a.OOO Rarely wise

X   2       1       2           .aXX. This blocks a potential threat

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

class SearchOrderIndexTest(unittest.TestCase):
    def testSOI_Us(self):
        #get_priority_slot_index(our_turn, length, ps, ns) -> i
        self.assertEquals(search_order_us, range(35))

        # TODO
        #print search_order_them
        self.assertEquals(search_order_them, [1, 0, 6, 10, 12, 11, 2, 13, 15, 14, 3, 5, 4, 7, 9, 8, 35, 24, 23, 25, 26, 28, 27, 18, 17, 19, 20, 22, 21, 33, 32, 34, 30, 29, 31])
