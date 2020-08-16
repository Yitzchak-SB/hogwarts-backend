import json
from classes.Admin import Admin
from classes.Student import Student
from data.MongoDataLayer import MongoDataLayer
from data.mySql.SqlDataLayer import SqlDataLayer


class DataLayer:
    def __init__(self, students={}, admins={}):
        self._students = students
        self._admins = admins
        self._mongo = MongoDataLayer()
        self._mySql = SqlDataLayer()

    def get_student_by_email(self, email):
        student_data = self._mySql.get_student_by_email(email)
        student = Student(first_name=student_data["first_name"], last_name=student_data["last_name"], email=student_data["email"], password=student_data["password"],
                          id=student_data["id"], creation_time=student_data["creation_time"], image_url=student_data["image_url"], existing_magic_skills=student_data["existing_magic_skills"], desired_magic_skills=student_data["desired_magic_skills"])
        return student

    def get_admin_by_email(self, email):
        admin_data = self._mongo.get_admin_by_email(email)
        admin = Admin(admin_data["_first_name"], admin_data["_last_name"], admin_data["_email"],
                      admin_data["_password"], admin_data["_id"], admin_data["_creation_time"])
        return admin

    def create_new_admin(self, admin_data):
        admin_ins = Admin(admin_data["first_name"], admin_data["last_name"],
                          admin_data["email"], admin_data["password"])
        admin = self._mySql.set_new_admin(admin_ins.get_new_admin())
        return admin

    def create_new_student(self, student_data):
        student_ins = Student(first_name=student_data["first_name"], last_name=student_data["last_name"],
                              email=student_data["email"], password=student_data["password"], image_url=student_data["image_url"], existing_magic_skills=student_data["existing_magic_skills"], desired_magic_skills=student_data["desired_magic_skills"])
        student_ins.get_student_data()
        student = self._mySql.set_new_student(student_ins.get_student_data())
        return student

    def set_student_by_email(self, student_data):
        email = student_data["initial_email"]
        new_student_data = student_data["student"]
        old_student_data = self._mySql.get_student_by_email(email)
        existing_magic_skills = self._mySql.get_desired_skills_by_id(
            old_student_data[6])
        desired_magic_skills = self._mySql.get_existing_skills_by_id(
            old_student_data[6])
        student = Student(first_name=old_student_data[0], last_name=old_student_data[1], email=old_student_data[2],
                          password=old_student_data[3], image_url=old_student_data[4], creation_time=old_student_data[5], id=student_data[6])
        student.update_existing_skills(existing_magic_skills)
        student.update_desired_skills(desired_magic_skills)
        for key in new_student_data:
            if key == "first_name":
                student.set_first_name(new_student_data[key])
            elif key == "last_name":
                student.set_last_name(new_student_data[key])
            elif key == "email":
                student.set_email(new_student_data[key])
            elif key == "image_url":
                student.set_image_url(new_student_data[key])
            elif key == "desired_magic_skills":
                student.update_existing_skills(new_student_data[key])
            elif key == "existing_magic_skills":
                student.update_desired_skills(new_student_data[key])
        new_student = self._mySql.edit_student_by_email(
            email, student.get_student_data())
        return new_student

    def get_all_students(self):
        students_data = self._mySql.get_all_students()
        students = []
        for student in students_data:
            student_ins = Student(first_name=student["_first_name"], last_name=student["_last_name"], email=student["_email"], password=student["_password"],
                                  id=student["_id"], image_url=student["_image_url"], creation_time=student["_creation_time"], existing_magic_skills=student["_existing_magic_skills"], desired_magic_skills=student["_desired_magic_skills"])
            students.append(student_ins.get_student_secure_data())
        return students

    def delete_student(self, student_id):
        student = self._mySql.delete_student_by_id(student_id)
        return student

    def get_count_of_existing_skills(self, skill):
        result = self._mySql.get_count_of_existing_skill(skill)
        return result

    def get_count_of_desired_skills(self, skill):
        result = self._mySql.get_count_of_desired_skill(skill)
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
        result = self._mySql.get_count_of_students_added_at_date(date)
        return result

    def get_most_recent_created_students(self):
        result = self._mySql.get_most_recent_created_students()
        return result

    def get_most_recent_updated_students(self):
        result = self._mySql.get_most_recent_updated_students()
        return result

    def shutdown(self):
        self._mongo.shutdown()
