import json
from classes.Admin import Admin
from classes.Student import Student
from data.JsonEnc import JsonEnc
from data.MongoDataLayer import MongoDataLayer


class DataLayer:
    def __init__(self, students={}, admins={}):
        self._students = students
        self._admins = admins
        self._mongo = MongoDataLayer()

    def get_student_by_email(self, email):
        student_data = self._mongo.get_student_by_email(email)
        student = Student(student_data["first_name"], student_data["last_name"], student_data["email"], student_data["password"],
                          student_data["_id"], student_data["creation_time"], student_data["existing_magic_skills"], student_data["desired_magic_skills"])
        return student

    def get_admin_by_email(self, email):
        admin_data = self._mongo.get_admin_by_email(email)
        admin = Admin(admin_data["_first_name"], admin_data["_last_name"], admin_data["_email"],
                      admin_data["_password"], admin_data["_id"], admin_data["_creation_time"])
        return admin

    def create_new_admin(self, admin_data):
        admin_ins = Admin(admin_data["first_name"], admin_data["last_name"],
                          admin_data["email"], admin_data["password"])
        admin = self._mongo.set_new_admin(admin_ins.get_new_admin())
        return admin

    def create_new_student(self, student_data):
        student_ins = Student(student_data["first_name"], student_data["last_name"],
                              student_data["email"], student_data["password"])
        student = self._mongo.set_new_student(student_ins.get_student_data())
        return student

    def set_student_by_email(self, student_data):
        email = student_data["initial_email"]
        new_student_data = student_data["data"]
        old_student_data = self._mongo.get_student_by_email(email)
        student = Student(old_student_data["_first_name"], old_student_data["_last_name"], old_student_data["_email"], old_student_data["_password"],
                          old_student_data["_id"], old_student_data["_creation_time"], old_student_data["_existing_magic_skills"], old_student_data["_desired_magic_skills"])
        for key in new_student_data:
            if key == "first_name":
                student.set_first_name(new_student_data[key])
            elif key == "last_name":
                student.set_last_name(new_student_data[key])
            elif key == "email":
                student.set_email(new_student_data[key])
            elif key == "desired_magic_skills":
                student.update_existing_skills(new_student_data[key])
            elif key == "existing_magic_skills":
                student.update_desired_skills(new_student_data[key])
        print("done updating")
        new_student = self._mongo.edit_student_by_email(
            email, student.get_student_data())
        return new_student

    def get_all_students(self):
        students_data = self._mongo.get_all_students()
        students = []
        for student in students_data:
            student_ins = Student(student["_first_name"], student["_last_name"], student["_email"], student["_password"],
                                  student["_id"], student["_creation_time"], student["_existing_magic_skills"], student["_desired_magic_skills"])
            students.append(student_ins.get_student_secure_data())
        return students

    def delete_student(self, student_id):
        student = self._mongo.delete_student_by_id(student_id)
        return student

    def persist_all_students(self):
        students = {"students": self._students}
        with open("data/students.json", "w") as write_file:
            json.dump(students, write_file, cls=JsonEnc, indent=1)

    def persist_all_admins(self):
        admins = {"admins": self._admins}
        with open("data/admins.json", "w") as write_file:
            json.dump(admins, write_file, cls=JsonEnc, indent=1)

    def load_students(self):
        with open("data/students.json", "r") as read_file:
            raw_data = json.load(read_file)
            students_data = raw_data["students"]
            for key in students_data:
                student = Student(students_data[key]["_first_name"], students_data[key]["_last_name"], students_data[key]["_email"], students_data[key]
                                  ["_password"], students_data[key]["_creation_time"], students_data[key]["_existing_magic_skills"], students_data[key]["_desired_magic_skills"])
                self._students[students_data[key]["_email"]] = student

    def load_admins(self):
        with open("data/admins.json", "r") as read_file:
            raw_data = json.load(read_file)
            admins_data = raw_data["admins"]
            for key in admins_data:
                admin = Admin(admins_data[key]["_first_name"], admins_data[key]["_last_name"],
                              admins_data[key]["_email"], admins_data[key]["_password"])
                self._admins[admins_data[key]["_email"]] = admin

    def get_count_of_existing_skills(self, skill):
        result = self._mongo.get_count_of_existing_skill(skill)
        return result

    def get_count_of_desired_skills(self, skill):
        result = self._mongo.get_count_of_desired_skill(skill)
        return result

    def add_existing_skill_by_email(self, data):
        student = self._students[data["email"]]
        student.add_existing_skills(
            data["skill"]["name"], data["skill"]["level"])
        student.edit_update_time()

    def add_desired_skill_by_email(self, data):
        student = self._students[data["email"]]
        student.add_desired_skills(
            data["skill"]["name"], data["skill"]["level"])
        student.edit_update_time()

    def get_count_of_students_added_at_date(self, date):
        result = self._mongo.get_count_of_students_added_at_date(date)
        return result

    def shutdown(self):
        self._mongo.shutdown()
