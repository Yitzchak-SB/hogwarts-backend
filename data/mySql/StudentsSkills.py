import mysql.connector
from data.mySql.SqlBase import SqlBase
from data.mySql.context import get_cursor


class StudentsSkills(SqlBase):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_all_skills(students):
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

    @staticmethod
    def get_count_of_existing_skill(skill):
        with get_cursor(SqlBase._connect()) as cursor:
            search = "SELECT COUNT(*) FROM students_skills WHERE skill_type='existing' AND skill_name=%s"
            cursor.execute(search, (skill.replace(" ", "_"),))
            result = cursor.fetchone()
            return [{"result": result[0]}]

    @staticmethod
    def get_count_of_desired_skill(skill):
        with get_cursor(SqlBase._connect()) as cursor:
            search = "SELECT COUNT(*) FROM students_skills WHERE skill_type='desired' AND skill_name=%s"
            cursor.execute(search, (skill.replace(" ", "_"),))
            result = cursor.fetchone()
            return [{"result": result[0]}]

    @staticmethod
    def get_count_of_existing_skill_by_level(skill, level):
        with get_cursor(SqlBase._connect()) as cursor:
            search = "SELECT COUNT(*) FROM students_skills WHERE skill_type='existing' AND skill_name=%s AND skill_level=%s"
            cursor.execute(search, (skill.replace(" ", "_"), level))
            result = cursor.fetchone()
            return {"result": result[0], "level": level}

    @staticmethod
    def get_count_of_desired_skill_by_level(skill, level):
        with get_cursor(SqlBase._connect()) as cursor:
            search = "SELECT COUNT(*) FROM students_skills WHERE skill_type='desired' AND skill_name=%s AND skill_level=%s"
            cursor.execute(search, (skill.replace(" ", "_"), level))
            result = cursor.fetchone()
            return {"result": result[0], "level": level}

    @staticmethod
    def get_all_skills_by_id(id):
        desired_skills = StudentsSkills.get_desired_skills_by_id(id)
        existing_skills = StudentsSkills.get_existing_skills_by_id(id)
        return [existing_skills, desired_skills]

    @staticmethod
    def get_desired_skills_by_id(id):
        with get_cursor(SqlBase._connect()) as cursor:
            search_desired_skills = "SELECT ss.skill_name, ss.skill_level, s.num_of_levels from students_skills AS ss JOIN skills AS s ON ss.skill_name = s.skill_name AND ss.student_id=%s AND ss.skill_type='desired'"
            desired_skills = []
            cursor.execute(search_desired_skills,
                           (id,))
            for (skill_name, skill_level, num_of_levels) in cursor:
                desired_skills.append({"name": skill_name, "level": skill_level, "num_of_levels": num_of_levels})
            return desired_skills

    @staticmethod
    def get_existing_skills_by_id(id):
        with get_cursor(SqlBase._connect()) as cursor:
            search_existing_skills = "SELECT ss.skill_name, ss.skill_level, s.num_of_levels from students_skills AS ss JOIN skills AS s ON ss.skill_name = s.skill_name AND student_id=%s AND skill_type='existing'"
            existing_skills = []
            cursor.execute(search_existing_skills,
                           (id,))
            for (skill_name, skill_level, num_of_levels) in cursor:
                existing_skills.append({"name": skill_name, "level": skill_level, "num_of_levels": num_of_levels})
            return existing_skills

    @staticmethod
    def add_skill_by_id(id, skill):
        with get_cursor(SqlBase._connect()) as cursor:
            add = "INSERT INTO students_skills (skill_level, skill_name, skill_type, student_id) VALUES ('%s', %s, %s, '%s')"
            cursor.execute(add, (skill["level"], skill["name"], skill["type"], id,))

    @staticmethod
    def edit_skill_by_id(id, skill):
        with get_cursor(SqlBase._connect()) as cursor:
            add = "UPDATE students_skills SET skill_level=%s WHERE student_id=%s AND skill_name=%s AND skill_type=%s"
            cursor.execute(
                add, (skill["level"], id, skill["name"], skill["type"],))

    def edit_skills_by_email(self):
        pass
