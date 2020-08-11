from datetime import datetime
import uuid


class Person:
    def __init__(self, first_name, last_name, email, password, id=[], creation_time=[]):
        self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._password = password
        self._creation_time = self.add_creation_time(creation_time)
        self._last_update_time = datetime.now().strftime("%d/%m/%y - %H:%M:%S")

    @staticmethod
    def add_creation_time(creation_time):
        if not creation_time:
            return datetime.now().strftime("%d/%m/%y")
        return creation_time

    def edit_update_time(self):
        self._last_update_time = datetime.now().strftime("%d/%m/%y - %H:%M:%S")
