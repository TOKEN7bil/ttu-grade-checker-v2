from flask import Flask, request, Response
import csv
import os

app = Flask(__name__)

def load_students():
    students = {}
    passwords = {}
    with open('data_students.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            students[row['index_number'].strip()] = row['full_name'].strip()
            passwords[row['index_number'].strip()] = row['password'].strip()
    return students, passwords

def load_grades():
    grades = {}
    with open('data_grades.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            idx = row['index_number'].strip()
            if idx not in grades:
                grades[idx] = []
            grades[idx].append(f"{row['course_code'].strip()}: {row['grade'].strip()}")
    return grades

students, passwords = load_students()
grades = load_grades()

@app.route('/ussd/', methods=['GET', 'POST']) # <-- MATCHES YOUR ARKESEL URL
def ussd():
    if request.method == 'GET':
        return Response("CON Welcome to TTU Grade Checker\n1. Check Results", mimetype='text/plain')
    
    text = request.values.get('text', '')

    if text == '':
        response = "CON Welcome to TTU Grade Checker\n1. Check Results"
    elif text == '1':
        response = "CON Enter IndexNumber*Password\nExample: BCITD22003*EOB22"
    else:
        try:
            parts = text.split('*')
            index_number = parts[0].strip().upper()
            pin = parts[1].strip()
            
            if index_number in students and passwords[index_number] == pin:
                student_grades = grades.get(index_number, [])
                if student_grades:
                    response = f"END Welcome {students[index_number]}\n\nRESULTS:\n"
                    response += "\n".join(student_grades)
                    response += "\n\nThank you"
                else:
                    response = "END No results found for this index number"
            else:
                response = "END Invalid Index Number or Password"
        except:
            response = "END Invalid format. Use: IndexNumber*Password"

    return Response(response, mimetype='text/plain', status=200)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
