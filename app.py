from flask import Flask, request, jsonify
from openpyxl import load_workbook

app = Flask(__name__)

# Load Excel
wb = load_workbook('data.xlsx')
sheet = wb['students']

students = {}
for row in sheet.iter_rows(min_row=2, values_only=True):
    index, name, password = row
    students[index] = {'name': name, 'password': password}

@app.route('/ussd', methods=['POST'])
def ussd():
    data = request.get_json()
    
    session_id = data.get('sessionID', '')
    user_id = data.get('userID', '')
    msisdn = data.get('msisdn', '')
    user_input = data.get('message', '') # Arkesel calls it "message" not "input"

    # Step 1: Welcome Menu
    if user_input == '':
        return jsonify({
            "sessionID": session_id,
            "userID": user_id,
            "msisdn": msisdn,
            "message": "Welcome to TTU Results Checker\n1. Login to view grades\n2. Exit",
            "continueSession": True
        })

    # Step 2: Ask for credentials
    if user_input == '1':
        return jsonify({
            "sessionID": session_id,
            "userID": user_id,
            "msisdn": msisdn,
            "message": "Enter IndexNumber*Password",
            "continueSession": True
        })

    # Step 3: Check login
    if '*' in user_input:
        try:
            index, password = user_input.split('*')
            if index in students and str(students[index]['password']) == password:
                name = students[index]['name']
                return jsonify({
                    "sessionID": session_id,
                    "userID": user_id,
                    "msisdn": msisdn,
                    "message": f"Welcome {name}\nLogin Successful",
                    "continueSession": False
                })
            else:
                return jsonify({
                    "sessionID": session_id,
                    "userID": user_id,
                    "msisdn": msisdn,
                    "message": "Invalid Index or Password",
                    "continueSession": False
                })
        except:
            return jsonify({
                "sessionID": session_id,
                "userID": user_id,
                "msisdn": msisdn,
                "message": "Wrong format. Use: Index*Password",
                "continueSession": False
            })

    # Exit
    if user_input == '2':
        return jsonify({
            "sessionID": session_id,
            "userID": user_id,
            "msisdn": msisdn,
            "message": "Goodbye",
            "continueSession": False
        })

if __name__ == '__main__':
    app.run()
