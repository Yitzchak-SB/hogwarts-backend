import re
from datetime import datetime


class Validations:

    @staticmethod
    def validate_email_format(email):
        valid = re.search("[^@]+@[^@]+\.[^@]+", email)
        if valid is None:
            raise ValueError("This is not a valid email address")
        return True

    @staticmethod
    def validate_add_new_user(data):
        if not data["first_name"] or type(data["first_name"]) != str:
            raise ValueError("First name is not Valid")
        elif not data["last_name"] or type(data["last_name"]) != str:
            raise ValueError("Last name is not Valid")
        elif not data["email"] or not Validations.validate_email_format(data["email"]):
            raise ValueError("Email is not Valid")
        elif not data["password"] or type(data["password"]) != str:
            raise ValueError("Password is not Valid")
        return True

    @staticmethod
    def validate_existing(data, users_pool):
        """
        if not data["data"]["id"] or type(data["id"]) != str:
            raise ValueError("Id is not Valid")
        elif not data["data"]["password"] or type(data["password"]) != str:
            raise ValueError("Password is not Valid")
        elif data["initial_email"] not in users_pool:
            raise ValueError("User does not exist")"""

        return True

    @staticmethod
    def validate_email_existing(email, users_pool):
        if email not in users_pool:
            raise ValueError("User does not exist")
        return True

    @staticmethod
    def validate_email_duplicate(data, users_pool):
        if data["email"] in users_pool:
            raise ValueError("User already exists")
        return True

    @staticmethod
    def validate_student_by_email(email):
        if not email or not Validations.validate_email_format(email):
            raise ValueError("email is not Valid")
        return True

    @staticmethod
    def validate_date(date):
        if not date:
            raise ValueError("Date is not Valid")
        try:
            datetime.strptime(date, '%d/%m/%y')
        except ValueError:
            raise ValueError("Date is not Valid")
        return True

    @staticmethod
    def validate_login():
        pass

    @staticmethod
    def validate_admin(data, data_layer):
        try:
            email = data["_email"]
            admin = data_layer.get_admin_by_email(email)
            if data["_password"] != admin.get_password():
                raise ValueError("Admin not valid")
        except ValueError:
            print("Admin not valid")
        return True

    @staticmethod
    def validate_admin_login(data, data_layer):
        try:
            email = data["username"]
            admin = data_layer.get_admin_by_email(email)
            if data["password"] != admin.get_password():
                raise ValueError("Admin not valid")
        except ValueError:
            print("Admin not valid")
        return True
