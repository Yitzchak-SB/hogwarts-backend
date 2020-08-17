import mysql.connector
from data.mySql.SqlBase import SqlBase


class Skills(SqlBase):
    def __init__(self):
        super().__init__()