from flask import Flask, request, jsonify

app = Flask(__name__)

# Student Login Data
students = {
    "BCITD22003": {"name": "ERIC ORLEANS BOHAM", "password": "EOB22"},
    "BCITD22004": {"name": "JOHN KWAD WOYTE", "password": "JK22"},
    "BCITD22005": {"name": "AMA ADJEI", "password": "AA22"}
}

# Student Results Data
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

# To remember who is logged in during the session
logged_in_user = {}

@app.route('/ussd/', methods=['POST'])
def ussd():
    data = request.get_json()
    session_id = data.get('sessionID', '')
    user_id = data.get('userID', '')
    msisdn = data.get('msisdn', '')
    user_input = data.get('userData', '')
    new_session = data.get('newSession', True)

    # WELCOME SCREEN
    if new_session or user_input == '':
        message = "Welcome to TTU Results Checker\n1. Login to view grades\n2. Exit"
        continue_session = True
    
    # LOGIN SCREEN
    elif user_input == '1':
        message = "Enter IndexNumber*Password"
        continue_session = True
    
    # CHECK LOGIN
    elif '*' in user_input and session_id not in logged_in_user:
        try:
            index, password = user_input.split('*')
            index = index.strip().upper()
            password = password.strip()
            
            if index in students and students[index]['password'] == password:
                logged_in_user[session_id] = index # Remember this user
                message = f"Welcome {students[index]['name']}\n1. View Sem 1 Results\n2. View Sem 2 Results\n3. Logout"
                continue_session = True
            else:
                message = "Invalid Index or Password\n1. Try Again\n2. Exit"
                continue_session = True
        except:
            message = "Wrong format. Use: Index*Password"
            continue_session = False
    
    # USER IS LOGGED IN - SHOW RESULTS
    elif session_id in logged_in_user:
        index = logged_in_user[session_id]
        
        if user_input == '1':
            res = results.get(index, {}).get("Sem1", "No results found")
            message = f"Semester 1 Results:\n{res}\n\n0. Back"
            continue_session = True
        
        elif user_input == '2':
            res = results.get(index, {}).get("Sem2", "No results found")
            message = f"Semester 2 Results:\n{res}\n\n0. Back"
            continue_session = True
        
        elif user_input == '3':
            del logged_in_user[session_id]
            message = "Logged out successfully. Goodbye"
            continue_session = False
        
        elif user_input == '0':
            message = f"Welcome {students[index]['name']}\n1. View Sem 1 Results\n2. View Sem 2 Results\n3. Logout"
            continue_session = True
        
        else:
            message = "Invalid option"
            continue_session = True
    
    # EXIT
    elif user_input == '2':
        message = "Goodbye"
        continue_session = False
    
    else:
        message = "Invalid option"
        continue_session = False

    return jsonify({
        "sessionID": session_id,
        "userID": user_id,
        "msisdn": msisdn,
        "message": message,
        "continueSession": continue_session
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
