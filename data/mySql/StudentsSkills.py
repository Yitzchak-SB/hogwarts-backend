import mysql.connector
from data.mySql.SqlDataLayer


class StudentsSkills(SqlDataLayer):
    def __init__(self):
        super().__init__()
