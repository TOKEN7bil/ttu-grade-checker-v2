from flask import Flask, request, jsonify
import sqlite3
import pandas as pd
import os

app = Flask(__name__)

DB_NAME = "grades.db"
EXCEL_FILE = "data.xlsx" # Name your file this and upload to GitHub

# 1. INIT DATABASE AND LOAD EXCEL
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS grades 
                      (index_number TEXT, course TEXT, grade TEXT)''')
    
    # Clear old data and load new data from Excel
    cursor.execute("DELETE FROM grades")
    
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE, sheet_name="grades") # reads your "grades" sheet
        for _, row in df.iterrows():
            cursor.execute("INSERT INTO grades VALUES (?,?,?)", 
                           (str(row['index number']), str(row['course']), str(row['grade'])))
    
    conn.commit()
    conn.close()

def get_grades(index):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT course, grade FROM grades WHERE index_number=?", (index,))
    results = c.fetchall()
    conn.close()
    return results

# 2. PASSWORD CHECK: last 4 digits of index number
def check_login(index_no, password):
    if len(index_no) < 4:
        return False
    return password == index_no[-4:]


# 3. USSD ENDPOINT - JSON MODE FOR ARKESEL
@app.route("/ussd", methods=['POST'])
def ussd():
    text = request.values.get("text", "")
    inputs = text.split('*')

    # Level 0: Main Menu
    if text == "":
        message = "Welcome to TTU Grade Checker\n1. Login to view grades\n2. Exit"
        response = {"type": "response", "message": message}
    
    # Level 1: User chose 1
    elif text == "1":
        message = "Enter your Index Number:"
        response = {"type": "response", "message": message}
    
    # Level 2: User entered Index Number
    elif len(inputs) == 2:
        message = "Enter your Password:"
        response = {"type": "response", "message": message}
    
    # Level 3: User entered Index*Password
    elif len(inputs) == 3:
        index_no = inputs[1].upper() # make it uppercase to match BCITD22003
        password = inputs[2]
        
        if check_login(index_no, password):
            results = get_grades(index_no)
            if results:
                msg = f"Results for {index_no}:\n"
                for course, grade in results:
                    msg += f"{course}: {grade}\n"
            else:
                msg = "No results found for this Index Number"
        else:
            msg = "Wrong Password. Try again"
        
        response = {"type": "end", "message": msg}
    
    # Level 1: User chose 2
    elif text == "2":
        response = {"type": "end", "message": "Thank you for using TTU Grade Checker"}
    
    else:
        response = {"type": "end", "message": "Invalid option"}

    return jsonify(response)


# 4. RUN THE APP
if __name__ == "__main__":
    init_db() 
    app.run(host="0.0.0.0", port=10000)
