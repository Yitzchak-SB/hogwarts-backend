from decouple import config

class BaseDBLayer:
    """def __init__(self):
        self.__dataBase = self.filter_db()
        print(self.__dataBase)

    def filter_db(self):
        if config("DB") == "mySql":
            return SqlDataLayer()
        return MongoDataLayer()"""
