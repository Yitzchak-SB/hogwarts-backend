import mysql.connector
from data.mySql.SqlBase import SqlBase


class StudentsSkills(SqlBase):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_all_skills(students):
        try:
            connection = SqlBase._connect()
            cursor = connection.cursor()
            results = []
            for student in students:
                id = (student["_id"])
                existing_skills, desired_skills = StudentsSkills.get_all_skills_by_id(id)
                if existing_skills and desired_skills:
                    student["_existing_magic_skills"] = existing_skills
                    student["_desired_magic_skills"] = desired_skills
                else:
                    student["_existing_magic_skills"] = []
                    student["_desired_magic_skills"] = []
                results.append(student)
            return results
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_count_of_existing_skill(skill):
        try:
            connection = SqlBase._connect()
            cursor = connection.cursor()
            search = "SELECT COUNT(*) FROM students_skills WHERE skill_type='existing' AND skill_name=%s"
            cursor.execute(search, (skill.replace(" ", "_"),))
            result = cursor.fetchone()
            return [{"result": result[0]}]
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_count_of_desired_skill(skill):
        try:
            connection = SqlBase._connect()
            cursor = connection.cursor()
            search = "SELECT COUNT(*) FROM students_skills WHERE skill_type='desired' AND skill_name=%s"
            cursor.execute(search, (skill.replace(" ", "_"),))
            result = cursor.fetchone()
            return [{"result": result[0]}]
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_skills_by_id(id):
        desired_skills = StudentsSkills.get_desired_skills_by_id(id)
        existing_skills = StudentsSkills.get_existing_skills_by_id(id)
        return [existing_skills, desired_skills]

    @staticmethod
    def get_desired_skills_by_id(id):
        try:
            connection = SqlBase._connect()
            cursor = connection.cursor()
            search_desired_skills = "SELECT skill_name,skill_level from students_skills WHERE student_id=%s AND skill_type='desired'"
            desired_skills = []
            cursor.execute(search_desired_skills,
                           (id,))
            for (skill_name, skill_level) in cursor:
                desired_skills.append({"name": skill_name, "level": skill_level})
            return desired_skills
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_existing_skills_by_id(id):
        try:
            connection = SqlBase._connect()
            cursor = connection.cursor()
            search_existing_skills = "SELECT skill_name,skill_level from students_skills WHERE student_id=%s AND skill_type='existing'"
            existing_skills = []
            cursor.execute(search_existing_skills,
                           (id,))
            for (skill_name, skill_level) in cursor:
                existing_skills.append({"name": skill_name, "level": skill_level})
            return existing_skills
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def add_skill_by_id(id, skill):
        try:
            connection = SqlBase._connect()
            cursor = connection.cursor()
            print(skill)
            add = "UPDATE students_skills SET skill_level=%s WHERE student_id=%s AND skill_name=%s AND skill_type=%s"
            cursor.execute(
                add, (skill["level"], id, skill["name"], skill["type"],))
            connection.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()

    def edit_skills_by_email(self):
        pass
