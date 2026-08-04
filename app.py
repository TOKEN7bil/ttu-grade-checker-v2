from flask import Flask, request, jsonify

app = Flask(__name__)

students = {
    "BCITD22003": {"name": "ERIC ORLEANS BOHAM", "password": "EOB22"},
    "BCITD22004": {"name": "JOHN KWAD WOYTE", "password": "JK22"},
    "BCITD22005": {"name": "AMA ADJEI", "password": "AA22"}
}

@app.route('/ussd/', methods=['POST'])
def ussd():
    data = request.get_json()
    print("FULL DATA:", data)
    
    session_id = data.get('sessionID', '')
    user_id = data.get('userID', '')
    msisdn = data.get('msisdn', '')
    
    # ARKESEL USES 'userData'!!!
    user_input = data.get('userData', '')
    new_session = data.get('newSession', True)

    if new_session or user_input == '':
        message = "Welcome to TTU Results Checker\n1. Login to view grades\n2. Exit"
        continue_session = True
    
    elif user_input == '1':
        message = "Enter IndexNumber*Password"
        continue_session = True
    
    elif '*' in user_input:
        try:
            index, password = user_input.split('*')
            index = index.strip().upper()
            password = password.strip()
            
            if index in students and students[index]['password'] == password:
                message = f"Welcome {students[index]['name']}\nLogin Successful"
                continue_session = False
            else:
                message = "Invalid Index or Password"
                continue_session = False
        except:
            message = "Wrong format. Use: Index*Password"
            continue_session = False
    
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
