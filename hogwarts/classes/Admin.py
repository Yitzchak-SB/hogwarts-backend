from classes.Person import Person


class Admin(Person):
    def __init__(self, id, first_name, last_name, email, password):
        Person.__init__(self, id, first_name, last_name, email, password)

