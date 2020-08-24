from flask import Flask, request, json
from flask_cors import CORS
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import atexit
from data.DataLayer import DataLayer
from Validations import Validations
from data.JsonEnc import JsonEnc
from data.mySql.Admins import Admins


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id
users = []
admins = Admins.get_all_admins()
for admin in admins:
    users.append(User(admin["id"], admin["email"], admin["password"]))

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']

    return userid_table.get(user_id, None)

app = Flask(__name__)
cors = CORS(app)
data_layer = DataLayer()
app.config['SECRET_KEY'] = 'super-secret'
jwt = JWT(app, authenticate, identity)



@app.route("/student/<student_email>")
@jwt_required()
def get_student_by_email(student_email):
    try:
        Validations.validate_student_by_email(student_email)
    except ValueError as e:
        print(e)
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                  mimetype="application/json")
    try:
        student = data_layer.get_student_by_email(student_email)
        return app.response_class(response=json.dumps(student.get_student_secure_data()), status=200, mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Student not found"}), status=404, mimetype="application/json")


@app.route("/student-del", methods=["POST"])
@jwt_required()
def delete_student():
    try:
        request_data = request.json
        if request_data is not None:
            admin_data = request_data["admin"]
            student_data = request_data["student"]
            student_id = data_layer.get_student_id_by_email(
                student_data["email"])
            try:
                Validations.validate_admin(admin_data, data_layer)
                Validations.validate_existing(
                    student_data, data_layer._students)
            except ValueError as e:
                print(e)
                return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                          mimetype="application/json")
            student = data_layer.delete_student(student_id)
            return app.response_class(response=json.dumps({"message": "{} was deleted".format(student_data["email"]), "deleted": student}), status=200, mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Student not found"}), status=404,
                                  mimetype="application/json")


@app.route("/student")
@jwt_required()
def get_count_of_students_added_at_date():
    date = request.args.get("date")
    date = date.replace("/", "_")
    result = data_layer.get_count_of_students_added_at_date(date)
    return app.response_class(response=json.dumps({"result": result}, indent=1), status=200, mimetype="application/json")



@app.route("/student", methods=["POST"])
@jwt_required()
def add_new_student():
    try:
        request_data = request.json["data"]

        if request_data is not None:
            admin_data = request_data["admin"]
            student_data = request_data["student"]
            try:
                Validations.validate_admin(admin_data, data_layer)
                Validations.validate_add_new_user(student_data)
            except ValueError as e:
                print(e)
                return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                          mimetype="application/json")
            data_layer.create_new_student(student_data)
            return app.response_class(response=json.dumps({"message": "{} was created".format(student_data["email"])}), status=200, mimetype="application/json")
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")


@app.route("/student/login", methods=["POST"])
@jwt_required()
def login_student():
    try:
        student_data = request.json
        if student_data is not None:
            try:
                Validations.validate_existing(
                    student_data, data_layer._students)
            except ValueError as e:
                print(e)
                return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                          mimetype="application/json")
            student = data_layer.get_student_by_email(student_data["email"])
            return app.response_class(response=json.dumps(student, cls=JsonEnc, indent=1), status=200, mimetype="application/json")
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")


@app.route("/student/edit", methods=["POST"])
@jwt_required()
def edit_student():
    try:
        raw_data = request.json
        student_data = raw_data["data"]["student"]
        if student_data:
            try:
                Validations.validate_existing(
                    student_data, data_layer._students)
            except ValueError as e:
                print(e)
                return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                          mimetype="application/json")
            student = data_layer.set_student_by_email(raw_data["data"])
            return app.response_class(response=json.dumps(student, cls=JsonEnc, indent=1), status=200, mimetype="application/json")
    except KeyError as e:
        print(e)
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")


@app.route("/students")
@jwt_required()
def get_all_students():
    term = request.args.get("term")
    index = request.args.get("index")
    [students, row_count] = data_layer.get_all_students(term, index)
    return app.response_class(response=json.dumps({"students": students, "row_count": row_count}), status=200, mimetype="application/json")


@app.route("/students/")
@jwt_required()
def get_students_by_added_date():
    try:
        date = request.args.get("date")
        date_str = date.replace("_", "/")
        try:
            Validations.validate_date(date_str)
        except ValueError as e:
            print(e)
            return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                      mimetype="application/json")
        students = {}
        students_pool = data_layer.get_all_students()
        for key in students_pool:
            if students_pool[key]["_creation_time"] == date_str:
                students[students_pool[key]["_email"]] = students_pool[key]
        return app.response_class(response=json.dumps(students, cls=JsonEnc, indent=1), status=200, mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")


@app.route("/updated")
@jwt_required()
def get_most_recent_updated_students():
    try:
        results = data_layer.get_most_recent_updated_students()
        return app.response_class(response=json.dumps(results), status=200, mimetype="application/json")

    except KeyError:
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")


@app.route("/created")
@jwt_required()
def get_most_recent_created_students():
    try:
        results = data_layer.get_most_recent_created_students()
        return app.response_class(response=json.dumps(results), status=200, mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")


@app.route("/admin", methods=["POST"])
@jwt_required()
def add_new_admin():
    try:
        admin_data = request.json
        if admin_data is not None:
            try:
                Validations.validate_add_new_user(admin_data)
            except ValueError as e:
                print(e)
                return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                          mimetype="application/json")
            data_layer.create_new_admin(admin_data)
            return app.response_class(response=json.dumps({"message": "{} was created".format(admin_data["email"])}), status=200, mimetype="application/json")
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")


@app.route("/admin/login", methods=["POST"])
@jwt_required()
def login_admin():
    try:
        admin_data = request.json
        print(admin_data)
        if admin_data is not None:
            try:
                Validations.validate_admin_login(
                    admin_data, data_layer)
                print(admin_data["username"])
                admin = data_layer.get_admin_by_email(admin_data["username"])
            except ValueError as e:
                print(e)
                return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                          mimetype="application/json")
            return app.response_class(response=json.dumps(admin, cls=JsonEnc, indent=1), status=200, mimetype="application/json")
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")

@app.route("/desire")
@jwt_required()
def get_count_of_desired_skill():
    skill = request.args.get("skill")
    level = request.args.get("level")
    if level:
        count = data_layer.get_count_of_desired_skills_by_level(skill, level)
    else:
        count = data_layer.get_count_of_desired_skills(skill)
    return app.response_class(response=json.dumps({skill: count}), status=200, mimetype="application/json")


@app.route("/exist")
@jwt_required()
def get_count_of_existing_skill():
    skill = request.args.get("skill")
    level = request.args.get("level")
    max_level = request.args.get("max_level")
    if level:
        count = data_layer.get_count_of_existing_skills_by_level(skill, level)
    elif max_level:
        count = data_layer.get_count_of_existing_skills_by_all_levels(skill, max_level)
    else:
        count = data_layer.get_count_of_existing_skills(skill)
    return app.response_class(response=json.dumps({skill: count}), status=200, mimetype="application/json")


@app.route("/desire", methods=["POST"])
@jwt_required()
def add_desired_skill():
    try:
        data = request.json
        if data is not None:
            try:
                Validations.validate_email_existing(
                    data["email"], data_layer._students)
                Validations.validate_email_format(data["email"])
            except ValueError as e:
                print(e)
                return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                          mimetype="application/json")
            data_layer.add_desired_skill_by_email(data)
            return app.response_class(response=json.dumps({"message": "{} level {} was added to {}".format(data["skill"]["name"], data["skill"]["level"], data["email"])}), status=200, mimetype="application/json")
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")


@app.route("/exist", methods=["POST"])
@jwt_required()
def add_existing_skill():
    try:
        data = request.json
        if data is not None:
            try:
                Validations.validate_email_existing(
                    data["email"], data_layer._students)
                Validations.validate_email_format(data["email"])
            except ValueError as e:
                print(e)
                return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                          mimetype="application/json")
            data_layer.add_existing_skill_by_email(data)
            return app.response_class(response=json.dumps({"message": "{} level {} was added to {}".format(
                data["skill"]["name"], data["skill"]["level"], data["email"])}), status=200, mimetype="application/json")
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")


@app.route("/skills")
@jwt_required()
def get_all_magic_skill():
    try:
        skills = data_layer.get_all_magic_skills()
        return app.response_class(response=json.dumps({"skills": skills}), status=200,
                                  mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")


@app.route("/skills", methods=["POST"])
@jwt_required()
def add_new_magic_skill():
    try:
        skill_data = request.json
        if skill_data is not None:
            data_layer.add_new_magic_skills(skill_data)
            return app.response_class(response=json.dumps({"added_skill": skill_data}), status=200, mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")



@atexit.register
def shutdown():
    data_layer.shutdown()


if __name__ == "__main__":
    app.run(debug=True)
