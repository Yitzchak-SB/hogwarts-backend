import json
from classes.Person import Person
from classes.Skill import Skill


class Student(Person):
    def __init__(self, id, first_name, last_name, email, password, existing_magic_skills=[], desired_magic_skills=[]):
        Person.__init__(self, id, first_name, last_name, email, password)
        self.existing_magic_skills = existing_magic_skills
        self.desired_magic_skills = desired_magic_skills

    def add_existing_skills(self, name, level):
        skill = Skill(name, level)
        self.existing_magic_skills.append(skill)

    def add_desired_skills(self, name, level):
        skill = Skill(name, level)
        self.desired_magic_skills.append(skill)

    def __str__(self):
        return json.dumps(self.__dict__)

    def set_id(self, id):
        self._id = id

    def set_first_name(self, first_name):
        self._first_name = first_name

    def set_last_name(self, last_name):
        self._last_name = last_name

    def set_password(self, password):
        self._password = password

    def set_email(self, email):
        self._email = email

    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        return cls(data["id"], data["first_name"], data["last_name"], data["email"], data["password"])


