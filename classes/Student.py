import json
from classes.Person import Person
from classes.Skill import Skill


class Student(Person):
    def __init__(self, first_name, last_name, email, password, creation_time=[], existing_magic_skills={}, desired_magic_skills={}):
        Person.__init__(self, first_name, last_name, email, password, creation_time=[])
        self._existing_magic_skills = existing_magic_skills
        self._desired_magic_skills = desired_magic_skills

    def add_existing_skills(self, name, level):
        skill = Skill(name, level)
        self._existing_magic_skills[name] = skill
        if name in self._desired_magic_skills and self._desired_magic_skills[name]["level"]:
            if self._existing_magic_skills[name]["level"] >= 5:
                del self._desired_magic_skills[name]
                return
            self._desired_magic_skills[name]["level"] += 1

    def add_desired_skills(self, name, level):
        skill = Skill(name, level)
        self._desired_magic_skills[name] = skill

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


