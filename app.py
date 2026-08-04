from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load your excel
df = pd.read_excel('results.xlsx')

@app.route('/ussd', methods=['POST'])
def ussd():
    data = request.get_json()
    user_input = data.get('input', '')
    session_id = data.get('session_id', '')

    # Step 1: Show menu
    if user_input == '':
        return jsonify({
            "response": "Welcome to TTU Results Checker\n1. Login to view grades\n2. Exit",
            "type": "response"
        })

    # Step 2: User pressed 1
    if user_input == '1':
        return jsonify({
            "response": "Enter IndexNumber*Password",
            "type": "response"
        })

    # Step 3: User entered Index*Pass
    if '*' in user_input:
        try:
            index, password = user_input.split('*')
            student = df[(df['IndexNumber'] == index) & (df['Password'] == password)]
            
            if not student.empty:
                grade = student.iloc[0]['Grade']
                return jsonify({
                    "response": f"Your Grade: {grade}\nThank you",
                    "type": "end"
                })
            else:
                return jsonify({
                    "response": "Invalid Index or Password",
                    "type": "end"
                })
        except:
            return jsonify({"response": "Wrong format. Use: Index*Password", "type": "end"})

    # Step 2: User pressed 2
    if user_input == '2':
        return jsonify({"response": "Goodbye", "type": "end"})

if __name__ == '__main__':
    app.run()
