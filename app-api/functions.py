import sqlite3
import datetime as datetime

connection = sqlite3.connect('database.db')
cursor = connection.cursor()


def mark_attendance(user_id, date, status='Present'):
    try:
        cursor.execute(
            "INSERT INTO attendance (user_id, date, status) VALUES (? ? ?)",
            (user_id, date,status)
        )
        connection.commit()
        print("attendance successfull")
    except sqlite3.IntegrityError:
        print("attendance already taken for user ")



def get_attendance(user_id, start_date, end_date):
    cursor.execute(
        "SELECT * FROM attendance WHERE user_id = ? AND date BETWEEN ? AND?",
        (user_id, start_date, end_date)
    )
    return cursor.fetchall()

