import mysql.connector
from data.mySql.SqlBase import SqlBase


class Admins(SqlBase):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_admin_by_email(email):
        search = "SELECT first_name, last_name, email, password, id, creation_time, last_updated, image_url FROM admins WHERE email=%s"
        return SqlBase.get_by_email(search, email)

    @staticmethod
    def set_new_admin(admin_data):
        add = "INSERT INTO admins (first_name, last_name, email, password, image_url, creation_time) VALUES (%s, %s, %s, %s, %s)"
        return SqlBase.set_new(add, admin_data)

    @staticmethod
    def delete_admin_by_id(id):
        delete = "DELETE FROM admins WHERE id=%s"
        return SqlBase.delete_by_id("admins", delete, id)

