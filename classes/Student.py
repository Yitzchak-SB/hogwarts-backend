import json
from classes.Person import Person
from classes.Skill import Skill


class Student(Person):
    def __init__(self, first_name, last_name, email, password, image_url, _id=[], creation_time=[], existing_magic_skills=[], desired_magic_skills=[]):
        Person.__init__(self, first_name, last_name, email,
                        password, _id, creation_time, )
        self._image_url = image_url
        self._existing_magic_skills = existing_magic_skills
        self._desired_magic_skills = desired_magic_skills
        
    def set_image_url(self, image_url):
        self._image_url = image_url

    def update_existing_skills(self, skills_array):
        for skill in skills_array:
            if type(skill) is dict:
                self.add_existing_skills(skill["name"], skill["level"])

    def update_desired_skills(self, skills_array):
        for skill in skills_array:
            if type(skill) is dict:
                self.add_desired_skills(skill["name"], skill["level"])

    def get_student_data(self):
        data = {"_first_name": self._first_name, "_last_name": self._last_name, "_email": self._email,
                "_password": self._password, "_image_url": self._image_url, "_creation_time": self._creation_time, "_last_update_time": self._last_update_time, "_desired_magic_skills": self._desired_magic_skills, "_existing_magic_skills": self._existing_magic_skills, "_id": self._id}
        return data

    def get_student_secure_data(self):
        data = {"_first_name": self._first_name, "_last_name": self._last_name, "_email": self._email,
                "_id": self._id, "_image_url": self._image_url, "_creation_time": self._creation_time, "_last_update_time": self._last_update_time, "_desired_magic_skills": self._desired_magic_skills, "_existing_magic_skills": self._existing_magic_skills}
        return data

    def add_existing_skills(self, name, level):
        skill = Skill(name, level)
        if skill in self._existing_magic_skills:
            return
        else:
            self._existing_magic_skills.append(skill.__dict__)
            return skill

    def add_desired_skills(self, name, level):
        skill = Skill(name, level)
        if skill in self._desired_magic_skills:
            return
        else:
            self._desired_magic_skills.append(skill.__dict__)
            return skill

    def __str__(self):
        return json.dumps(self.__dict__)

    def set_id(self, id):
        self._id = id

    def get_id(self):
        return self._id

    def set_first_name(self, first_name):
        self._first_name = first_name

    def set_last_name(self, last_name):
        self._last_name = last_name

    def set_password(self, password):
        self._password = password

    def set_email(self, email):
        self._email = email
