class BoardTooBigException():
    pass
class BoardTooSmallException():
    pass

class Rules():
    def __init__(self, size, typeStr):
        if size < 5:
            raise BoardTooSmallException()
        if size > 19:
            raise BoardTooBigException()
        self.size = size
        ts = typeStr.lower()
        if ts == "standard":
            self.centerFirst = True
            self.stonesForCaptureWin = 10
            self.canCapturePairs = True
            self.canCaptureThrees = False
            self.exactlyFive = False
        elif ts == "tournament":
            self.centerFirst = True
            self.stonesForCaptureWin = 10
            self.canCapturePairs = True
            self.canCaptureThrees = False
            self.exactlyFive = False
        elif ts[:5] == "keryo":
            self.centerFirst = True
            self.stonesForCaptureWin = 15
            self.canCapturePairs = True
            self.canCaptureThrees = True
            self.exactlyFive = False
        elif ts == "freestyle":
            self.centerFirst = False
            self.stonesForCaptureWin = 10
            self.canCapturePairs = True
            self.canCaptureThrees = False
            self.exactlyFive = False
        elif ts[:4] == "five":
            self.centerFirst = False
            self.stonesForCaptureWin = 0 # can capture, but wins are only from 5
            self.canCapturePairs = True
            self.canCaptureThrees = False
            self.exactlyFive = True
        elif ts[:2] == "no": # no captures
            self.centerFirst = False
            self.stonesForCaptureWin = 0
            self.canCapturePairs = False
            self.canCaptureThrees = False
            self.exactlyFive = False
        else:
            raise UnknownRuleType
     
'''
    Standard rules
    First player must move on the center point - all subsequent moves are open. Pairs can be captured. Win by placing 5 or more stones in a row, OR by capturing 5 or more pairs of the opponent's stones.
     
    Tournament rules
    First player must move on the center point. First player's second move must be 3 or more points removed from the center point. Pairs can be captured. Win by placing 5 or more stones in a row, OR by capturing 5 or more pairs of the opponent's stones.
     
    Keryo-Pente rules
    First player must move on the center point - all subsequent moves are open. Using these rules three of your opponent's stones in a row can be captured, just like pairs. Pairs can also be captured. Win by capturing 15 or more of your opponents stones (compared to the usual 5 pairs, which is 10 stones), OR by placing 5 or more stones in a row.
     
    Freestyle rules
    Stones may be placed anywhere on the board, including the first player's first move. Pairs can be captured. Win by placing 5 or more stones in a row, OR by capturing 5 or more pairs of the opponent's stones.
     
    Five-In-A-Row rules
    Stones may be placed anywhere on the board, including the first player's first move. Pairs can be captured, but don't count towards a win. Win ONLY by placing 5 or more stones in a row.
     
    No Capture rules
    Stones may be placed anywhere on the board, including the first player's first move. Pairs can NOT be captured. Win ONLY by placing 5 or more stones in a row.
'''
