import mysql.connector
from data.mySql.SqlBase import SqlBase


class Skills(SqlBase):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_all_magic_skills():
        try:
            results = []
            connection = SqlBase._connect()
            cursor = connection.cursor()
            search = "SELECT skill_name, num_of_levels, skill_description FROM skills"
            cursor.execute(search,)
            for (skill_name, num_of_levels, skill_description) in cursor:
                result = {"skill_name": skill_name, "num_of_levels": num_of_levels, "skill_description": skill_description}
                results.append(result)
            return results
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def add_new_magic_skill(skill_data):
        try:
            connection = SqlBase._connect()
            cursor = connection.cursor()
            add = "INSERT INTO skills (skill_name, num_of_levels, skill_description) VALUES(%s, %s, %s)"
            cursor.execute(add, (skill_data["skill_name"], skill_data["num_of_levels"], skill_data["skill_description"],))
            connection.commit()
            return skill_data
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()