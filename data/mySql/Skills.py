from data.mySql.SqlBase import SqlBase
from data.mySql.context import get_cursor


class Skills(SqlBase):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_all_magic_skills():
        with get_cursor(SqlBase._connect()) as cursor:
            results = []
            search = "SELECT skill_name, num_of_levels, skill_description FROM skills"
            cursor.execute(search,)
            for (skill_name, num_of_levels, skill_description) in cursor:
                result = {"skill_name": skill_name, "num_of_levels": num_of_levels, "skill_description": skill_description}
                results.append(result)
            return results

    @staticmethod
    def add_new_magic_skill(skill_data):
        with get_cursor(SqlBase._connect()) as cursor:
            add = "INSERT INTO skills (skill_name, num_of_levels, skill_description) VALUES(%s, %s, %s)"
            cursor.execute(add, (skill_data["skill_name"], skill_data["num_of_levels"], skill_data["skill_description"],))
            return skill_data
