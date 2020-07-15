from flask import Flask, request, json
from data.DataLayer import DataLayer
from Validations import Validations
app = Flask(__name__)


@app.before_first_request
def setup():
    global data_layer
    data_layer = DataLayer()
    data_layer.load_students()
    data_layer.load_admins()


@app.route("/student/<student_email>")
def get_student_by_email(student_email):
    Validations.validate_student_by_email(student_email)
    student = data_layer.get_student_by_email(student_email)
    return app.response_class(response=json.dumps(student), status=200, mimetype="application/json")


@app.route("/student", methods=["DELETE"])
def delete_student():
    request_data = request.json
    admin_data = request_data["admin"]
    student_data = request_data["student"]
    Validations.validate_admin(admin_data, data_layer)
    Validations.validate_existing(student_data, data_layer._students)
    data_layer.delete_student(student_data["email"])
    return app.response_class(response=json.dumps({"message": "{} was deleted".format(student_data["email"]) }), status=200, mimetype="application/json")


@app.route("/student", methods=["POST"])
def add_new_student():
    request_data = request.json
    admin_data = request_data["admin"]
    student_data = request_data["student"]
    Validations.validate_admin(admin_data, data_layer)
    Validations.validate_add_new_user(student_data)
    data_layer.create_new_student(student_data)
    return app.response_class(response=json.dumps({"message": "{} was created".format(student_data["email"]) }), status=200, mimetype="application/json")


@app.route("/student/login", methods=["POST"])
def login_student():
    student_data = request.json
    Validations.validate_existing(student_data, data_layer._students)
    student = data_layer.get_student_by_email(student_data["email"])
    return app.response_class(response=json.dumps(student), status=200, mimetype="application/json")


@app.route("/student/edit", methods=["POST"])
def edit_student():
    student_data = request.json
    Validations.validate_existing(student_data, data_layer._students)
    data_layer.set_student_by_email(student_data)
    student = data_layer.get_student_by_email(student_data["email"])
    return app.response_class(response=json.dumps(student), status=200, mimetype="application/json")


@app.route("/students")
def get_all_students():
    students = data_layer.get_all_students_json()
    return app.response_class(response=students, status=200, mimetype="application/json")


@app.route("/students/")
def get_students_by_added_date():
    date = request.args.get("date")
    date_str = date.replace("_", "/")
    Validations.validate_date(date_str)
    students = {}
    students_pool = data_layer.get_all_students()
    for key in students_pool:
        if students_pool[key]["_creation_time"] == date_str:
            students[students_pool[key]["_email"]] = students_pool[key]
    return app.response_class(response=json.dumps(students), status=200, mimetype="application/json")


@app.route("/desire")
def get_count_of_desired_skill():
    skill = request.get("skill")
    pass


@app.route("/have")
def get_count_of_skill():
    skill = request.get("skill")
    pass


if __name__ == "__main__":
    app.run(debug=True)
