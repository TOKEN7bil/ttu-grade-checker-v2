from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ussd/', methods=['POST'])
def ussd():
    data = request.get_json()
    print("FULL DATA RECEIVED:", data) # Check Render Logs
    
    session_id = data.get('sessionID', '')
    user_id = data.get('userID', '')
    msisdn = data.get('msisdn', '')
    user_input = data.get('message', 'NO_MESSAGE')

    # Just echo back whatever they typed
    message = f"You typed: {user_input}"
    continue_session = True

    return jsonify({
        "sessionID": session_id,
        "userID": user_id,
        "msisdn": msisdn,
        "message": message,
        "continueSession": continue_session
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
