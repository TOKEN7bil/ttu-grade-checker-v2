from flask import Flask, request, jsonify

app = Flask(__name__)

students = {
    "BCITD22003": {"name": "ERIC ORLEANS BOHAM", "password": "EOB22"},
    "BCITD22004": {"name": "JOHN KWAD WOYTE", "password": "JK22"},
    "BCITD22005": {"name": "AMA ADJEI", "password": "AA22"}
}

@app.route('/ussd', methods=['POST'])
@app.route('/ussd/', methods=['POST']) # ADD THIS LINE
def ussd():
    data = request.get_json()
    session_id = data.get('sessionID', '')
    user_id = data.get('userID', '')
    msisdn = data.get('msisdn', '')
    user_input = data.get('message', '').strip()

    print("GOT INPUT:", user_input) # For logs

    if user_input == '':
        return jsonify({"sessionID": session_id, "userID": user_id, "msisdn": msisdn, "message": "Welcome to TTU Results Checker\n1. Login to view grades\n2. Exit", "continueSession": True})

    if user_input == '1':
        return jsonify({"sessionID": session_id, "userID": user_id, "msisdn": msisdn, "message": "Enter IndexNumber*Password", "continueSession": True})

    if '*' in user_input:
        try:
            index, password = user_input.split('*')
            index = index.strip().upper()
            password = password.strip()
            
            if index in students and students[index]['password'] == password:
                msg = f"Welcome {students[index]['name']}\nLogin Successful"
            else:
                msg = "Invalid Index or Password"
        except:
            msg = "Wrong format. Use: Index*Password"
        return jsonify({"sessionID": session_id, "userID": user_id, "msisdn": msisdn, "message": msg, "continueSession": False})

    if user_input == '2':
        return jsonify({"sessionID": session_id, "userID": user_id, "msisdn": msisdn, "message": "Goodbye", "continueSession": False})

    return jsonify({"sessionID": session_id, "userID": user_id, "msisdn": msisdn, "message": "Invalid option", "continueSession": False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000) # Important for Render
