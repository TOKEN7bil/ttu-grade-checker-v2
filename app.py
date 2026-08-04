from flask import Flask, request, jsonify

app = Flask(__name__)

# Temporary memory to remember who is logged in per session
sessions = {}

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

    # If new session, clear old data
    if new_session:
        if session_id in sessions:
            del sessions[session_id]

    # STEP 1: MAIN MENU
    if user_input == '':
        return reply(session_id, data, "Welcome to TTU Results Checker\n1. Login to view grades\n2. Exit", True)

    # STEP 2: USER PRESSED 1
    if user_input == '1':
        sessions[session_id] = {"step": "login"}
        return reply(session_id, data, "Enter IndexNumber*Password", True)

    # STEP 3: USER ENTERED LOGIN
    if sessions.get(session_id, {}).get("step") == "login" and '*' in user_input:
        try:
            index, password = user_input.split('*')
            index = index.strip().upper()
            password = password.strip()
            
            if index in students and students[index]['password'] == password:
                sessions[session_id] = {"step": "menu", "index": index} # REMEMBER THE STUDENT
                msg = f"Welcome {students[index]['name']}\n1. View Sem 1 Results\n2. View Sem 2 Results\n3. Logout"
                return reply(session_id, data, msg, True)
            else:
                del sessions[session_id]
                return reply(session_id, data, "Invalid Index or Password\n1. Try Again\n2. Exit", True)
        except:
            return reply(session_id, data, "Wrong format. Use: Index*Password", True)

    # STEP 4: USER IS IN MENU - CHECK IF LOGGED IN
    if sessions.get(session_id, {}).get("step") == "menu":
        index = sessions[session_id]["index"]
        
        if user_input == '1':
            res = results[index]["Sem1"]
            return reply(session_id, data, f"Semester 1 Results:\n{res}\n\n0. Back", True)
        
        if user_input == '2':
            res = results[index]["Sem2"]
            return reply(session_id, data, f"Semester 2 Results:\n{res}\n\n0. Back", True)
        
        if user_input == '3':
            del sessions[session_id]
            return reply(session_id, data, "Logged out. Goodbye", False)
        
        if user_input == '0':
            msg = f"Welcome {students[index]['name']}\n1. View Sem 1 Results\n2. View Sem 2 Results\n3. Logout"
            return reply(session_id, data, msg, True)

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
