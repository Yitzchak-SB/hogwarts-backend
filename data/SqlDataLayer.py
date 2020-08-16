import mysql.connector
from data.private import config


class SqlDataLayer():

    def __connect(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user=config["MYSQL_USER"],
                password=config["PASSWORD"],
                database="hogwarts"
            )
            return connection
        except:
            print("connection error")
            exit(1)

    def search_skills(self, skill):
        if skill == "Spells":
            return "WHERE Spells != 0"
        elif skill == "Potion making":
            return "WHERE Potion_making != 0"
        elif skill == "Quidditch":
            return "WHERE Quidditch != 0"
        elif skill == "Animagus":
            return "WHERE Animagus != 0"
        elif skill == "Apparate":
            return "WHERE Apparate != 0"
        elif skill == "Metamorphmagi":
            return "WHERE Metamorphmagi != 0"
        elif skill == "Parseltongue":
            return "WHERE Parseltongue != 0"
        return skill

    def get_all_students(self):
        try:
            connection = self.__connect()
            cursor = connection.cursor()
            search_all_students = "SELECT * from students"
            search_desired_skills = "SELECT skill_name,skill_level from students_skills WHERE student_id=%s AND skill_type=%s"
            search_existing_skills = "SELECT skill_name,skill_level from students_skills WHERE student_id=%s AND skill_type=%s"
            initial_results = []
            final_results = []
            cursor.execute(search_all_students)
            for (student) in cursor:
                initial_results.append({"_id": student[0], "_first_name": student[1], "_last_name": student[2], "_email": student[3],
                                        "_password": student[4], "_creation_time": student[5], "_last_updated": student[6], "_image_url": student[7]})
            for student in initial_results:
                desired_skills = []
                existing_skills = []
                id = (student["_id"])
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
                if existing_skills and desired_skills:
                    student["_existing_magic_skills"] = existing_skills
                    student["_desired_magic_skills"] = desired_skills
                else:
                    student["_existing_magic_skills"] = []
                    student["_desired_magic_skills"] = []
                final_results.append(student)
            return final_results
        finally:
            cursor.close()
            connection.close()

    def get_student_by_email(self, email):
        try:
            connection = self.__connect()
            get_student_cursor = connection.cursor()
            search = "SELECT first_name, last_name, email, password, image_url, creation_time, id FROM students WHERE email=%s"
            get_student_cursor.execute(search, (email,))
            res = get_student_cursor.fetchone()
            return res
        finally:
            get_student_cursor.close()
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
            print("!@#")
            connection.commit()
            return new_student_data
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
        finally:
            new_student_cursor.close()
            connection.close()

    def delete_student_by_id(self, id):
        try:
            connection = self.__connect()
            delete_student_cursor = connection.cursor()
            delete = "DELETE FROM students WHERE id=%s ADD CONSTRAINT `students_skills_student_id_foreign` FOREIGN KEY (`students_id`) REFERENCES `students` (`id`) ON DELETE CASCADE;"
            delete_student_cursor.execute(delete, (id,))
            connection.commit()
            return id
        finally:
            delete_student_cursor.close()
            connection.close()

    def get_count_of_existing_skill(self, skill):
        try:
            connection = self.__connect()
            count_of_existing_cursor = connection.cursor()
            search = "SELECT COUNT(*) FROM students_skills WHERE skill_type='existing' AND skill_name=%s"
            count_of_existing_cursor.execute(search, (skill,))
            result = count_of_existing_cursor.fetchone()
            return [{"result": result[0]}]
        finally:
            count_of_existing_cursor.close()
            connection.close()

    def get_count_of_desired_skill(self, skill):
        try:
            connection = self.__connect()
            count_of_desired_cursor = connection.cursor()
            search = "SELECT COUNT(*) FROM students_skills WHERE skill_type='desired' AND skill_name=%s"
            count_of_desired_cursor.execute(search, (skill,))
            result = count_of_desired_cursor.fetchone()
            return [{"result": result[0]}]
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
        finally:
            count_of_students_date_cursor.close()
            connection.close()

    def get_existing_skills_by_id(self, id):
        try:
            connection = self.__connect()
            existing_skills_id_cursor = connection.cursor()
            search = "SELECT Potion_making, Spells, Quidditch, Animagus, Apparate, Metamorphmagi, Parseltongue FROM existing_magic_skills WHERE id=%s"
            existing_skills_id_cursor.execute(search, (id,))
            result = existing_skills_id_cursor.fetchone()
            existing_magic_skills = [{"name": "Potion_making", "level": result[0]}, {"name": "Spells", "level": result[1]}, {"name": "Quidditch", "level": result[2]}, {
                "name": "Animagus", "level": result[3]}, {"name": "Apparate", "level": result[4]}, {"name": "Metamorphmagi", "level": result[5]}, {"name": "Parseltongue", "level": result[6]}]
            return existing_magic_skills
        finally:
            existing_skills_id_cursor.close()
            connection.close()

    def get_desired_skills_by_id(self, id):
        try:
            connection = self.__connect()
            desired_skills_id_cursor = connection.cursor()
            search = "SELECT Potion_making, Spells, Quidditch, Animagus, Apparate, Metamorphmagi, Parseltongue FROM desired_magic_skills WHERE id=%s"
            desired_skills_id_cursor.execute(search, (id,))
            result = desired_skills_id_cursor.fetchone()
            desired_magic_skills = [{"name": "Potion_making", "level": result[0]}, {"name": "Spells", "level": result[1]}, {"name": "Quidditch", "level": result[2]}, {
                "name": "Animagus", "level": result[3]}, {"name": "Apparate", "level": result[4]}, {"name": "Metamorphmagi", "level": result[5]}, {"name": "Parseltongue", "level": result[6]}]
            return desired_magic_skills
        finally:
            desired_skills_id_cursor.close()
            connection.close()

    def add_skill_by_id(self, id, skill):
        try:
            connection = self.__connect()
            add_skill_cursor = connection.cursor()
            add = "SET skill_level=%s WHERE student_id=%s skill_name=%s skill_type=%s"
            add_skill_cursor.execute(
                add, (skill["level"], id, skill["name"], skill["type"],))
            connection.commit()
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
        finally:
            cursor.close()
            connection.close()
