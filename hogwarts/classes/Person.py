from datetime import datetime


class Person:
    def __init__(self, id, first_name, last_name, email, password):
        self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._password = password
        self._creation_time = datetime.now().strftime("%d/%m/%y")
        self._last_update_time = datetime.now().strftime("%d/%m/%y - %H:%M:%S")
