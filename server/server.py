from flask import Flask, request, jsonify, make_response
from database import Database, hash_string
import person as user
from flask_cors import CORS
from main import PrologCalculator
# from predictor import predict

# Setup Flask app and CORS
app = Flask(__name__)
CORS(app, supports_credentials=True)

# Initialize database and Prolog calculator
db = Database(
    host="localhost", 
    user="root", 
    password="", 
    database="ai_project"
)
prolog = PrologCalculator(db)

# Secret key for session management
secret_key = '31c0209df72619cdf46'
sessions = {}

# Utility functions
unique_key = lambda key : hash_string(key)

def create_response(message, status_code=200, cookie=None):
    response = make_response(jsonify(message), status_code)
    if cookie:
        response.set_cookie("secret_key", cookie, max_age=3600, httponly=True)
    return response

def handle_error(message, status_code=400):
    return jsonify({"error": message}), status_code

# Routes
@app.route('/login', methods=["POST"])
def authenticate_user():
    data = request.get_json()
    usrID, passwd = data.get("userID"), data.get("password")

    status = db.is_user_registered(usrID, passwd)
    print("Status: ", status)
    if status:
        usrKey = unique_key(f"{secret_key}{usrID}{passwd}")
        sessions[usrKey] = usrID
        return create_response({"type": status[1]}, 200, usrKey)

    return handle_error("Invalid credentials", 401)

@app.route('/verify-id', methods=["POST"])
def verify_user_id():
    data = request.get_json()
    status = db.is_user_registered(data.get("id"), "")
    return jsonify({'status': status}), 200 if status else 204


@app.route('/authenticate', methods=["POST"])
def authorise_user(): 
    data = request.get_json()
    status = db.update_password(data.get("id"), data.get("passwd"))
    return jsonify({'status': status}), 200 if status else 500

@app.route('/register', methods=["POST"])
def sign_up_user():
    data = request.get_json()
    user_info = [data.get('id'), data.get('fName'), data.get('lName'), data.get('email')]

    if data.get('type') == 'student':
        user_info.append(data.get('programme'))
        status = db.create_student(user.Student(*user_info))
    elif data.get('type') == 'staff':
        status = db.create_staff(user.Staff(*user_info))

    return jsonify({"status": True if status else False}), 200 if status else 409

@app.route('/', methods=["GET"])
def home():
    sessionKey = request.cookies.get("secret_key")
    if sessionKey in sessions:
        client = db.get_user_byID(sessions[sessionKey])
        full_name = f"{client[1]} {client[2]}" if client else "Administrator"
        return jsonify({"name": full_name}), 200
    return jsonify({"path": "login.html"}), 401

@app.route('/logout', methods=["GET"])
def logout():
    sessionKey = request.cookies.get("secret_key")
    if sessionKey in sessions:
        del sessions[sessionKey]
        return create_response({"status": "Logged out"}, 200, '')
    return handle_error("Not logged in", 401)

@app.route('/student/records', methods=["POST", "GET"])
def get_student_records():
    ID = sessions.get(request.cookies.get("secret_key"))
    if not ID:
        return handle_error("Session expired", 401)
    if request.method == 'GET':
        records = db.get_records_by_year(ID)
    elif request.method == 'POST':
        year = request.get_json().get('year')
        records = db.get_records_by_year(ID, year)
        print("Records from server:", records)

    return jsonify({"records": records if records else "No records found"}), 200 if records else 401

@app.route('/student/gpa', methods=["POST"])
def get_gpa():
    sessionKey = request.cookies.get("secret_key")
    if sessionKey in sessions:
        data = request.get_json()
        usrID, year = sessions[sessionKey], data['year']

        gpa1 = prolog.calculate_GPA(usrID, 1, year)
        gpa2 = prolog.calculate_GPA(usrID, 2, year)
        gpaT = prolog.cumulative_GPA(usrID, year)

        return jsonify({"GPAs": [gpa1, gpa2, gpaT]}), 200 if gpa1 or gpa2 or gpaT else 401

    return handle_error("No records found", 401)

@app.route('/staff/stud-record', methods=["POST"])
def get_student_records_for_staff():
    data = request.get_json()
    stud_id, year = data.get('studID'), data.get("year")

    student = db.get_user_byID(stud_id)
    if not student:
        return handle_error("Student not found", 404)

    name = f"{student[1]} {student[2]}"
    prog = student[4]
    gpa1 = prolog.calculate_GPA(stud_id, 1, year)
    gpa2 = prolog.calculate_GPA(stud_id, 2, year)
    gpaT = prolog.cumulative_GPA(stud_id, year)

    if not any([gpa1, gpa2, gpaT]):
        return handle_error("No GPA data found", 204)

    return jsonify({"student": [name, stud_id, gpa1, gpa2, gpaT, prog]}), 200

@app.route('/staff/target-students', methods=["POST"])
def get_target_gpa():
    data = request.get_json()
    year = data.get("year")
    targetGPA = data.get("targetGPA")
    
    # Fetch all students from the database
    students = db.get_all_students()
    # Determine the grade that corresponds to the target GPA
    grade = prolog.get_grade(targetGPA)
    
    targeted_students = []
    
    for student in students:
        stud_id = student[0]
        # Check if the student is registered for courses

        # Calculate the GPAs for the student
        gpa1 = prolog.calculate_GPA(stud_id, 1, year)
        gpa2 = prolog.calculate_GPA(stud_id, 2, year)
        gpaT = prolog.cumulative_GPA(stud_id, year)

        # Check if the GPA meets the target grade for either semester
        A = prolog.get_grade(gpa1) == grade
        B = prolog.get_grade(gpa2) == grade

        # If the student meets the target GPA, add them to the list
        if A or B:
            name = f"{student[1]} {student[2]}"  # Full name
            prog = student[4]  # Programme
            targeted_students.append([name, stud_id, gpa1, gpa2, gpaT, prog])

    # Return the list of targeted students, or a 204 status if no students match the target GPA
    if not targeted_students:
        return jsonify({"status": "No data found"}), 204
    return jsonify({"student": targeted_students}), 200


@app.route('/admin-add-module', methods=["POST"])
def add_new_module():
    data = request.get_json()
    info = (data.get("name"), data.get("code"), data.get("credit"))

    status = db.insert_module(*info)
    return jsonify({"status": True if status else False}), 200 if status else 409

@app.route('/add-module-details', methods=["POST"])
def add_module_details():
    # Parse incoming JSON data
    data = request.get_json()
    
    # Extract relevant information from the incoming data
    module_code = data.get('moduleCode')
    module_name = data.get('moduleName')
    student_id = data.get('stdID')
    year = data.get('year')
    semester = data.get('semester')
    gradepoint = data.get('gradepoint')

    # Insert the grade information into the database
    status = db.insert_grade(module_code, module_name, student_id, year, semester, gradepoint)

    # Log the status for debugging purposes
    print("Insertion status:", status)

    # Return a success response if insertion was successful, otherwise an error response
    if status:
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "failure"}), 500

@app.route('/gpa-threshold', methods=["GET"])
def get_default_gpa():
    """
    Endpoint to retrieve the default GPA threshold.
    """
    gpa = prolog.get_default_gpa()
    if gpa is not None:
        return jsonify({"GPA": gpa}), 200
    return jsonify({"error": "Failed to retrieve GPA"}), 500

@app.route('/update-gpa-threshold', methods=["POST"])
def update_default_gpa():
    # Get the new GPA threshold value from the request
    data = request.get_json()
    new_gpa_threshold = data.get("gpa")

    # Call the Prolog function to update the GPA threshold
    result = prolog.update_gpa_threshold(new_gpa_threshold)

    # If the update is successful, return a 200 status, otherwise return a 500 error
    if result:
        return jsonify({"status": True}), 200
    return jsonify({"status": False}), 500

@app.route('/student/bot', methods=["POST"])
def bot9():
    data = request.get_json()
    query = data.get('query')
    query, res = predict(query)
    return jsonify({"query": query, "res": res})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3001)
