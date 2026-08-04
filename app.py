from flask import Flask, request, jsonify
from openpyxl import load_workbook

app = Flask(__name__)

# Load Excel
wb = load_workbook('data.xlsx')
students_sheet = wb['students']
grades_sheet = wb['grades']

# Load students into dict
students = {}
for row in students_sheet.iter_rows(min_row=2, values_only=True):
    index, name, password = row
    students[index] = {'name': name, 'password': password}

# Load grades into dict
grades = {}
for row in grades_sheet.iter_rows(min_row=2, values_only=True):
    index, course, grade = row
    if index not in grades:
        grades[index] = []
    grades[index].append(f"{course}: {grade}")

@app.route('/ussd', methods=['POST'])
def ussd():
    data = request.get_json()
    user_input = data.get('input', '')

    # Step 1: Menu
    if user_input == '':
        return jsonify({
            "response": "Welcome to TTU Results Checker\n1. Check Results\n2. Exit",
            "type": "response"
        })

    # Step 2: Ask for login
    if user_input == '1':
        return jsonify({
            "response": "Enter IndexNumber*Password",
            "type": "response"
        })

    # Step 3: Check login and show results
    if '*' in user_input:
        try:
            index, password = user_input.split('*')
            
            if index in students and str(students[index]['password']) == password:
                name = students[index]['name']
                
                if index in grades:
                    result_text = f"Results for {name}\n"
                    for g in grades[index]:
                        result_text += g + "\n"
                    result_text += "Thank you"
                    return jsonify({"response": result_text, "type": "end"})
                else:
                    return jsonify({"response": f"Welcome {name}\nNo grades found", "type": "end"})
            else:
                return jsonify({"response": "Invalid Index or Password", "type": "end"})
        except:
            return jsonify({"response": "Wrong format. Use: Index*Password", "type": "end"})

    if user_input == '2':
        return jsonify({"response": "Goodbye", "type": "end"})

if __name__ == '__main__':
    app.run()
