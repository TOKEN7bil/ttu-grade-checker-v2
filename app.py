from flask import Flask, request
import sqlite3
import openpyxl
import os

app = Flask(__name__)

DB_NAME = "grades.db"
EXCEL_FILE = "data.xlsx"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS grades 
                      (index_number TEXT, course TEXT, grade TEXT)''')
    
    cursor.execute("DELETE FROM grades")
    
    if os.path.exists(EXCEL_FILE):
        wb = openpyxl.load_workbook(EXCEL_FILE)
        sheet = wb['grades']
        for row in sheet.iter_rows(min_row=2, values_only=True):
            index_no, course, grade = row
            cursor.execute("INSERT INTO grades VALUES (?,?,?)", 
                           (str(index_no), str(course), str(grade)))
    
    conn.commit()
    conn.close()

def get_grades(index):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT course, grade FROM grades WHERE index_number=?", (index,))
    results = c.fetchall()
    conn.close()
    return results

def check_login(index_no, password):
    if len(index_no) < 4:
        return False
    return password == index_no[-4:]


@app.route("/ussd", methods=['POST'])
def ussd():
    text = request.values.get("text", "")
    inputs = text.split('*')

    if text == "":
        message = "CON Welcome to TTU Grade Checker\n1. Login to view grades\n2. Exit"
    
    elif text == "1":
        message = "CON Enter your Index Number:"
    
    elif len(inputs) == 2:
        message = "CON Enter your Password:"
    
    elif len(inputs) == 3:
        index_no = inputs[1].upper()
        password = inputs[2]
        
        if check_login(index_no, password):
            results = get_grades(index_no)
            if results:
                msg = f"END Results for {index_no}:\n"
                for course, grade in results:
                    msg += f"{course}: {grade}\n"
            else:
                msg = "END No results found for this Index Number"
        else:
            msg = "END Wrong Password. Try again"
        
        message = msg
    
    elif text == "2":
        message = "END Thank you for using TTU Grade Checker"
    
    else:
        message = "END Invalid option"

    return message, 200, {'Content-Type': 'text/plain'}


if __name__ == "__main__":
    init_db() 
    app.run(host="0.0.0.0", port=10000)
