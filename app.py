from flask import Flask, request

app = Flask(__name__)

students = {
    "BCITD22003": {"name": "ERIC ORLEANS BOHAM", "password": "EOB22"},
    "BCITD22004": {"name": "JOHN KWAD WOYTE", "password": "JK22"},
    "BCITD22005": {"name": "AMA ADJEI", "password": "AA22"}
}

@app.route('/ussd/', methods=['POST'])
def ussd():
    # Arkesel sends form data, not JSON
    session_id = request.form.get('sessionId', '')
    service_code = request.form.get('serviceCode', '')
    phone_number = request.form.get('phoneNumber', '')
    text = request.form.get('text', '') # This is what user typed

    print("TEXT RECEIVED:", text) # For logs

    if text == '':
        # First screen
        response = "CON Welcome to TTU Results Checker\n"
        response += "1. Login to view grades\n"
        response += "2. Exit"
    
    elif text == '1':
        # Ask for login
        response = "CON Enter IndexNumber*Password"
    
    elif '*' in text:
        # They typed: BCITD22003*EOB22
        try:
            index, password = text.split('*')
            index = index.strip().upper()
            password = password.strip()
            
            if index in students and students[index]['password'] == password:
                response = f"END Welcome {students[index]['name']}\nLogin Successful"
            else:
                response = "END Invalid Index or Password"
        except:
            response = "END Wrong format. Use: Index*Password"
    
    elif text == '2':
        response = "END Goodbye"
    
    else:
        response = "END Invalid option"

    return response, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
