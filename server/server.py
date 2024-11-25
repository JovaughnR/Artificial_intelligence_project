from flask import Flask, request, jsonify, make_response
from database import Database, hash_string
import person as user
from flask_cors import CORS
# from predictor import predict
from main import PrologCalculator
# import logging


# logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
CORS(app, supports_credentials=True)

# Initialize a database object and initialize the attributes
db = Database(
   host="localhost", 
   user="root", 
   password="",  
   db="ai_project"
)

prolog = PrologCalculator(db)

unique_key = lambda key: hash_string(key)
sessions = dict({})

secret_key = '31c0209df72619cdf46'

@app.route('/login', methods=["POST"])
def authenticate_user():
    data = request.get_json()
    usrID = data.get("userID")
    passwd = data.get("password")

    status = db.is_user_registered(usrID, passwd)
    if status:
        usrKey = unique_key(f"{secret_key}{usrID}{passwd}")
        sessions[usrKey] = usrID
        res = jsonify({"type": status[1]})
        response = make_response(res)
        response.set_cookie(
            "secret_key", usrKey, max_age=3600, 
            httponly=True
        )
        return response, 200

    return jsonify({ "msg": "Invalid credentials"}), 401


@app.route('/register', methods=["POST"])
def sign_up_user():
    data = request.get_json()
    info = [ 
        data.get('id'), data.get('fName'),
        data.get('lName'), data.get('email'),
    ]
    if data.get('type') == 'student':
        info.append(data.get('programme'))
        db.create_student(user.Student(*info))
    else:
        db.create_staff(user.Staff(*info))

    return jsonify({"status": True, }), 201


@app.route('/', methods=["GET"])
def home():
    sessionKey = request.cookies.get("secret_key")
    if sessionKey in sessions:
        client = db.get_user_byID(sessions[sessionKey])
        full_name = f"{client[1]} {client[2]}"
        return jsonify({"name": full_name}), 200
    
    return jsonify({"path": "login.html"}), 401
    

@app.route('/logout', methods=["GET"])
def logout():
    sessionKey = request.cookies.get("secret_key")
    if sessionKey and sessionKey in sessions:
        del sessions[sessionKey] 
        response = make_response(jsonify({"status": "Logged out"}), 200)
        response.set_cookie("secret_key", '', expires=0) 
        return response
    return jsonify({"status": "Not logged in"}), 401

@app.route('/student/records', methods=["POST", "GET"])
def get_records():
    print("End point requested")
    ID = sessions[request.cookies.get("secret_key")]
    print('sessionKey', ID)
    if request.method == 'GET':
        records = db.get_student_records(ID)
    elif request.method == 'POST':
        data = request.get_json()
        year = data.get('year')
        records = db.get_student_records(ID, year)


    if records:
        return jsonify({"records": records}), 200
    else:
        return jsonify({"status": "no records found"}), 401
    
@app.route('/student/bot', methods=["POST"])
def bot9():
    data = request.get_json()
    query = data.get('query')
    query, res = predict(query)
    print("Query: ", query)
    print("res: ", res)
    print(query, res)
    return jsonify({"query":query, "res": res})

@app.route('/student/gpa', methods=["POST"])
def get_gpa():
    print("End point requested")
    sessionKey = request.cookies.get("secret_key")
    print("Session Key:", sessionKey)
    if sessionKey in sessions:
        data = request.get_json()
        usrID = sessions[sessionKey]
        year = data['year']

        gpa1 = prolog.calculate_GPA(usrID, 1, year)
        gpa2 = prolog.calculate_GPA(usrID, 2, year)
        gpaT = prolog.cumulative_GPA(usrID, year)

        return jsonify({"GPAs":[gpa1, gpa2, gpaT]}), 200
    
    return jsonify({"status": "no records found"}), 401


@app.route('/staff/stud-record', methods=["POST"])
def get_student_records():
    data = request.get_json()
    stud_id = data.get('studID')
    year = data.get("year")

    student = db.get_user_byID(stud_id)
    name = f"{student[1]} {student[2]}"
    prog = student[4]

    # 1 Calculate student GPA
    gpa1 = prolog.calculate_GPA(stud_id,1,year)
    gpa2 = prolog.calculate_GPA(stud_id,2,year)
    gpaT = prolog.cumulative_GPA(stud_id, year)

    if not (gpa1 or gpa2 or gpaT):
        return jsonify({"status": "No data found"}), 204

    res = jsonify({"student":[
        name, stud_id, gpa1, gpa2, gpaT, prog
    ]}), 200

    return res
        
@app.route('/staff/target-students', methods=["POST"])
def get_target_gpa():
    data = request.get_json()
    year = data.get("year")
    targetGPA = data.get("targetGPA")
    students = db.get_all_students()
    grade = prolog.get_grade(targetGPA)
    targeted_students = []

    for student in students:
        id = student[0]
        if db.isRegisteredForCourses(id):
            gpa1 = prolog.calculate_GPA(id, 1, year)
            gpa2 = prolog.calculate_GPA(id, 2, year)
            gpaT = prolog.cumulative_GPA(id, year)

            A = prolog.get_grade(gpa1) == grade
            B = prolog.get_grade(gpa2) == grade

            if A or B:
                name = f"{student[1]} {student[2]}"
                prog = student[4]
                targeted_students.append(
                    [name, id, gpa1, gpa2, gpaT, prog]
                )
    if not targeted_students:
        return jsonify({"status": "No data found"}), 204
    return jsonify({"student": targeted_students}), 200

@app.route('/add-module-details/new', methods=["POST"])
def get_module_details():
    data = request.get_json()
    info = (
        data.get('moduleCode'), data.get('moduleName'),
        data.get('stdID'), data.get('year'), 
        data.get('semester'), data.get('gradepoint') 
    )
    status = db.insert_grade(*info)
    print(status)
    if status:
        return jsonify({"status": status}), 200
    
    return jsonify({"status": status}), 500

@app.route('/register-student/new', methods=["POST"])
def register_student():
    print('End point requested')
    data = request.get_json()
    info = (
        data.get('stdID'), data.get('fName'),
        data.get('lName'), data.get('email'),
        data.get('programme')
    )
    print(info)
    student = user.Student(*info)
    status = db.create_student(student)
    print(status)
    if status:
        return jsonify({"status": True}), 200
    return jsonify({"status":False}), 409

@app.route('/gpa-threshold', methods=["GET"])
def get_default_gpa():
    print("End point requested")
    gpa = prolog.get_default_gpa()
    if gpa:
        print("GPA:", gpa)
        return jsonify({"GPA": gpa}), 200
    return jsonify({"GPA": 0.0}), 204

@app.route('/update-gpa-threshold', methods=["POST"])
def update_default_gpa():
    print("End point requested")
    data = request.get_json()
    result = prolog.update_gpa_threshold(data["gpa"])
    if result:
        return jsonify({"status": True}), 200
    return jsonify({"status": False}), 500
    

@app.route('/admin-add-module', methods=["POST"])
def add_new_module():
    data = request.get_json()
    info = (data.get("name"), data.get("code"),  
        data.get("credit"))
    
    status = db.insert_module(*info)
    if status:
        return jsonify({"status": True}), 200
    return jsonify({"status": False}), 409

            
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3001)
