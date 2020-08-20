import mysql.connector

from data.mySql.SqlBase import SqlBase
from data.mySql.StudentsSkills import StudentsSkills


class Students(SqlBase):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_all_students(term, index):
        try:
            connection = SqlBase._connect()
            cursor = connection.cursor()
            search_all_students = Students.get_search_term_by_order(term, index)
            results = []
            cursor.execute(search_all_students,)
            for (id, first_name, last_name, email, password, creation_time, last_updated, image_url) in cursor:
                results.append(
                    {"_id": id, "_first_name": first_name, "_last_name": last_name, "_email": email,
                     "_password": password, "_creation_time": creation_time, "_last_updated": last_updated,
                     "_image_url": image_url})
            return results
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_student_by_email(email):
        search = "SELECT id, first_name, last_name, email, password, creation_time, last_updated, image_url FROM students WHERE email=%s"
        result = SqlBase.get_by_email(search, email)
        return result

    @staticmethod
    def set_new_student(student_data):
        add = "INSERT INTO students (first_name, last_name, email, password, image_url, creation_time) VALUES (%s, %s, %s, %s, %s, %s)"
        student_id = SqlBase.set_new(add, student_data)
        for skill in student_data["_existing_magic_skills"]:
            skill["type"] = "existing"
            StudentsSkills.add_skill_by_id(student_id, skill)
        for skill in student_data["_desired_magic_skills"]:
            skill["type"] = "desired"
            StudentsSkills.add_skill_by_id(student_id, skill)
        return student_data

    @staticmethod
    def edit_student_by_email(email, new_student_data):
        edit_data = "UPDATE students SET first_name=%s, last_name=%s, email=%s, image_url=%s, last_updated=%s WHERE email=%s"
        new_data = {"_first_name": new_student_data["_first_name"], "_last_name": new_student_data["_last_name"], "_email": new_student_data["_email"], "_last_updated": new_student_data["_last_update_time"], "_image_url": new_student_data["_image_url"]}
        SqlBase.edit_by_email(edit_data, email, new_data)
        for skill in new_student_data["_desired_magic_skills"]:
            skill["type"] = "desired"
            StudentsSkills.edit_skill_by_id(new_student_data["_id"], skill)
        for skill in new_student_data["_existing_magic_skills"]:
            skill["type"] = "existing"
            StudentsSkills.edit_skill_by_id(new_student_data["_id"], skill)
        return new_student_data

    @staticmethod
    def delete_student_by_id(id):
        delete = "DELETE FROM students WHERE id=%s"
        return SqlBase.delete_by_id(delete, id, "students")

    @staticmethod
    def get_count_of_students_added_at_date(date):
        search = "SELECT COUNT(*) FROM students WHERE creation_time=%s"
        return SqlBase.get_count_of_added_at_date(search, date)

    @staticmethod
    def get_students_id_by_email(email):
        search = "SELECT id FROM students WHERE email=%s"
        return SqlBase.get_id_by_email(search, email)

    @staticmethod
    def get_5_most_recent_created_students():
        search = "SELECT first_name, last_name, image_url, creation_time FROM students ORDER BY creation_time DESC LIMIT 5"
        return SqlBase.get_5_most_recent_created(search)

    @staticmethod
    def get_5_most_recent_updated_students():
        search = "SELECT first_name, last_name, image_url, last_updated FROM students ORDER BY last_updated DESC LIMIT 5"
        return SqlBase.get_5_most_recent_updated(search)

    @staticmethod
    def check_student_email_exists(email):
        search = "SELECT COUNT(*) FROM students WHERE email=%s"
        return SqlBase.check_email_exists(search, email)

    @staticmethod
    def get_search_term_by_order(term, index):
        if term == "date_asc":
            return 'SELECT id, first_name, last_name, email, password, creation_time, last_updated, image_url  from students ORDER BY creation_time ASC LIMIT {}, 5'.format(int(index))
        elif term == "date_desc":
            return 'SELECT id, first_name, last_name, email, password, creation_time, last_updated, image_url  from students ORDER BY creation_time DESC LIMIT {}, 5'.format(int(index))
        elif term == "name_asc":
            return 'SELECT id, first_name, last_name, email, password, creation_time, last_updated, image_url  from students ORDER BY last_name ASC LIMIT {}, 5'.format(int(index))
        elif term == "name_desc":
            return 'SELECT id, first_name, last_name, email, password, creation_time, last_updated, image_url  from students ORDER BY last_name DESC LIMIT {}, 5'.format(int(index))

    @staticmethod
    def get_row_count_of_students():
        count = "SELECT COUNT(*) FROM STUDENTS"
        result = SqlBase.get_count_of_rows_at_table(count)
        return result
