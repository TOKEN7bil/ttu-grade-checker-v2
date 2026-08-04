from flask import Flask, request
import csv
import os

app = Flask(__name__)

def load_students():
    students = {}
    passwords = {}
    with open('data_students.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            students[row['index_number']] = row['full_name'] # <-- full_name
            passwords[row['index_number']] = row['password']
    return students, passwords

def load_grades():
    grades = {}
    with open('data_grades.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            idx = row['index_number']
            if idx not in grades:
                grades[idx] = []
            grades[idx].append(f"{row['course_code']}: {row['grade']}")
    return grades

students, passwords = load_students()
grades = load_grades()

@app.route('/', methods=['POST'])
def ussd():
    session_id = request.form.get('sessionId')
    service_code = request.form.get('serviceCode')
    phone_number = request.form.get('phoneNumber')
    text = request.form.get('text')

    if text == '':
        response = "CON Welcome to TTU Grade Checker\n"
        response += "1. Check Results"
    elif text == '1':
        response = "CON Enter IndexNumber*Password\n"
        response += "Example: BCITD22003*EOB22"
    else:
        try:
            parts = text.split('*')
            index_number = parts[0].strip()
            pin = parts[1].strip()
            
            if index_number in students and passwords[index_number] == pin:
                student_grades = grades.get(index_number, [])
                response = f"END Welcome {students[index_number]}\n\n" # shows ERIC ORLEANS BOHAM
                response += "RESULTS:\n"
                response += "\n".join(student_grades)
                response += "\n\nThank you"
            else:
                response = "END Invalid Index Number or Password"
        except:
            response = "END Invalid format. Use: IndexNumber*Password"

    return response, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
