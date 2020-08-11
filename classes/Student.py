import json
from classes.Person import Person
from classes.Skill import Skill


class Student(Person):
    def __init__(self, first_name, last_name, email, password, id=[], creation_time=[], existing_magic_skills={}, desired_magic_skills={}):
        Person.__init__(self, first_name, last_name, email,
                        password, id=[], creation_time=[])
        self._existing_magic_skills = existing_magic_skills
        self._desired_magic_skills = desired_magic_skills

    def update_existing_skills(self, skills_array):
        for skill in skills_array:
            if type(skill) is dict:
                print(skill)
                self.add_existing_skills(skill["name"], skill["level"])

    def update_desired_skills(self, skills_array):
        for skill in skills_array:
            if type(skill) is dict:
                print(skill)
                self.add_desired_skills(skill["name"], skill["level"])

    def get_student_data(self):
        data = {"_first_name": self._first_name, "_last_name": self._last_name, "_email": self._email,
                "_password": self._password, "_creation_time": self._creation_time, "_last_update_time": self._last_update_time, "_desired_magic_skills": self._desired_magic_skills, "_existing_magic_skills": self._existing_magic_skills}
        return data

    def get_student_secure_data(self):
        data = {"_first_name": self._first_name, "_last_name": self._last_name, "_email": self._email,
                "_id": self._id, "_creation_time": self._creation_time, "_last_update_time": self._last_update_time, "_desired_magic_skills": self._desired_magic_skills, "_existing_magic_skills": self._existing_magic_skills}
        return data

    def add_existing_skills(self, name, level):
        skill = Skill(name, level)
        if skill in self._existing_magic_skills:
            return
        else:
            print(["adding", skill])
            self._existing_magic_skills.append(skill.__dict__)
            return skill

    def add_desired_skills(self, name, level):
        skill = Skill(name, level)
        if skill in self._desired_magic_skills:
            return
        else:
            print(["adding", skill])
            self._desired_magic_skills.append(skill.__dict__)
            return skill

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
