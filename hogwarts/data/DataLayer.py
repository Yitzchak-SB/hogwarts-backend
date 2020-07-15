import json

from classes.Admin import Admin
from classes.Student import Student


class DataLayer:
    def __init__(self, students={}, admins={}):
        self._students = students
        self._admins = admins

    def get_student_by_email(self, email):
        student = self._students[email]
        return student.__dict__

    def create_new_student(self, student_data):
        student = Student(student_data["id"], student_data["first_name"], student_data["last_name"],
                          student_data["email"], student_data["password"])
        self._students[student._email] = student

    def set_student_by_email(self, new_student_data):
        for key in new_student_data:
            if key == "id":
                self._students[new_student_data["email"]].set_id(new_student_data["id"])
            elif key == "first_name":
                self._students[new_student_data["email"]].set_first_name(new_student_data["first_name"])
            elif key == "last_name":
                self._students[new_student_data["email"]].set_last_name(new_student_data["last_name"])
            elif key == "password":
                self._students[new_student_data["email"]].set_password(new_student_data["password"])
            elif key == "email":
                self._students[new_student_data["email"]].set_email(new_student_data["email"])

    def get_all_students(self):
        students_dict = {}
        for student in self._students:
            students_dict[self._students[student]._email] = self._students[student].__dict__
        return students_dict

    def get_all_students_json(self):
        data = self.get_all_students()
        result = map(lambda key: json.dumps({key: data[key]}), data)
        return result

    def delete_student(self, student_email):
        del self._students[student_email]

    def persist_all_students(self):
        with open("data/students.json", "w") as write_file:
            json.dump(self._students, write_file)

    def persist_all_admins(self):
        with open("data/admins.json", "w") as write_file:
            json.dump(self._admins, write_file)

    def load_students(self):
        with open("data/students.json", "r") as read_file:
            students_data = json.load(read_file)
            for key in students_data:
                student = Student(students_data[key]["id"], students_data[key]["first_name"], students_data[key]["last_name"], students_data[key]["email"], students_data[key]["password"], students_data[key]["existing_magic_skills"], students_data[key]["desired_magic_skills"])
                self._students[students_data[key]["email"]] = student

    def load_admins(self):
        with open("data/admins.json", "r") as read_file:
            admins_data = json.load(read_file)
            for key in admins_data:
                admin = Admin(admins_data[key]["id"], admins_data[key]["first_name"], admins_data[key]["last_name"], admins_data[key]["email"], admins_data[key]["password"])
                self._admins[admins_data[key]["email"]] = admin
