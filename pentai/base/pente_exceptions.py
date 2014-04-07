class IllegalMoveException(Exception):
    pass

class OffBoardException(Exception):
    pass

class BoardTooBigException(Exception):
    pass

class BoardTooSmallException(Exception):
    pass

class NoMovesException(Exception):
    pass

class IncompatibleFileException(Exception):
    pass

class UnknownRuleType(Exception):
    pass

class OpeningsBookDuplicateException(Exception):
    pass
