from flask import Flask, request, jsonify

app = Flask(__name__)

students = {
    "BCITD22003": {"name": "ERIC ORLEANS BOHAM", "password": "EOB22"},
    "BCITD22004": {"name": "JOHN KWAD WOYTE", "password": "JK22"},
    "BCITD22005": {"name": "AMA ADJEI", "password": "AA22"}
}

results = {
    "BCITD22003": {
        "Sem1": "CS101: A\nMATH101: B+\nICT101: A\nGPA: 3.67",
        "Sem2": "CS102: A\nMATH102: A\nDB101: B\nGPA: 3.75"
    },
    "BCITD22004": {
        "Sem1": "CS101: B\nMATH101: C+\nICT101: B\nGPA: 2.89",
        "Sem2": "CS102: B+\nMATH102: B\nDB101: A\nGPA: 3.25"
    },
    "BCITD22005": {
        "Sem1": "CS101: A\nMATH101: A\nICT101: A\nGPA: 4.00",
        "Sem2": "CS102: A-\nMATH102: B+\nDB101: A\nGPA: 3.80"
    }
}

@app.route('/ussd/', methods=['POST'])
def ussd():
    data = request.get_json()
    session_id = data.get('sessionID', '')
    user_input = data.get('userData', '').strip()
    new_session = data.get('newSession', True)

    # STEP 1: WELCOME
    if new_session or user_input == '':
        return reply(session_id, data, "Welcome to TTU Results Checker\n1. Check Results\n2. Exit", True)

    # STEP 2: ASK FOR LOGIN
    if user_input == '1':
        return reply(session_id, data, "Enter IndexNumber*Password", True)

    # STEP 3: LOGIN + SHOW RESULTS IMMEDIATELY
    if '*' in user_input:
        try:
            index, password = user_input.split('*')
            index = index.strip().upper()
            password = password.strip()
            
            if index in students and students[index]['password'] == password:
                s1 = results[index]["Sem1"]
                s2 = results[index]["Sem2"]
                msg = f"Welcome {students[index]['name']}\n\nSEMESTER 1:\n{s1}\n\nSEMESTER 2:\n{s2}\n\nThank you"
                return reply(session_id, data, msg, False) # END SESSION
            else:
                return reply(session_id, data, "Invalid Index or Password. Try again", False)
        except:
            return reply(session_id, data, "Wrong format. Use: Index*Password", True)

    if user_input == '2':
        return reply(session_id, data, "Goodbye", False)

    return reply(session_id, data, "Invalid option", True)


def reply(session_id, data, message, continue_session):
    return jsonify({
        "sessionID": session_id,
        "userID": data.get('userID', ''),
        "msisdn": data.get('msisdn', ''),
        "message": message,
        "continueSession": continue_session
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
