import mysql.connector
from decouple import config
from data.BaseDBLayer import BaseDBLayer


class SqlDataLayer(BaseDBLayer):
    def __init__(self):
        super().__init__()

    @staticmethod
    def __connect():
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user=config("MYSQL_USER"),
                password=config("PASSWORD"),
                database="hogwarts"
            )
            return connection
        except:
            print("connection error")
            exit(1)

    def get_all_students(self):
        try:
            connection = self.__connect()
            cursor = connection.cursor()
            search_all_students = "SELECT * from students"
            initial_results = []
            final_results = []
            cursor.execute(search_all_students)
            for (student) in cursor:
                initial_results.append({"_id": student[0], "_first_name": student[1], "_last_name": student[2], "_email": student[3],
                                        "_password": student[4], "_creation_time": student[5], "_last_updated": student[6], "_image_url": student[7]})
            for student in initial_results:
                id = (student["_id"])
                existing_skills, desired_skills = self.get_skills_by_id(id)
                if existing_skills and desired_skills:
                    student["_existing_magic_skills"] = existing_skills
                    student["_desired_magic_skills"] = desired_skills
                else:
                    student["_existing_magic_skills"] = []
                    student["_desired_magic_skills"] = []
                final_results.append(student)
            return final_results
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()

    def get_student_by_email(self, email):
        try:
            connection = self.__connect()
            cursor = connection.cursor()
            search = "SELECT id, first_name, last_name, email, password, creation_time, image_url FROM students WHERE email=%s"
            cursor.execute(search, (email,))
            for (id, first_name, last_name, email, password, creation_time, image_url) in cursor:
                result = {"id": id, "first_name": first_name, "last_name": last_name, "email": email,
                          "password": password, "image_url": image_url, "creation_time": creation_time}
                existing_skills, desired_skills = self.get_skills_by_id(id)
                result["existing_magic_skills"] = existing_skills
                result["desired_magic_skills"] = desired_skills
            return result
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()

    def edit_student_by_email(self, email, new_student_data):
        try:
            connection = self.__connect()
            edit_student_cursor = connection.cursor()
            print(new_student_data)
            edit_data = "UPDATE students SET first_name=%s, last_name=%s, email=%s, image_url=%s WHERE email=%s"
            edit_student_cursor.execute(edit_data, (new_student_data["_first_name"], new_student_data["_last_name"],
                                                    new_student_data["_email"], new_student_data["_image_url"], email,))
            for skill in new_student_data["_desired_magic_skills"]:
                skill["type"] = "desired"
                self.add_skill_by_id(new_student_data["_id"], skill)
            for skill in new_student_data["_existing_magic_skills"]:
                skill["type"] = "existing"
                self.add_skill_by_id(new_student_data["_id"], skill)
            connection.commit()
            return new_student_data
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            edit_student_cursor.close()
            connection.close()

    def get_admin_by_email(self, email):
        try:
            connection = self.__connect()
            get_admin_cursor = connection.cursor()
            search = "SELECT first_name, last_name, email, creation_time FROM admins WHERE email=%s"
            get_admin_cursor.execute(search, (email,))
            res = get_admin_cursor.fetchone()
            return res
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            get_admin_cursor.close()
            connection.close()

    def set_new_admin(self, admin_data):
        try:
            connection = self.__connect()
            new_admin_cursor = connection.cursor()
            add = "INSERT INTO admins (first_name, last_name, email, password, image_url, creation_time) VALUES (%s, %s, %s, %s, %s)"
            new_admin_cursor.execute(add, (admin_data["_first_name"], admin_data["_last_name"],
                                           admin_data["_email"], admin_data["_password"], admin_data["_creation_time"]))
            connection.commit()
            return admin_data
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            new_admin_cursor.close()
            connection.close()

    def set_new_student(self, student_data):
        try:
            connection = self.__connect()
            new_student_cursor = connection.cursor()
            add = "INSERT INTO students (first_name, last_name, email, password, image_url, creation_time) VALUES (%s, %s, %s, %s, %s, %s)"
            new_student_cursor.execute(add, (student_data["_first_name"], student_data["_last_name"],
                                             student_data["_email"], student_data["_password"], student_data["_image_url"], student_data["_creation_time"]))
            connection.commit()
            student_id = self.get_students_id_by_email(student_data["_email"])
            for skill in student_data["_existing_magic_skills"]:
                add_skill = "INSERT INTO students_skills (skill_name, skill_level, student_id, skill_type) VALUES (%s, %s, %s, %s)"
                new_student_cursor.execute(
                    add_skill, (skill["name"].replace(" ", "_"),
                                skill["level"], student_id[0], "existing"))
            for skill in student_data["_desired_magic_skills"]:
                add_skill = "INSERT INTO students_skills (skill_name, skill_level, student_id, skill_type) VALUES (%s, %s, %s, %s)"
                new_student_cursor.execute(
                    add_skill, (skill["name"].replace(" ", "_"),
                                skill["level"], student_id[0], "desired"))
            connection.commit()
            return student_data
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            new_student_cursor.close()
            connection.close()

    def delete_student_by_id(self, id):
        try:
            connection = self.__connect()
            delete_student_cursor = connection.cursor()
            delete_skills = "DELETE FROM students_skills WHERE student_id=%s"
            delete_student = "DELETE FROM students WHERE id=%s;"
            delete_student_cursor.execute(delete_skills, (id,))
            delete_student_cursor.execute(delete_student, (id,))
            connection.commit()
            return id
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            delete_student_cursor.close()
            connection.close()

    def get_count_of_existing_skill(self, skill):
        try:
            connection = self.__connect()
            cursor = connection.cursor()
            search = "SELECT COUNT(*) FROM students_skills WHERE skill_type='existing' AND skill_name=%s"
            cursor.execute(search, (skill.replace(" ", "_"),))
            print(cursor.statement)
            result = cursor.fetchone()
            return [{"result": result[0]}]
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()

    def get_count_of_desired_skill(self, skill):
        try:
            connection = self.__connect()
            count_of_desired_cursor = connection.cursor()
            search = "SELECT COUNT(*) FROM students_skills WHERE skill_type='desired' AND skill_name=%s"
            count_of_desired_cursor.execute(search, (skill.replace(" ", "_"),))
            result = count_of_desired_cursor.fetchone()
            return [{"result": result[0]}]
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            count_of_desired_cursor.close()
            connection.close()

    def get_count_of_students_added_at_date(self, date):
        try:
            connection = self.__connect()
            count_of_students_date_cursor = connection.cursor()
            search = "SELECT COUNT(*) FROM students WHERE creation_time=%s"
            count_of_students_date_cursor.execute(search, (date,))
            result = count_of_students_date_cursor.fetchone()
            return result[0]
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            count_of_students_date_cursor.close()
            connection.close()

    def get_skills_by_id(self, id):
        try:
            connection = self.__connect()
            cursor = connection.cursor()
            search_desired_skills = "SELECT skill_name,skill_level from students_skills WHERE student_id=%s AND skill_type=%s"
            search_existing_skills = "SELECT skill_name,skill_level from students_skills WHERE student_id=%s AND skill_type=%s"
            desired_skills = []
            existing_skills = []
            cursor.execute(search_desired_skills,
                           (id, "desired",))
            for (skill_name, skill_level) in cursor:
                desired_skills.append(
                    {"name": skill_name, "level": skill_level})
            cursor.execute(search_existing_skills,
                           (id, "existing",))
            for (skill_name, skill_level) in cursor:
                existing_skills.append(
                    {"name": skill_name, "level": skill_level})
            return [existing_skills, desired_skills]
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()

    def add_skill_by_id(self, id, skill):
        try:
            connection = self.__connect()
            add_skill_cursor = connection.cursor()
            add = "SET skill_level=%s WHERE student_id=%s skill_name=%s skill_type=%s"
            add_skill_cursor.execute(
                add, (skill["level"], id, skill["name"], skill["type"],))
            connection.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            add_skill_cursor.close()
            connection.close()

    def get_students_id_by_email(self, email):
        try:
            connection = self.__connect()
            cursor = connection.cursor()
            search = "SELECT id FROM students WHERE email=%s"
            cursor.execute(search, (email,))
            result = cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()

    def get_most_recent_created_students(self):
        try:
            connection = self.__connect()
            cursor = connection.cursor()
            search = "SELECT first_name, last_name, image_url, creation_time FROM students ORDER BY creation_time DESC LIMIT 5"
            cursor.execute(search,)
            results = []
            for (first_name, last_name, image_url, creation_time) in cursor:
                results.append(
                    {"first_name": first_name, "last_name": last_name, "image_url": image_url, "creation_time": creation_time})
            return results
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()

    def get_most_recent_updated_students(self):
        try:
            connection = self.__connect()
            cursor = connection.cursor()
            search = "SELECT first_name, last_name, image_url, last_updated FROM students ORDER BY last_updated DESC LIMIT 5"
            cursor.execute(search,)
            results = []
            for (first_name, last_name, image_url, last_updated) in cursor:
                results.append(
                    {"first_name": first_name, "last_name": last_name, "image_url": image_url, "last_updated": last_updated})
            return results
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()

    def check_email_exists(self, email):
        try:
            connection = self.__connect()
            cursor = connection.cursor()
            search = "SELECT COUNT(*) FROM students WHERE email=%s"
            cursor.execute(search, (email,))
            result = cursor.fetchone()
            if result[0] > 0:
                raise ValueError("Email already Exits")
            print(result)
            return True
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()
