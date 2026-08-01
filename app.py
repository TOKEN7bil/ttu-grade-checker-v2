from flask import Flask, request
import sqlite3
import openpyxl
import os

app = Flask(__name__)
DB_NAME = "grades.db"
EXCEL_FILE = "data.xlsx"

def init_db():
    if os.path.exists(DB_NAME): os.remove(DB_NAME)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE grades (index_number TEXT, course_code TEXT, grade TEXT)''')
    if os.path.exists(EXCEL_FILE):
        wb = openpyxl.load_workbook(EXCEL_FILE)
        sheet = wb.active
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row[0]: cursor.execute("INSERT INTO grades VALUES (?,?,?)", row)
    conn.commit(); conn.close()

def get_grades(index):
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute("SELECT course_code, grade FROM grades WHERE index_number=?", (index,))
    results = c.fetchall(); conn.close(); return results

init_db()

@app.route("/ussd", methods=['GET', 'POST'])
def ussd():
    text = request.values.get("text", "")
    inputs = text.split('*')
    if text == "": response = " Welcome to TTU Results Portal\n1. Check Grades"
    elif text == "1": response = "CON Enter your Index Number"
    else:
        if len(inputs) >= 2:
            results = get_grades(inputs[1])
            if results: response = "END Your Grades:\n" + "\n".join([f"{c}: {g}" for c,g in results])
            else: response = "END Index Number not found."
        else: response = "END Invalid input"
    return response

if __name__ == "__main__": app.run(host='0.0.0.0', port=10000)
