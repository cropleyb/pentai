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

class UnknownRuleType(Exception): # TODO: Rename to UnknownRulesTypeException
    pass

class UnknownSizeException(Exception):
    pass

class OpeningsBookDuplicateException(Exception):
    pass

class ParseException(Exception):
    pass

class MultiplePopupsException(Exception):
    pass
