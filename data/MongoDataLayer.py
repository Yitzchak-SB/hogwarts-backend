import pymongo


class MongoDataLayer:
    def __init__(self):
        self.__create()

    def __create(self):
        self.__client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.__db = self.__client["hogwarts"]

    def get_all_students(self):
        students_data = self.__db.students.find()
        students = list(students_data)
        return students

    def get_student_by_email(self, email):
        student = self.__db.students.find_one({"_email": email})
        return student

    def edit_student_by_email(self, email, new_student_data):
        self.__db.students.update({"_email": email}, new_student_data)

    def get_admin_by_email(self, email):
        admin = self.__db.admins.find_one({"_email": email})
        return admin

    def set_new_admin(self, admin_data):
        admin = self.__db.admins.insert_one(admin_data)
        return admin

    def set_new_student(self, student_data):
        student = self.__db.students.insert_one(student_data)
        return student

    def delete_student_by_id(self, id):
        student = self.__db.students.remove({"_id": id})
        return student
