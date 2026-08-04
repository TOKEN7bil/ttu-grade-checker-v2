from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

def load_students():
    students = {}
    with open('data_students.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            students[row['index_number'].strip().upper()] = {
                "name": row['full_name'].strip(),
                "password": row['password'].strip()
            }
    return students

def load_results():
    results = {}
    with open('data_grades.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            idx = row['index_number'].strip().upper()
            sem = row['semester'].strip()
            course = f"{row['course_code'].strip()}: {row['grade'].strip()}"
            
            if idx not in results:
                results[idx] = {}
            if sem not in results[idx]:
                results[idx][sem] = []
            results[idx][sem].append(course)
    return results

students = load_students()
results = load_results()

@app.route('/ussd/', methods=['POST'])
def ussd():
    data = request.get_json()
    session_id = data.get('sessionID', '')
    user_input = data.get('userData', '').strip()
    new_session = data.get('newSession', True)

    if new_session or user_input == '':
        return reply(session_id, data, "Welcome to Takoradi Technical University\n1. Check Results\n2. Exit", True)

    if user_input == '1':
        return reply(session_id, data, "Enter IndexNumber*Password\nExample: BCITD22003*EOB22", True)

    if '*' in user_input:
        try:
            index, password = user_input.split('*')
            index = index.strip().upper()
            password = password.strip()
            
            if index in students and students[index]['password'] == password:
                if index in results:
                    msg = f"Welcome {students[index]['name']}\n\n"
                    for sem, courses in results[index].items():
                        msg += f"{sem}:\n" + "\n".join(courses) + "\n\n"
                    msg += "Thank you"
                    return reply(session_id, data, msg, False)
                else:
                    return reply(session_id, data, "No results found for this index", False)
            else:
                return reply(session_id, data, "Invalid Index or Password", False)
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
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
