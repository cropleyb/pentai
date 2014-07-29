from pentai.base.defines import *

search_order_table = {}

psi_table = {}

def get_priority_slot_index(is_us, length, ps, ns):
    return psi_table[(is_us, length, ps, ns)]

current_max_ind = 0

def add_to_psi_table(is_us, length, ps, ns):
    global current_max_ind
    psi_table[(is_us, length, ps, ns)] = current_max_ind

def next_psi_ind():
    global current_max_ind
    current_max_ind += 1

def create_psi_table():
    # add_to_psi_table(is_us, length, ps, ns)
    add_to_psi_table(True, 4, 0, 0)
    add_to_psi_table(True, 4, 1, 0)
    add_to_psi_table(True, 4, 2, 0)
    next_psi_ind() 

    add_to_psi_table(False, 4, 0, 0)
    add_to_psi_table(False, 4, 1, 0)
    add_to_psi_table(False, 4, 2, 0)
    next_psi_ind() 

    add_to_psi_table(True, 3,1,2) # .XXaX These ones first because they XXaX. close up the threat
    next_psi_ind() 

    add_to_psi_table(True, 3,2,2) # aXXXa These can often form an open four.
    next_psi_ind() 

    add_to_psi_table(True, 3,1,1) # aXX.X Not so good
    next_psi_ind() 

    add_to_psi_table(True, 3,0,1) # XXa.X Same resultant structure as below, stops a threat to us
    next_psi_ind() 

    add_to_psi_table(True, 3,1,0) # XX.Xa Two threats to us when it is blocked
    next_psi_ind() 

    add_to_psi_table(False, 3,1,2) # .OOaO OOaO. Threat + block
    next_psi_ind() 

    add_to_psi_table(False, 3,1,1) # aOO.O Threat + block, but prob X 4 response
    next_psi_ind() 

    add_to_psi_table(False, 3,2,2) # aOOOa .aOOO
    next_psi_ind() 

    add_to_psi_table(False, 3,0,1) # OaOaO
    next_psi_ind() 

    add_to_psi_table(False, 3,1,0) # OO.Oa
    next_psi_ind() 

    add_to_psi_table(False, 3,2,1) # a.OOO Rarely wise
    next_psi_ind() 

    '''
    add_to_psi_table(True,
    2,2,2           .aXX. This blocks a potential threat
    next_psi_ind() 

    add_to_psi_table(True,
    2,2,2           .XaX. ..XaX
    next_psi_ind() 

    add_to_psi_table(True,
    2,0,1           X.aX.
    2,2,1           X.Xa.
    next_psi_ind() 

    add_to_psi_table(True,
    2,0,0           X..Xa
    2,0,0           X..aX
    next_psi_ind() 

    add_to_psi_table(
    2,2,2           .OaO. ..OaO
    next_psi_ind() 

    add_to_psi_table(
    2,1,2           .aOO. ..OOa Threaten
    next_psi_ind() 

    add_to_psi_table(
    2,1,1           O.aO. Allows two potential threats
    next_psi_ind() 

    add_to_psi_table(
    2,2,1           O.Oa.
    next_psi_ind() 

    add_to_psi_table(
    2,0,0           O..aO Not sure which is better, if any
    2,0,0           O.a.O
    next_psi_ind() 

    add_to_psi_table(
    2,0,0           O..Oa A bit remote
    next_psi_ind() 

    add_to_psi_table(
    2,1,2           aOOa.
    next_psi_ind() 

    add_to_psi_table(
    2,1,1           .OO.a
    next_psi_ind() 

    add_to_psi_table(True,
X   1       0       2           .a.X.
    next_psi_ind() 

    add_to_psi_table(True,
X   1       0       1           ..aX.
    next_psi_ind() 

    add_to_psi_table(True,
X   1       0       0           a..X.
    next_psi_ind() 

    add_to_psi_table(
O   1       0       1           ..aO.
    next_psi_ind() 

    add_to_psi_table(
O   1       0       2           .a.O.
    next_psi_ind() 

    add_to_psi_table(
O   1       0       0           a..O.
    next_psi_ind() 
    '''

create_psi_table()

'''
    4,0,0           XXaXX For completeness. Won game
    4,1,0           XXXaX
    4,2,0           XXXXa

    4,0,0           OOaOO If X doesn't block then they lose, so all are 
    4,1,0           OOOaO equivalent
    4,2,0           OOOOa

    3,1,2           .XXaX These ones first because they
                    XXaX. close up the threat

    3,2,2           aXXXa These can often form an open four.

    3,1,1           aXX.X Not so good
    3,0,1           XXa.X Same resultant structure as below,
       ,                 but stops a threat to us

    3,0,1           XaXaX Same resultant structure, but no threat stopped

    3,1,0           XX.Xa Two threats to us when it is blocked

    3,1,2           .OOaO OOaO. Threat + block

    3,1,1           aOO.O Threat + block, but prob X 4 response

    3,2,2           aOOOa .aOOO

    3,0,1           OaOaO

    3,1,0           OO.Oa

    3,2,1           a.OOO Rarely wise

    2,2,2           .aXX. This blocks a potential threat

    2,2,2           .XaX. ..XaX

    2,0,1           X.aX.
    2,2,1           X.Xa.

    2,0,0           X..Xa
    2,0,0           X..aX

    2,2,2           .OaO. ..OaO

    2,1,2           .aOO. ..OOa Threaten

    2,1,1           O.aO. Allows two potential threats

    2,2,1           O.Oa.

    2,0,0           O..aO Not sure which is better, if any
    2,0,0           O.a.O

    2,0,0           O..Oa A bit remote

    2,1,2           aOOa.

    2,1,1           .OO.a

X   1       0       2           .a.X.

X   1       0       1           ..aX.

X   1       0       0           a..X.

O   1       0       1           ..aO.

O   1       0       2           .a.O.

O   1       0       0           a..O.


    #return tc != sc
'''

def lookup_search_order_index(length, ps, ns, sc, tc):
    """
    ps: previous subtype
    ns: next subtype
    sc: search colour
    tc: turn colour
    """

"""
    Take                        .XOO.
    Threat                      ..OO.
"""
