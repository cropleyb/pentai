import base_db

class GamesDB(base_db.BaseDB):
    """ Key is an id allocated by the GameManager;
        Value is a PreservedGame instance """

