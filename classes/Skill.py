import json


class Skill:
    def __init__(self, name, level):
        self.name = name
        self.level = level

    def __str__(self):
        return json.dumps({self.name: self.__dict__})