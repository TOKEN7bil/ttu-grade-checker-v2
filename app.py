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
    user_input = data.get('userData', '')
    new_session = data.get('newSession', True)

    # Step 1: New session - Show menu
    if new_session or user_input == '':
        return response(session_id, data, "Welcome to TTU Results Checker\n1. Login to view grades\n2. Exit", True)

    # Step 2: User pressed 1
    if user_input == '1':
        return response(session_id, data, "Enter IndexNumber*Password", True)

    # Step 3: User entered login details
    if '*' in user_input:
        try:
            index, password = user_input.split('*')
            index = index.strip().upper()
            password = password.strip()
            
            if index in students and students[index]['password'] == password:
                # Login success - show results menu
                msg = f"Welcome {students[index]['name']}\n1. View Sem 1 Results\n2. View Sem 2 Results\n3. Logout"
                return response(session_id, data, msg, True)
            else:
                return response(session_id, data, "Invalid Index or Password\n1. Try Again\n2. Exit", True)
        except:
            return response(session_id, data, "Wrong format. Use: Index*Password", True)

    # Step 4: User is in results menu - check last input
    # We check if input is 1, 2, 3, or 0
    if user_input == '1':
        # Find which student by checking if we can get their name from previous login
        # Arkesel keeps session_id same, so we assume user just logged in
        # Better way: ask user to re-enter index, but for now let's use a temp fix
        return response(session_id, data, "Please login again to view results", True)
    
    if user_input == '2':
        return response(session_id, data, "Please login again to view results", True)
    
    if user_input == '3':
        return response(session_id, data, "Logged out successfully. Goodbye", False)
    
    if user_input == '0':
        return response(session_id, data, "1. View Sem 1 Results\n2. View Sem 2 Results\n3. Logout", True)

    if user_input == '2':
        return response(session_id, data, "Goodbye", False)

    return response(session_id, data, "Invalid option", True)


def response(session_id, data, message, continue_session):
    return jsonify({
        "sessionID": session_id,
        "userID": data.get('userID', ''),
        "msisdn": data.get('msisdn', ''),
        "message": message,
        "continueSession": continue_session
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
