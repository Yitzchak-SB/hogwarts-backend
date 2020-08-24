import mysql.connector
from decouple import config
from data.mySql.Admins import Admins
from data.mySql.Skills import Skills
from data.mySql.Students import Students
from data.mySql.StudentsSkills import StudentsSkills


class SqlDataLayer:
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_all_students(term, index):
        initial_results = Students.get_all_students(term, index)
        final_results = StudentsSkills.get_all_skills(initial_results)
        return final_results

    @staticmethod
    def get_student_by_email(email):
        return Students.get_student_by_email(email)

    @staticmethod
    def get_student_and_skills_by_email(email):
        student_data = Students.get_student_by_email(email)
        print(student_data)
        [existing_skills, desired_skills] = StudentsSkills.get_all_skills_by_id(student_data["id"])
        student_data["existing_magic_skills"] = existing_skills
        student_data["desired_magic_skills"] = desired_skills
        return student_data

    @staticmethod
    def edit_student_by_email(email, new_student_data):
        Students.edit_student_by_email(email, new_student_data)
        return

    @staticmethod
    def get_admin_by_email(email):
        return Admins.get_admin_by_email(email)

    @staticmethod
    def set_new_admin(admin_data):
        return Admins.set_new_admin(admin_data)

    @staticmethod
    def set_new_student(student_data):
        return Students.set_new_student(student_data)

    @staticmethod
    def delete_student_by_id(id):
        return Students.delete_student_by_id(id)

    @staticmethod
    def get_count_of_existing_skill(skill):
        return StudentsSkills.get_count_of_existing_skill(skill)

    @staticmethod
    def get_count_of_desired_skill(skill):
        return StudentsSkills.get_count_of_desired_skill(skill)

    @staticmethod
    def get_count_of_existing_skill_by_level(skill, level):
        return StudentsSkills.get_count_of_existing_skill_by_level(skill, level)

    @staticmethod
    def get_count_of_desired_skill_by_level(skill, level):
        return StudentsSkills.get_count_of_desired_skill_by_level(skill, level)

    @staticmethod
    def get_count_of_students_added_at_date(date):
        return Students.get_count_of_students_added_at_date(date)

    @staticmethod
    def get_all_skills_by_id(id):
        return StudentsSkills.get_all_skills_by_id(id)

    @staticmethod
    def get_desired_skills_by_id(id):
        return StudentsSkills.get_existing_skills_by_id(id)

    @staticmethod
    def get_existing_skills_by_id(id):
        return StudentsSkills.get_desired_skills_by_id(id)

    @staticmethod
    def add_skill_by_id(id, skill):
        return StudentsSkills.add_skill_by_id(id, skill)

    @staticmethod
    def get_students_id_by_email(email):
        result = Students.get_students_id_by_email(email)
        return result[0]

    @staticmethod
    def get_5_most_recent_created_students():
        return Students.get_5_most_recent_created_students()

    @staticmethod
    def get_5_most_recent_updated_students():
        return Students.get_5_most_recent_updated_students()

    @staticmethod
    def check_student_email_exists(email):
        return Students.check_student_email_exists(email)

    @staticmethod
    def get_all_magic_skills():
        return Skills.get_all_magic_skills()

    @staticmethod
    def add_new_magic_skill(skill_data):
        return Skills.add_new_magic_skill(skill_data)

    @staticmethod
    def get_row_count_of_students():
        return Students.get_row_count_of_students()

    def shutdown(self):
        pass