from flask import Flask, request, Response
import csv
import os

app = Flask(__name__)

# Load data once when app starts
def load_data():
    students = {}
    passwords = {}
    grades = {}
    
    # Load students
    with open('data_students.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            idx = row['index_number'].strip()
            students[idx] = row['full_name'].strip()
            passwords[idx] = row['password'].strip()
    
    # Load grades
    with open('data_grades.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            idx = row['index_number'].strip()
            if idx not in grades:
                grades[idx] = []
            grades[idx].append(f"{row['course_code'].strip()}: {row['grade'].strip()}")
    
    return students, passwords, grades

students, passwords, grades = load_data()

@app.route('/', methods=['GET', 'POST']) # ARKESEL USES ROOT /
def ussd():
    # Get data - Arkesel sends POST
    text = request.values.get('text', '')
    
    # Level 0: Main Menu
    if text == '':
        response = "CON Welcome to TTU Grade Checker\n"
        response += "1. Check Results"
    
    # Level 1: Ask for login
    elif text == '1':
        response = "CON Enter IndexNumber*Password\n"
        response += "Example: BCITD22003*EOB22"
    
    # Level 2: Process login
    else:
        try:
            parts = text.split('*')
            if len(parts) == 2:
                index_number = parts[0].strip().upper()
                pin = parts[1].strip()
                
                if index_number in students and passwords[index_number] == pin:
                    student_grades = grades.get(index_number, [])
                    if student_grades:
                        response = f"END Welcome {students[index_number]}\n\n"
                        response += "RESULTS:\n"
                        response += "\n".join(student_grades)
                        response += "\n\nPowered by TTU"
                    else:
                        response = "END No results found for this index number"
                else:
                    response = "END Invalid Index Number or Password"
            else:
                response = "END Invalid format.\nUse: IndexNumber*Password"
        except Exception as e:
            response = "END An error occurred. Try again"

    # Arkesel MUST get text/plain
    return Response(response, mimetype='text/plain', status=200)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
