from flask import Flask, request, jsonify
from openpyxl import load_workbook

app = Flask(__name__)

# Load Excel
wb = load_workbook('data.xlsx')
sheet = wb['students']

students = {}
for row in sheet.iter_rows(min_row=2, values_only=True):
    if row[0]: # skip empty rows
        index = str(row[0]).strip().upper() # force uppercase, no spaces
        name = str(row[1]).strip()
        password = str(row[2]).strip()
        students[index] = {'name': name, 'password': password}

print("LOADED STUDENTS:", students) # Check Render logs

@app.route('/ussd', methods=['POST'])
def ussd():
    data = request.get_json()
    
    session_id = data.get('sessionID', '')
    user_id = data.get('userID', '')
    msisdn = data.get('msisdn', '')
    user_input = data.get('message', '').strip()

    if user_input == '':
        return jsonify({"sessionID": session_id, "userID": user_id, "msisdn": msisdn, "message": "Welcome to TTU Results Checker\n1. Login to view grades\n2. Exit", "continueSession": True})

    if user_input == '1':
        return jsonify({"sessionID": session_id, "userID": user_id, "msisdn": msisdn, "message": "Enter IndexNumber*Password", "continueSession": True})

    if '*' in user_input:
        try:
            index, password = user_input.split('*')
            index = index.strip().upper() # make input uppercase too
            password = password.strip()
            
            print(f"TRYING: {index} with {password}") # Check Render logs
            
            if index in students and students[index]['password'] == password:
                name = students[index]['name']
                msg = f"Welcome {name}\nLogin Successful"
            else:
                msg = "Invalid Index or Password"
                
            return jsonify({"sessionID": session_id, "userID": user_id, "msisdn": msisdn, "message": msg, "continueSession": False})
        except Exception as e:
            return jsonify({"sessionID": session_id, "userID": user_id, "msisdn": msisdn, "message": f"Error: {str(e)}", "continueSession": False})

    if user_input == '2':
        return jsonify({"sessionID": session_id, "userID": user_id, "msisdn": msisdn, "message": "Goodbye", "continueSession": False})

if __name__ == '__main__':
    app.run()
