from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

def load_students():
    students = {}
    try:
        with open('data_students.csv', 'r', encoding='utf-8-sig') as f: # utf-8-sig kills BOM
            reader = csv.DictReader(f)
            for row in reader:
                index = row['index_number'].strip().upper()
                name = row['full_name'].strip()
                password = row['password'].strip() # strip spaces
                students[index] = {"name": name, "password": password}
        print(f"✅ SUCCESS: Loaded {len(students)} students: {list(students.keys())}")
    except Exception as e:
        print(f"❌ ERROR LOADING STUDENTS: {e}")
    return students

def load_results():
    results = {}
    try:
        with open('data_grades.csv', 'r', encoding='utf-8-sig') as f: # utf-8-sig
            reader = csv.DictReader(f)
            for row in reader:
                idx = row['index_number'].strip().upper()
                course = f"{row['course_code'].strip()}: {row['grade'].strip()}"
                if idx not in results:
                    results[idx] = []
                results[idx].append(course)
        print(f"✅ SUCCESS: Loaded results for {len(results)} students")
    except Exception as e:
        print(f"❌ ERROR LOADING RESULTS: {e}")
    return results

print("STARTING APP...")
students = load_students()
results = load_results()

@app.route('/ussd/', methods=['POST'])
def ussd():
    data = request.get_json()
    session_id = data.get('sessionID', '')
    user_input = data.get('userData', '').strip()
    new_session = data.get('newSession', True)

    print(f"REQUEST: newSession={new_session}, input='{user_input}'")

    # STEP 1: WELCOME
    if new_session or user_input == '':
        return reply(session_id, data, "Welcome to Takoradi Technical University\n1. Check Results\n2. Exit", True)

    # STEP 2: ASK FOR LOGIN
    if user_input == '1':
        return reply(session_id, data, "Enter IndexNumber*Password", True)

    # STEP 3: LOGIN + SHOW ALL RESULTS
    if '*' in user_input:
        try:
            parts = user_input.split('*')
            index = parts[0].strip().upper()
            password = parts[1].strip()
            print(f"LOGIN ATTEMPT: index='{index}' password='{password}'")

            if index in students:
                csv_password = students[index]['password']
                print(f"DEBUG CSV PASSWORD: '{csv_password}'")
                print(f"DEBUG TYPED PASSWORD: '{password}'")
                print(f"DEBUG MATCH: {csv_password == password}")

                if csv_password == password:
                    print(f"LOGIN SUCCESS: {index}")
                    if index in results:
                        msg = f"Welcome {students[index]['name']}\n\nRESULTS:\n"
                        msg += "\n".join(results[index])
                        msg += "\n\nThank you"
                        return reply(session_id, data, msg, False)
                    else:
                        return reply(session_id, data, "No results found for this index", False)
                else:
                    return reply(session_id, data, "Invalid Password", False)
            else:
                print(f"LOGIN FAILED: Index {index} not found")
                return reply(session_id, data, "Invalid Index", False)
                
        except Exception as e:
            print(f"ERROR: {e}")
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
