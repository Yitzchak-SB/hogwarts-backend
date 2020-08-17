from classes.Person import Person


class Admin(Person):
    def __init__(self, first_name, last_name, email, password, _id=[], creation_time=[]):
        Person.__init__(self, first_name, last_name, email,
                        password, _id, creation_time)

    def get_new_admin(self):
        data = {"_first_name": self._first_name, "_last_name": self._last_name, "_email": self._email,
                "_password": self._password, "_creation_time": self._creation_time, "_last_update_time": self._last_update_time}
        return data

    def get_password(self):
        return self._password
