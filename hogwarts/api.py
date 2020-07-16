from flask import Flask, request, json
from data.DataLayer import DataLayer
from Validations import Validations
from data.JsonEnc import JsonEnc

app = Flask(__name__)


@app.before_first_request
def setup():
    global data_layer
    data_layer = DataLayer()
    data_layer.load_students()
    data_layer.load_admins()


@app.route("/student/<student_email>")
def get_student_by_email(student_email):
    try:
        Validations.validate_student_by_email(student_email)
    except ValueError as e:
        print(e)
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                  mimetype="application/json")
    try:
        student = data_layer.get_student_by_email(student_email)
        return app.response_class(response=json.dumps(student), status=200, mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Student not found"}), status=404, mimetype="application/json")


@app.route("/student", methods=["DELETE"])
def delete_student():
    try:
        request_data = request.json
        if request_data is not None:
            admin_data = request_data["admin"]
            student_data = request_data["student"]
            try:
                Validations.validate_admin(admin_data, data_layer)
                Validations.validate_existing(student_data, data_layer._students)
            except ValueError as e:
                print(e)
                return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                          mimetype="application/json")
            student = data_layer.get_student_by_email(student_data["email"])
            data_layer.delete_student(student_data["email"])
            data_layer.persist_all_students()
            return app.response_class(response=json.dumps({"message": "{} was deleted".format(student_data["email"]), "deleted": student}), status=200, mimetype="application/json")
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Student not found"}), status=404,
                                  mimetype="application/json")


@app.route("/student", methods=["POST"])
def add_new_student():
    try:
        request_data = request.json
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
            data_layer.persist_all_students()
            return app.response_class(response=json.dumps({"message": "{} was created".format(student_data["email"])}), status=200, mimetype="application/json")
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")


@app.route("/student/login", methods=["POST"])
def login_student():
    try:
        student_data = request.json
        if student_data is not None:
            try:
                Validations.validate_existing(student_data, data_layer._students)
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
def edit_student():
    try:
        student_data = request.json
        if student_data is not None:
            try:
                Validations.validate_existing(student_data, data_layer._students)
            except ValueError as e:
                print(e)
                return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                          mimetype="application/json")
            data_layer.set_student_by_email(student_data)
            student = data_layer.get_student_by_email(student_data["email"])
            data_layer.persist_all_students()
            return app.response_class(response=json.dumps(student, cls=JsonEnc, indent=1), status=200, mimetype="application/json")
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")


@app.route("/students")
def get_all_students():
    students = data_layer.get_all_students_json()
    return app.response_class(response=students, status=200, mimetype="application/json")


@app.route("/students/")
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
        data_layer.persist_all_students()
        return app.response_class(response=json.dumps(students, cls=JsonEnc, indent=1), status=200, mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")


@app.route("/desire")
def get_count_of_desired_skill():
    skill = request.args.get("skill")
    count = data_layer.get_count_of_desired_skills(skill)
    data_layer.persist_all_students()
    return app.response_class(response=json.dumps({skill: count}), status=200, mimetype="application/json")


@app.route("/have")
def get_count_of_existing_skill():
    skill = request.args.get("skill")
    count = data_layer.get_count_of_existing_skills(skill)
    data_layer.persist_all_students()
    return app.response_class(response=json.dumps({skill: count}), status=200, mimetype="application/json")


@app.route("/desire", methods=["POST"])
def add_desired_skill():
    try:
        data = request.json
        if data is not None:
            try:
                Validations.validate_email_existing(data["email"], data_layer._students)
                Validations.validate_email_format(data["email"])
            except ValueError as e:
                print(e)
                return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                          mimetype="application/json")
            data_layer.add_desired_skill_by_email(data)
            data_layer.persist_all_students()
            return app.response_class(response=json.dumps({"message": "{} level {} was added to {}".format(data["skill"]["name"], data["skill"]["level"], data["email"])}), status=200, mimetype="application/json")
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")

@app.route("/have", methods=["POST"])
def add_existing_skill():
    try:
        data = request.json
        if data is not None:
            try:
                Validations.validate_email_existing(data["email"], data_layer._students)
                Validations.validate_email_format(data["email"])
            except ValueError as e:
                print(e)
                return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                          mimetype="application/json")
            data_layer.add_existing_skill_by_email(data)
            data_layer.persist_all_students()
            return app.response_class(response=json.dumps({"message": "{} level {} was added to {}".format(
                data["skill"]["name"], data["skill"]["level"], data["email"])}), status=200, mimetype="application/json")
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")
    except KeyError:
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=404,
                                  mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)
