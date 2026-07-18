import sqlite3
import datetime
import os

DB_NAME = "attendance.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create students table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        register_number TEXT,
        enroll_number TEXT,
        UNIQUE(name, register_number, enroll_number)
    )
    ''')
    
    # Create attendance table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        time TEXT,
        status TEXT,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    ''')
    
    conn.commit()
    conn.close()

def add_student(student_string):
    parts = student_string.split('_')
    name = parts[0]
    register_number = parts[1] if len(parts) > 1 else 'N/A'
    enroll_number = parts[2] if len(parts) > 2 else 'N/A'

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students (name, register_number, enroll_number) VALUES (?, ?, ?)", (name, register_number, enroll_number))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # Student already exists
    conn.close()

def mark_attendance(student_string, status="Present"):
    parts = student_string.split('_')
    name = parts[0]
    register_number = parts[1] if len(parts) > 1 else 'N/A'
    enroll_number = parts[2] if len(parts) > 2 else 'N/A'

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Get student id
    cursor.execute("SELECT id FROM students WHERE name = ? AND register_number = ? AND enroll_number = ?", (name, register_number, enroll_number))
    student = cursor.fetchone()
    
    if student is None:
        # Avoid foreign key error if student doesn't exist
        # Also could register the student automatically here
        add_student(student_string)
        cursor.execute("SELECT id FROM students WHERE name = ? AND register_number = ? AND enroll_number = ?", (name, register_number, enroll_number))
        student = cursor.fetchone()
        
    student_id = student[0]
    
    now = datetime.datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    
    # Check if already marked for today
    cursor.execute("SELECT id FROM attendance WHERE student_id = ? AND date = ?", (student_id, current_date))
    record = cursor.fetchone()
    
    if record is None:
        cursor.execute("INSERT INTO attendance (student_id, date, time, status) VALUES (?, ?, ?, ?)",
                       (student_id, current_date, current_time, status))
        conn.commit()
        ret = True
    else:
        ret = False # Already marked today
        
    conn.close()
    return ret

def get_attendance():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT students.name, students.register_number, students.enroll_number, attendance.date, attendance.time, attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        ORDER BY attendance.date DESC, attendance.time DESC
    ''')
    records = cursor.fetchall()
    conn.close()
    
    return [{"name": row[0], "register_number": row[1], "enroll_number": row[2], "date": row[3], "time": row[4], "status": row[5]} for row in records]

def clear_attendance():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attendance")
    conn.commit()
    conn.close()

if not os.path.exists(DB_NAME):
    init_db()
