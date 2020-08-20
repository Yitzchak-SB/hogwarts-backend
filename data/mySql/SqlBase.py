import mysql.connector
from decouple import config


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
        try:
            connection = SqlBase._connect()
            cursor = connection.cursor()
            cursor.execute(edit_term, (new_data["_first_name"], new_data["_last_name"], new_data["_email"], new_data["_image_url"], new_data["_last_updated"], email,))
            print(new_data)
            connection.commit()
            return new_data
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_by_email(search_term, email):
        try:
            connection = SqlBase._connect()
            cursor = connection.cursor()
            cursor.execute(search_term, (email, ))
            result = {}
            for (id, first_name, last_name, email, password, creation_time, last_updated, image_url) in cursor:
                result = { "id": id, "first_name": first_name, "last_name": last_name, "email": email, "image_url": image_url, "creation_time": creation_time,
                     "last_updated": last_updated, "password": password}
            return result
        except Exception as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def set_new(set_term, new_data):
        try:
            connection = SqlBase._connect()
            cursor = connection.cursor()
            connection.start_transaction()
            cursor.execute(set_term, (new_data["_first_name"], new_data["_last_name"],
                                 new_data["_email"], new_data["_password"], new_data["_image_url"], new_data["_creation_time"]))
            connection.commit()
            return cursor.lastrowid
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete_by_id(delete_term, id, table=False):
        try:
            connection = SqlBase._connect()
            cursor = connection.cursor()
            connection.start_transaction()
            if table == "students":
                delete_skills = "DELETE FROM students_skills WHERE student_id=%s"
                cursor.execute(delete_skills, (id,))
            cursor.execute(delete_term, (id,))
            connection.commit()
            return id
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_count_of_added_at_date(search_term, date):
        try:
            connection = SqlBase._connect()
            cursor = connection.cursor()
            cursor.execute(search_term, (date,))
            result = cursor.fetchone()
            return result[0]
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_id_by_email(search_term, email):
        try:
            connection = SqlBase._connect()
            cursor = connection.cursor()
            cursor.execute(search_term, (email,))
            result = cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_5_most_recent_created(search_term):
        try:
            connection = SqlBase._connect()
            cursor = connection.cursor()
            cursor.execute(search_term, )
            results = []
            for (first_name, last_name, image_url, creation_time) in cursor:
                results.append(
                    {"first_name": first_name, "last_name": last_name, "image_url": image_url,
                     "creation_time": creation_time})
            return results
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_5_most_recent_updated(search_term):
        try:
            connection = SqlBase._connect()
            cursor = connection.cursor()
            cursor.execute(search_term, )
            results = []
            for (first_name, last_name, image_url, last_updated) in cursor:
                results.append(
                    {"first_name": first_name, "last_name": last_name, "image_url": image_url,
                     "last_updated": last_updated})
            return results
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()


    @staticmethod
    def get_count_of_rows_at_table(search_term):
        try:
            connection = SqlBase._connect()
            cursor = connection.cursor()
            cursor.execute(search_term, ())
            result = cursor.fetchone()
            return result[0]
        except Exception as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()