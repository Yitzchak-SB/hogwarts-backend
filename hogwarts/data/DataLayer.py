import json
from classes.Admin import Admin
from classes.Student import Student
from data.JsonEnc import JsonEnc


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
            self._students[new_student_data["email"]].edit_update_time()
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
        result = map(lambda key: json.dumps({key: data[key]}, cls=JsonEnc, indent=1), data)
        return result

    def delete_student(self, student_email):
        del self._students[student_email]

    def persist_all_students(self):
        with open("data/students.json", "w") as write_file:
            json.dump(self._students, write_file, cls=JsonEnc, indent=1)

    def persist_all_admins(self):
        with open("data/admins.json", "w") as write_file:
            json.dump(self._admins, write_file, cls=JsonEnc, indent=1)

    def load_students(self):
        with open("data/students.json", "r") as read_file:
            students_data = json.load(read_file)
            for key in students_data:
                student = Student(students_data[key]["_id"], students_data[key]["_first_name"], students_data[key]["_last_name"], students_data[key]["_email"], students_data[key]["_password"], students_data[key]["_creation_time"], students_data[key]["_existing_magic_skills"], students_data[key]["_desired_magic_skills"])
                self._students[students_data[key]["_email"]] = student

    def load_admins(self):
        with open("data/admins.json", "r") as read_file:
            admins_data = json.load(read_file)
            for key in admins_data:
                admin = Admin(admins_data[key]["_id"], admins_data[key]["_first_name"], admins_data[key]["_last_name"], admins_data[key]["_email"], admins_data[key]["_password"])
                self._admins[admins_data[key]["_email"]] = admin

    def get_count_of_existing_skills(self, skill):
        count = 0
        students_pool = self.get_all_students()
        for key in students_pool:
            for name in students_pool[key]["_existing_magic_skills"]:
                if skill == name:
                    count += 1
        return count

    def get_count_of_desired_skills(self, skill):
        count = 0
        students_pool = self.get_all_students()
        for key in students_pool:
            for name in students_pool[key]["_desired_magic_skills"]:
                if skill == name:
                    count += 1
        return count

    def add_existing_skill_by_email(self, data):
        student = self._students[data["email"]]
        student.add_existing_skills(data["skill"]["name"], data["skill"]["level"])
        student.edit_update_time()

    def add_desired_skill_by_email(self, data):
        student = self._students[data["email"]]
        student.add_desired_skills(data["skill"]["name"], data["skill"]["level"])
        student.edit_update_time()

