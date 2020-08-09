from classes.Person import Person


class Admin(Person):
    def __init__(self, first_name, last_name, email, password):
        Person.__init__(self, first_name, last_name, email, password)

    def get_password(self):
        return self._password

