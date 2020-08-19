from datetime import datetime
import uuid


class Person:
    def __init__(self, first_name, last_name, email, password):
        self._id = None
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._password = password
        self._creation_time = None
        self._last_update_time = datetime.now().strftime("%y/%m/%d - %H:%M:%S")

    def set_new_creation_time(self):
        self._creation_time = datetime.now().strftime("%y/%m/%d")

    def set_creation_time(self, creation_time):
        self._creation_time = creation_time.strftime("%y/%m/%d")

    def set_id(self, id):
        self._id = id

    def edit_update_time(self):
        self._last_update_time = datetime.now().strftime("%y/%m/%d - %H:%M:%S")
