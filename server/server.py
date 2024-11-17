from flask import Flask, request, jsonify, session
from database import Database 
import person as user
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize a database object and initialize the attributes
db = Database(
   host="localhost", 
   user="root", 
   password="", 
   db="ai_project"
)

unique_key = lambda key: Database.__hash(key)
sessions = dict({})

secret_key = '31c0209df72619cdf46'

@app.route('/login', methods=["POST"])
def authenticate_user():
    data = request.get_json()
    usrID = data.get("userID")
    passwd = data.get("password")

    # Authenticate the user
    status = db.lookupUser(usrID, passwd)
    # If authentication is successful
    if status:
        usrKey = unique_key(f"{secret_key}{passwd}{usrID}")
        sessions[usrID] = passwd
        sessions[usrkey] = True
        return jsonify({"key": usrkey}, 200)
    else:
        return jsonify({"status": False, "message": "Invalid credentials"}), 401

@app.route('/register', methods=["POST"])
def sign_up_user():
    data = request.get_json()
    info = [
        data.get('userID'), data.get('fName'),
        data.get('lName'), data.get('email'),
        data.get('passwd')
    ]
    if data.get('accountType') == 'student':
        info.append(data.get('programme'))
        db.create_student(user.Student(*info))
    else:
        info.append(data.get('staffType'))
        info.append(data.get('school'))
        db.create_staff(user.Staff(*info))

    return jsonify({"status": True, "message": "User registered successfully"}), 201

@app.route('/', methods=["GET"])
def home():
    # Check if the user is authorized based on the session
    if session.get('is_authorized'):
        return jsonify({"path": "index.html"}), 200
    else:
        return jsonify({"path": "login.html", "message": "Unauthorized user"}), 401

@app.route('/logout', methods=["GET"])
def logout():
    sessions.clear()
    return jsonify({"status": True, "message": "Logged out successfully"}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3001)
