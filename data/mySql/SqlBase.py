import mysql.connector
from decouple import config

from data.mySql.context import get_cursor


class SqlBase:

    @staticmethod
    def _connect():
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user=config("MYSQL_USER"),
                password=config("PASSWORD"),
                database="hogwarts"
            )
            connection.autocommit = False
            return connection
        except Exception as e:
            print("connection error: {}".format(e))

    @staticmethod
    def edit_by_email(edit_term, email, new_data):
        with get_cursor(SqlBase._connect()) as cursor:
            cursor.execute(edit_term, (new_data["_first_name"], new_data["_last_name"], new_data["_email"], new_data["_image_url"], new_data["_last_updated"], email,))
            return new_data

    @staticmethod
    def get_by_email(search_term, email):
        with get_cursor(SqlBase._connect()) as cursor:
            cursor.execute(search_term, (email, ))
            result = {}
            for (id, first_name, last_name, email, password, creation_time, last_updated, image_url) in cursor:
                result = { "id": id, "first_name": first_name, "last_name": last_name, "email": email, "image_url": image_url, "creation_time": creation_time,
                     "last_updated": last_updated, "password": password}
            return result

    @staticmethod
    def set_new(set_term, new_data):
        with get_cursor(SqlBase._connect()) as cursor:
            cursor.execute(set_term, (new_data["_first_name"], new_data["_last_name"],
                                 new_data["_email"], new_data["_password"], new_data["_image_url"], new_data["_creation_time"]))
            return cursor.lastrowid

    @staticmethod
    def delete_by_id(delete_term, id, table=False):
        with get_cursor(SqlBase._connect()) as cursor:
            if table == "students":
                delete_skills = "DELETE FROM students_skills WHERE student_id=%s"
                cursor.execute(delete_skills, (id,))
            cursor.execute(delete_term, (id,))
            return id

    @staticmethod
    def get_count_of_added_at_date(search_term, date):
        with get_cursor(SqlBase._connect()) as cursor:
            cursor.execute(search_term, (date,))
            result = cursor.fetchone()
            return result[0]


    @staticmethod
    def get_id_by_email(search_term, email):
        with get_cursor(SqlBase._connect()) as cursor:
            cursor.execute(search_term, (email,))
            result = cursor.fetchone()
            return result


    @staticmethod
    def get_5_most_recent_created(search_term):
        with get_cursor(SqlBase._connect()) as cursor:
            cursor.execute(search_term, )
            results = []
            for (first_name, last_name, image_url, creation_time) in cursor:
                results.append(
                    {"first_name": first_name, "last_name": last_name, "image_url": image_url,
                     "creation_time": creation_time})
            return results

    @staticmethod
    def get_5_most_recent_updated(search_term):
        with get_cursor(SqlBase._connect()) as cursor:
            cursor.execute(search_term, )
            results = []
            for (first_name, last_name, image_url, last_updated) in cursor:
                results.append(
                    {"first_name": first_name, "last_name": last_name, "image_url": image_url,
                     "last_updated": last_updated})
            return results

    @staticmethod
    def get_count_of_rows_at_table(search_term):
        with get_cursor(SqlBase._connect()) as cursor:
            cursor.execute(search_term, ())
            result = cursor.fetchone()
            return result[0]
